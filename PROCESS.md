# Process

![Logo](doc/NI_logo.svg)

## Committed on April 1 2020
### Proposal Document,
Nothing special

## Committed on April 3 2020
### Added prerequisites,
Nothing Special

## Committed on April 5 2020
### Design Document,
Nothing Special

## Committed on April 8 2020
### Setup minimal app,
I decided to use flask, flask-admin, flask-login, flask-migrate
These will be used because I'll be using this because the app needs to be written in python and has a database. Since I'd like to be able to easily edit the database as an Admin I'll be using flask-login and flask-admin (for login and admin) Because of this current models include a user (with username, password, email) and an anonymous user (for when someone is not logged on).
As a result of this I think it'l be easier to create the app and manage it.
From Web App studio I have some experience with those modules.

## Committed on April 16 2020
### Basic setup of line and stop pages,
I've linked the stops table and the lines table with a many-to-many relationship, this is because A stop can have multiple lines and a line can have multiple stops.
With this a network can be created using these tables.

I've also intelinked the stop and line pages.
This way the you can reach all lines/stops on a line/stop page
This makes it easier to traverse the application

## Committed on April 20 2020
### Added search function
With this you'll be able to search lines or stops based on their parameters.
The search function will split the queries into sub-queries and lookup every possible result and sort it by relevance.

## Committed on April 23 2020
### Uniform style across main side and admin side.
This will make the app look more consistent across the whole app.
I think it also makes the app look more professional when the style is consistent across the whole app.

## Committed on April 30 2020
### Not redefining all pages on the admin side,
This should in theory be less work, redefining all admin pages is a lot of work and instead using the already available ids and classes will make it easier to restyle the pages.

## Committed on May 7 2020
### Added custom edit/delete glyphs (free to use ones, credit see image_refs.txt)
Nothing Special

### Finally decided on the final network for the database, the Hankyū Electric Railways network
This network conveniently covers all the functionalities I'd like to show. It has multiple stops across multiple lines, it has train types and a through service to a different railway company. The latter both of which I'm going to still add.

## Committed on May 10 2020
### Added company to lines and continue stoptype implementation and link from admin side to main side and back when admin is logged on.
I decided to do this becaus this way when an admin is signed on he/she can easily go to the adminside. This has been done as an convenience to future admins, this way they don't have to know the url to the admin side.

## Committed on May 11 2020
### Finished stoptype implementation,
Nothing Special

## Committed on May 12 2020
### Pocess Document,
Nothing Special

## Committed on May 14 2020
### Added stopnumbers
This was added because it would make it easier to order the stops in the lines table. I think this because stopnumbers are of the letter-number format. Thus if it has numbers it could be used to sort the stops array in a line.

## Committed on May 15 2020
### Data Loader using a flask app
I saw this in a tutorial from Harvard's CS50 and thought can't be that hard. This should make it easy to load the data into the database.

### Added an __init__.py to the app directory
This way the modules in /app can be easily imported from outside the /app directory. Else you get a import error: no parent package found.

## Commited on May 16 2020
### Loading data in database same as for the Books Project
Well *APEARENTLY* I could not get it to work what I told about yesterday... I got the error that the database was not found even though I could use it in the app, I even tried using a new database but that didn't work...
So decided to use the same method in the Books Project, since I know that method does work...

## Committed on May 17 2020
### Added macron query and pages
I decided to add the macron_query because not all users will know how to add a macron to a vowel in a search query and people should be able to still search. I won't change the database entries to macron less entries because the aesthetics, the English names in Japan are with them so I have the entries with them.

I also decided to add pages to the lists (/lines, /stops and /search) because this way the lists won't go on for forever and this will make them loop more organized. This does also mean I have to add links to the other pages of the same list. The maximum number of items per list will be 50.

### Exact search
I realized that an exact search result sould be more on top of the search results. I think this because of relevance, this way when I search for a specific line name or stop name it should appear on top of the search results.

## Committed on May 18 2020
### Adding more Comments, Logo and finishing some css
Nothing Special

### README document, requirements.txt, Model chart update
Nothing Special

## Committed on May 19 2020
### Fixed some minor bugs found and removed some dead code
Nothing Special

### DESIGN document update
Nothing Special