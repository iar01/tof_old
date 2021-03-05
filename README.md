## TOF

```
git clone -b DEV branch
git checkout -b test_user
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
update app/settings/dev.py to set the correct database name, host name & password
createdb database_name
cd app
python manage.py migrate
python manage.py createsuperuser
>>> test_admin
>>> test_pass
python manage.py collectstatic
```
