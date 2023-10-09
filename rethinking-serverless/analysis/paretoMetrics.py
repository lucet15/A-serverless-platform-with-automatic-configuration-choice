import os
from matplotlib import pyplot as plt
import pandas as pd
import glob

from paretofront import get_pareto_front
from utils import calculate_cost, calculate_cpu_mem_costs

def splitConfiguration(configuration, cpu_limits, memory_limits, instance_types):
    print("INICIO")
    print(configuration)
    print(instance_types)
    memory = ""
    cpu = ""
    instance = ""
    for variable in configuration:
        print("CONFIGURATIONS")
        print(variable)
        if variable in cpu_limits:
            cpu = variable
        elif variable in memory_limits:
            memory = variable
        else:
            instance_variable = variable.split('.')[0]
            print("????????????")
            print(instance_variable)
            if instance_variable in instance_types:
                instance = instance_variable
            else:
                print("Error in split configuration")

    return {"memory": memory, "cpu": cpu, "instance": instance}

def multiObjectiveDataframe(predictions):

    # Instance configurations
    CPU_LIMITS= [ '250m', '500m', '750m', '1000m', '1250m', '1500m', '1750m', '2000m' ]
    MEMORY_LIMITS=[ '128Mi', '256Mi', '512Mi', '768Mi', '1024Mi', '2048Mi' ]
    instance_types = ['m5', 'm5a', 'c5', 'c5a', 'c6g', 'm6g']

    # Calculate cost for each instance_type
    calculate_cpu_mem_costs()

    # paretoset_performance will save the performance and cost values
    paretoset_performance =  pd.DataFrame(columns=["Function Runtime (s)", "Function Exec. Cost ($)"])

    configs = []

    #is it necessary to have a min_runtime and min_cost?

    for index, row in predictions.iterrows():
        # Extract the response time and configuration details
        runtime = row['Function Runtime']
        configurations = splitConfiguration(row['Configurations'], CPU_LIMITS, MEMORY_LIMITS, instance_types)

        instance_type = configurations["instance"]
        cpu = configurations["cpu"]
        memory = configurations["memory"]

        print("cpu")
        print(cpu)
        print("memory")
        print(memory)
        print("instance")
        print(instance_type)


        cost = calculate_cost(str(cpu), str(memory), float(runtime), str(instance_type))
        
        paretoset_performance = paretoset_performance.append({"Function Runtime (s)": float(runtime), "Function Exec. Cost ($)": cost}, ignore_index=True)
        
        configs.append({instance_type, cpu, memory}) 

    print(paretoset_performance)
    print(configs)

    return paretoset_performance, configs


def main():
    # Change the function's name
    functionName = "linpack"
    path = "./data/metrics/" + functionName

    df = pd.DataFrame(columns=['Function Runtime', 'Configurations'])

    for file_path in glob.glob(path + "/*.csv"):
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        print("FILENAME")
        print(file_name)
        
        # Remove the '.csv' extension and split the file name on '_'
        parts = file_name[:-4].split('_')
        print("PARTS")
        print(parts)
        # Extract the memory, CPU, and instance type from the parts
        memory = parts[2]
        print("memory")
        print(memory)
        cpu = parts[3]
        print("CPU")
        print(cpu)
        instance_type = parts[4]
        print("INSTANCE")
        print(instance_type)

        # Read the CSV file
        data = pd.read_csv(file_path)

        # Extract the response time
        if ('Response-delay' in data.columns):
            response_time = data['Response-delay'].mean()
            print("RESPONSE TIME")
            print(response_time)

            # Append the function name and response time to the DataFrame
            df = df.append({'Function Runtime': response_time, 'Configurations': {instance_type, cpu, memory}}, ignore_index=True)
            print(df)


    print("SAIU DO LOOP")
    paretoset_performance, configs = multiObjectiveDataframe(df)

    paretoset_configs, metrics_paretoset = get_pareto_front(functionName,paretoset_performance, configs, sense=["min", "min"]) # Max performance and mim cost



    plt.scatter(metrics_paretoset["Function Runtime (s)"], metrics_paretoset["Function Exec. Cost ($)"])
    plt.xlabel("Function Runtime (s)")
    plt.ylabel("Function Exec. Cost ($)")

    #plt.show()

    plt.savefig("./data/paretoPlots/paretoMetricsPlot/" + functionName + ".png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)



if __name__ == "__main__":
    main()
    