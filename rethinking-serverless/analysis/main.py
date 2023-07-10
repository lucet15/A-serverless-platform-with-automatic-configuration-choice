from helpers import create_model
import sys
import yaml



def updateConfiguration(functionFile, instante_type, cpu_limit, memory_limit):
    # Update the configurations in the YAML file with model's output
    
    with open(functionFile, "r") as file:
    #yaml_content = yaml.safe_load(file)
    yaml_content = yaml.safe_load(file)

    # Modify the value in the YAML content
    functionName = list(yaml_content["functions"].keys())[0]
    content = yaml_content["functions"][functionName]


    content["limits"] = {
        'memory:' + memory_limit,
        'cpu:' + cpu_limit   
    }

    if "constraints" in content:
        print("ola")
        content["constraints"][0] = "beta.kubernetes.io/instance-type=" + instance_type

    else: 
        content["constraints"] = ["beta.kubernetes.io/instance-type=" + instance_type]

    # Save the modified content back to the file
    with open(functionFile, "w") as file:
        yaml.safe_dump(yaml_content, file, sort_keys=False)



def updateURL(functionFile, openfaasURL):
    # Update OpenFaas'a gateway

    with open(functionFile, "r") as file:
        #yaml_content = yaml.safe_load(file)
        yaml_content = yaml.safe_load(file)

    # Modify the value in the YAML content
    yaml_content["provider"]["gateway"] = openfaasURL

    # Save the modified content back to the file
    with open(functionFile, "w") as file:
        yaml.safe_dump(yaml_content, file, sort_keys=False)




def main():

    # Parse the information
    functionFile = sys.argv[1]
    openfaasURL = sys.argv[2]

    # Setup OpenFaas URL
    updateURL(functionFile, openfaasURL)

    # Correr modelo
    print("Executing the main() function in create_model")
    create_model.main()
    print("Finished executing the main() function in create_model")


    # Get information from model's output
    # instante_type
    # cpu_limit
    # memory_limit

    updateConfiguration(functionFile, instante_type, cpu_limit, memory_limit)

if __name__ == "__main__":
    main()