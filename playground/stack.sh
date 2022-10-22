#!/bin/bash
set -euo pipefail

# override default name to connect to an instance: `NAME=<...> ./stack.sh -i <key>`
: ${NAME:=playground}
# Jupyter broken on "AWS Deep Learning AMI GPU TensorFlow 2.8.0 (Amazon Linux 2) 20220216":
# would need to rebuild python with sqlite
IMAGE="AWS Deep Learning AMI Habana TensorFlow 2.7.0 SynapseAI 1.2.0 (Amazon Linux 2) 20220208"

image () {
    aws ec2 describe-images --owners amazon \
        --filters Name=is-public,Values=true Name=name,Values="$IMAGE" \
        --query Images[0].ImageId --output text
}

remote_ip () {
    local name=$1
    aws ec2 describe-instances \
        --filters Name=image-id,Values=`image` \
                  Name=tag:Name,Values=$name \
                  Name=instance-state-name,Values=pending,running \
        --query Reservations[0].Instances[0].PublicIpAddress --output text
}

case $1 in

    # `./stack.sh storage.yaml BucketName=<bucket name>` creates a bucket along EFS
    storage.yaml)
        default_vpc=`aws ec2 describe-vpcs --filters Name=is-default,Values='true' \
            --query Vpcs[0].VpcId --output text`
        # create csv list
        subnets=`aws ec2 describe-subnets --filters Name=vpc-id,Values=$default_vpc \
             --query Subnets[*].SubnetId --output text | tr '[:blank:]' ,`
        aws cloudformation deploy --stack-name $NAME-storage --template-file $1 \
            --capabilities CAPABILITY_IAM --parameter-overrides Subnets=$subnets ${@:2};;

    # key required: `./stack.sh playground.yaml PublicKeyPath=<path/to/.ssh/my-key.pub>`
    playground.yaml)
        params=()
        for param in ${@:2}; do
            IFS== read key value <<< "$param"
            if [ $key = PublicKeyPath ]; then
                params+=( PublicKey=`cat $value` )
            elif [ $key = InstanceName ]; then
                NAME=$value
                params+=( $key=$value )
            else
                params+=( $key=$value )
            fi
        done
        ip=`curl -sL checkip.amazonaws.com`
        aws cloudformation deploy --stack-name $NAME --template-file $1 \
            --parameter-overrides ImageId=`image` ConnectionIp=$ip "${params[@]}"
        echo "Your instance should be ready within 5mn. Already connect with:"
        echo
        echo "ssh -L 8888:localhost:8888 ec2-user@`remote_ip $NAME` -i <private key>"
        echo or
        echo "./stack.sh -i <private key>"
        echo
        echo "The instance is ready when /var/log/cfn-init.log exists and completes.";;

    -i)
        ssh -L 8888:localhost:8888 ec2-user@`remote_ip $NAME` -i $2;;

    *) echo "$1 template undefined";;

esac

