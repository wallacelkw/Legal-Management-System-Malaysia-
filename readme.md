## Overview
Legal CRM System in Malaysia is help the new law firm handle the client relationship and cases. Besides it also provide the basic analysis of the client and case. The system include create client,
cases, invoice.


## Step
1. Clone the git
   `git clone [repo]`
2. Create virtual environment
   `python -m venv env`
3. Install the dependencis
   `pip install -r requirements.txt`
4. Make migrations
   `python manage.py makemigrations`
5. Migrate to database
  `python manage.py migrate`
6. Run the program
   `python manage.py runserver`

**This is only use db.sqlite**. If want use PostgreSQL it need to link the database under `settings.py`

DATABASES = {<br />
&emsp;&emsp;&emsp;&emsp;"default": {<br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"ENGINE": "django.db.backends.postgresql_psycopg2", <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"NAME": env("DB_NAME"), <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"USER": env("DB_USER"), <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"PASSWORD": env("DB_PASSWORD"), <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"HOST": env("DB_HOST"), <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"PORT": env("DB_PORT"), <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;} <br />
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;} <br />

## Screeshot of the System
![alt text](myadmin/static/images/dashboard.png)
