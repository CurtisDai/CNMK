User guide of the Playbook
*********
Author: Zhaoqian Dai
*********

The structure of playbook:
- roles
  - couchdb 
  - docker
  - harvester
  - instance
  - local_env
  - mountvolume
  - network
  - security_groups
  - software
  - spark_hadoop
  - tool
  - web
- vars
  - vm_settings.yml
- deploy_everything.yml
- env_install_ubuntu.sh
- env_install_macos.sh
- launch.yml
- launch.sh
- ReadMe.md
- openrc.file


How to use the resources:

If it is the first time you use, run the env_install.sh to make sure all related packages are install on your local:

sudo ./env_install.sh

For the person to execute, make sure you have a accessible openstack cloud platform download the OpenStack RC file, and run it:

sudo . [your path the the file]/xxxxopenrc.sh

Modify the parameters in vars/vm_settings.yml, some vars have to be changed which also has been emphasized in the file.
    
If you haven’t deployed any distance now, just run the launch.sh file to creating instances and deploy everything:

sudo ./launch.sh


The last step for you is to login to the master node with ssh:

ssh -i [the path to your key]/xxx.pem ubuntu@xxx.xxx.xxx.xxx

Run:

cd /mnt/data/web_server/DeadlySins && sudo npm run dev - <IP address of master>


Open a browser and visit <IP address of master>:80 , then you can get the web page of the web server。




Error Handling:
1. no module named 'wordnet'/'vader_lexicon':
run these command:
python3
import nltk
nltk.download()
d wordnet
d vader_lexicon
q
exit(0)

