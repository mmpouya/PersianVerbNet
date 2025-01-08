import os
import xml.etree.ElementTree as ET
from rdflib import Namespace, URIRef


def parse_and_generate_OWL(xml_file_path):
    go1 = Namespace("http://tavasi.majles.ir/ontology/general#")

    final_output = ""
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
      
    for j in root.iter('VNCLASS'):
        id = j.attrib['ID']
        id_uri = URIRef('<'+ go1 + id +'>')
        selrestr_elements = []
        themroles = j.find('THEMROLES')
        if themroles is None:
            continue
        
        for t in themroles.findall('THEMROLE'):
            themrole_type = t.attrib['type']
            predicate = predicate_uri(themrole_type)
            

            for frst in t.findall('SELRESTRS'):
                for sec in frst.findall('SELRESTRS'):
                    for thrd in sec.findall('SELRESTRS'):                      
                        for type3 in thrd.findall('SELRESTR'): 
                            type3_uri = URIRef('<'+ go1 + type3.attrib['type'] +'>')                                 
                            if type3.attrib.get('Value') == '-':
                                nottype3 = nottype(type3_uri)
                                selrestr_elements.append(nottype3)
                            else:
                                selrestr_elements.append(type3_uri) 
                        if thrd.findall('SELRESTR'):
                            SELRESTR_element = thrd.find('SELRESTR')
                            SELRESTR_count = len(list(SELRESTR_element))
                            if thrd.attrib.get('logic') == "or":
                                if len(selrestr_elements) >= 2:
                                    or_type3 = OR(selrestr_elements[-1],selrestr_elements[-2])
                                    selrestr_elements.append(or_type3)
                            elif thrd.text is None:
                                pass
                            elif SELRESTR_count == 1:
                                pass
                            elif not thrd.attrib.get('logic') == "or":
                                if len(selrestr_elements) >= 2:
                                    AND_type3 = AND(selrestr_elements[-1],selrestr_elements[-2])
                                    selrestr_elements.append(AND_type3)
                    for type2 in sec.findall('SELRESTR'):
                        type2_uri = URIRef('<'+ go1 + type2.attrib['type'] +'>')
                        if type2.attrib.get('Value') == '-':
                            nottype2 = nottype(type2_uri)
                            selrestr_elements.append(nottype2)
                        else:
                            selrestr_elements.append(type2_uri)
                    if sec.findall('SELRESTR'): 
                        SELRESTR_element = sec.find('SELRESTR')
                        SELRESTR_count = len(list(SELRESTR_element))
                        if sec.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                or_type2 = OR(selrestr_elements[-1],selrestr_elements[-2])
                                selrestr_elements.append(or_type2)
                        elif sec.text is None:
                            pass
                        elif SELRESTR_count == 1:
                            pass
                        elif not sec.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                AND_type2 = AND(selrestr_elements[-1],selrestr_elements[-2])
                                selrestr_elements.append(AND_type2)
                for type1 in frst.findall('SELRESTR'):
                    type1_uri = URIRef('<'+ go1 + type1.attrib['type'] +'>')
                    if type1.attrib.get('Value') == '-':
                        nottype1 = nottype(type1_uri)
                        selrestr_elements.append(nottype1)
                    else:
                        selrestr_elements.append(type1_uri) 
                if frst.findall('SELRESTR'):
                    SELRESTR_element = frst.find('SELRESTR')
                    SELRESTR_count = len(list(SELRESTR_element))
                    if frst.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            or_type1 = OR(selrestr_elements[-1],selrestr_elements[-2])
                            selrestr_elements.append(or_type1)
                    elif frst.text is None:
                        pass
                    elif SELRESTR_count == 1:
                        pass
                    elif not frst.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            AND_type1 = AND(selrestr_elements[-1],selrestr_elements[-2])
                            selrestr_elements.append(AND_type1)
            if len(selrestr_elements) >= 1:         
                if frst.text is None:
                    pass
                else:            
                    final1 = only(id_uri,predicate,selrestr_elements[-1])
                # print(final_output)
                    final_output = final_output + final1

#-------------------------------------------------------------------
    
    for j in root.iter('VNSUBCLASS'):
        id = j.attrib['ID']
        id_uri = URIRef('<'+ go1 + id +'>')
        selrestr_elements = []
        themroles = j.find('THEMROLES')
        if themroles is None:
            continue
        
        for t in themroles.findall('THEMROLE'):
            themrole_type = t.attrib['type']
            predicate = predicate_uri(themrole_type)

            for frst in t.findall('SELRESTRS'):
                for sec in frst.findall('SELRESTRS'):
                    for thrd in sec.findall('SELRESTRS'):                      
                        for type3 in thrd.findall('SELRESTR'):
                            type3_uri = URIRef('<'+ go1 + type3.attrib['type'] +'>')                                 
                            if type3.attrib.get('Value') == '-':
                                nottype3 = nottype(type3_uri)
                                selrestr_elements.append(nottype3)
                            else:
                                selrestr_elements.append(type3_uri) 
                        if thrd.findall('SELRESTR'):
                            SELRESTR_element = thrd.find('SELRESTR')
                            SELRESTR_count = len(list(SELRESTR_element))
                            if thrd.attrib.get('logic') == "or":
                                if len(selrestr_elements) >= 2:
                                    or_type3 = OR(selrestr_elements[-1],selrestr_elements[-2])
                                    selrestr_elements.append(or_type3)
                            elif thrd.text is None:
                                pass
                            elif SELRESTR_count == 1:
                                pass
                            elif not thrd.attrib.get('logic') == "or":
                                if len(selrestr_elements) >= 2:
                                    AND_type3 = AND(selrestr_elements[-1],selrestr_elements[-2])
                                    selrestr_elements.append(AND_type3)
                    for type2 in sec.findall('SELRESTR'):
                        type2_uri = URIRef('<'+ go1 + type2.attrib['type'] +'>')
                        if type2.attrib.get('Value') == '-':
                            nottype2 = nottype(type2_uri)
                            selrestr_elements.append(nottype2)
                        else:
                            selrestr_elements.append(type2_uri)
                    if sec.findall('SELRESTR'): 
                        SELRESTR_element = sec.find('SELRESTR')
                        SELRESTR_count = len(list(SELRESTR_element))
                        if sec.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                or_type2 = OR(selrestr_elements[-1],selrestr_elements[-2])
                                selrestr_elements.append(or_type2)
                        elif sec.text is None:
                            pass
                        elif SELRESTR_count == 1:
                            pass
                        elif not sec.attrib.get('logic') == "or":
                            if len(selrestr_elements) >= 2:
                                AND_type2 = AND(selrestr_elements[-1],selrestr_elements[-2])
                                selrestr_elements.append(AND_type2)
                for type1 in frst.findall('SELRESTR'):
                    type1_uri = URIRef('<'+ go1 + type1.attrib['type'] +'>')
                    if type1.attrib.get('Value') == '-':
                        nottype1 = nottype(type1_uri)
                        selrestr_elements.append(nottype1)
                    else:
                        selrestr_elements.append(type1_uri) 
                if frst.findall('SELRESTR'):
                    SELRESTR_element = frst.find('SELRESTR')
                    SELRESTR_count = len(list(SELRESTR_element))
                    if frst.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            or_type1 = OR(selrestr_elements[-1],selrestr_elements[-2])
                            selrestr_elements.append(or_type1)
                    elif frst.text is None:
                        pass
                    elif SELRESTR_count == 1:
                        pass
                    elif not frst.attrib.get('logic') == "or":
                        if len(selrestr_elements) >= 2:
                            AND_type1 = AND(selrestr_elements[-1],selrestr_elements[-2])
                            selrestr_elements.append(AND_type1)
            if len(selrestr_elements) >= 1:            
                if frst.text is None:
                    pass
                else:
                    final2 = only(id_uri,predicate,selrestr_elements[-1])
                    final_output = final_output + final2
                    # print(final_output)
    return final_output
                    
            
            

def predicate_uri (themrole):
    go3 = "<http://tavasi.majles.ir/ontology/general#EventHas" 
    predicate = go3 + themrole + ">"
    return predicate

def nottype(type):
    notType = f"""[ rdf:type owl:Class ; owl:complementOf {type} ]"""
    return notType

#check
def only(id, predicate, rest):
    only = f"""{id} rdfs:subClassOf [ rdf:type owl:Restriction ;
                      owl:onProperty {predicate} ;
                      owl:allValuesFrom {rest}
                    ].\n"""
    return only
def AND (type1, type2):
    ANDrest = f"""[owl:intersectionOf ( {type1}
                                            {type2}
                                            ) ;
                                          rdf:type owl:Class]"""
    return ANDrest
def OR (type1, type2):
    ORrest = f"""[ rdf:type owl:Class ;
                                          owl:unionOf ( {type1}
                                                        {type2}
                                                      )]
"""
    return ORrest

if __name__ == "__main__":
    xml_directory = "XMLs/"
    for filename in os.listdir(xml_directory):       
        xml_file_path = os.path.join(xml_directory, filename)
        x = parse_and_generate_OWL(xml_file_path)
        print(x)