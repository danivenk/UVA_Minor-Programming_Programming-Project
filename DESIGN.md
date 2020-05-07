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
Line_type refers to the type of vehicles using this line (Metro, Train, Tram, Bus etc.)

## Database
The database will be constructed using SQLAlchemy. I'll be using the train network of Hankyū Electric Railways in Ōsaka, Japan. Since I haven't found a good api to use, I'm going to construct the database myself.

#### Info about the used network
The train network of Hankyū Electric Railways contains 3 main lines with branchlines, the Kōbe Main Line, the Takarazuka Main Line and the Kyōto Main Line. On these lines serveral different rail services run. These are for example: Local, Rapid, Limited Express and more.