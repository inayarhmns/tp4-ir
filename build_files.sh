apt-get update && apt-get install -y python3 python3-pip
pip install -r requirements.txt
python manage.py collectstatic --no-input --clear