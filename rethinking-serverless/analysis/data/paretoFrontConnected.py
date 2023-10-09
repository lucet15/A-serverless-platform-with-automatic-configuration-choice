import sys
import glob
from matplotlib import pyplot as plt
import pandas as pd

from paretofront import get_pareto_front
from utils import calculate_cost, calculate_cpu_mem_costs

def plot_data(df1, df2):
    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Plot the data from the first dataframe
    ax.scatter(df1['paretoset_configs'], df1['Function Runtime (s)'], color='blue', label='df1')
    ax.scatter(df1['paretoset_configs'], df1['Function Exec. Cost ($)'], color='blue')

    # Plot the data from the second dataframe
    ax.scatter(df2['paretoset_configs'], df2['Function Runtime (s)'], color='red', label='df2')
    ax.scatter(df2['paretoset_configs'], df2['Function Exec. Cost ($)'], color='red')

    # Connect the dots from the two dataframes with the same configuration
    for config in set(df1['paretoset_configs']).intersection(df2['paretoset_configs']):
        ax.plot([config, config], 
                [df1.loc[df1['paretoset_configs'] == config, 'Function Runtime (s)'].values[0], 
                 df2.loc[df2['paretoset_configs'] == config, 'Function Runtime (s)'].values[0]], 
                color='gray')
        ax.plot([config, config], 
                [df1.loc[df1['paretoset_configs'] == config, 'Function Exec. Cost ($)'].values[0], 
                 df2.loc[df2['paretoset_configs'] == config, 'Function Exec. Cost ($)'].values[0]], 
                color='gray')

    # Add a legend and labels
    ax.legend()
    ax.set_xlabel('paretoset_configs')
    ax.set_ylabel('Values')

    # Display the plot
    plt.show()


def multiObjectiveDataframe(predictions):

    # Calculate cost for each instance_type
    calculate_cpu_mem_costs()

    # paretoset_performance will save the performance and cost values
    paretoset_performance =  pd.DataFrame(columns=["Function Runtime (s)", "Function Exec. Cost ($)"])

    configs = []

    #is it necessary to have a min_runtime and min_cost?

    for prediction in predictions:
            
            print("PREDICTIONS")
            print(prediction)

            clean_prediction = [item.replace('(', '').replace(')', '').strip() for item in prediction]
            print("CLEAN PREDICTIONS")
            print(clean_prediction)
            runtime = prediction[0] 
            

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
            cost = calculate_cost(cpu, memory, float(prediction[0]), instance_type)
           

            # print(cost, runtime)

            print("_______________????????????????")
            print(type(runtime),runtime)
            print(type(cost),cost)
            paretoset_performance = paretoset_performance.append({"Function Runtime (s)": float(runtime), "Function Exec. Cost ($)": cost}, ignore_index=True)
            
            configs.append({instance_type, cpu, memory}) 

    print(paretoset_performance)
    print(configs)

    return paretoset_performance, configs

def main():


    # Define the folder path and file pattern
    #folder_path = "../../metrics/" + functionName
    #file_pattern = 'functionName_Input_Memory_Cpu_InstanceType.csv'

    # Iterate over the files in the folder
    #for file_path in glob.glob(f"{folder_path}/{file_pattern}"):
        # Read the file using pandas
    #    df = pd.read_csv(file_path)
        
        # Calculate the average response time
    #    average_response_time = df['response_time'].mean()
        
        # Extract the relevant part of the file name
    #    file_name = file_path.split('/')[-1].split('_')[1:]
    #    new_file_name = '_'.join(file_name)
        
        # Save the average response time to a new file
    #    new_file_path = f"./dataframes/{new_file_name}"
    #    pd.DataFrame({'average_response_time': [average_response_time]}).to_csv(new_file_path, index=False)





    # Dataframe from real values

    functionName = "linpack"

    data_real = []

    # Convert txt real valus to data
    with open("./quality_model/" + functionName + "_real.txt", "r") as file:
        lines = file.read().split("\n")
        for line in lines:
            elements = line.split(",")
            if len(line.strip()) != 0:
                data_real.append(elements) # Function Runtime, metrics

    print("DATA ________________________-")
    print(data_real)

    paretoset_performance_real, configs_real = multiObjectiveDataframe(data_real)

    
    # Dataframe with prediction values

    # Initialize empty list to store rows
    data_predictions = []


    df = pd.read_csv("./quality_model/" + functionName + ".txt", sep='\t')


    df[['Config1', 'Config2', 'Config3']] = df['paretoset_configs'].str.split(',', expand=True)
    df[['Runtime', 'Cost']] = df['paretoset_metrics'].str.split(',', expand=True)

    data_predictions = pd.DataFrame()
    data_predictions['Runtime'] = df['Runtime']
    data_predictions['Configuration'] = df['Config1'] + ', ' + df['Config2'] + ', ' + df['Config3']


    # Convert txt real valus to data
    with open("./quality_model/" + functionName + ".txt", "r") as file:
        lines = file.read().split("\n")
        for line in lines:
            elements = line.split(",")
            if len(line.strip()) != 0:
                data_predictions.append(elements) # Function Runtime, metrics

    print("DATA ________________________-")
    print(data_predictions)

    # Prepare the data
    for configs, (index, metrics) in zip(paretoset_configs, paretoset_metrics.iterrows()):
        config_str = ', '.join(configs) # Convert set to string
        metrics_values = metrics.tolist() # Convert metrics to list
        data.append([metrics_values[0], metrics_values[1], config_str]) # Append the row to data

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Function Runtime (s)', 'Function Exec. Cost ($)', 'paretoset_configs'])



    #paretoset_performance, configs = multiObjectiveDataframe(data)

    #print("DEPOIS DO MULTI")
    #print(paretoset_performance)
    #print(configs)

    # Get dataframe from prediction
    dfPrefictions = []


    plot_data(df, dfPrefictions)




    plt.scatter(paretoset_performance["Function Runtime (s)"], paretoset_performance["Function Exec. Cost ($)"])
    plt.xlabel("Function Runtime (s)")
    plt.ylabel("Function Exec. Cost ($)")



    plt.savefig("./quality_model/plots/" + functionName + ".png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)

    plt.show()

    

if __name__ == "__main__":
    main()