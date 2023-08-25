import yaml
import sys

functionFile = sys.argv[1]

with open(functionFile, "r") as file:
    #yaml_content = yaml.safe_load(file)
    yaml_content = yaml.safe_load(file)

# Modify the value in the YAML content
functionName = [yaml_content["functions"].keys()][0]

print(next(iter(functionName)))

# Save the modified content back to the file
with open(functionFile, "w") as file:
    yaml.safe_dump(yaml_content, file, sort_keys=False)


