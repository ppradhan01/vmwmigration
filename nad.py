import yaml
import json

def replace_vlan_id_in_yaml(input_file, output_file, vlan_id):
    """
    Reads a YAML file, replaces all occurrences of the hardcoded VLAN ID '1522'
    with the specified vlan_id, and writes the modified YAML to the output file.

    :param input_file: Path to the input YAML file.
    :param output_file: Path to the output YAML file.
    :param vlan_id: VLAN ID to replace the hardcoded ID.
    """
    # Load the YAML file
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

    # Update the metadata name and annotations if they contain 1522
    if "metadata" in data:
        if "name" in data["metadata"] and "1522" in data["metadata"]["name"]:
            data["metadata"]["name"] = data["metadata"]["name"].replace("1522", str(vlan_id))
        if "annotations" in data["metadata"]:
            for key, value in data["metadata"]["annotations"].items():
                if "1522" in value:
                    data["metadata"]["annotations"][key] = value.replace("1522", str(vlan_id))

    # Update the "spec" -> "config" field, which is a JSON string
    if "spec" in data and "config" in data["spec"]:
        config_json = json.loads(data["spec"]["config"])
        if "name" in config_json and "1522" in config_json["name"]:
            config_json["name"] = config_json["name"].replace("1522", str(vlan_id))
        if "netAttachDefName" in config_json and "1522" in config_json["netAttachDefName"]:
            config_json["netAttachDefName"] = config_json["netAttachDefName"].replace("1522", str(vlan_id))
        if "vlanID" in config_json and config_json["vlanID"] == 1522:
            config_json["vlanID"] = vlan_id
        
        # Convert back to a JSON string and update the YAML
        data["spec"]["config"] = json.dumps(config_json, indent=2)

    # Write the updated YAML to the output file
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Example usage
#if __name__ == "__main__":
#    input_yaml = "./nad-template.yaml"  # Path to the input YAML file
#    output_yaml = "./nad.yaml"  # Path to the output YAML file
#    vlan_id = 2022  # The new VLAN ID to replace 1522
#    replace_vlan_id_in_yaml(input_yaml, output_yaml, vlan_id)
#    print(f"Modified YAML written to {output_yaml}")
