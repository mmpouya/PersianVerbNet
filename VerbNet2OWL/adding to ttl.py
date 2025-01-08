import os
from Final1 import xmlclass_to_rdf
from Final2 import parse_and_generate_OWL

ttl_directory = "TTLs"
xml_directory = "XMLs"  #path


for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, filename)
        rdf_output_path = os.path.join(ttl_directory, os.path.splitext(filename)[0] + '.ttl')
        xmlclass_to_rdf(xml_file_path, rdf_output_path)
        print (f"corresponding ttl from {filename} is created")
# for filename in os.listdir(ttl_directory):
#     if filename.endswith(".ttl"):
#         ttl_output_path = os.path.join(ttl_directory, filename)
#         with open(ttl_output_path, 'r') as file:
#             ttl = file.read()
#         ttl.replace("@prefix go: <http://tavasi.majles.ir/ontology/general/> .", "@prefix go: <http://tavasi.majles.ir/ontology/general/#> .")
#         with open(ttl_output_path, 'w') as file:
#             file.write(modified_content)

for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, filename)
        ttl_output_path = os.path.join(ttl_directory, os.path.splitext(filename)[0] + '.ttl')
        # ttl_output_path = os.path.join(ttl_directory, filename + '.ttl')
        ttl_added_string = parse_and_generate_OWL(xml_file_path)
        
        with open(ttl_output_path, 'r') as file:
            content = file.read()
        if ttl_added_string == "":
            modified_content = content + "\n#This verb has no selectional restriction \n"
        else:
            modified_content = content + f"\n# Generated String:\n{ttl_added_string}\n"
        with open(ttl_output_path, 'w') as file:
            file.write(modified_content)
        print (f"corresponding ttl from {filename} is modified")