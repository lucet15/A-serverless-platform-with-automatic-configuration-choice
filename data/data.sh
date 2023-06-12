#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh

echo "==================== Face Detection ===================="
cd ../rethinking-serverless/benchmarks/face-detection

# Variables
FUNCTION_NAME=$(basename *.yml)
INSTANCE_TYPE=t3.small

echo Run function in a node with instace_type = $INSTANCE_TYPE
python3 ../../../data/updateConfiguration.py $FUNCTION_NAME $INSTANCE_TYPE

python3 updateURL.py $FUNCTION_NAME $url

echo Check if there is any avaiable node with instance_type = $INSTANCE_TYPE
NODES_INSTANCE_TYPES={ $(kubectl get nodes -o json|jq -Cjr '.items[] |" ",.metadata.labels."beta.kubernetes.io/instance-type","\n"'|sort -k3 -r) }

if [[ " ${NODES_INSTANCE_TYPE[*]} " =~ " ${INSTANCE_TYPE} " ]]; then

  echo Instance type exists

else

  echo Instance type does not exist
  echo Creating a new nodegroup with instance type $INSTANCE_TYPE
  
  eksctl create nodegroup --region=$cluster_region --cluster=$cluster_name --node-type=$INSTANCE_TYPE --node-count=2 --volume-size=80

fi

echo "Building the function...
faas-cli build -f $FUNCTION_NAME

echo "Pushing the function...
faas-cli push -f $FUNCTION_NAME 

echo "Publishing the function...
faas-cli publish -f $FUNCTION_NAME --platforms linux/arm/v7,linux/amd64

echo "Deploying the function...
faas-cli deploy -f $FUNCTION_NAME -



