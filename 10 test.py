import os
import xml.etree.ElementTree as ET
from rdflib import Graph, URIRef, Literal, Namespace, RDF

# Define the directory containing the XML files
xml_directory = 'D:/Hamtaa project/10 test/xml_files'  # Updated path

# Namespaces
EX = Namespace("http://example.org/")
VNCLASS = Namespace("http://example.org/vnclass/")
NS = Namespace("http://example.org/ns#")
XSI = Namespace("http://www.w3.org/2001/XMLSchema-instance")

def process_xml_file(xml_file_path, rdf_output_path):
    print(f"Processing file: {xml_file_path}")
    
    # Create RDF Graph
    g = Graph()
    g.bind("ex", EX)
    g.bind("vnclass", VNCLASS)
    g.bind("ns", NS)
    g.bind("xsi", XSI)

    # Parse the XML file
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        print(f"Successfully parsed '{xml_file_path}'. Root tag: {root.tag}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # Function to convert XML to RDF triples
    def add_triples_from_xml_element(element, parent_uri=None):
        # Skip xsi attributes to avoid invalid URIs
        element_uri = VNCLASS[element.tag]

        # Add a triple for the element itself
        if parent_uri:
            g.add((parent_uri, EX.hasChild, element_uri))
        g.add((element_uri, RDF.type, VNCLASS[element.tag]))

        # Add attributes as triples, skipping xsi namespace attributes
        for attr_name, attr_value in element.attrib.items():
            if attr_name.startswith("{http://www.w3.org/2001/XMLSchema-instance}"):
                continue
            attr_uri = VNCLASS[attr_name]
            g.add((element_uri, attr_uri, Literal(attr_value)))

        # Add text content as a triple
        if element.text and element.text.strip():
            g.add((element_uri, EX.hasValue, Literal(element.text.strip())))

        # Recursively process child elements
        for child in element:
            add_triples_from_xml_element(child, element_uri)

    # Convert the root XML element
    add_triples_from_xml_element(root)

    # Serialize the RDF graph to a file
    g.serialize(destination=rdf_output_path, format='turtle')
    print(f"RDF data has been saved to '{rdf_output_path}'.")

# Iterate through all XML files in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, filename)
        rdf_output_path = os.path.join(xml_directory, os.path.splitext(filename)[0] + '.ttl')
        process_xml_file(xml_file_path, rdf_output_path)

print("All files processed.")

