import os
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, RDF, URIRef , RDFS , BNode

xml_directory = ''  #path

def xmlclass_to_rdf(xml_file_path, rdf_output_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    go = Namespace("http://tavasi.majles.ir/ontology/general/")    
    go1 = "http://tavasi.majles.ir/ontology/general/"  
    go2 = "http://tavasi.majles.ir/ontology/general/Has" 

    g = Graph()
    g.bind("go", go)
    

    for j in root.iter('VNCLASS'):
        id = j.attrib['ID']
        id_uri = URIRef(go1 + id)

        for i in j.find('MEMBERS').findall('MEMBER'):
            name = i.attrib['name']
            name_uri = URIRef(go1 + name)
            g.add((name_uri, RDFS.subClassOf, id_uri))
        
        for p in root.iter('SUBCLASSES'):        
            for k in p.iter('VNSUBCLASS'):
                id2 = k.attrib['ID']
                id2_uri = URIRef(go1 + id2)
                for i in k.find('MEMBERS').findall('MEMBER'):
                    name = i.attrib['name']
                    name_uri = URIRef(go1 + name)
                    g.add((name_uri, RDFS.subClassOf, id2_uri))
                    
    for a in root.iter('VNCLASS'):
        id = a.attrib['ID']
        id_uri = URIRef(go1 + id)
        for p in a.find('SUBCLASSES').findall('VNSUBCLASS'):
            id2 = p.attrib['ID']
            id2_uri = URIRef(go1 + id2)
            g.add((id2_uri, RDFS.subClassOf, id_uri))
            for f in p.find('SUBCLASSES').findall('VNSUBCLASS'):
                id3 = f.attrib['ID']
                id3_uri = URIRef(go1 + id3)
                g.add((id3_uri, RDFS.subClassOf, id2_uri))
                for m in f.find('SUBCLASSES').findall('VNSUBCLASS'):  
                    id4 = m.attrib['ID']
                    id4_uri = URIRef(go1 + id4) 
                    g.add((id4_uri, RDFS.subClassOf, id3_uri)) 
                        
        

    for m in root.iter('THEMROLE'):
        type = m.attrib['type']
        type_uri = URIRef(go2 + type)
        g.add((id_uri, RDFS.subClassOf, type_uri)) 
        

    g.serialize(destination=rdf_output_path, format='turtle')  


for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, filename)
        rdf_output_path = os.path.join(xml_directory, os.path.splitext(filename)[0] + '.ttl')
        xmlclass_to_rdf(xml_file_path, rdf_output_path)

