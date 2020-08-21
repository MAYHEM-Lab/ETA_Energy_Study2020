if [ ! -d "venv" ]
then
  pip3 install virtualenv
  virtualenv venv --python=python3.8
fi
source venv/bin/activate
pip install -r requirements.txt
