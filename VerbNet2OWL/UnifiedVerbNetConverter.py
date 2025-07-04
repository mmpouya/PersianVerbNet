import os
import xml.etree.ElementTree as ET
import re
from rdflib import Graph, Namespace, URIRef, RDFS, RDF, OWL, Literal

class UnifiedVerbNetConverter:
    """
    Unified class that combines XML to RDF conversion, OWL generation with selectional restrictions,
    and the complete processing workflow for VerbNet XML files.
    """
    
    def __init__(self, xml_directory="XMLs", ttl_directory="TTLs", namespace_uri="http://tavasi.majles.ir/ontology/general#"):
        self.xml_directory = xml_directory
        self.ttl_directory = ttl_directory
        self.go = Namespace(namespace_uri)
        self.ontology_iri = URIRef("http://tavasi.majles.ir/ontology/general")
        self.base = "http://tavasi.majles.ir/ontology/general/Verbnet"
        self.final_output = ""

    def sanitize_uri(self, text):
        """Sanitize text to be used in URIs by replacing invalid characters"""
        # Replace spaces and other invalid URI characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized

    def xmlclass_to_rdf(self, xml_file_path, rdf_output_path):
        """
        Convert XML file to RDF/OWL format with enhanced features including frames and examples.
        This combines functionality from Final1.py and EnhancedConverter.py
        """
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        g = Graph(base=self.base)
        
        # Bind namespaces
        g.bind("go", self.go)
        g.bind("owl", OWL)
        g.bind("rdfs", RDFS)
        g.bind("rdf", RDF)
        
        # Add ontology declaration
        g.add((self.ontology_iri, RDF.type, OWL.Ontology))

        for vnclass in root.iter('VNCLASS'):
            class_id = vnclass.attrib['ID']
            class_uri = URIRef(self.go[class_id])
            
            # Process MEMBERS
            members = vnclass.find('MEMBERS')
            if members is not None:
                for member in members.findall('MEMBER'):
                    name = member.attrib['name']
                    name2 = str(name).replace(" ", "_")
                    name_uri = URIRef(self.go[name2])
                    g.add((name_uri, RDFS.subClassOf, class_uri))
            
            # Process FRAMES - enhanced version with examples and semantics
            frames = vnclass.find('FRAMES')
            if frames is not None:
                frame_classes = []
                for frame in frames.findall('FRAME'):
                    # Create frame class
                    description = frame.find('DESCRIPTION')
                    if description is not None:
                        desc_num = description.attrib.get('descriptionNumber', '')
                        primary = description.attrib.get('primary', '')
                        secondary = description.attrib.get('secondary', '')
                        xtag = description.attrib.get('xtag', '')
                        
                        # Sanitize the frame class name to be URI-safe
                        sanitized_secondary = self.sanitize_uri(secondary)
                        frame_class_name = f"Frame_{desc_num.replace('.', '_')}_{sanitized_secondary}"
                        frame_uri = URIRef(self.go[frame_class_name])
                        frame_classes.append(frame_uri)
                        
                        g.add((frame_uri, RDF.type, OWL.Class))
                        g.add((frame_uri, self.go.hasDescriptionNumber, Literal(desc_num)))
                        g.add((frame_uri, self.go.hasPrimaryPattern, Literal(primary)))
                        g.add((frame_uri, self.go.hasSecondaryPattern, Literal(secondary)))
                        g.add((frame_uri, self.go.hasXTag, Literal(xtag)))
                        
                        # Add examples
                        examples = frame.find('EXAMPLES')
                        if examples is not None:
                            for example in examples.findall('EXAMPLE'):
                                g.add((frame_uri, self.go.hasExample, Literal(example.text)))
                        
                        # Add semantic predicate as string only
                        semantics = frame.find('SEMANTICS')
                        if semantics is not None:
                            for pred in semantics.findall('PRED'):
                                pred_value = pred.attrib.get('value', '')
                                if pred_value:
                                    g.add((frame_uri, self.go.hasSemanticPredicate, Literal(pred_value)))
                
                # Add frame classes to main verb class
                for frame_class in frame_classes:
                    g.add((class_uri, RDFS.subClassOf, frame_class))

            # Process SUBCLASSES - recursive handling
            self._process_subclasses(g, vnclass, class_uri)

            # Process THEMROLES
            themroles = vnclass.find('THEMROLES')
            if themroles is not None:
                for themrole in themroles.findall('THEMROLE'):
                    themrole_type = themrole.attrib['type']
                    themrole_uri = URIRef(self.go["has" + themrole_type])
                    g.add((class_uri, RDFS.subClassOf, themrole_uri))

        g.serialize(destination=rdf_output_path, format='turtle')

    def _process_subclasses(self, g, parent_element, parent_uri):
        """Recursively process subclasses"""
        subclasses = parent_element.find('SUBCLASSES')
        if subclasses is not None:
            for subclass in subclasses.findall('VNSUBCLASS'):
                subclass_id = subclass.attrib['ID']
                subclass_uri = URIRef(self.go[subclass_id])
                g.add((subclass_uri, RDFS.subClassOf, parent_uri))
                
                # Process nested members in subclasses
                subclass_members = subclass.find('MEMBERS')
                if subclass_members is not None:
                    for member in subclass_members.findall('MEMBER'):
                        name = member.attrib['name']
                        name2 = str(name).replace(" ", "_")
                        name_uri = URIRef(self.go[name2])
                        g.add((name_uri, RDFS.subClassOf, subclass_uri))
                
                # Recursively process nested subclasses
                self._process_subclasses(g, subclass, subclass_uri)

    def parse_and_generate_OWL(self, xml_file_path):
        """
        Generate OWL restrictions based on selectional restrictions in XML.
        This is the functionality from Final2.py
        """
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        self.final_output = ""
        self._process_classes(root, 'VNCLASS')
        self._process_classes(root, 'VNSUBCLASS')
        return self.final_output

    def _process_classes(self, root, tag):
        """Process classes for selectional restrictions"""
        for j in root.iter(tag):
            id = j.attrib['ID']
            id_uri = URIRef('<' + str(self.go) + id + '>')
            selrestr_elements = []
            themroles = j.find('THEMROLES')
            if themroles is None:
                continue
            for t in themroles.findall('THEMROLE'):
                themrole_type = t.attrib['type']
                predicate = self.predicate_uri(themrole_type)
                selrestr_elements = self._process_selrestrs(t, selrestr_elements)
                if len(selrestr_elements) >= 1:
                    # Only add if frst.text is not None (mimic original logic)
                    frst = t.find('SELRESTRS')
                    if frst is not None and frst.text is not None:
                        final = self.only(id_uri, predicate, selrestr_elements[-1])
                        self.final_output += final

    def _process_selrestrs(self, t, selrestr_elements):
        """Process selectional restrictions recursively"""
        for frst in t.findall('SELRESTRS'):
            for sec in frst.findall('SELRESTRS'):
                for thrd in sec.findall('SELRESTRS'):
                    for type3 in thrd.findall('SELRESTR'):
                        type3_uri = URIRef('<' + str(self.go) + type3.attrib['type'] + '>')
                        if type3.attrib.get('Value') == '-':
                            nottype3 = self.nottype(type3_uri)
                            selrestr_elements.append(nottype3)
                        else:
                            selrestr_elements.append(type3_uri)
                    if thrd.findall('SELRESTR'):
                        SELRESTR_element = thrd.find('SELRESTR')
                        SELRESTR_count = len(list(SELRESTR_element))
                        if thrd.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                or_type3 = self.OR(selrestr_elements[-1], selrestr_elements[-2])
                                selrestr_elements.append(or_type3)
                        elif thrd.text is None:
                            pass
                        elif SELRESTR_count == 1:
                            pass
                        elif not thrd.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                AND_type3 = self.AND(selrestr_elements[-1], selrestr_elements[-2])
                                selrestr_elements.append(AND_type3)
                for type2 in sec.findall('SELRESTR'):
                    type2_uri = URIRef('<' + str(self.go) + type2.attrib['type'] + '>')
                    if type2.attrib.get('Value') == '-':
                        nottype2 = self.nottype(type2_uri)
                        selrestr_elements.append(nottype2)
                    else:
                        selrestr_elements.append(type2_uri)
                if sec.findall('SELRESTR'):
                    SELRESTR_element = sec.find('SELRESTR')
                    SELRESTR_count = len(list(SELRESTR_element))
                    if sec.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            or_type2 = self.OR(selrestr_elements[-1], selrestr_elements[-2])
                            selrestr_elements.append(or_type2)
                    elif sec.text is None:
                        pass
                    elif SELRESTR_count == 1:
                        pass
                    elif not sec.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            AND_type2 = self.AND(selrestr_elements[-1], selrestr_elements[-2])
                            selrestr_elements.append(AND_type2)
            for type1 in frst.findall('SELRESTR'):
                type1_uri = URIRef('<' + str(self.go) + type1.attrib['type'] + '>')
                if type1.attrib.get('Value') == '-':
                    nottype1 = self.nottype(type1_uri)
                    selrestr_elements.append(nottype1)
                else:
                    selrestr_elements.append(type1_uri)
            if frst.findall('SELRESTR'):
                SELRESTR_element = frst.find('SELRESTR')
                SELRESTR_count = len(list(SELRESTR_element))
                if frst.attrib.get('logic') == "or":
                    if len(selrestr_elements) >= 2:
                        or_type1 = self.OR(selrestr_elements[-1], selrestr_elements[-2])
                        selrestr_elements.append(or_type1)
                elif frst.text is None:
                    pass
                elif SELRESTR_count == 1:
                    pass
                elif not frst.attrib.get('logic') == "or":
                    if len(selrestr_elements) >= 2:
                        AND_type1 = self.AND(selrestr_elements[-1], selrestr_elements[-2])
                        selrestr_elements.append(AND_type1)
        return selrestr_elements

    @staticmethod
    def predicate_uri(themrole):
        """Generate predicate URI for thematic role"""
        go3 = "<http://tavasi.majles.ir/ontology/general#EventHas"
        predicate = go3 + themrole + ">"
        return predicate

    @staticmethod
    def nottype(type_uri):
        """Generate NOT type restriction"""
        return f"""[ rdf:type owl:Class ; owl:complementOf {type_uri} ]"""

    @staticmethod
    def only(id_uri, predicate, rest):
        """Generate ONLY restriction"""
        return f"""{id_uri} rdfs:subClassOf [ rdf:type owl:Restriction ;\n                      owl:onProperty {predicate} ;\n                      owl:allValuesFrom {rest}\n                    ].\n"""

    @staticmethod
    def AND(type1, type2):
        """Generate AND (intersection) restriction"""
        return f"""[owl:intersectionOf ( {type1}\n                                            {type2}\n                                            ) ;\n                                          rdf:type owl:Class]"""

    @staticmethod
    def OR(type1, type2):
        """Generate OR (union) restriction"""
        return f"""[ rdf:type owl:Class ;\n                                          owl:unionOf ( {type1}\n                                                        {type2}\n                                                      )]\n"""

    def process_single_file(self, xml_filename):
        """
        Process a single XML file through the complete pipeline:
        1. Convert XML to RDF/OWL
        2. Add selectional restrictions
        """
        xml_file_path = os.path.join(self.xml_directory, xml_filename)
        ttl_filename = os.path.splitext(xml_filename)[0] + '.ttl'
        ttl_output_path = os.path.join(self.ttl_directory, ttl_filename)
        
        # Step 1: Convert XML to RDF/OWL
        self.xmlclass_to_rdf(xml_file_path, ttl_output_path)
        print(f"Corresponding TTL from {xml_filename} is created")
        
        # Step 2: Add selectional restrictions
        ttl_added_string = self.parse_and_generate_OWL(xml_file_path)
        
        with open(ttl_output_path, 'r') as file:
            content = file.read()
        
        if ttl_added_string == "":
            modified_content = content + "\n#This verb has no selectional restriction \n"
        else:
            modified_content = content + f"\n# Generated String:\n{ttl_added_string}\n"
        
        with open(ttl_output_path, 'w') as file:
            file.write(modified_content)
        print(f"Corresponding TTL from {xml_filename} is modified")

    def process_all_files(self):
        """
        Process all XML files in the directory through the complete pipeline.
        This is the main workflow from 'adding to ttl.py'
        """
        for filename in os.listdir(self.xml_directory):
            if filename.endswith(".xml"):
                self.process_single_file(filename)

    def convert_all_basic(self):
        """
        Convert all XML files to basic RDF/OWL format without selectional restrictions.
        This is the basic conversion functionality.
        """
        for filename in os.listdir(self.xml_directory):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.xml_directory, filename)
                ttl_filename = os.path.splitext(filename)[0] + '.ttl'
                rdf_output_path = os.path.join(self.ttl_directory, ttl_filename)
                print(f"Converting {filename} to {ttl_filename}")
                self.xmlclass_to_rdf(xml_file_path, rdf_output_path)


def main():
    """Main function demonstrating usage of the unified converter"""
    # Create converter instance
    converter = UnifiedVerbNetConverter()
    
    # Process all files with complete pipeline (including selectional restrictions)
    print("Processing all files with complete pipeline...")
    converter.process_all_files()
    
    # Alternative: Process only basic conversion
    # print("Converting all files to basic RDF/OWL...")
    # converter.convert_all_basic()
    
    # Alternative: Process single file
    # converter.process_single_file("example-verb.xml")


if __name__ == "__main__":
    main() 