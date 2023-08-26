#from helpers import create_model
from create_model import main, create_model
from optimizer.boskopt import Models
from utils import calculate_cost, calculate_cpu_mem_costs
from paretofront import get_pareto_front
from pathlib import Path

import pandas as pd 
import sys
import yaml
import os


def getInstanceSize(directory, benchmark, data_name, mem, cpu, instance_type):
    # Get from data what type of machine is needed


    filename_large = directory + "/" + benchmark + "/" + benchmark + "_" + data_name + "_" + mem + "_" + cpu + "_" + instance_type + ".large.csv"
    filename_xlarge = directory + "/" + benchmark + "/" + benchmark + "_" + data_name + "_" + mem + "_" + cpu + "_" + instance_type + ".xlarge.csv" 

    print("filename large")
    print(filename_large)
    print("filename xlarge")
    print(filename_xlarge)

    filename = ''
    if os.path.exists(filename_large): 
        filename = filename_large

    elif os.path.exists(filename_xlarge):
        filename = filename_xlarge

    else:
        print("Error")

    parts = filename.split(".")
    instance_size = parts[-2]

    return instance_size


def updateConfiguration(functionFile, instance_type, cpu_limit, memory_limit):
    # Update the configurations in the YAML file with model's output

    with open(functionFile, "r") as file:
        #yaml_content = yaml.safe_load(file)
        yaml_content = yaml.safe_load(file)

    # Modify the value in the YAML content
    functionName = list(yaml_content["functions"].keys())[0]
    content = yaml_content["functions"][functionName]


    content["limits"] = {
        "memory": memory_limit,
        "cpu": cpu_limit   
    }

    if "constraints" in content:
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


def getFunctionYaml(functionFile):
    with open(functionFile, "r") as file:
        #yaml_content = yaml.safe_load(file)
        yaml_content = yaml.safe_load(file)

    # Modify the value in the YAML content
    function = [yaml_content["functions"].keys()][0]

    functionName = next(iter(function))

    # Save the modified content back to the file
    with open(functionFile, "w") as file:
        yaml.safe_dump(yaml_content, file, sort_keys=False)

    return functionName



def multiObjectiveDataframe(predictions):

    # Calculate cost for each instance_type
    calculate_cpu_mem_costs()

    # paretoset_performance will save the performance and cost values
    paretoset_performance =  pd.DataFrame(columns=["Function Runtime (s)", "Function Exec. Cost ($)"])

    configs = []

    #is it necessary to have a min_runtime and min_cost?

    for prediction in predictions:
            runtime = prediction[0] 
            instance_type, cpu, memory = prediction[1]
            cost = calculate_cost(cpu, memory, prediction[0], instance_type)
           

            # print(cost, runtime)
            paretoset_performance = paretoset_performance.append({"Function Runtime (s)": runtime, "Function Exec. Cost ($)": cost}, ignore_index=True)
            
            configs.append({instance_type, cpu, memory}) 

    print(paretoset_performance)
    print(configs)

    return paretoset_performance, configs


def splitConfiguration(configuration, cpu_limits, memory_limits, instance_types):
    memory = ""
    cpu = ""
    instance = ""
    for variable in configuration:
        if str(variable) + "m" in cpu_limits:
            cpu = str(variable) + "m"
        elif str(variable) + "Mi" in memory_limits:
            memory = str(variable) + "Mi"
        elif variable in instance_types:
            instance = str(variable)
        else:
            print("Error in split configuration")

    configurations = {"memory": memory, "cpu": cpu, "instance": instance}

    return configurations


def main():

    # Parse the information
    functionFile = sys.argv[1]
    openfaasURL = sys.argv[2]
    functionInput = str(sys.argv[3])
    functionInputName = str(sys.argv[4])
    # clusterName = str(sys.argv[5])

    # Instance configurations
    CPU_LIMITS= [ '250m', '500m', '750m', '1000m', '1250m', '1500m', '1750m', '2000m' ]
    MEMORY_LIMITS=[ '128Mi', '256Mi', '512Mi', '768Mi', '1024Mi', '2048Mi' ]
    instance_types = ['m5', 'm5a', 'c5', 'c5a', 'c6g', 'm6g']


    # Setup OpenFaas URL
    updateURL(functionFile, openfaasURL)

    # Get OpenFaas's function
    functionName = getFunctionYaml(functionFile)

    # Path to data folder
    data_path = "./data/"

    print(data_path)
    
    # Check if metrics exist
    if Path("./data/metrics/" + functionName).is_dir():
        print("Directory ./data/metrics/" + functionName + "and metrics for the model exists.")
    else:
        print("Directory does not exist. Starting to get metrics to train the model...")
        os.system("./data/getData.sh " + functionFile + " " + functionInput + " " + functionInputName)
        print("data ready")


    # Run model
    print("Executing the main() function in create_model")
    # model: Models = create_model(instance_types=instance_types, cpu_limits=CPU_LIMITS, memory_limits=MEMORY_LIMITS, function_name="transcode", data_name="cats-1", n_trials=10, base_estimator="GP", seed=1, n_init_samples=3)
    model: Models = create_model("./data/metrics", instance_types=instance_types, cpu_limits=CPU_LIMITS, memory_limits=MEMORY_LIMITS, function_name=functionName, data_name=functionInputName, n_trials=10, base_estimator="GP", seed=1, n_init_samples=3)
    print("Finished executing the main() function in create_model")
    predictions = model.get_all_config_predictions(function=functionName)

    print(predictions)

    paretoset_performance, configs = multiObjectiveDataframe(predictions)

    paretoset_configs, paretoset_metrics = get_pareto_front(paretoset_performance, configs)


    # Show results from predictions

    print("paretoset_confis")
    print(paretoset_configs)
    print("paretoset_metrics")
    print(paretoset_metrics)

    # Prompt the user for input
    while True:
        try:
            preference = eval(input("On a scale from 0 to 5, where 0 represents the maximum performance and 5 represents the minimum cost, please indicate your preference for the deployment of this function: "))
            if isinstance(preference, (int, float)):
                # Check if the value is between 0 and 5 (inclusive)
                if 0 <= preference <= 5:
                    index = paretoset_metrics.index[preference] # Get the index of the metrics, correspondent to the metrics array
                    specific_config = paretoset_configs[preference]

                    break  # exit the loop
                else:
                    print("The variable is a number, but it's not between 0 and 5.")
            else:
                print("The variable is not a number.")
        except NameError:
            print("The input was not a number. Please try again.")

    configurations = splitConfiguration(specific_config, CPU_LIMITS, MEMORY_LIMITS, instance_types)

    final_memory = configurations["memory"]
    print("MEMORY")
    print(final_memory)
    final_cpu = configurations["cpu"]
    print("CPU")
    print(final_cpu)
    final_instance = configurations["instance"]
    print("INSTANCE")
    print(final_instance)

    print("For your preference, it will be used: memory = " + final_memory + ", cpu = " + final_cpu + " and instance type = " + final_instance )

    instance_size = getInstanceSize("./data/metrics", functionName, functionInputName, final_memory, final_cpu, final_instance)

    final_instance = final_instance + "." + instance_size

    updateConfiguration(functionFile, final_instance, final_cpu, final_memory)


    """
    paretoset_configs, paretoset_metrics = get_pareto_front(metrics=metrics, configs=[{"m5.2xlarge", "200m"}, 
                                                                                    {"m5.2xlarge", "500m"}, 
                                                                                    {"c5.2xlarge", "200m"}, 
                                                                                    {"c5.2xlarge", "500m"}])

    print(paretoset_configs)
    print(paretoset_metrics)
    """

    # Get information from model's output
    # instante_type
    # cpu_limit
    # memory_limit

    #updateConfiguration(functionFile, instance_type, cpu_limit, memory_limit)

if __name__ == "__main__":
    main()
    
    print("Function is ready to be deployed")




