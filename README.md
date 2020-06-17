# Django SNS

## Quick start

```bash
git clone https://github.com/aciddust/Django_SNS.git
cd Django_SNS

# dependencies
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py makemigrations contents
python manage.py migrate

# create admin account
python manage.py createsuperuser
```

### Run as `Develop` mod
```bash
./on_dev.sh
```

### Run as `Product` mod
```bash
./on_prod.sh
```

## Settings

setting files are in `${PROJECT}/settings`  
Basically, common items are included in base.py.  
Use dev.py and prod.py as appropriate depending on the situation.  

### AWS : S3 Boto3

If you want to chain S3 Bucket, change the settings below in base.py.

```python
# AWS S3
AWS_ACCESS_KEY_ID = 'YOUR KEY'
AWS_SECRET_ACCESS_KEY = ' YOUR SECRET'

AWS_DEFAULT_ACL = 'public-read'
AWS_REGION = 'YOUR REGION'
AWS_STORAGE_BUCKET_NAME = 'YOUR BUCKET'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### WSGI on Apache2

#### Create Virtual environment

```bash
pip install virtualenv
virtualenv your_virtualenv_name --python=python3.6
source your_virtualenv_name/bin/activate
deactivate
```
If there is nothing wrong with the use after creating the virtual environment, go to the next step.  


#### Apache setting
please check [this page](https://github.com/aciddust/Django_SNS/tree/master/lonelygourmet)



# Have Fun

## Home
![image_home](/demo/home.gif)

## Follow
![image_follow](/demo/follow.gif)

## MyPage
![image_mypage](/demo/mypage.gif)