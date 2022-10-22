# Playground

A simple AWS instance for on-demand compute.

- Jupyter server in default VPC on AWS Deep Learning AMI
- SSH access granted to public ip of the owner
- notebooks and code are stored on EFS
- by design, data is expected to rest in s3

### How To

- *Create* or *update* storage and playground stacks with provided `stack.sh` script.
- *Monitor* or *delete* resources in CloudFormation console (UI).

## Storage

*deploy once before any playground*

Playground is stateless. So files and data outlive cloud instances, deploy `storage.yaml`:
 ```
./stack.sh storage.yaml BucketName=my-unique-playground-data-name
```
or, if you do not wish to create a dedicated bucket with write permissions:
```
./stack.sh storage.yaml
```

## Instance

Point to a public key stored locally to grant remote access to your playground instance:
```
./stack.sh playground.yaml PublicKeyPath=<path/to/.ssh/key.pub>
```
*Note*: you will lose remote access if your public IP changes. In this case, run the same command again to update the security group.

By default, playground runs on a small m5.large instance, i.e. `InstanceType=m5.large`. You can change this parameter to any instance type and add it to your command. The AMI is configured by AWS to support GPUs out of the box.

### Connect

`ssh -i <private key> -L 8888:localhost:8888 ec2-user@$remote_ip`

where `$remote_ip` is the public ip of your playground, as shown in EC2 console.

The script will echo this ip in your terminal after successful deployment. You can also use it to connect without ip:\
`./stack.sh -i <key>` for a default playground or `NAME=<...> ./stack.sh -i <key>` for a custom InstanceName.

### Multiple Instances
Specify `InstanceName` to differentiate when running several playgrounds. Default is `InstanceName=playground`.

## Jupyter

Start a Jupyter server in playground terminal: `jupyter lab` or `jupyter notebook`.

Copy the `http://localhost:8888/?token=...` address from the logs and paste in your browser to start playing.

**Tip**

Wrap the command between `nohup` and `&` so your server keeps running despite disconnections:\
`nohup jupyter lab &` or `nohup jupyter notebook &`

Secret jupyter url won't show in your terminal. It will have to be taken from the `nohup.out` file.

