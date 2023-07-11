import yaml
import sys

functionFile = sys.argv[1]
instance_type = sys.argv[2]
cpu_limits = sys.argv[3]
memory_limits = sys.argv[4]

with open(functionFile, "r") as file:
    #yaml_content = yaml.safe_load(file)
    yaml_content = yaml.safe_load(file)

# Modify the value in the YAML content
functionName = list(yaml_content["functions"].keys())[0]
content = yaml_content["functions"][functionName]


#content["limits"] = {
#    'memory': memory_limits,
#    'cpu': cpu_limits   
#}



# CHATGPT; TESTAR
# Check if 'functions' key exists and is a dictionary
if 'functions' in content and isinstance(content['functions'], dict):
    # Iterate over the functions
    for function_name, function_data in content['functions'].items():
        # Check if 'limits' key exists and is a dictionary
        if 'limits' not in function_data or not isinstance(function_data['limits'], dict):
            # Create 'limits' dictionary if it doesn't exist
            function_data['limits'] = {}
        
        # Add CPU and memory limits to the function
        function_data['limits']['cpu'] = '1'
        function_data['limits']['memory'] = '512Mi'






if "limits" in content:
    content["limits"]["memory"] = {memory_limits}
    content["limits"]["cpu"] = {cpu_limits}

else:
    content["limits"] = "memory" + memory_limits
    content["limits"] = "cpu" + cpu_limits


if "constraints" in content:
    print("ola")
    content["constraints"][0] = "beta.kubernetes.io/instance-type=" + instance_type

else: 
    content["constraints"] = ["beta.kubernetes.io/instance-type=" + instance_type]

# Save the modified content back to the file
with open(functionFile, "w") as file:
    yaml.safe_dump(yaml_content, file, sort_keys=False)
