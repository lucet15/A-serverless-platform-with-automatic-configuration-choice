import yaml
import sys

functionFile = sys.argv[1]
instance_type = sys.argv[2]

with open(functionFile, "r") as file:
    #yaml_content = yaml.safe_load(file)
    yaml_content = yaml.safe_load(file)

# Modify the value in the YAML content
functionName = list(yaml_content["functions"].keys())[0]
content = yaml_content["functions"][functionName]

if "constraints" in content:
    print("ola")
    content["constraints"][0] = "beta.kubernetes.io/instance-type=" + instance_type

else: 
    content["constraints"] = ["beta.kubernetes.io/instance-type=" + instance_type]

# Save the modified content back to the file
with open(functionFile, "w") as file:
    yaml.safe_dump(yaml_content, file, sort_keys=False)
