#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh


# Receives through the input the directory of the function's folder and the directory of the data's directory


DIRECTORY=\$1
DATA_DIRECTOTY=\$2

echo "================== ===================="
cd $DIRECTORY || ( ( echo "Error. Function does not exist" ) && exit )

# Variables
FUNCTION_NAME=$(basename -- *.yml)

echo filename = $FUNCTION_NAME

instance_list=("m5.large" "m5a.large" "c5.large" "c5a.large" "c6g.medium" "m6g.medium")

 # Vale a pena arescentar mais tipos de instancias?
INSTANCE_TYPE=t3.nano

echo Run function in a node with instace_type = "$INSTANCE_TYPE"
python3 DATA_DIRECTOTY/updateConfiguration.py "$FUNCTION_NAME" "$INSTANCE_TYPE"

python3 DATA_DIRECTORY/updateURL.py "$FUNCTION_NAME" "$openfaas_url"

#python3 DATA_DIRECTORY/getFunctionYaml.py "$FUNCTION_NAME" > >(read -r faas_function)

faas_function=$(python3 DATA_DIRECTORY/getFunctionYaml.py "$FUNCTION_NAME")

echo Function name = $faas_function

echo Check if there is any avaiable node with instance_type = "$INSTANCE_TYPE"

# NODES_INSTANCE_TYPES=( $(kubectl get nodes -o json|jq -Cjr '.items[] |" ",.metadata.labels."beta.kubernetes.io/instance-type","\n"'|sort -k3 -r) )

output_file=$(mktemp)

output=$(kubectl get nodes -o json | jq -Cjr '.items[] | "", .metadata.labels."beta.kubernetes.io/instance-type", "\n"' | sort -k3 -r)

echo "$output" > "$output_file"

# echo Available instance types nodes = "$NODES_INSTANCE_TYPES" 


if grep -q "${INSTANCE_TYPE}" "$output_file"; then

  echo Instance type exists
  
else

  echo Instance type does not exists
  echo Creating a new nodegroup with instance type "$INSTANCE_TYPE"
  
  eksctl create nodegroup --region=$cluster_region --cluster=$cluster_name --node-type="$INSTANCE_TYPE" --nodes=2 --node-volume-size=80

fi
  
rm "$output_file"

echo "Building the function..."
faas-cli build -f "$FUNCTION_NAME"

echo "Pushing the function..."
#faas-cli push -f "$FUNCTION_NAME" 

echo "Publishing the function..."
#faas-cli publish -f "$FUNCTION_NAME" --platforms linux/arm/v7,linux/amd64

echo "Deploying the function..."
faas-cli deploy -f "$FUNCTION_NAME" 

for i in {1..5}; 
do
    # CHAMAR A FUNCÂO
     curl -i "$openfaas_url"/function/face-detection --data https://github.com/MBtech/rethinking-serverless/blob/main/input/images/faces2.jpg
done
