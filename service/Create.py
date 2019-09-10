from flask import jsonify, request
from flask_restful import Resource
import boto3
from model.Model import User, db, users_schema


globreq = 0
globtvalue = 0


class Creates(Resource):
    def get(self):
        val = User.query.all()
        return users_schema.jsonify(val)

    def post(self):
        global globreq
        global globtvalue
        jsonval = request.get_json()
        print(jsonval)
        securitygroups = []
        instancecount = jsonval['instancecount']
        imageid = jsonval['imageid']
        instancetype = jsonval['instancetype']
        keyname = jsonval['keyname']
        securitygroup = jsonval['securitygroup']
        spotprice = jsonval['spotprice']
        tvalue = jsonval['tvalue']
        globtvalue = tvalue
        print(instancecount)
        instancecount = int(instancecount)
        securitygroups.append(securitygroup)

        client = boto3.client('ec2', region_name='us-east-1')
        req = client.request_spot_instances(InstanceCount=instancecount,
                                            LaunchSpecification={
                                                'SecurityGroups': securitygroups,
                                                'ImageId': imageid,
                                                'InstanceType': instancetype,
                                                'KeyName': keyname,
                                            },
                                            SpotPrice=spotprice
                                            )
        globreq = req
        print('Spot request created, status: ' + req['SpotInstanceRequests'][0]['State'])
        req = globreq
        tvalue = str(globtvalue)
        client = boto3.client('ec2')
        index = 0
        for spotInstanceRequestId in req['SpotInstanceRequests']:
            current_req = client.describe_spot_instance_requests(
                SpotInstanceRequestIds=[req['SpotInstanceRequests'][index]['SpotInstanceRequestId']])
            index += 1
            if current_req['SpotInstanceRequests'][0]['State'] == 'active':
                instanceId = (current_req['SpotInstanceRequests'][0]['InstanceId'])
                print('Instance allocated ,Id: ',
                      current_req['SpotInstanceRequests'][0]['InstanceId'])
                newtval = tvalue + str(index)
                client.create_tags(Resources=[current_req['SpotInstanceRequests'][0]['InstanceId']],
                                   Tags=[{
                                       'Key': 'Name',
                                       'Value': newtval
                                   }])
                bitprice = current_req['SpotInstanceRequests'][0]['SpotPrice']
                time = current_req['ResponseMetadata']
                time1 = time['HTTPHeaders']
                ltime = time1['date']
                # spotrequestid = current_req['SpotInstanceRequests'][0]['SpotInstanceRequestId']
                req2 = client.describe_instances(InstanceIds=[instanceId])
                publicdns = req2['Reservations'][0]['Instances'][0]['PublicDnsName']
                print(instanceId)
                jsonva = User(TAG_VALUE=newtval, PUBLIC_DNS=publicdns, DATE=ltime, SPOTINSTANCE=bitprice, INSTANCEID=instanceId)
                db.session.add(jsonva)
                db.session.commit()
        return jsonify({'Creation': 'success'})

    def delete(self):
        jsonval = request.get_json()
        instanceid = jsonval['instanceid']
        client = boto3.client('ec2')
        term = client.terminate_instances(
            InstanceIds=[
                instanceid,
            ],
        )
        User.query.filter_by(INSTANCEID=instanceid).delete()
        db.session.commit()
        return jsonify({'Terminated': instanceid})


class Volume(Resource):
    def get(self):
        a = []
        client = boto3.client('ec2')
        response = client.describe_volumes()
        n = 0
        while True:
            try:
                volumeid = response['Volumes'][n]['VolumeId']
                a.append(volumeid)
                n += 1
            except:
                break
        return jsonify({'Volumeid': a})

    def post(self):
        userval = request.get_json()
        client = boto3.client('ec2', region_name='us-east-1')
        response = client.create_volume(
            AvailabilityZone='us-east-1c',
            Encrypted=True,
            Size=5,
            VolumeType='gp2',
            TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': userval['tvalue']
                        },
                    ]
                },
            ]
        )
        jsonval = response
        volumeid = jsonval['VolumeId']
        vtag = jsonval['Tags'][0]['Value']
        return jsonify({'Volumeid': volumeid, 'Volumetag': vtag})

    def put(self):
        client = boto3.client('ec2')
        jsonval = request.get_json()
        instanceid = jsonval['instanceid']
        volumeid = jsonval['volumeid']
        mount = client.attach_volume(VolumeId=volumeid, InstanceId=instanceid, Device='/dev/sdf')
        return jsonify({'Attached Volume to': instanceid})


    def delete(self):
        client = boto3.client('ec2')
        jsonval = request.get_json()
        volumeid = jsonval['volumeid']
        term = client.delete_volume(VolumeId=volumeid)
        return jsonify({'Terminated': volumeid})


class Keypair(Resource):
    def get(self):
        client = boto3.client('ec2')
        a = []
        response = client.describe_key_pairs()
        n = 0
        print(a)
        while True:
            try:
                keypairs = response['KeyPairs'][n]['KeyName']
                n += 1
                a.append(keypairs)
            except:
                break
        print(a)
        return jsonify({'KeyPairs': a})

    def post(self):
        client = boto3.client('ec2')
        jsonval = request.get_json()
        keyname = jsonval['keypair']
        response = client.create_key_pair(KeyName=keyname)
        a = response['KeyName']
        return jsonify({'KeyName': a})

    def delete(self):
        client = boto3.client('ec2')
        jsonval = request.get_json()
        keypair = jsonval['keypair']
        term = client.delete_key_pair(KeyName=keypair)
        return jsonify({'Deleted': keypair})
