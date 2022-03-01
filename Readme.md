_INSTALLATION_:
pip install requirements.txt

_RUN_:
python manage.py runserver

_API TESTING_:

TASK 1:http://localhost:8000/news/

TASK 2: Try hit the url

TASK 3:http://localhost:8000/news/favourite/

query params = {"id":447,"user":"enganaskhalid@gmail.com"}


**API_DOCUMENTATION**:
All the valid apis provided above are documented by DRF

**CONFIGURATION**
configuration.py create instances of all the sources listed in config.ini

required :
    base_url,name

The app is very much scalable. We can add multiple news apis in future.

