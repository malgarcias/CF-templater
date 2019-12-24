import argparse
import re
import os
from subprocess import call
from troposphere import (GetAtt, Output, Parameter,
                         Ref, Tags, Template)
from troposphere.autoscaling import Metadata

from troposphere.ec2 import (VPC, Instance, InternetGateway, NetworkAcl,
                             NetworkAclEntry, NetworkInterfaceProperty,
                             PortRange, SecurityGroup, SecurityGroupRule,
                             VPCGatewayAttachment)



class pyCfVpc:
    def __init__(self, vpc_cidr, environment, port, incidr, outcidr):
        
        self.vpc_cidr = vpc_cidr
        self.environment = environment
        self.port = port
        self.incidr = incidr
        self.outcidr = outcidr

def validate_cidr(cidr):
    z = re.search('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))$',cidr)
    if z:
        return True
    raise ValueError('Invalid CIDR block notation')





def make_template(obj):
    t = Template()

    t.set_version('2010-09-09')

    t.set_description("Service VPC")
    ref_stack_id = Ref('AWS::StackId')
    ref_region = Ref('AWS::Region')
    ref_stack_name = Ref('AWS::StackName')
 
    
    cidr_block = obj.vpc_cidr
    environment = obj.environment
    port = obj.port
    incidr = obj.incidr
    outcidr = obj.outcidr

    VPCInstance = t.add_resource(
    VPC(
        'VPC',
        CidrBlock=cidr_block,
        EnableDnsHostnames=True,
        EnableDnsSupport=True,
        Tags=Tags(
            Application=ref_stack_id,
            Name = '{}-ServiceVPC'.format(environment),
            Environment=environment)))
   
    internetGateway = t.add_resource(
        InternetGateway(
            'InternetGateway',
            Tags=Tags(
                Application=ref_stack_id,
                Environment=environment,
                Name='{}-InternetGateway'.format(environment))))

    gatewayAttachment = t.add_resource(
        VPCGatewayAttachment(
            'AttachGateway',
            VpcId=Ref(VPCInstance),
            InternetGatewayId=Ref(internetGateway)))

    networkAcl = t.add_resource(
        NetworkAcl(
            'NetworkAcl',
            VpcId=Ref(VPCInstance),
            Tags=Tags(
                Name='{}-NetworkAcl'.format(environment),
                Environment=environment,
                Application=ref_stack_id),
        ))
    vpcNetworkAclInboundRule = t.add_resource(
        NetworkAclEntry(
            'InboundHTTPNetworkAclEntry',
            NetworkAclId=Ref(networkAcl),
            RuleNumber='100',
            Protocol='6',
            PortRange=PortRange(To=port, From=port),
            Egress='false',
            RuleAction='allow',
            CidrBlock=incidr,
        ))

    vpcNetworkAclOutboundRule= t.add_resource(
        NetworkAclEntry(
            'OutBoundHTTPNetworkAclEntry',
            NetworkAclId=Ref(networkAcl),
            RuleNumber='200',
            Protocol='6',
            Egress='true',
            RuleAction='allow',
            CidrBlock=outcidr,
        ))

    t.add_output(
        [Output('URL',
                Description='Newly created application URL',
                Value='Prueba')])
    print(t.to_json())
#

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cidr', '-c', help="VPC CIDR Address Block", type= str, required=True)
    parser.add_argument('--environment', '-e', help="Environment Name", type= str, required=True)
    parser.add_argument('--port', '-p', help="Inbound ACL port", type= int, default=443)
    parser.add_argument('--incidr', '-i', help="Inbound ACL CIDR Block", type= str, default='0.0.0.0/0' )
    parser.add_argument('--outcidr', '-o', help="Outbound ACL CIDR Block", type= str, default='0.0.0.0/0' )
    args=parser.parse_args()
    if validate_cidr(args.cidr):
        v = pyCfVpc(args.cidr, args.environment, args.port, args.incidr, args.outcidr)
        make_template(v)
    
        