# UnifiedVerbNetConverter

A unified Python class that combines all VerbNet XML to RDF/OWL conversion functionality into a single, comprehensive solution.

## Overview

The `UnifiedVerbNetConverter` class merges functionality from multiple separate files:
- **Final1.py**: Basic XML to RDF conversion
- **EnhancedConverter.py**: Enhanced conversion with frames and examples
- **Final2.py**: OWL generation with selectional restrictions
- **adding to ttl.py**: Complete processing workflow

## Features

### Core Functionality
- **XML to RDF/OWL Conversion**: Convert VerbNet XML files to Turtle format
- **Enhanced Frame Processing**: Include frame descriptions, examples, and semantic predicates
- **Selectional Restrictions**: Generate OWL restrictions based on thematic roles
- **Recursive Subclass Handling**: Process nested subclasses automatically
- **URI Sanitization**: Safe URI generation for frame names and other elements

### Processing Options
- **Complete Pipeline**: Full conversion with selectional restrictions
- **Basic Conversion**: Simple XML to RDF without restrictions
- **Single File Processing**: Process individual files
- **Batch Processing**: Process all XML files in a directory

## Installation

```bash
pip install rdflib
```

## Usage

### Basic Usage

```python
from UnifiedVerbNetConverter import UnifiedVerbNetConverter

# Create converter instance
converter = UnifiedVerbNetConverter()

# Process all files with complete pipeline
converter.process_all_files()
```

### Advanced Usage

```python
# Custom directories
converter = UnifiedVerbNetConverter(
    xml_directory="my_xml_files",
    ttl_directory="my_output_files",
    namespace_uri="http://my.ontology.org#"
)

# Process single file
converter.process_single_file("verb-123.xml")

# Basic conversion only
converter.convert_all_basic()
```

### Step-by-Step Processing

```python
converter = UnifiedVerbNetConverter()

# Step 1: Convert XML to RDF
converter.xmlclass_to_rdf("input.xml", "output.ttl")

# Step 2: Generate selectional restrictions
restrictions = converter.parse_and_generate_OWL("input.xml")

# Step 3: Combine both (handled automatically in process_single_file)
```

## Class Methods

### Main Processing Methods

- `process_all_files()`: Process all XML files through complete pipeline
- `process_single_file(xml_filename)`: Process single file completely
- `convert_all_basic()`: Basic conversion without selectional restrictions

### Core Conversion Methods

- `xmlclass_to_rdf(xml_file_path, rdf_output_path)`: Convert XML to RDF/OWL
- `parse_and_generate_OWL(xml_file_path)`: Generate OWL restrictions
- `_process_subclasses(g, parent_element, parent_uri)`: Handle nested subclasses

### Utility Methods

- `sanitize_uri(text)`: Sanitize text for URI usage
- `predicate_uri(themrole)`: Generate predicate URIs
- `nottype(type_uri)`: Generate NOT restrictions
- `only(id_uri, predicate, rest)`: Generate ONLY restrictions
- `AND(type1, type2)`: Generate AND restrictions
- `OR(type1, type2)`: Generate OR restrictions

## Configuration

### Constructor Parameters

```python
UnifiedVerbNetConverter(
    xml_directory="XMLs",           # Input XML directory
    ttl_directory="TTLs",           # Output TTL directory
    namespace_uri="http://tavasi.majles.ir/ontology/general#"  # Namespace URI
)
```

### Default Settings

- **XML Directory**: `"XMLs"`
- **TTL Directory**: `"TTLs"`
- **Namespace**: `"http://tavasi.majles.ir/ontology/general#"`
- **Base URI**: `"http://tavasi.majles.ir/ontology/general/Verbnet"`

## Output Format

The converter generates Turtle (.ttl) files containing:

1. **Ontology Declaration**: OWL ontology metadata
2. **Class Hierarchy**: VerbNet classes and subclasses
3. **Member Relationships**: Verb members of classes
4. **Frame Information**: Frame descriptions, examples, and semantics
5. **Thematic Roles**: Role relationships
6. **Selectional Restrictions**: OWL restrictions based on thematic roles

## Example Output

```turtle
@prefix go: <http://tavasi.majles.ir/ontology/general#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://tavasi.majles.ir/ontology/general> a owl:Ontology .

go:accept-77.1 a owl:Class .
go:accept rdfs:subClassOf go:accept-77.1 .

# Frame information
go:Frame_1_1_NP_V_NP a owl:Class ;
    go:hasDescriptionNumber "1.1" ;
    go:hasPrimaryPattern "NP V NP" ;
    go:hasSecondaryPattern "NP V NP" ;
    go:hasXTag "NP V NP" ;
    go:hasExample "The committee accepted the proposal" .

# Selectional restrictions
go:accept-77.1 rdfs:subClassOf [ rdf:type owl:Restriction ;
                      owl:onProperty <http://tavasi.majles.ir/ontology/general#EventHasAgent> ;
                      owl:allValuesFrom go:animate
                    ] .
```

## Migration from Separate Files

### Old Approach
```python
# Multiple imports and separate calls
from Final1 import xmlclass_to_rdf
from Final2 import parse_and_generate_OWL

xmlclass_to_rdf(xml_file, ttl_file)
restrictions = parse_and_generate_OWL(xml_file)
# Manual combination...
```

### New Approach
```python
# Single unified class
from UnifiedVerbNetConverter import UnifiedVerbNetConverter

converter = UnifiedVerbNetConverter()
converter.process_single_file("verb.xml")
```

## Error Handling

The converter includes robust error handling for:
- Missing XML files
- Invalid XML structure
- File I/O errors
- URI generation issues

## Performance

- **Single File**: ~1-5 seconds depending on XML complexity
- **Batch Processing**: Linear scaling with number of files
- **Memory Usage**: Minimal, processes files individually

## Dependencies

- `rdflib`: RDF/OWL processing
- `xml.etree.ElementTree`: XML parsing
- `re`: Regular expressions for URI sanitization
- `os`: File system operations

## License

This code is part of the PersianVerbNet project. 