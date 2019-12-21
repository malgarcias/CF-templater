#!/usr/bin/env python3
__version__ = '1.00'

import argparse
import socket
import sys
import types

from troposphere import (GetAtt, Output, Parameter,
                         Ref, Tags, Template)
from troposphere.autoscaling import Metadata
from troposphere.cloudformation import (Init, InitConfig, InitFile, InitFiles,
                                        InitService, InitServices)
from troposphere.ec2 import (VPC, Instance, InternetGateway, NetworkAcl,
                             NetworkAclEntry, NetworkInterfaceProperty,
                             PortRange, SecurityGroup, SecurityGroupRule,
                             VPCGatewayAttachment)
from troposphere.policies import CreationPolicy, ResourceSignal
t = Template()

t.set_version('2010-09-09')

t.set_description("Service VPC")
ref_stack_id = Ref('AWS::StackId')
ref_region = Ref('AWS::Region')
ref_stack_name = Ref('AWS::StackName')
parser = argparse.ArgumentParser()
parser.add_argument('--cidr', '-c', help="VPC CIDR Address Block", type= str)
parser.add_argument('--environment', '-e', help="Environment Name", type= str)
args=parser.parse_args()
if args == None:
    pass
#print("***",args)
cidr_block = args.cidr
environment = args.environment
VPC = t.add_resource(
    VPC(
        'VPC',
        CidrBlock=cidr_block,
        EnableDnsHostnames=True,
        EnableDnsSupport=True,
        Tags=Tags(
            Application=ref_stack_id,
            Name = '{}-ServiceVPC'.format(environment),
            Environment=environment)))

def make_template():

   
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
            VpcId=Ref(VPC),
            InternetGatewayId=Ref(internetGateway)))

    networkAcl = t.add_resource(
        NetworkAcl(
            'NetworkAcl',
            VpcId=Ref(VPC),
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
            PortRange=PortRange(To='443', From='443'),
            Egress='false',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
        ))

    vpcNetworkAclOutboundRule= t.add_resource(
        NetworkAclEntry(
            'OutBoundHTTPNetworkAclEntry',
            NetworkAclId=Ref(networkAcl),
            RuleNumber='200',
            Protocol='6',
            Egress='true',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
        ))

    t.add_output(
        [Output('URL',
                Description='Newly created application URL',
                Value='Prueba')])
    print(t.to_json())


make_template()