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

```

