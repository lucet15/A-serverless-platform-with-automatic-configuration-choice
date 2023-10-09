import csv
import glob
import os
import sys
import pandas as pd
import yaml
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import re

from paretofront import get_pareto_front
from utils import calculate_cost, calculate_cpu_mem_costs




def splitConfiguration(configuration, cpu_limits, memory_limits, instance_types):
    print("INICIO")
    print(configuration)
    memory = ""
    cpu = ""
    instance = ""
    print(type(configuration))
    for variable in configuration:
        print("CONFIGURATIOIN TYPE")
        print(type(variable))
        print(variable)
        print("CONFIGURATIONS")
        if str(variable) + "m" in cpu_limits:
            print("cpu")
            cpu = str(variable) + "m"
        elif str(variable) + "Mi" in memory_limits:
            print("memory")
            memory = str(variable) + "Mi"
        elif str(variable) in instance_types:
            print("instance")
            instance = str(variable)
        else:
            print("Error in split configuration")

    configurations = {"memory": memory, "cpu": cpu, "instance": instance}

    return configurations

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


def qualityModel(functionName):
    # Open the file in read mode ('r')
    with open(functionName, 'r') as f:
        lines = f.readlines()

    # Loop through the lines to find the values
    for i, line in enumerate(lines):
        config, metric = line.strip().split('\t')


def multiObjectiveDataframe(predictions):

    # Calculate cost for each instance_type
    calculate_cpu_mem_costs()

    # paretoset_performance will save the performance and cost values
    paretoset_performance =  pd.DataFrame(columns=["Function Runtime (s)", "Function Exec. Cost ($)"])

    configs = []

    #is it necessary to have a min_runtime and min_cost?

    for prediction in predictions:
            
        for prediction in predictions:
            
            print("PREDICTIONS")
            print(prediction)

            # Convert prediction to string, split into a list and remove non-alphanumeric characters
            prediction = str(prediction).split(',')
            clean_prediction = [''.join(c for c in item if c.isalnum() or c == '.') for item in prediction]

            print("CLEAN PREDICTIONS")
            print(clean_prediction)

            runtime = float(clean_prediction[0])

            # Now you can unpack your cleaned list
            instance_type, cpu, memory = clean_prediction[1:]

            print("cpu")
            print(cpu)
            print("memory")
            print(memory)
            print("instance")
            print(instance_type)
            #instance_type, cpu, memory = prediction[1]

            #cpu_number = int(re.findall(r'\d+', cpu)[0])
            #memory_number = int(re.findall(r'\d+', memory)[0])
            cost = calculate_cost(cpu, memory, float(runtime), instance_type)
            

            # print(cost, runtime)

            print("_______________????????????????")
            print(type(runtime),runtime)
            print(type(cost),cost)
            paretoset_performance = paretoset_performance.append({"Function Runtime (s)": float(runtime), "Function Exec. Cost ($)": float(cost)}, ignore_index=True)
            
            configs.append({instance_type, cpu, memory}) 

    print("PARETO PARETP", paretoset_performance)
    print("CONFIG CONFIG", configs)

    return paretoset_performance, configs


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
        content["constraints"][0] = "beta.kubernetes.io/instance-type=" + instance_type + ".large"

    else: 
        content["constraints"] = ["beta.kubernetes.io/instance-type=" + instance_type + ".large"]

    # Save the modified content back to the file
    with open(functionFile, "w") as file:
        yaml.safe_dump(yaml_content, file, sort_keys=False)

def main():

    # Parse the information
    functionFile = sys.argv[1]
    openfaasURL = sys.argv[2]
    functionInput = str(sys.argv[3])
    functionInputName = str(sys.argv[4])


    # Get OpenFaas's function
    functionName = getFunctionYaml(functionFile)

    # Instance configurations
    CPU_LIMITS= [ '250m', '500m', '750m', '1000m', '1250m', '1500m', '1750m', '2000m' ]
    MEMORY_LIMITS=[ '128Mi', '256Mi', '512Mi', '768Mi', '1024Mi', '2048Mi' ]
    instance_types = ['m5', 'm5a', 'c5', 'c5a', 'c6g', 'm6g']

    # Get folder "./quality_model/"  and get file "functionName.txt", this file was the values from the predictions
    # Open the file in read mode ('r')
    # with open("./quality_model/" + functionName + ".txt", 'r') as f:
    #    next(f)  # Skip the header line
    #    # Iterate over each line
    #    for i, line in enumerate(f, start=1):
    #        configs, metrics = line.strip().split('\t')
    #        runtime, cost = metrics.split(', ')
    #        print(f'Line {i}: configs={configs}, runtime={runtime}, cost={cost}')


            # Split the string into a list
    #        list_configuration = configs.split(',')

            # Remove leading/trailing white spaces from each item
    #        list_configuration = [item.strip() for item in list_configuration]
            
    #        configurations = splitConfiguration(list_configuration, CPU_LIMITS, MEMORY_LIMITS, instance_types)

    #        updateConfiguration(functionFile, configurations["instance"], configurations["cpu"], configurations["memory"])


            # In this file, is saved the new values to run
            #cpu_number = int(re.findall(r'\d+', cpu)[0])
            #memory_number = int(re.findall(r'\d+', memory)[0])
            #command = "./runFunction.sh " + functionFile + " " + functionInput + " " + functionInputName + " " + configurations["instance"] + " " + cpu_number + " " + memory_number
            #command = "./runFunction.sh " + functionFile + " " + functionInput + " " + functionInputName + " " + configurations["instance"] + " " +  configurations["cpu"] + " " +  configurations["memory"]
            #os.system(command)

    # Get the real metrics from the samples
    #directory = "./data/metrics/" + functionName
    #directory_output = "./data/metricsConfigurations/"

    #for filename in os.listdir(directory):
    #    if filename.endswith('.csv'):
    #        file_path = os.path.join(directory, filename)
    #        df = pd.read_csv(file_path)
    #        print(filename)
    #        function, input, memory, cpu, instance = filename[:-4].split('_')

    #       output_filename = f"{directory_output}/{function}_real.txt"

    #        with open(output_filename, 'w') as f:
    #            for index, row in df.iterrows():
    #                line = f"{row['Response-delay']},({instance},{cpu},{memory})\n"
    #                f.write(line)



    # Read data from txt file into a pandas dataframe
    dfPredictions_initial = pd.read_csv("./quality_model/" + functionName + ".txt", sep='\t', header=0, names=['paretoset_configs', 'paretoset_metrics'])

    print(dfPredictions_initial.columns)

    # Split the 'paretoset_metrics' column
    dfPredictions_initial[['Function Runtime (s)', 'Function Exec. Cost ($)']] = dfPredictions_initial['paretoset_metrics'].str.split(',', expand=True)

    # Convert the columns to float
    dfPredictions_initial[['Function Runtime (s)', 'Function Exec. Cost ($)']] = dfPredictions_initial[['Function Runtime (s)', 'Function Exec. Cost ($)']].astype(float)


    # Only keep the desired columns
    dfPredictions = dfPredictions_initial[['Function Runtime (s)', 'Function Exec. Cost ($)']]

    print(dfPredictions)

    dfPredictions_initial['paretoset_configs'] = dfPredictions_initial['paretoset_configs'].str.split(',').apply(lambda x: [i.strip() for i in x])
    #dfPredictions_initial['paretoset_configs'] = dfPredictions_initial['paretoset_configs'].str.split(',', expand=True)
    #dfPredictions_initial[['Function Runtime (s)', 'Function Exec. Cost ($)']] = dfPredictions_initial['paretoset_metrics'].str.split(',', expand=True)
    paretoset_configs = dfPredictions_initial['paretoset_configs'].tolist()

    print("DFPRETICTIONS")
    print(dfPredictions)

    print("PARETO CONFIGS")
    print(paretoset_configs)
    
    data = []

    folder = "./data/metrics/" + functionName


    for configuration in paretoset_configs:
        print("NO FOR")
        print(configuration)
        config = splitConfiguration(configuration, CPU_LIMITS, MEMORY_LIMITS, instance_types)

        # Create the search pattern
        search_pattern = folder + "/{}_{}_{}_{}_{}.large.csv".format(functionName, functionInputName, config["memory"], config["cpu"], config["instance"])
        search_pattern_xlarge = folder + "/{}_{}_{}_{}_{}.xlarge.csv".format(functionName, functionInputName, config["memory"], config["cpu"], config["instance"])

        print("SEARCH FILE")
        print(search_pattern)

        # Find files that match the search pattern
        files = glob.glob(search_pattern)
        files_xlarge = glob.glob(search_pattern_xlarge)

        # Check if a file was found
        if len(files) > 0:
            # Read the first file into a DataFrame
            print("FILES")
            print(files[0])
            df = pd.read_csv(files[0])

            avg_response_delay = df['Response-delay'].mean()

            # Save the result in a list in the desired format
            data.append(f"{float(avg_response_delay)},({config['instance']},{config['cpu']},{config['memory']})")
        elif len(files_xlarge) > 0:
            # Read the first file into a DataFrame
            print("FILES")
            print(files_xlarge[0])
            df = pd.read_csv(files_xlarge[0])

            avg_response_delay = df['Response-delay'].mean()

            # Save the result in a list in the desired format
            data.append(f"{float(avg_response_delay)},({config['instance']},{config['cpu']},{config['memory']})")
        
        else:
            print("No file found that matches the search pattern.")






    # Convert txt real valus to data
    #with open("./data/metricsConfigurations/" + functionName + "_real.txt", "r") as file:
    #    lines = file.read().split("\n")
    #    for line in lines:
    #        elements = line.split(",")
    #        if len(line.strip()) != 0:
    #            data.append(elements)

    #print("DATA ________________________-")
    #print(data)

    # To real values
    paretoset_performance, configs = multiObjectiveDataframe(data)

    print("DEPOIS DO MULTI")
    print(paretoset_performance)
    print(type(paretoset_performance["Function Runtime (s)"][0]))
    print(configs)

    plt.figure(figsize=(8, 6))

    # Because of data contains the real values, it isn't supposed to run Pareto front
    plt.scatter(paretoset_performance["Function Runtime (s)"], paretoset_performance["Function Exec. Cost ($)"], label='Real Pareto Front values')
    plt.xlabel("Function Runtime (s)")
    plt.ylabel("Function Exec. Cost ($)")

    
    
    # Values from prediction
    #file_path = "./quality_model/" + functionName + ".txt"
    #df = pd.read_csv(file_path)
    
    plt.scatter(dfPredictions["Function Runtime (s)"], dfPredictions["Function Exec. Cost ($)"], marker='o', color='red', label='Predicted Pareto Front values')

    plt.legend()


    plt.savefig("./quality_model/plots/" + functionName + ".png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)

    #plt.show()


if __name__ == "__main__":
    main()
    