import yaml

def replace_interfaces_in_yaml(input_file, output_file, inf0, inf1):
    # Load the YAML file
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

    # Function to recursively replace values in a nested structure
    def replace_values(obj, target, replacement):
        if isinstance(obj, dict):
            return {key: replace_values(value, target, replacement) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [replace_values(item, target, replacement) for item in obj]
        elif isinstance(obj, str) and obj == target:
            return replacement
        return obj

    # Replace all occurrences of ens6f0 and ens6f1
    data = replace_values(data, "ens6f0", inf0)
    data = replace_values(data, "ens6f1", inf1)

    # Write the modified YAML to the output file
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Example usage
#if __name__ == "__main__":
#    input_yaml = "./nmstate-config-template.yaml"  # Input file path
#    output_yaml = "./nmstate-config.yaml"  # Output file path
#    replace_interfaces_in_yaml(input_yaml, output_yaml, "eth0", "eth1")
#    print(f"Modified YAML written to {output_yaml}")
