# Welcome to pyVPC!

This tool will help you create your CloudFormation VPC template with your choice of CIDR block, environment name and other custom features.


# Usage

```bash
# pyCfVpc.py [-h] --cidr CIDR --environment ENVIRONMENT [--port PORT]  [--incidr INCIDR] [--outcidr OUTCIDR]   

```
####Required Parameters
__ __            | __ __
-----------------|---------
-c --cidr | VPC cidr block
-e --environment | Environment name 
####Optional Parameters
_ | _
------|-------
-p --port| ACL inbound port number, defaults to 443
-i --incidr | CIDR ACl inbound rule, defaults to 0.0.0.0/0
-o --outcidr | CIDR CL outbound, defaults to 0.0.0.0/0