../config.sh saves the cluster's name and regions, and OpenFaas's URL

________

Folders:
- metrics: Folder with metrics needed to train the model

Scripts:
- cluster.sh: Start the cluster and deploy OpenFaas
- deleteCluster.sh: Delete OpenFaas service and cluster
- getData.sh: Get metrics to train the model; creates a folder with the function's name and saves the data
    - Input: 
        - *Path to function YAML* 
        - *Function's Input*
        - *Function's Input name*

Python files:
- getFunctionYaml.py: Get OpenFaas function's name
- updateConfiguration.py: Updates YALM file and adds the constrains from the output's model
- updateURL.py: Sets OpenFaas URL in the YAML file
