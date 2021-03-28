# git fetch origin new
# git merge origin/master new
git pull
sh i18n.sh
# pip3 install -r requirements.txt

cd backend
python3 manage.py migrate --settings=backend.settings_prod
python3 manage.py collectstatic --no-input --settings=backend.settings_prod

supervisorctl restart ark2020
service nginx restart