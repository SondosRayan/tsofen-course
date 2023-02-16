import boto3
import os
import json


def get_all_regions():
    # Get list of regions
    ec2_client = boto3.client('ec2')
    all_regions = ec2_client.describe_regions().get('Regions',[] )
    regions_names = [region.get("RegionName") for region in all_regions]
    return regions_names


def get_all_instances_iterator(region):
    ec2_resource = boto3.resource('ec2', region)
    instances_iterator = ec2_resource.instances.all()
    return instances_iterator


def get_all_nat_getways(region):
    
    ec2_client = boto3.client('ec2',region)
    all_nats = ec2_client.describe_nat_gateways().get("NatGateways", [])
    nat_ids = [nat.get("NatGatewayId",[]) for nat in all_nats]
    nat_addresses = [nat.get("NatGatewayAddresses",[]) for nat in all_nats]
    nat_ips = [address[0].get("AllocationId",[]) for address in nat_addresses]
    nat_states = [nat["State"] for nat in all_nats] 
    return nat_ids, nat_states, nat_ips
    

def terminate_region(region):
    # terminate all instances in this region
    ec2_client = boto3.client('ec2', region)
    instances_iterator = get_all_instances_iterator(region)
    ids = [inst.id for inst in instances_iterator]
    if ids != []:
        response = ec2_client.terminate_instances(InstanceIds=ids)
    
    # delete all nat getways in this region
    nat_getways_id, nat_states, nat_getways_ip = get_all_nat_getways(region)
    if nat_getways_id != []:
        # delete this nat getway
        for i in range(len(nat_getways_id)):
            id = nat_getways_id[i]
            ip = nat_getways_ip[i]
            state = nat_states[i]
            if state == "available":
                response = ec2_client.delete_nat_gateway(NatGatewayId=id)
                while state != "deleted": 
                    nat = ec2_client.describe_nat_gateways(NatGatewayIds=[id,],).get("NatGateways", [])
                    state = nat[0]["State"]
                response = ec2_client.release_address(AllocationId=ip)
            

def terminate_all_regions():
    regions = get_all_regions()
    for region in regions:
        terminate_region(region)


terminate_all_regions()