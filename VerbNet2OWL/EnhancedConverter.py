import os
import xml.etree.ElementTree as ET
import re
from rdflib import Graph, Namespace, URIRef, RDFS, RDF, OWL, Literal

class EnhancedVerbNetXMLtoRDFConverter:
    def __init__(self, xml_directory="verbnet3.3", ttl_directory="TTLs"):
        self.xml_directory = xml_directory
        self.ttl_directory = ttl_directory
        self.go = Namespace("http://tavasi.majles.ir/ontology/general#")
        self.ontology_iri = URIRef("http://tavasi.majles.ir/ontology/general")
        self.base = "http://tavasi.majles.ir/ontology/general/Verbnet"

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
            
            # Process FRAMES - simplified version
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

            # Process SUBCLASSES - simplified
            subclasses = vnclass.find('SUBCLASSES')
            if subclasses is not None:
                for subclass in subclasses.findall('VNSUBCLASS'):
                    subclass_id = subclass.attrib['ID']
                    subclass_uri = URIRef(self.go[subclass_id])
                    g.add((subclass_uri, RDFS.subClassOf, class_uri))
                    
                    # Process nested members in subclasses - simplified
                    subclass_members = subclass.find('MEMBERS')
                    if subclass_members is not None:
                        for member in subclass_members.findall('MEMBER'):
                            name = member.attrib['name']
                            name2 = str(name).replace(" ", "_")
                            name_uri = URIRef(self.go[name2])
                            g.add((name_uri, RDFS.subClassOf, subclass_uri))

        g.serialize(destination=rdf_output_path, format='turtle')

    def convert_all(self):
        """Convert all XML files in the directory to TTL"""
        for filename in os.listdir(self.xml_directory):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.xml_directory, filename)
                ttl_filename = os.path.splitext(filename)[0] + '.ttl'
                rdf_output_path = os.path.join(self.ttl_directory, ttl_filename)
                print(f"Converting {filename} to {ttl_filename}")
                self.xmlclass_to_rdf(xml_file_path, rdf_output_path)

if __name__ == "__main__":
    converter = EnhancedVerbNetXMLtoRDFConverter()
    
    # Convert a single file for testing
    xml_file = "verbnet3.3/accept-77.1.xml"
    ttl_file = "TTLs/accept-77.1.ttl"
    ttl_file = "accept-77.1.ttl"
    converter.xmlclass_to_rdf(xml_file, ttl_file)
    
    # Uncomment to convert all files
    # converter.convert_all() 