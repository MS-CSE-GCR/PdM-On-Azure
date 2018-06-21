# PdM-On-Azure
This is a template for PdM on Azure

## Azure Service
* DSVM (Data Science Virtual Machine)
* HDInsight - Spark
* Azure Machine Learning Service
    * Azure Machine Learning Workbench
    * Azure Machine Learning Model Management
* IoT (Internet of Things)
    * IoT Hub
    * IoT Edge

## Environment Setup
1. Create a new DSVM windows 2016 with CPU following the [Documentation](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/provision-vm)
2. After creation of DSVM, use RDP to connect to the VM;
3. Install Azure Machine Learning Workbench using the `AmlWorkbenchSetup.exe` on the Desktop and it takes about 10-20 minutes to finish the installation.
4. After installation, launch AML workbench and login with azure account.
    4.1. if your account don't have an AML experimentation, you should create one first
        4.1.1. Open `Command Line Windows`;
        4.1.2. Login in using Azure CLI
            
            az login

        4.1.3. Setup Default Active Subscription in Azure account

            az account list
            
            az account set -s \<subscription id>
        
        4.1.4. Create new experimentation

            az ml account experimentation create -n \<experimenataion name> -g \<resource group name>

        4.1.5. Reload or relaunch AML workbench

## Good Reference
* [How to read/write files](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/how-to-read-write-files)
* [How to use MMLSpark](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/how-to-use-mmlspark)

