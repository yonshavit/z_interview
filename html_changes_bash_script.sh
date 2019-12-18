sudo apt -y update
sudo apt -y install python2.7
sudo apt -y install python-pip
pip2 install requests
pip2 install boto3

sudo apt -y install git-all
git clone https://github.com/yonshavit/z_interview.git

cd z_interview

sudo cp -i ./webpage_watcher.py /bin
crontab ./crontab_file
python2.7 ./webpage_watcher.py
