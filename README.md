PUR BEURRE - OPENCLASSROOMS PYTHON - PROJECT #11

This open source project was created for the OpenClassRooms' Python developer course (Project 8/13)). It is a DJANGO application integrating a back-end part based on Python 3.7 and a front-end part developed with HTML5, CSS3 and JavaScript using Bootsrap.

Ask the application a product name, select one of the products to confirm your choice and it will give you a list of similar products with a better nutriscore. When registered, the user can save those favorite subsitutes.
How to install this project
1 - Fork the project
2 - Clone the project on your PC
3 - Create and set the database

This project was conceived with postgresql, but we can use an other db engine.
STEP 1 : Create a database.

(with postgresql)
createdb <your database name>
STEP 2: Create your virtualenv

(on mac and linux)
cd PB_P8
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
STEP 3 : Create a setting file pur_beurre_project/settings/.env

SECRET_KEY = '<your secret key>'

IP = 'localhost'

DB_NAME = '<your database name>'
DB_USER = '<your database username>'
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = '5432'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STEP 4 : Migrate the model into the database

./manage.py migrate

STEP 5 : Load database

    Option 1 : fastest one, with a dump file(.json) and the django loaddata command

./manage.py loaddata foodSearch/dumps/foodSearch.json

    Option 2 : slowest one, with the script that imports datas from the OpenFoodFacts API

    We uses the OpenFoodFacts API for python
    Make sure you've installed it on your environnement (not in the requirements.txt)
    sudo pip install git+https://github.com/openfoodfacts/openfoodfacts-python

    Open the module pur_beurre_project/foodSearch/management/commands/settings.py.
    Change the pages from OpenFoodFacts you want to include in your database
    NB: 10 products per page (around 5 seconds per page on my mac)

FIRST_PAGE =  <first page from openfoodfacts api you want to load>
LAST_PAGE = <last page from openfoodfacts api you want to load>
DB_REPORTS_FILE = <file in which you want a report of your DB changes>

    Launch the command on your terminal
    ./manage.py fill_db -f

4 - Launch project

./manage.py runserver With your usual browser, use the application on url http://127.0.0.1:8000/
Find the project online

This project can be tested on url https://pbp8.herokuapp.com/
NB: Due to django database size limitation, the number of products may be limited to a few products from breakfasts category
Next Steps

This app tries to correspond to the specifications. Some features, specified as not required, have not been developped:

    For now, user can't change his password or ask for an other one if he lost it
    It could be interesting for user to be able to save product as favorite from detail product page (not into site visuals provided)
    This app only compares products with nutriscore, it would be relevant to add criterias as organic, components...
    The user profile is, as specified almost empty, we could add more informations on the user
    We could add a research input in the favorite page.
