#!/bin/sh

ansible-playbook --ask-become-pass launch.yml
ansible-playbook deploy_everything.yml
