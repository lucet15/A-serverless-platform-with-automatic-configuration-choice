#! /bin/bash

# chmod +x scriptfile.sh

source config.sh

# Receives through the input the YAML file of the function (in function's directory) and the input's function
# Run in data directory

# Directory to YAML file
FUNCTION_DIRECTORY=$1 

# Function Input
INPUT=$2
INPUT_NAME=$3
# cluster_name=$4

echo cluster name = $cluster_name

openfaas_url=$openfaas_url

machine="large"

# Parameters

CPU_LIMITS=('250m' '500m' '750m' '1000m' '1250m' '1500m' '1750m' '2000m')
MEMORY_LIMITS=('128Mi' '256Mi' '512Mi' '768Mi' '1024Mi' '2048Mi')
instance_types=('m5' 'm5a' 'c5' 'c5a' 'c6g' 'm6g')

# OpenFaas's function name
faas_function=$(python3 getFunctionYaml.py "$FUNCTION_DIRECTORY")
echo Function\'s name = "$faas_function"

dir="metrics/${faas_function}"
mkdir -p "$dir"


if [ ! -d "metrics/${faas_function}" ]; then
  mkdir "metrics/${faas_function}"
fi

# Run all possible configurations
for instance in "${instance_types[@]}";
do

  nodegroup_name="$instance$machine"

  echo "$nodegroup_name"

  eksctl create nodegroup --cluster="$cluster_name" --name="$nodegroup_name" --node-type="$instance.$machine" --nodes=2 --node-volume-size=80

  if [ $? -eq 0 ]; then
     echo "Cluster Setup Completed with eksctl command."
  else
     echo "Cluster Setup Failed while running eksctl command."
  fi


  # To create the next nodegroup
  # if (( i + 1 < ${#instance_types[@]} )); then
    # echo Creating a new nodegroup
    # newInstance="${instance_types[$(( $i + 1))]}"
    # echo $newInstance
    # echo $newInstance.$machine
    # eksctl create nodegroup --cluster="$cluster_name" --name="$newInstance$machine" --node-type="$newInstance.$machine" --nodes=2 --node-volume-size=80 & 
  # echo New nodegroup created
  # fi

  for memory in "${MEMORY_LIMITS[@]}";
  do
    for cpu in "${CPU_LIMITS[@]}";
    do
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

	echo $(pwd)

if [ "$i" -eq 1 ]; then
	  echo Response-delay,status-code >> "metrics/${faas_function}/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}.csv"
	fi	

        echo "$response_delay,$status_code" >> "metrics/${faas_function}/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}.csv"
        echo Saved in "metrics/${faas_function}/${faas_function}_${INPUT_NAME}_${memory}_${cpu}_${instance}.${machine}.csv"
      done

    done
  done

  # Delete the node cluster
  echo Deleting node group with instance = $instance.$machine
  eksctl delete nodegroup --cluster $cluster_name --name $nodegroup_name &
done
