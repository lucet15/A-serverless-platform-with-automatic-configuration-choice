from typing import Any, List, Tuple
from paretoset import paretoset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # Import matplotlib

def get_pareto_front(functionName, metrics: pd.DataFrame, configs: List[Any], sense=["min", "min"]) -> Tuple[Any, Any]:
    """
    Returns the pareto front
    Args:
        metrics: A dataframe container metrics. For example if have a list of runtime and costs for each configuration 
                then your metrics could be: 
                    metrics = pd.DataFrame({"Function Runtime (s)": runtimes, "Function Exec. Cost ($)": costs})
                Both runtimes and costs will need to have same dimensions
        configs: A list of configurations that correspond to each entry in metrics. 
        sense: list
                List with strings for each column (objective). The value `min` (default)
                indicates minimization, `max` indicates maximization and `diff` indicates
                different values. Using `diff` is equivalent to a group-by operation
                over the columns marked with `diff`. If None, minimization is assumed.
    Returns:
        A tuple with two lists. One with configs and the other with metric values
    """

    # Calculate the mask for pareto front
    # Mask has true for elements that are part of paretoset / pareto front
    print("====================================")
    print(metrics)
    print(type(metrics))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    metrics['Function Runtime (s)'] = pd.to_numeric(metrics['Function Runtime (s)'], errors='coerce')
    metrics['Function Exec. Cost ($)'] = pd.to_numeric(metrics['Function Exec. Cost ($)'], errors='coerce')

    mask = paretoset(costs=metrics, sense=sense)
    print("mask")
    print(mask)
    metrics_paretoset = metrics[mask]
    print("metrics_paretoset")
    print(metrics_paretoset)
    
    configs = np.array(configs)
    print("configs")
    print(configs)
    configs_paretoset = configs[mask]
    print("configs_paretoset")
    print(configs_paretoset)


    file_path = "./quality_model/" + functionName + "_prediction.csv"
    file = open(file_path, 'w')

    metrics_paretoset.to_csv(file_path, index=False)


    # Create a scatter plot of the Pareto front
    plt.figure(figsize=(8, 6))
    plt.scatter(metrics_paretoset["Function Runtime (s)"], metrics_paretoset["Function Exec. Cost ($)"])

    plt.xlabel("Function Runtime (s)")
    plt.ylabel("Function Exec. Cost ($)")
    plt.title("Pareto Front")

    #plt.show()

    plt.savefig("./data/paretoPlots/basic/" + functionName + ".png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)

    #plt.savefig("./data/paretoPlots/trials/pareto_" + functionName + "_35_trials.png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)
    #plt.savefig("./data/paretoPlots/initSamples/pareto_" + functionName + "_5_initSamples.png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)
    
    return configs_paretoset, metrics_paretoset



if __name__ == "__main__":
    metrics = pd.DataFrame({"Function Runtime (s)": [10, 20, 15, 50], "Function Exec. Cost ($)": [10, 10, 2, 3]})

    paretoset_configs, paretoset_metrics = get_pareto_front(metrics=metrics, configs=[{"m5.2xlarge", "200m"}, 
                                                                                    {"m5.2xlarge", "500m"}, 
                                                                                    {"c5.2xlarge", "200m"}, 
                                                                                    {"c5.2xlarge", "500m"}])

    print(paretoset_configs)
    print(paretoset_metrics)