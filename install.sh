sudo apt-get update && apt-get upgrade -y
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install python3-virtualenv
sudo apt-get install nginx-light
sudo apt-get install postgresql


virtualenv venv
source venv/bin/activate
pip install -r requirements_deploy.txt

