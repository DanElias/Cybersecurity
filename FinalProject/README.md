# Setup

- In FinalProject folder:
- Create a virtualenv .env with: virtualenv .env

- Activate virtualenv: .env/Scripts/activate

- Run pip install -r requirements.txt

- go to Protech folder

- Run migrations: python manage.py makemigrations
- Then: python manage.py migrate

- Create your local super user: python manage.py createsuperuser

- Run server: python manage.py runserver