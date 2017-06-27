
# coding: utf-8

# # The Task at Hand:  Getting Airline Data In Order

# (CC) Creative Commons BY-SA Lynd Bacon & Associates, Ltd. DBA Loma Buena Associates

# ## Your Data

# The data you'll use for this assignment are from [OpenFlights.org](http://www.openflights.org).

# You are provided with three data files, one for airports, one for routes, and one for airlines.  The data are for up to January 2012.  You'll be using this data for a couple of upcoming tasks, so be sure to keep track of them and to save your work with them.

# The data in the file **airports.dat** look like this. Here are the first four (4) records in this file:
# 
# 1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby" <br/>
# 2,"Madang","Madang","Papua New Guinea","MAG","AYMD",-5.207083,145.7887,20,10,"U","Pacific/Port_Moresby"<br />
# 3,"Mount Hagen","Mount Hagen","Papua New Guinea","HGU","AYMH",-5.826789,144.295861,5388,10,"U","Pacific/Port_Moresby" <br />
# 4,"Nadzab","Nadzab","Papua New Guinea","LAE","AYNZ",-6.569828,146.726242,239,10,"U","Pacific/Port_Moresby" <br />

# What you have here is a character (comma in this case) separated value file.
# 
# Here are the fields in this file, according to OpenFlights.org:
# 
# * Airport ID : Unique OpenFlights identifier for this airport. 
# * Name : Name of airport. May or may not contain the City name.
# * City : Main city served by airport. May be spelled differently from Name.
# * Country : Country or territory where airport is located.
# * IATA/FAA : 3-letter FAA code, for airports located in Country "United States of America". 3-letter IATA code, for all other airports. Blank if not assigned.
# * ICAO : 4-letter ICAO code. Blank if not assigned.
# * Latitude : Decimal degrees, usually to six significant digits. Negative is South, positive is North.
# * Longitude : Decimal degrees, usually to six significant digits. Negative is West, positive is East.
# * Altitude : In feet.
# * Timezone : Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.
# * DST : Daylight savings time. One of E (Europe), A (US/Canada), S (South America), O (Australia), Z (New Zealand), N (None) or U (Unknown).
# * Tz : database time zoneTimezone in "tz" (Olson) format, eg. "America/Los_Angeles". 
# 
# 
# 
# 
# 
# 

# OpenFlights says:
#     
# The data is ISO 8859-1 (Latin-1) encoded, with no special characters.
# 
# Note: Rules for daylight savings time change from year to year and from country to country. The current data is an approximation for 2009, built on a country level. Most airports in DST-less regions in countries that generally observe DST (eg. AL, HI in the USA, NT, QL in Australia, parts of Canada) are marked incorrectly."

# The other two files, **routes.dat** and **airlines.dat**, are similar to **airports.dat**.  The fields in **airlines.dat** are:
# 
# * Airline ID : Unique OpenFlights identifier for this airline. 
# * Name : Name of the airline. 
# * Alias : Alias of the airline. For example, All Nippon Airways is commonly known as "ANA". 
# * IATA : 2-letter IATA code, if available.
# * ICAO : 3-letter ICAO code, if available.
# * Callsign : Airline callsign.
# * Country : Country or territory where airline is incorporated.
# * Active : "Y" if the airline is or has until recently been operational, "N" if it is defunct. This field is not reliable: in particular, major airlines that stopped flying long ago, but have not had their IATA code reassigned (eg. Ansett/AN), will incorrectly show as "Y".
# 

# Additional information about the **airlines.dat** data from OpenFlights:
#     
# The data is ISO 8859-1 (Latin-1) encoded. The special value \N is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.
# Notes: Airlines with null codes/callsigns/countries generally represent user-added airlines. Since the data is intended primarily for current flights, defunct IATA codes are generally not included. For example, "Sabena" is not listed with a SN IATA code, since "SN" is presently used by its successor Brussels Airlines.

# **routes.dat** has the following data fields:
# 
# * Airline : 2-letter (IATA) or 3-letter (ICAO) code of the airline. 
# * Airline ID : Unique OpenFlights identifier for airline (see Airline). 
# * Source airport : 3-letter (IATA) or 4-letter (ICAO) code of the source airport.
# * Source airport ID : Unique OpenFlights identifier for source airport (see Airport) 
# * Destination airport : 3-letter (IATA) or 4-letter (ICAO) code of the destination airport.
# * Destination airport ID : Unique OpenFlights identifier for destination airport (see Airport) 
# * Codeshare : "Y" if this flight is a codeshare (that is, not operated by Airline, but another carrier), empty otherwise.
# * Stops : Number of stops on this flight ("0" for direct)
# * Equipment : 3-letter codes for plane type(s) generally used on this flight, separated by spaces
# 

# Here's some additional information about **routes.dat**:
# 
# The data is ISO 8859-1 (Latin-1) encoded. The special value \N is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.  (Note: the \N is how missings were coded. It's not be taken as the _newline_ character.)
# 
# Notes: 
# * Routes are directional: if an airline operates services from A to B and from B to A, both A-B and B-A are listed separately. 
# * Routes where one carrier operates both its own and codeshare flights are listed only once. 
# 

# ## What You Need to Do

# Here's what you need to do for this exercise.  You'll use Python do to it. You can use the Enthought Canopy distribution, or some other version of Python, like the Continuum Anaconda scientific Python distribution.    For each of the following, provide syntactically correct and commented code, followed by the results that your code produced for what is requested.  Your commenting should explain what your code does.  Use Python conventions for including your comments with your code.
# 
# Here's a style guide for Python code that you might find useful:
# 
# [PEP 8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
# 
# Submit your assignment in a pdf file of three or four pages, _but in no more than six (6) pages_. 
# 
# #### 1. Read each data file into a Pandas DataFrame.  Add meaningful names (i.e., names that would make sense to other people, given the data) to the columns of each DataFrame.
#     
# * Provide your syntactically correct, commented code.
# * Print the first three rows of each DataFrame.  Provide your code, and the results it produced. 
#     
# #### 2. Check each DataFrame for duplicate records.  For each, report the number of duplicates you found.
#     
# * Provide your commented, syntactically correct code and the results it produced.  
#     
# #### 3. Describe the data types of the columns in each of the DataFrames.
#     
# * Provide your commented, syntactically correct code and the results it produced.  
#         
# #### 4. Determine how many of the airlines are "defunct." 
#     
# * Provide your definition of what a defunct airline is.
# * Provide your commented, syntactically correct code and the results it produced.  
#     
# 
# #### 5. Determine how many "routes from nowhere" there are in the data.  These are flights that don't originate from an airport.
#     
# * Provide your commented, syntactically correct code and the results it produced.  
#         
# #### 6. Save your DataFrames for future use.  You may pickle them, put them in a shelve db, on in a the tables of a SQL db.  Check to make sure that they are saved correctly.
#     
#  * Provide your commented, syntactically correct code and the results it produced.

# ## Tips and Hints

# Before you can use pandas you may need may to install it, if you haven't already done so.  You should be able to find it in Canopy and in Anaconda.
# 
# You might find the documentation at (http://pandas.pydata.org) useful in addition to what has already been made available.
# 
# Pickling is a basic and venerable Python "serializing" method. Pickling and unpickling are methods of converting Python objects in RAM to and from character streams so that they can persist.  Pickle files can be text files or binary files.  Here's a nice piece about pickling:
# 
# (http://python.about.com/od/pythonstandardlibrary/a/pickle_intro.htm)
# 
# You can find a notebook about the __shelve__ package on Canvas. It should be in the _Resources_ section of the course home page.

# In[1]:

#setup imports
import pandas as pd
import numpy as np
import urllib2


# In[2]:

### Micro assignment
def read_col_names(path):
    """A function that takes in a file path, reads the file and returns a list of the items in the file.
    Assumes that files are constructed with a single line of data as the first line that contains the space delimited 
    list."""
    # open the file
    f = open(path)
    # get the list object from the file. Assumes only one list in the first row delimited by spaces
    col_names = f.read().split()
    # close the file
    f.close()
    #return the list
    return col_names

#get the column names from the config text files
airport_col_names = read_col_names("config/airport-col-names.txt")
airline_col_names = read_col_names("config/airline-col-names.txt")
routes_col_names = read_col_names("config/route-col-names.txt")


# Using Entought Canopy version 1.6.2 (64 bit) on OS X Yosemite version 10.10.5

# In[3]:

# 1 read files and name appropriately from the micro assignment 

#read in all of the data files using pandas native csv reader and assign the appropriate column names
df_airports = pd.read_csv("config/airports.dat",header=None,names=airport_col_names)
df_routes = pd.read_csv("config/routes.dat",header=None,names=routes_col_names)
df_airlines = pd.read_csv("config/airlines.dat",header=None,names=airline_col_names)


# In[4]:

# 2 check each data frame for duplicate records

# need to get rid of the index columns in df_airport and df_airlines as these indeces prevent us from
# identifying duplicate columns

# get columns and remove the id column in position 1 of the list
airport_clean = df_airports.columns.tolist()
airport_clean.pop(0)
airlines_clean = df_airlines.columns.tolist()
airlines_clean.pop(0)

#print the number of duplicated columns per data frame, removing the id columns
print "%s number of duplicated rows: %d"%('df_airports',sum(df_airports[airport_clean].duplicated()))
print "%s number of duplicated rows: %d"%('df_airlines',sum(df_airlines[airlines_clean].duplicated()))
print "%s number of duplicated rows: %d"%('df_airports',sum(df_routes.duplicated()))

# drop the duplicates from the affected subseted data frames. inplace directly modifies the object
df_airports[airport_clean].drop_duplicates(inplace=True)
df_airlines[airlines_clean].drop_duplicates(inplace=True)


# In[5]:

#convert special null char to pandas null
df_airlines = df_airlines.replace('\N',np.nan)
df_airports = df_airports.replace('\N',np.nan)
df_routes = df_routes.replace('\N',np.nan)


# ### df_airports column types
# * airport_id: A numeric integer column that serves as a unique identifier for each airport
# * name: a char column that stores the name of the airport
# * city: a char column that stores the name of the city the airport resides in
# * country: a char column that stores the name of the country the airport resides in
# * iata/faa: a char column that stores the iata/faa code
# * icao: a char column that stores the icao code
# * latitude: a numeric float column that stores the degrees of latitude
# * longitude: a numeric float column that stores the degrees of longitude
# * altitude: a numeric integer column that stores the measure of altitude
# * timezone: a numeric float that gives the time zone offset from UTC
# * dst: a char column that indicates daylight savings time
# * tz: a char column that indicates the time zone
# 
# ### df_airlines column types
# * airline_id: a numeric integer column that serves as a unique key for each airline
# * name: a char column that stores the name of the airline
# * alias: a char column that stores the alias of the airline
# * iata: a char column that stores the iata code of the airline
# * icao: a char column that stores the icao code of the airline
# * callsign: a char column that stores the callsign of the airline
# * country: a char column that stores the country of the airline
# * active: a char column that flags an airline as active or inactive
# 
# ### df_routes column types
# * airline: a char column that stores the iata or icao of the airline
# * airline_id: a char column the provides a unique identifier for each airline. (will need to be converted to int to be compatible with other columns)
# * source_airport: a char column that stores the source airport a flight originates from
# * source_airport_id: a char column that stores a unique identifier for source airports
# * destination_airport: a char column that stores the destination airport a flight ends at
# * destination_airport_id: a char column that stores a unique identifier for destination airports
# * codeshare: a char column that has "Y" or NaN for codeshare status
# * stops: a numeric integer column that counts the number of stops the flight has
# * equipment: a char column that denotes the 3 letter code for plane types used on flight
# 

# In[6]:

# 3 describe the data types of all the columns
print df_airports.dtypes
print df_airlines.dtypes
print df_routes.dtypes


# In[7]:

# 4 determine how many airlines are defunct

# scrape wikipedia for data frame of defunct airlines
defunct_airline_url = "https://en.wikipedia.org/wiki/List_of_airline_codes"
r = urllib2.urlopen(defunct_airline_url).read()

# pandas read_html returns a list of data frames, did some scraping with beautiful soup to 
# determine the correct class that identifies the table of airline codes then map it to a data frame
defunct_airlines=pd.read_html(r,attrs={'class':"wikitable sortable"},header=0)[0]

# parse the Comment column for a boolean identifier of defunctness
defunct_airlines['defunct'] = defunct_airlines.Comments.apply(lambda x: 1 if type(x) == str and "defunct" in x.lower() else 0)

#return a list of defunct airlines identify by ICAO
def_airlines = defunct_airlines[(defunct_airlines.defunct==1)&(defunct_airlines.ICAO.notnull())]['ICAO'].tolist()


# In[8]:

# defining defunct airlines as active=='N' and nan icao value and icao membership in def_airlines

# add an identifier for defunct airline membership
df_airlines['defunct_list_membership'] = df_airlines.icao.apply(lambda x: x in def_airlines)

#apply definition of defunct airlines as filter to return only active airlines
df_airlines_no_defunct = df_airlines[(df_airlines.active!='N')&(df_airlines.icao.notnull())                                     &(df_airlines.defunct_list_membership==False)]


# In[9]:

# 5 determine how many routes from nowhere there are 

# route from nowhere defined as either a null source airport code or source airport is not 
# contained in the airport_codes.txt file.

# read in the airport_codes.txt file
df_airport_codes = pd.read_csv("config/airports_codes.txt",delim_whitespace=True,header=0)

# compare the source airport to this file
df_routes_ap_codes = pd.merge(df_routes,df_airport_codes,how='left'                              ,left_on='source_airport',right_on="AirportCode",indicator=True)

# ones that do not get matched or have a null source_airport_id are routes from nowhere
num_routes_nowhere = df_routes_ap_codes[(df_routes_ap_codes._merge=='left_only')|                                        (df_routes_ap_codes.source_airport_id.isnull())].source_airport_id                                        .value_counts(dropna=False).sum()
print "Number of routes originating from nowhere: %d" %(num_routes_nowhere)

#filter out the routes that came from no where
df_routes_filtered = df_routes_ap_codes[(df_routes_ap_codes._merge=='both')&(df_routes_ap_codes.source_airport_id.notnull())]
#remove unnecessary columns
df_routes_filtered = df_routes_filtered[df_routes.columns]


# In[10]:

# 6 pickle the data frames df_routes_filtered, df_airports, and df_airlines_no_defunct
df_routes_filtered.to_pickle("config/df_routes.pkl")
df_airports.to_pickle("config/df_airports.pkl")
df_airlines_no_defunct.to_pickle("config/df_airlines.pkl")


# In[ ]:



