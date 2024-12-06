import os
import xml.etree.ElementTree as ET
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from rdflib.namespace import XSD

# Define paths
xml_file_path = 'D:/Hamtaa project/10 test/search-35.2.xml'  # Ensure this path is correct
rdf_output_path = 'output.ttl'

# Check if the XML file exists
if not os.path.isfile(xml_file_path):
    print(f"The file '{xml_file_path}' was not found.")
    exit(1)

# Debugging output for confirmation
print(f"File '{xml_file_path}' exists, proceeding with parsing...")

# Namespaces
EX = Namespace("http://example.org/")
VNCLASS = Namespace("http://example.org/vnclass/")
NS = Namespace("http://example.org/ns#")
XSI = Namespace("http://www.w3.org/2001/XMLSchema-instance")

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
    exit(1)

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


g.serialize(destination='D:/Hamtaa project/10 test/search-35.2.ttl', format='turtle')

print("RDF data has been saved to 'D:/Hamtaa project/10 test/search-35.2.ttl'.")