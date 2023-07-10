#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh

# Before doing anything, it is necessary to run
# docker pull <function image>; docker tag <new_tag>; docker push <new_image>

# Receives through the input the directory of the function's folder, the directory of the data's directory

FUNCTION_DIRECTORY=\$1
DATA_DIRECTOTY=\$2
INPUT=\$3

# Parameters

CPU_LIMITS= ('250m', '500m', '750m', '1000m', '1250m', '1500m', '1750m', '2000m')
MEMORY_LIMITS= ('128Mi', '256Mi', '512Mi', '768Mi', '1024Mi', '2048Mi')
instance_types = ('m5', 'm5a', 'c5', 'c5a', 'c6g', 'm6g')

faas_function=$(python3 DATA_DIRECTORY/getFunctionYaml.py "$FUNCTION_NAME")

# Run all possible configurations

for instace in $instance_types;
do
  for memory in $MEMORY_LIMITS;
  do
    for cpu in $CPU_LIMITS;
    do

      # Create a node cluster with this caracteristcs
      eksctl create nodegroup --region=$cluster_region --cluster=$cluster_name --node-type=instance --nodes=2 --node-volume-size=80

      python3 DATA_DIRECTOTY/updateConfiguration.py "$FUNCTION_NAME" "$instante" "$cpu" "$memory"

      # Deploy function
      echo "Building the function..."
      faas-cli build -f "$FUNCTION_NAME"

      echo "Pushing the function..."
      faas-cli push -f "$FUNCTION_NAME"

      echo "Publishing the function..."
      faas-cli publish -f "$FUNCTION_NAME" --platforms linux/arm/v7,linux/amd64

      echo "Deploying the function..."
      faas-cli deploy -f "$FUNCTION_NAME"

      # Run function several times
      for i in {1..5};
      do
        # CHAMAR A FUNCÂO
        curl -i "$openfaas_url"/function/"$faas_function" --data "$INPUT"
      done

      # Export the data in csv
      

    done
  done
  # Delete the node cluster
done
