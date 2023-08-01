#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh

# Before doing anything, it is necessary to run
# docker pull <function image>; docker tag <new_tag>; docker push <new_image>

# Receives through the input the directory of the function's folder, the directory of the data's directory

# Directory to YAML file
FUNCTION_DIRECTORY=$1 
echo Function Directory "$FUNCTION_DIRECTORY"

# DATA_DIRECTOTY=\$2

# Function Input
INPUT=$2
echo Input "$INPUT"


openfaas_url=$openfaas_url

# Parameters

CPU_LIMITS=('250m' '500m' '750m' '1000m' '1250m' '1500m' '1750m' '2000m')
MEMORY_LIMITS=('128Mi' '256Mi' '512Mi' '768Mi' '1024Mi' '2048Mi')
instance_types=('m5' 'm5a' 'c5' 'c5a' 'c6g' 'm6g')

# OpenFaas's function name
faas_function=$(python3 getFunctionYaml.py "$FUNCTION_DIRECTORY")
echo Function\'s name = "$faas_function"


# Run all possible configurations

for instance in "${instance_types[@]}";
do
  for memory in "${MEMORY_LIMITS[@]}";
  do
    for cpu in "${CPU_LIMITS[@]}";
    do

      # Create a node cluster with this caracteristcs
      echo Creating a node group with instante type = "$instance".large, memory limit = "$MEMORY_LIMITS" and cpu limits = "$CPU_LIMITS"

      echo Cluster name = "$cluster_name", Region = "$cluster_region"

      nodegroup_name="$instance$memory$cpu"

      echo "$nodegroup_name"



      # eksctl create nodegroup --cluster="$cluster_name" --name="$instance-$memory-$cpu" --node-type="$instance.large" --nodes=2 --node-volume-size=80

      if [ $? -eq 0 ]; then
	 echo "Cluster Setup Completed with eksctl command."
      else
         echo "Cluster Setup Failed while running eksctl command."
      fi

      sleep 1



      echo Function Directory = "$FUNCTION_DIRECTORY"
      echo Instance Type = "$instance.large"
      echo CPU = "$cpu"
      echo memory = "$memory"

      python3 updateConfiguration.py "$FUNCTION_DIRECTORY" "$instance.large" "$cpu" "$memory"

      # Deploy function
      # echo "Building the function..."
      # faas-cli build -f "$FUNCTION_NAME"

      # echo "Pushing the function..."
      # faas-cli push -f "$FUNCTION_NAME"

      # echo "Publishing the function..."
      # faas-cli publish -f "$FUNCTION_NAME" --platforms linux/arm/v7,linux/amd64

      echo Deploying the function... "$faas_function"
      faas-cli deploy -f "$FUNCTION_DIRECTORY"

      url="$openfaas_url/function/$faas_function"
      echo URL = "$url"

      sleep 1

      # Run function several times
      for i in {1..5};
      do
        # CHAMAR A FUNCÂO
        
        url="$openfaas_url/function/$faas_function"

        echo Run the function for the "$i" time with input = "$INPUT"
        
        response_headers=$(curl -i "$url" --data "$INPUT")

	# Check if response is 200, save the response value

	response_delay=$(echo "$response_headers" | grep -i "X-Duration-Seconds" | awk -F ': ' '{print $2}' | tr -d '\r')
	echo "$faas_function,$response_delay"

        status_code=$(echo "$response_headers" | grep -i "HTTP/1.1" | awk -F ' ' '{    print $2}' | tr -d '\r')
        echo "$faas_function,$status_code"

        echo "$response_delay,$status_code" >> "metrics/${faas_function}_${INPUT}_${memory}_${cpu}.csv"

      done

      # Export the data in csv

      #echo Exporting data from grafana


      # response-time,DNS+dialup,DNS,Request-write,Response-delay,Response-read,status-code,offset
      
      # Delete the node cluster
 
      echo Deleting node group with instance
      eksctl delete nodegroup \
     --cluster $cluster_name \
     --region $cluster_region \
     --name $nodegroup_name

    done
  done
done
