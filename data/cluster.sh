#! /bin/bash

# chmod +x scriptfile.sh

source ../config.sh

CLUSTER_NAME=$cluster_name
CLUSTER_REGION=$cluster_region

# Set AWS credentials before script execution

aws sts get-caller-identity >> /dev/null
if [ $? -eq 0 ]
then
  echo "Credentials tested, proceeding with the cluster creation."

# Creation of EKS cluster
eksctl create cluster \
  --name $CLUSTER_NAME \
  --region $CLUSTER_REGION \
  --nodes 2 \
  --node-type t3.large \
  --auto-kubeconfig

if [ $? -eq 0 ]
  then
    echo "Cluster Setup Completed with eksctl command."
  else
    echo "Cluster Setup Failed while running eksctl command."
    exit 1
  fi
else
  echo "Please run aws configure & set right credentials."
  echo "Cluster setup failed."
  exit 1
fi

sleep 5

echo export KUBECONFIG=~/.kube/eksctl/clusters/$cluster_name

export KUBECONFIG=~/.kube/eksctl/clusters/$cluster_name

# Configuring resources

echo "Creating namespaces, adding openfaas and logging"

echo "Namespace..."
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml

echo "Adding repository and creating de service..."
helm repo add openfaas https://openfaas.github.io/faas-netes/

helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set functionNamespace=openfaas-fn \
    --set serviceType=LoadBalancer \
    --set basic_auth=true \
    --set gateway.replicas=2 \
    --set queueWorker.replicas=2

sleep 100
echo "Getting password..."
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode) && echo "OpenFaaS admin password: $PASSWORD"

echo "Getting the gateway URL..."
export OPENFAAS_URL=$(kubectl get svc -n openfaas gateway-external -o  jsonpath='{.status.loadBalancer.ingress[*].hostname}'):8080 && echo Your gateway URL is: $OPENFAAS_URL

echo openfaas_url=$OPENFAAS_URL >> ../config.sh

echo "Logging..."
echo -n $PASSWORD | faas-cli login -g $OPENFAAS_URL -u admin --password-stdin
echo "loggin with success"
