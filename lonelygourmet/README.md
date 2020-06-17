# How to set WSGI with Apache

## 1. Install `Apache2`

```bash
sudo apt install apache2
```

## 2. Install Apache mod-wsgi

```bash
sudo apt install libapache2-mod-wsgi-py3
```

## 3. Edit `wsgi.py`

```python
import os, sys
from django.core.wsgi import get_wsgi_application

path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
  sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
application = get_wsgi_application()
```

## 4. Open Port

```bash
cd /etc/apache2
sudo vi ports.conf
```

```conf
Listen 80
Listen 8000
```

## 5. Edit `000-default.conf`

```bash
cd /etc/apache2/sites-available/
sudo vi 000-default.conf
```

```conf
<VirtualHost *:80>
	#ServerName www.example.com

	ServerAdmin acidlab.help@gmail.com
	DocumentRoot /var/www/html

	#LogLevel info ssl:warn

	WSGIDaemonProcess lonelygourmet python-path=/home/ubuntu/lonely-py36/lib/python3.6/site-packages
	WSGIProcessGroup lonelygourmet

	WSGIScriptAlias / /home/ubuntu/LonelyGourmet/lonelygourmet/wsgi.py process-group=lonelygourmet application-group=%{GLOBAL}
	<Directory /home/ubuntu/LonelyGourmet/lonelygourmet>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	Alias /media/ /home/ubuntu/LonelyGourmet/media/
	<Directory /home/ubuntu/LonelyGourmet/media>
		Require all granted
	</Directory>

	Alias /static/ /home/ubuntu/LonelyGourmet/static/
	<Directory /home/ubuntu/LonelyGourmet/static>
		Require all granted
	</Directory>

	<Directory /home/ubuntu/lonely-py36/lib/python3.6/site-packages>
		Require all granted
	</Directory>

	<Directory /home/ubuntu/LonelyGourmet>
		Require all granted
	</Directory>

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

6. Restart Apache service
```bash
sudo apachectl -k restart
```

# Have Fun