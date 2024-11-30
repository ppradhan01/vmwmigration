import yaml

def replace_vlan_ids_in_yaml(input_file, output_file, vlan_ids):
    """
    Reads a YAML file, for each VLAN ID in vlan_ids, replaces the hardcoded VLAN ID '1522'
    with the specified vlan_id and repeats the bridge-mapping section for each vlan_id.
    Outputs the modified YAML to the output file.

    :param input_file: Path to the input YAML file.
    :param output_file: Path to the output YAML file.
    :param vlan_ids: List of VLAN IDs to replace 1522 with and repeat the section.
    """
    # Load the YAML file
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

    # Prepare the bridge mappings section
    bridge_mappings = []
    
    # Repeat the bridge-mapping section for each VLAN ID
    print("appending "+str(vlan_ids))

    for vlan_id in vlan_ids:
        bridge_mappings.append({
            "localnet": f"vlan-{vlan_id}",
            "bridge": "ovs-br1",
            "state": "present"
        })


    # Replace the original bridge-mappings with the new ones
    if "spec" in data and "ovn" in data["spec"]:
        data["spec"]["ovn"]["bridge-mappings"] = bridge_mappings
    print("bridge mappings was "+str(bridge_mappings))
    print("data was  "+str(data))

    # Write the updated YAML to the output file
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Example usage
#if __name__ == "__main__":
#    input_yaml = "./nncp-template.yaml"  # Path to the input YAML file
#    output_yaml = "./nncp.yaml"  # Path to the output YAML file
#    vlan_ids = [1522, 1523, 1524]  # List of VLAN IDs to replace 1522 with and repeat the section
#    replace_vlan_ids_in_yaml(input_yaml, output_yaml, vlan_ids)
#    print(f"Modified YAML written to {output_yaml}")
