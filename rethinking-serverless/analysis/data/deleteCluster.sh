#! /bin/bash

# chmod +x scriptfile.sh

source config.sh

CLUSTER_NAME=$cluster_name


line_number=5
file_path="config.sh"

sed -i "" "${line_number}d" "$file_path"


kubectl delete svc --namespace=openfaas gateway-external && eksctl delete cluster --name $CLUSTER_NAME

 
