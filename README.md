# AirSwAP Backend

This backend sits and waits for requests from the frontend.

# Overview - What is AirSWaP

AirSWaP allows people from different parts of the world to swap apartments/houses with each other for a certain amount of time. The motivation for the application comes from the fact that people want to travel to different parts of the world for various periods of time but don’t want to spend money on Airbnb or hotel costs. An ideal user of the app would be a person who wants a break in routine from their normal lives for a short while. This is mostly meant for people who are either able to work remotely, looking to take a vacation, or are not employed.

The pandemic showed us that with a surge of remote jobs, people want a break from their normal routine at a cost that won’t break their bank. This app can help fill this void. Airbnb users can short-term and long-term rent apartments and houses all around the world, however, they have to pay for the rental.

## Getting Started / Installation

### To run on Mac & Linux

Make sure you have `venv` installed. Then create your virtual env:

```bash
python3 -m venv venv
```

Now, activate via:

On Linux and Mac:
```bash
./venv/bin/activate
```

On Windows:
```bash
source venv\Scripts\activate.bat
```

Now install

```bash
pip3 install -r requirements.txt
```

Now you can run via `python3 App.py`

### To run on Windows
#### 1) Install Virtual Environment 
```pip install virtualenv```

#### 2) CD to your project directory then run virtualenv to create the new virtual environment.
The following commands will create a new virtual environment under my-project/my-venv.
```
   cd my-project
   virtualenv --python C:\Path\To\Python\python.exe venv
```

#### 3) Activate Environment
`venv\Scripts\activate.bat`

#### 4) Install requirements
`pip install -r requirements.txt`

#### 5) Run the App
`python App.py`


## Requirements

This system runs off of Python3 Flask for handling routing. We use Flask SQLAlchemy in order to communicate with our database. We also use the Flask JWT Extended library in order to simplify authentication. The full list of requirements can be found [in the requirements file](https://github.com/PredatorFeesh/airswap_backend/blob/master/requirements.txt).

## Data Model

All of our models are defined in (the models.py file)[https://github.com/PredatorFeesh/airswap_backend/blob/master/models.py]. Here is a breakdown:

```
User:
{
    id: 123,
    email: 'email@gmail.com',
    password: 'secure_password',
    first_name: 'Jane',
    last_name: 'Doe',
    image: 'google.com/imageloc',
    phone_number: '347-347-1010',
    description: 'I am a good person',
    listingrequested : Listing {Object},
    cities: City {Object}
}

Listing:
{
    id = 12,
    address = '12 Address Street',
    image: 'google.com/houseloc',
    description: "My Humble Abode",
    is_listed: true,
    date = March 12 2020 {Date Object},
    user_id: Foreign Key USER Id,
    city_id: Foreign Key CITY Id
}

City: 
{
    id: 12,
    name: Moscow',
    listings = Listing {Objects}
    followers = User {Object}
}
```

Additionally, we keep tables to keep relations between objects:
```
follows = db.Table(
    "follows",
    Date, User ID, City ID
)

requests = Table(
    Requester ID, Requestee ID
)
```

The different endpoints are described in the [frontend Data Model Section Here](https://github.com/PredatorFeesh/airswap_frontend/blob/master/README.md#data-model).

## Site Map

Please see the site map [on the frontend page here](https://github.com/PredatorFeesh/airswap_frontend/blob/master/README.md#sitemap).

## User Stories 

Swappers are users of our App. These are the people who would be swapping apartments or houses.

As a swapper, I want to be able to:

Auth based actions

 -Register an account
 -Login to my account
 -Log out of my account
 -Update my profile
 -Update my listing
 -Open my listing
 -Close my listing

Swap based actions

 -Follow a city
 -Unfollow a city
 -View listings of a given city
 -View listings in cities that I liked
 -Visit the profile and listing of any listing I see
 -Request to swap with someone else
 -Remove request to swap with someone else
 -View all the requests I sent
 -View all the requests I received

## References Used

- Flask JWT Docs https://flask-jwt-extended.readthedocs.io/en/stable/
- Flask Docs https://flask.palletsprojects.com/en/1.1.x/
- Flask SqlAlchemy docs https://flask.palletsprojects.com/en/1.1.x/
- SqlAlchemy Docs https://docs.sqlalchemy.org/en/13/
- Combining Tables https://swcarpentry.github.io/sql-novice-survey/07-join/index.html
- SQLite Docs https://sqlite.org/docs.html
- Postgres Docs https://www.postgresql.org/docs/

# Authors:

 -Pavlo Aleksyeyev, Pavlo.Aleksyeyev@gmail.com, https://github.com/PaulAlek
 -Natalia Harrow, nataliaharrow@gmail.com, https://github.com/nataliaharrow
 -Jason Azayev, azayevjason@gmail.com, https://github.com/PredatorFeesh



