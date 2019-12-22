import argparse
import pyVPC

class pyCfVpc:
    def __init__(self, vpc_cidr, environment, port, incidr, outcidr):
        
        self.vpc_cidr = vpc_cidr
        self.environment = environment
        self.port = port
        self.incidr = incidr
        self.outcidr = outcidr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cidr', '-c', help="VPC CIDR Address Block", type= str, required=True)
    parser.add_argument('--environment', '-e', help="Environment Name", type= str, required=True)
    parser.add_argument('--port', '-p', help="Inbound ACL port", type= int, default=443)
    parser.add_argument('--incidr', '-i', help="Inbound ACL CIDR Block", type= str, default='0.0.0.0/0' )
    parser.add_argument('--outcidr', '-o', help="Outbound ACL CIDR Block", type= str, default='0.0.0.0/0' )
    args=parser.parse_args()
    v = pyCfVpc(args.cidr, args.environment, args.port, args.incidr, args.outcidr)
    pyVPC.make_template(v)