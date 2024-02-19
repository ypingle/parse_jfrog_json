import parse_json_store
import json
import sys
import xml.etree.ElementTree as ET

def extract_dependencies(file_path, json_name_attribute, json_version_attribute):
    dependencies = {}

    # Load JSON data from the file with explicit encoding
    with open(file_path, encoding='utf-8') as file:
        json_data = json.load(file)

    # Parse each JSON object
    for obj in json_data:
        try:
            props = obj['props']
            title = props[json_name_attribute][0]
            version = props[json_version_attribute][0]

            # Store nuget_title as key and nuget_version as value in dependencies
            dependencies[title] = version

        except KeyError:
            # Handle missing 'props' or specific keys within 'props'
            print("Props or specific keys are missing for " + obj['path'])
            continue  # Continue to the next object in case of missing keys

    return dependencies

def extract_dependencies_maven(file_path):
    dependencies = {}
    version = ''
    title = ''
    group = 'org.apache.maven'

    # Load JSON data from the file with explicit encoding
    with open(file_path, encoding='utf-8') as file:
        json_data = json.load(file)

    # Parse each JSON object
    for obj in json_data:
        try:
            props = obj['path'].split('/')
            if(props):
                props = props[-1]
                if(props.endswith(".jar")):
                    props = props[:-4]                 
                    if(props.count('-') == 1):
                        props = props.split('-')
                        title = props[0]
                        version = props[1] + '|' + group
        except KeyError:
            # Handle missing 'props' or specific keys within 'props'
            print("Props or specific keys are missing for " + obj['path'])
            continue  # Continue to the next object in case of missing keys

        # Store title as key and nuget_version as value in dependencies
        dependencies[title] = version
    return dependencies

def main():

    # Check if the file path is provided as a command-line argument
    if len(sys.argv) < 3:
        print("usage: parse_jfrog_json <npm | nuget | pypi | maven2> <file path>")
        sys.exit(1)

    manifest = sys.argv[1]
    file_path = sys.argv[2]

    package_attrib = {
        'npm': {
            'name': 'npm.name',
            'version': 'npm.version'
        },
        'nuget': {
            'name': 'nuget.title',
            'version': 'nuget.version'
        },
        'pypi': {
            'name': 'pypi.name',
            'version': 'pypi.version'
        }
    }    

    if(manifest == 'maven2'):
        dependencies = extract_dependencies_maven(file_path)
    else:
        dependencies = extract_dependencies(file_path, package_attrib[manifest]['name'], package_attrib[manifest]['version'])
    parse_json_store.create_package(dependencies, file_path, manifest)

if __name__ == "__main__":
    main()
