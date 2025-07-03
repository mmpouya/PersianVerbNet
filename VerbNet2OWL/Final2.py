import os
import xml.etree.ElementTree as ET
from rdflib import Namespace, URIRef

class OWLGenerator:
    def __init__(self, namespace_uri="http://tavasi.majles.ir/ontology/general#"):
        self.go_ns = Namespace(namespace_uri)
        self.final_output = ""

    def parse_and_generate_OWL(self, xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        self.final_output = ""
        self._process_classes(root, 'VNCLASS')
        self._process_classes(root, 'VNSUBCLASS')
        return self.final_output

    def _process_classes(self, root, tag):
        for j in root.iter(tag):
            id = j.attrib['ID']
            id_uri = URIRef('<' + str(self.go_ns) + id + '>')
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
        for frst in t.findall('SELRESTRS'):
            for sec in frst.findall('SELRESTRS'):
                for thrd in sec.findall('SELRESTRS'):
                    for type3 in thrd.findall('SELRESTR'):
                        type3_uri = URIRef('<' + str(self.go_ns) + type3.attrib['type'] + '>')
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
                    type2_uri = URIRef('<' + str(self.go_ns) + type2.attrib['type'] + '>')
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
                type1_uri = URIRef('<' + str(self.go_ns) + type1.attrib['type'] + '>')
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
        go3 = "<http://tavasi.majles.ir/ontology/general#EventHas"
        predicate = go3 + themrole + ">"
        return predicate

    @staticmethod
    def nottype(type_uri):
        return f"""[ rdf:type owl:Class ; owl:complementOf {type_uri} ]"""

    @staticmethod
    def only(id_uri, predicate, rest):
        return f"""{id_uri} rdfs:subClassOf [ rdf:type owl:Restriction ;\n                      owl:onProperty {predicate} ;\n                      owl:allValuesFrom {rest}\n                    ].\n"""

    @staticmethod
    def AND(type1, type2):
        return f"""[owl:intersectionOf ( {type1}\n                                            {type2}\n                                            ) ;\n                                          rdf:type owl:Class]"""

    @staticmethod
    def OR(type1, type2):
        return f"""[ rdf:type owl:Class ;\n                                          owl:unionOf ( {type1}\n                                                        {type2}\n                                                      )]\n"""

def main():
    xml_directory = "XMLs/"
    generator = OWLGenerator()
    for filename in os.listdir(xml_directory):
        xml_file_path = os.path.join(xml_directory, filename)
        x = generator.parse_and_generate_OWL(xml_file_path)
        print(x)

if __name__ == "__main__":
    main()