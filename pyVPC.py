#!/usr/bin/env python3
__version__ = '1.00'

import argparse
import socket
import sys
import os
from subprocess import call
from troposphere import (GetAtt, Output, Parameter,
                         Ref, Tags, Template)
from troposphere.autoscaling import Metadata

from troposphere.ec2 import (VPC, Instance, InternetGateway, NetworkAcl,
                             NetworkAclEntry, NetworkInterfaceProperty,
                             PortRange, SecurityGroup, SecurityGroupRule,
                             VPCGatewayAttachment)





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


def main():
    make_template()

if __name__ == "__main__":
    main()