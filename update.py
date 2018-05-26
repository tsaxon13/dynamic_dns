#!/usr/bin/python3

import boto3
import urllib.request

client = boto3.client('route53')

zoneId = [x for x in client.list_hosted_zones()[
    'HostedZones'
    ] if x['Name'] == "tonysaxon.com."][0]['Id']

recordSet = "home.tonysaxon.com"
TTL = 300
Comment = "Auto Updating"
Type = "A"

myIP = urllib.request.urlopen(
         "http://utils.tonysaxon.com/myip.php"
       ).read().decode('ascii')

changeSet = {
    "Comment": Comment,
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "ResourceRecords": [
                    {
                        "Value": myIP
                    }
                ],
                "Name": recordSet,
                "Type": Type,
                "TTL": TTL
            }
        }
    ]
}

client.change_resource_record_sets(HostedZoneId=zoneId, ChangeBatch=changeSet)
