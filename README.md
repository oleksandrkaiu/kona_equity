# Kona Equity

Repository for Kona Equity's site at https://www.konaequity.com.

## Setting up locally

To set the site up locally, you'll need to have [Python 3.8.0](https://www.python.org/downloads/release/python-380/) installed on your local system. Once that is done and ready, proceed to download the repository. Since the repository is private, only collaborators can access it.

1. Make the directory for development:
```bash
mkdir konaequity
cd konaequity
```
2. Download the repository
```bash
git init
git remote add origin https://github.com/GeorgiI37/konaequity
git pull origin master
```
&nbsp;&nbsp;At this point, you'll be asked to provide credentials of your Github account.

3. While the repository is downloading, setup your database. Install MySQL using any of the installation guides commonly available on the internet, depending on your OS. Create a new user (referred to as username hereafter) and a new database (referred to as dbname hereafter).

4. Now, install required packages for this. You may use a virtual environment for this part. Activate the virtual environment before installing packages with:
```bash
pip install -r requirements.txt
```
5. In your project directory, open ```django_react/settings.py```, and change the database configuration to that set up in step 3:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'username',
        'PASSWORD': '123456789',
    }
}
```
&nbsp;&nbsp;Also turn on debug by setting the variable to ```True``` like this:
```python
DEBUG = True
```
6. Create required tables using Django's migration:
```bash
python manage.py migrate
```
&nbsp;&nbsp; This may take a few minutes. After this, create the cache table using:
```
python manage.py createcachetable
```
7. Download company data (partial SQL dump) from the [site home](https://www.pythonanywhere.com/user/Konaequity/files/home/Konaequity/django_react). The file would be named ```dpsome.sql```. This contains roughly 20,000 company records (~2%) which may be enough to start with. However, if you intend on doing profiling, you should consider getting a larger SQL dump. Place this file in the ```konaequity``` directory created in step 1.
8. In the same directory, run the following command to export to your database:
```bash
mysql -u <username> -p -h localhost <dbname> < dpsome.sql
```
9. Start up the site by running:
```bash
python manage.py runserver
```
If "no module named ..." error occured, you have to install pip packages until no error.
e.g: pip install xxx
&nbsp;&nbsp; You should see the following:
```bash
Django version 3.0.10, using settings 'django_react.local_settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
&nbsp;&nbsp; Go to http://127.0.0.1:8000/ to view the site.
