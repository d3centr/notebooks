#!/bin/bash
set -euo pipefail

PREFIX=playground

case $1 in

    # `./stack.sh storage.yaml BucketName=bucket-name` to create playground bucket along EFS
    storage.yaml)
        default_vpc=`aws ec2 describe-vpcs --filters Name=is-default,Values='true' \
            --query Vpcs[0].VpcId --output text`
        # create csv list
        subnets=`aws ec2 describe-subnets --filters Name=vpc-id,Values=$default_vpc \
             --query Subnets[*].SubnetId --output text | tr '[:blank:]' ,`
        aws cloudformation deploy --stack-name $PREFIX-storage --template-file $1 \
            --capabilities CAPABILITY_IAM --parameter-overrides Subnets=$subnets ${@:2};;

esac

