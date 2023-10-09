#! /bin/bash

# chmod +x scriptfile.sh

source config.sh

# Receives through the input the YAML file of the function (in function's directory) and the input's function
# Only to run in a simple cluster with a basic configuration
# t3.large
# Run in data directory

# Directory to YAML file
FUNCTION_DIRECTORY=$1 

# Function Input
INPUT=$2
INPUT_NAME=$3
# cluster_name=$4

echo cluster name = $cluster_name

openfaas_url=$openfaas_url

machine="2xlarge"

# Parameters

cpu='1000m'
memory='512Mi'
instance='m5'

# OpenFaas's function name
faas_function=$(python3 getFunctionYaml.py "$FUNCTION_DIRECTORY")
echo Function\'s name = "$faas_function"

dir="./metrics/${faas_function}_BASIC"
mkdir -p "$dir"


if [ ! -d "./metrics/${faas_function}_BASIC" ]; then
  mkdir "./metrics/${faas_function}_BASIC"
fi


file_name="$instance$machine-$memory-$cpu"

echo "$file_name"

echo Instance Type = "$instance.$machine"
echo CPU = "$cpu"
echo memory = "$memory"

python3 updateConfiguration.py "$FUNCTION_DIRECTORY" "$instance.$machine" "$cpu" "$memory"

echo Deploying the function... "$faas_function"
faas-cli deploy -f "$FUNCTION_DIRECTORY"

url="$openfaas_url/function/$faas_function"
echo OpenFaas Function URL = "$url"

sleep 1

# Run function several times
for i in {1..5};
do

    echo Run the function for the "$i" time with input = "$INPUT"
    echo url = $url
        
    response_headers=$(curl -i "$url" --data "$INPUT")

    # Check the response delay and if response is 200, save the response value

    response_delay=$(echo "$response_headers" | grep -i "X-Duration-Seconds" | awk -F ': ' '{print $2}' | tr -d '\r')
    echo "Response Delay = $response_delay"

        status_code=$(echo "$response_headers" | grep -i "HTTP/1.1" | awk -F ' ' '{    print $2}' | tr -d '\r')
        echo "Status Code = $status_code"

        if [[ $status_code != "200" ]]; then
            machine="xlarge" 
        else
            machine="large"
        fi


    if [ "$i" -eq 1 ]; then
        echo Response-delay,status-code >> "./metrics/${faas_function}_BASIC/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}_BASIC.csv"
        fi	

            echo "$response_delay,$status_code" >> "./metrics/${faas_function}_BASIC/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}_BASIC.csv"
            echo Saved in "./metrics/${faas_function}_BASIC/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}_BASIC.csv"

done


