#! /bin/bash

# chmod +x scriptfile.sh

source config.sh

# Directory to YAML file
FUNCTION_DIRECTORY=$1 

# Function Input
INPUT=$2
INPUT_NAME=$3

echo $INPUT

instance=$4
cpu=$5
memory=$6

machine="large"

faas_function=$(python3 ./data/getFunctionYaml.py "$FUNCTION_DIRECTORY")


while true
do

    echo $cluster_name

    nodegroup_name="$instance$machine"
    eksctl create nodegroup --cluster="$cluster_name" --name="$nodegroup_name" --node-type="$instance.$machine" --nodes=2 --node-volume-size=80

    if [ $? -eq 0 ]; then
        echo "Cluster Setup Completed with eksctl command."
    else
        echo "Cluster Setup Failed while running eksctl command."
    fi

    faas-cli deploy -f "$FUNCTION_DIRECTORY"

    url="$openfaas_url/function/$faas_function"
    echo OpenFaas Function URL = "$url"
    
    sleep 1
    
    # Run function 
    echo Run the function for the "$i" time with input = "$INPUT"
    echo url = $url
        
    response_headers=$(curl -i "$url" --data "$INPUT")

    echo $response_headers

    # Check the response delay and if response is 200, save the response value

    response_delay=$(echo "$response_headers" | grep -i "X-Duration-Seconds" | awk -F ': ' '{print $2}' | tr -d '\r')
    echo "Response Delay = $response_delay"

    status_code=$(echo "$response_headers" | grep -i "HTTP/1.1" | awk -F ' ' '{    print $2}' | tr -d '\r')
    echo $status_code

    if [[ $status_code != "200" ]]; then
        machine="xlarge" 
        echo XLARGE
    else
        machine="large"
        echo LARGE
        break
    fi
    
done
# eksctl delete nodegroup --cluster $cluster_name --name $nodegroup_name &

echo "$response_delay,(${instance}, ${cpu}, ${memory})" >> "./quality_model/${faas_function}_real.txt"
echo Saved in "./quality_model/${faas_function}_real.txt"