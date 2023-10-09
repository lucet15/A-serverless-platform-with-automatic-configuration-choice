import os
import matplotlib.pyplot as plt

# Initialize lists to store function names and execution times
function_names = []
execution_times = []

# Specify the folder path where the files are located
folder_path = "./"

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file name matches the expected format
    if filename.startswith("execution_time_") and filename.endswith(".txt"):
        # Extract the function name from the file name
        function_name = filename[15:-4]  # Remove "execution_time_" and ".txt"
        function_names.append(function_name)
        
        # Read the execution time data from the file
        with open(os.path.join(folder_path, filename), "r") as file:
            execution_time = float(file.read())
            execution_times.append(execution_time)

# Create the plot
plt.figure(figsize=(8, 10))

plt.bar(function_names, execution_times)
plt.xlabel("Function Name")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Times of Functions")
plt.xticks(rotation=45)

plt.savefig("./obtainigMetrics.png")  # You can specify the desired file format (e.g., .png, .jpg, .pdf)
