# Design

## Technical Components
Admin section to change/add parts of the Transport Network to the database;
* Using FlaskLogin and FlaskAdmin this can be achieved

Search function to search lines/stops (by name, by location);
Line/Stop lists showing all lines/stops;
Line/Stop page with info;
* Using SQLAlchemy this can be achieved by using the sqlalchemy class models.

![Models](doc/Models.png)

The extra part in the models is for the types,
Stop_type refers to it being served by for example Local, Rapid, Express services

## Database
The database will be constructed using SQLAlchemy. I'll be using the train network of Hankyū Electric Railways in Ōsaka, Japan. Since I haven't found a good API to use, I'm going to construct the database myself.

## Overview

#### Navigation bar
![Index page](doc/app_index.png)
![Index page as admin](doc/app_index_admin.png)
![Index page as user](doc/app_index_user.png)

This navigation bar can be seen on all pages *except* for the /admin urls and /register url.
The navigation bar is described in `template/layout.html`.

In the screenshot above a bar is shown for admins to go the admin page.

To the left are links to the rest of the app and to the right is a search bar and the login dropdown.

#### Login/Register
![Index page Login Dropdown](doc/app_index_login.png)
![Index page as user](doc/app_index_user.png)

The login form can be used to login, in the when someone is logged on it'll show the logout button.

URLs linked to this are the /login and /logout URLs, they have a next_page parameter to return you to the page you came from.
Loggin in and Loggin out is regulated in `app/application.py` and in `app/functions/security.py` are helpfunctions defined for password handling.

![Register page](doc/app_register.png)

The register page can be used to register a new user, it has a back button to go back if you decide not to register.

URLs linked to this is the /register URL, they have a next_page parameter to return you to the page you came from.
Registering is regulated in `app/application.py` and in `app/functions/security.py` are helpfunctions defined for password handling.

#### Search
![Search Result page](doc/app_search.png)
![Search Result page without macrons](doc/app_search_without_macron.png)
![Search Result page line/stop name and Location](doc/app_line-stop_name_location.png)

The searchbar described in `template/layout.html` can be used to look up Lines or Stops based on their names or Stops based on their location. Also the query can be written with or without [Macrons](https://en.wikipedia.org/wiki/Macron_(diacritic)).

URLs linked to this os the /search URL, they have a page parameter to show a page at the time with max 50 items and a query parameter which is used for the search.
The search is regulated in `app/application.py` and in `app/functions/search.py` are helpfunctions defined for handling the non macron queries and showing relevant items on the top of the results.

![Search Result page multiple pages 1](doc/app_search_pages_1.png)
![Search Result page multiple pages 2](doc/app_search_pages_2.png)
![Search Result page multiple pages 3](doc/app_search_pages_3.png)

Only 50 items per page are shown, this is described in `template/search.html`

#### Stops

