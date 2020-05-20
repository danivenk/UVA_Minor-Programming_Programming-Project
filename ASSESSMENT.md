# Assessment

![Logo](doc/NI_logo.svg)

# Proud/Liked parts
I'm pretty proud of the functionality of the search bar. I've written 2 helperfunctions to make in my opinion searching a little bit more easier. Although I could probably have made the search route function in [`app/applictation.py`](app/application.py) look a little bit more nicer. The functions, as in splitting the query up in subqueries as a list ranging from the full query to single word subqueries and the getting all the [Macrons](https://en.wikipedia.org/wiki/Macron_(diacritic)) versions of the query, are quite nice.

I really like how I was able to make the style of the application consistent across both the admin and main sides. I was meaning to do this on the previous projects too but I was not able to. So I'm really happy it worked out this time.

I like how I have created the functions for the neighbouring stops per stop type and the stopping pattern.

Getting the stopping order right was something I needed to think about good, but I quite like how it turned out.

I'm proud of how the datafiles and data_loading files worked out. I worked 2 days straight and wanted to use the correct locations for the 103 stops so I'm proud it went good in the end. Also, I was pretty fed up when I could not get the data_loading correctly, but in the end it works quite al right.

I like how the logo turned out, I made it using Inkscape and it is simple. But that is probably why I like it.

I think comments in the code look quite neat and I worked a lot on the documentation files. (So I hope they're OK)

# Biggest Decisions
* *"I've linked the stops table and the lines table with a many-to-many relationship, this is because A stop can have multiple lines and a line can have multiple stops. With this a network can be created using these tables."* Well with this I was able to do it just fine.

* *"Uniform style across main side and admin side. his will make the app look more consistent across the whole app. I think it also makes the app look more professional when the style is consistent across the whole app."* I think this made it look really good and still does.

* *"Added search function With this you'll be able to search lines or stops based on their parameters. The search function will split the queries into sub-queries and lookup every possible result and sort it by relevance."* & *"I decided to add the macron_query because not all users will know how to add a [Macrons](https://en.wikipedia.org/wiki/Macron_(diacritic)) to a vowel in a search query and people should be able to still search. I won't change the database entries to macron less entries because the aesthetics, the English names in Japan are with them so I have the entries with them."* This has made it easier to search entries in the database. Without those looking up Lines or Stops was scrolling the list with all Lines and list with all Stops. This takes way more time than a search functionality.

* *"Added stopnumbers This was added because it would make it easier to order the stops in the lines table. I think this because stopnumbers are of the letter-number format. Thus if it has numbers it could be used to sort the stops array in a line."* This one didn't work out like I wanted it. The stopnumbers actually were the same for different lines for this dataset (Hankyū). So I could not use it to sort the stops in a line row like I wanted. In the end I used a stop_order column to give the right order of stops to a line entry.

* *"I saw this in a tutorial from Harvard's CS50 and thought can't be that hard. This should make it easy to load the data into the database."* & *"Well APEARENTLY I could not get it to work what I told about yesterday... I got the error that the database was not found even though I could use it in the app, I even tried using a new database but that didn't work...So decided to use the same method in the Books Project, since I know that method does work..."* Well this was a rollercoaster, so first I looked at the source code of CS50 lecture 4 about SQLAlchemy and Flask and thought I could use it. But unfortunately I only got `database does not exist` errors. So yeah I used the code from the Books Project which did work.