import json
import yaml
import xmltodict

# File paths
json_path = "./raw_ping_reports/scan_results.json"
yaml_path = "./raw_ping_reports/scan_results.yaml"
xml_path = "./raw_ping_reports/scan_results.xml"

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_xml(path):
    with open(path, 'r') as f:
        return xmltodict.parse(f.read())

def main():
    json_dict = load_json(json_path)
    yaml_dict = load_yaml(yaml_path)
    xml_dict = load_xml(xml_path)

    print("JSON as dict:", json_dict)
    print("YAML as dict:", yaml_dict)
    print("XML as dict:", xml_dict)

if __name__ == "__main__":
    main()
