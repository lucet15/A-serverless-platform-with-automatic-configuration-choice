#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh

faas_function=$(python3 DATA_DIRECTORY/getFunctionYaml.py "$FUNCTION_NAME")

instante_type= #GET INSATNTE TYPE FROM MODEL'S OUTPUT

echo Function name = $faas_function

echo Check if there is any avaiable node with instance_type = "$instante_type"

# NODES_INSTANCE_TYPES=( $(kubectl get nodes -o json|jq -Cjr '.items[] |" ",.metadata.labels."beta.kubernetes.io/instance-type","\n"'|sort -k3 -r) )

output_file=$(mktemp)

output=$(kubectl get nodes -o json | jq -Cjr '.items[] | "", .metadata.labels."beta.kubernetes.io/instance-type", "\n"' | sort -k3 -r)

echo "$output" > "$output_file"

# echo Available instance types nodes = "$NODES_INSTANCE_TYPES"


if grep -q "${instante_type}" "$output_file"; then

  echo Instance type exists

else

  echo Instance type does not exists
  echo Creating a new nodegroup with instance type "$instante_type"

  eksctl create nodegroup --region=$cluster_region --cluster=$cluster_name --node-type="$instance_type" --nodes=2 --node-volume-size=80

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
