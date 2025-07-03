import os
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef , RDFS , RDF , OWL


ttl_directory = "TTLs"
xml_directory = "XMLs"  #path

class VerbNetXMLtoRDFConverter:
    def __init__(self, xml_directory="XMLs", ttl_directory="TTLs"):
        self.xml_directory = xml_directory
        self.ttl_directory = ttl_directory
        self.go = Namespace("http://tavasi.majles.ir/ontology/general#")
        self.ontology_iri = URIRef("http://tavasi.majles.ir/ontology/general")
        self.base = "http://tavasi.majles.ir/ontology/general/Verbnet"

    def xmlclass_to_rdf(self, xml_file_path, rdf_output_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        g = Graph(base=self.base)
        g.bind("go", self.go)
        g.add((self.ontology_iri, RDF.type, OWL.Ontology))

        for j in root.iter('VNCLASS'):
            id = j.attrib['ID']
            id_uri = URIRef(self.go[id])
            MEMBERS = j.find('MEMBERS')
            if MEMBERS is not None:
                for i in MEMBERS.findall('MEMBER'):
                    name = i.attrib['name']
                    name2 = str(name).replace(" ", "_")
                    name_uri = URIRef(self.go[name2])
                    g.add((name_uri, RDFS.subClassOf, id_uri))

            for p in root.iter('SUBCLASSES'):
                for k in p.iter('VNSUBCLASS'):
                    id2 = k.attrib['ID']
                    id2_uri = URIRef(self.go[id2])
                    MEMBERS = k.find('MEMBERS')
                    if MEMBERS is not None:
                        for i in MEMBERS.findall('MEMBER'):
                            name = i.attrib['name']
                            name2 = str(name).replace(" ", "_")
                            name_uri = URIRef(self.go[name2])
                            g.add((name_uri, RDFS.subClassOf, id2_uri))

        for a in root.iter('VNCLASS'):
            id = a.attrib['ID']
            id_uri = URIRef(self.go[id])
            SUBCLASSES = a.find('SUBCLASSES')
            if SUBCLASSES is not None:
                for p in SUBCLASSES.findall('VNSUBCLASS'):
                    id2 = p.attrib['ID']
                    id2_uri = URIRef(self.go[id2])
                    g.add((id2_uri, RDFS.subClassOf, id_uri))
                    SUBCLASSES2 = p.find('SUBCLASSES')
                    if SUBCLASSES2 is not None:
                        for f in SUBCLASSES2.findall('VNSUBCLASS'):
                            id3 = f.attrib['ID']
                            id3_uri = URIRef(self.go[id3])
                            g.add((id3_uri, RDFS.subClassOf, id2_uri))
                            SUBCLASSES3 = f.find('SUBCLASSES')
                            if SUBCLASSES3 is not None:
                                for m in SUBCLASSES3.findall('VNSUBCLASS'):
                                    id4 = m.attrib['ID']
                                    id4_uri = URIRef(self.go[id4])
                                    g.add((id4_uri, RDFS.subClassOf, id3_uri))

        for m in root.iter('THEMROLE'):
            type = m.attrib['type']
            type_uri = URIRef(self.go["has" + type])
            g.add((id_uri, RDFS.subClassOf, type_uri))

        g.serialize(destination=rdf_output_path, format='turtle')

    def convert_all(self):
        for filename in os.listdir(self.xml_directory):
            if filename.endswith(".xml"):
                xml_file_path = os.path.join(self.xml_directory, filename)
                rdf_output_path = os.path.join(self.ttl_directory, os.path.splitext(filename)[0] + '.ttl')
                self.xmlclass_to_rdf(xml_file_path, rdf_output_path)

if __name__ == "__main__":
    # Example usage for a single file (as in the original script)
    converter = VerbNetXMLtoRDFConverter()
    xml_file = "XMLs/appear-48.1.1.xml"
    ttl_file = "TTLs/appear-48.1.1.ttl"
    converter.xmlclass_to_rdf(xml_file, ttl_file)
    # To convert all files in the directory, uncomment the following line:
    # converter.convert_all()
