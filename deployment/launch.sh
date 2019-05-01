#!/bin/sh
. ./unimelb-comp90024-group-17-openrc.sh
echo "Please enter node name:"
read NODENAME
echo "Please enter volume name:"
read VOLUMENAME
sudo ansible-playbook launch.yaml --extra-vars "nodename=$NODENAME volumename=$VOLUMENAME"
