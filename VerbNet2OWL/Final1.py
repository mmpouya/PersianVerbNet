import os
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef , RDFS , RDF , OWL


ttl_directory = "TTLs"
xml_directory = "XMLs"  #path

def xmlclass_to_rdf(xml_file_path, rdf_output_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    g = Graph(base="http://tavasi.majles.ir/ontology/general/Verbnet")
    go = Namespace("http://tavasi.majles.ir/ontology/general#")     
    g.bind("go", go)
    
    ontology_iri = URIRef("http://tavasi.majles.ir/ontology/general")
    g.add((ontology_iri, RDF.type, OWL.Ontology))

    for j in root.iter('VNCLASS'):
        id = j.attrib['ID']
        id_uri = URIRef(go[id])
        MEMBERS = j.find('MEMBERS')
        if MEMBERS is None:
            pass
        else:
            for i in j.find('MEMBERS').findall('MEMBER'):
                name = i.attrib['name']
                name2 = str(name)
                name2.replace(" ", "_")
                name_uri = URIRef(go[name2])
                g.add((name_uri, RDFS.subClassOf, id_uri))
            
        for p in root.iter('SUBCLASSES'):        
            for k in p.iter('VNSUBCLASS'):
                id2 = k.attrib['ID']
                id2_uri = URIRef(go[id2])
                MEMBERS = k.find('MEMBERS')
                if MEMBERS is None:
                    pass
                for i in k.find('MEMBERS').findall('MEMBER'):
                    name = i.attrib['name']
                    name = str(name)
                    name.replace(" ","_")
                    name_uri = URIRef(go[name])
                    g.add((name_uri, RDFS.subClassOf, id2_uri))
                    
    for a in root.iter('VNCLASS'):
        id = a.attrib['ID']
        id_uri = URIRef(go[id])
        SUBCLASSES = a.find('SUBCLASSES')
        if SUBCLASSES is None:
            pass
        else:
            for p in a.find('SUBCLASSES').findall('VNSUBCLASS'):
                id2 = p.attrib['ID']
                id2_uri = URIRef(go[id2])
                g.add((id2_uri, RDFS.subClassOf, id_uri))
                SUBCLASSES = p.find('SUBCLASSES')
                if SUBCLASSES is None:
                    pass
                else:
                    for f in p.find('SUBCLASSES').findall('VNSUBCLASS'):
                        id3 = f.attrib['ID']
                        id3_uri = URIRef(go[id3])
                        g.add((id3_uri, RDFS.subClassOf, id2_uri))
                        SUBCLASSES = f.find('SUBCLASSES')
                        if SUBCLASSES is None:
                            pass
                        else:
                            for m in f.find('SUBCLASSES').findall('VNSUBCLASS'):  
                                id4 = m.attrib['ID']
                                id4_uri = URIRef(go[id4])
                                g.add((id4_uri, RDFS.subClassOf, id3_uri)) 
                                    
            

    for m in root.iter('THEMROLE'):
        type = m.attrib['type']
        has = "has"
        type = has + type
        type_uri = URIRef(go[type])
        g.add((id_uri, RDFS.subClassOf, type_uri)) 
        

    g.serialize(destination=rdf_output_path, format='turtle')  


# for filename in os.listdir(xml_directory):
#     if filename.endswith(".xml"):
#         xml_file_path = os.path.join(xml_directory, filename)
#         rdf_output_path = os.path.join(ttl_directory, os.path.splitext(filename)[0] + '.ttl')
#         xmlclass_to_rdf(xml_file_path, rdf_output_path)

if __name__ == "__main__":
    xml_directory = "XMLs/appear-48.1.1.xml"
    ttl_directory = "TTLs/appear-48.1.1.ttl"   
    xmlclass_to_rdf(xml_directory,ttl_directory)
