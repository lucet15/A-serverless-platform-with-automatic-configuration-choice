import os
import re
import matplotlib.pyplot as plt
from pathlib import Path



def extract_trials(filename):
    match = re.search(r'(\d+)_initSamples', filename)
    if match:
        return int(match.group(1))
    return None


def main():
    trial_numbers = []
    execution_times = []
    
    functionName = "s3"

    folder_path = "./time/initSample_cost_time/"

    if Path("./time/").is_dir():
        print("Directory time exists.")
    else:
        print("Directory not found time")
        return

    if Path(folder_path).is_dir():
        print("Directory" + folder_path + " exists.")
    else:
        print("Directory not found")
        return

    for filename in os.listdir(folder_path):
        if filename.startswith('execution_time') and filename.endswith("_initSamples_" + functionName + ".txt"):
            print(filename)
            trial_number = extract_trials(filename)
            if trial_number is not None:
                with open(os.path.join(folder_path, filename), 'r') as file:
                    execution_time = float(file.read())
                    trial_numbers.append(trial_number)
                    execution_times.append(execution_time)
    
    print(trial_numbers)
    print(execution_times)

    plt.figure(figsize=(5, 6))
    bars = plt.bar(trial_numbers, execution_times, width=2, align='center', alpha=0.7)
    plt.xlabel('Number of Init Samples')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs. Trials')
    plt.xticks(trial_numbers)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, time in zip(bars, execution_times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f'{time:.2f}', ha='center', va='bottom')

    plt.savefig("./time/initSample_cost_time/" + functionName + ".png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)




if __name__ == "__main__":
    main()

