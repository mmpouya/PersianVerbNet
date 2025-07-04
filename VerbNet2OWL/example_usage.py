#!/usr/bin/env python3
"""
Example usage of the UnifiedVerbNetConverter class.
This demonstrates how to use the unified class that combines all functionality.
"""

from UnifiedVerbNetConverter import UnifiedVerbNetConverter

def example_single_file():
    """Example: Process a single XML file"""
    print("=== Processing Single File ===")
    converter = UnifiedVerbNetConverter()
    
    # Process a single file through the complete pipeline
    converter.process_single_file("example-verb.xml")
    print("Single file processing completed!\n")

def example_basic_conversion():
    """Example: Basic conversion without selectional restrictions"""
    print("=== Basic Conversion ===")
    converter = UnifiedVerbNetConverter()
    
    # Convert all files to basic RDF/OWL format
    converter.convert_all_basic()
    print("Basic conversion completed!\n")

def example_complete_pipeline():
    """Example: Complete pipeline with selectional restrictions"""
    print("=== Complete Pipeline ===")
    converter = UnifiedVerbNetConverter()
    
    # Process all files through the complete pipeline
    converter.process_all_files()
    print("Complete pipeline processing completed!\n")

def example_custom_directories():
    """Example: Using custom directories"""
    print("=== Custom Directories ===")
    converter = UnifiedVerbNetConverter(
        xml_directory="custom_xml_folder",
        ttl_directory="custom_ttl_folder"
    )
    
    # Process files from custom directories
    converter.process_all_files()
    print("Custom directory processing completed!\n")

def example_step_by_step():
    """Example: Step-by-step processing"""
    print("=== Step-by-Step Processing ===")
    converter = UnifiedVerbNetConverter()
    
    # Step 1: Convert XML to RDF/OWL
    xml_file = "XMLs/example-verb.xml"
    ttl_file = "TTLs/example-verb.ttl"
    converter.xmlclass_to_rdf(xml_file, ttl_file)
    print("Step 1: XML to RDF conversion completed")
    
    # Step 2: Generate selectional restrictions
    owl_restrictions = converter.parse_and_generate_OWL(xml_file)
    print(f"Step 2: Generated OWL restrictions: {len(owl_restrictions)} characters")
    
    # Step 3: Combine both
    with open(ttl_file, 'r') as file:
        content = file.read()
    
    if owl_restrictions == "":
        modified_content = content + "\n#This verb has no selectional restriction \n"
    else:
        modified_content = content + f"\n# Generated String:\n{owl_restrictions}\n"
    
    with open(ttl_file, 'w') as file:
        file.write(modified_content)
    print("Step 3: Combined processing completed!\n")

if __name__ == "__main__":
    print("UnifiedVerbNetConverter Usage Examples")
    print("=" * 50)
    
    # Uncomment the example you want to run:
    
    # example_single_file()
    # example_basic_conversion()
    # example_complete_pipeline()
    # example_custom_directories()
    # example_step_by_step()
    
    print("To run examples, uncomment the desired function call above.")
    print("\nAvailable methods:")
    print("- process_single_file(xml_filename): Process one file completely")
    print("- process_all_files(): Process all XML files completely")
    print("- convert_all_basic(): Basic conversion without restrictions")
    print("- xmlclass_to_rdf(xml_path, ttl_path): Convert XML to RDF")
    print("- parse_and_generate_OWL(xml_path): Generate OWL restrictions") 