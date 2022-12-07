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
 ```bash
./stack.sh storage.yaml BucketName=<my-unique-playground-data-name>
```
or, if you do not wish to create a dedicated bucket with write permissions:
```
./stack.sh storage.yaml
```

## Instance

Specify the instance type and point to a public ssh key stored locally to grant remote access:
```bash
./stack.sh playground.yaml pub=<public key> type=m5.large  # default instance type can be omitted
```
*Note*: you will lose remote access if your public IP changes. Simply run `./stack.sh playground.yaml` to update the security group.

By default, playground runs on a small m5.large instance, i.e. `type=m5.large`. You can change this parameter to any instance type and add it to your command. The AMI is configured by AWS to support GPUs out of the box.

### Connect

```bash
# add -A to forward ssh authentication agent: useful to interact with a remote repo
ssh -i <private key> -L 8888:localhost:8888 ec2-user@<remote ip>
```

where `remote ip` is the public ip of your playground, as shown in EC2 console.

The script will echo this ip in your terminal after successful deployment. You can also use it to connect without ip:
```bash 
./stack.sh -i <private key>
```
Connect with `stack.sh` to a custom instance name:
```bash
NAME=<...> ./stack.sh -i <private key>
```

### Multiple Instances
Specify `name` in `./stack.sh` to differentiate when starting several playgrounds, e.g.:
```bash
./stack.sh playground.yaml pub=<public key> type=m5.large name=default-playground
./stack.sh playground.yaml pub=<public key> type=r5.large name=memory-optimized
```
Default is `name=playground`.

## Jupyter

Start a Jupyter server in playground terminal: `jupyter lab` or `jupyter notebook`.

Copy the `http://localhost:8888/?token=...` address from the logs and paste in your browser to start playing.

**Tip**

Wrap the command between `nohup` and `&` so your server keeps running despite disconnections:\
`nohup jupyter lab &` or `nohup jupyter notebook &`

Secret jupyter url won't show in your terminal. It will have to be taken from the `nohup.out` file.

