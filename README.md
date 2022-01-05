# FootballWebsite
Project involving webscraping and flask

Link: https://wh-fbstats.herokuapp.com/

ALL INFORMATION SCRAPED FROM FBREF.COM

Inspired by playing a whole lot of Football Manager and being way too invested in the game, I wanted to 
make something related to the real life footballing world as a fun passion project.
At first I wanted to simply play around with the data tables from fbref and find interesting stats. 
I wrote a script to obtain information on Europe's top five leagues but had no proper way of displaying the tables.
As a result, I decided to make a website (and learn how to do that) alongside the fbref information.
Originally the website was very simple and merely displayed tables of the information. Gradually over time, 
I began implementing separate tabs and other charts for the information. I created a system to rank a team's weaknesses and 
strengths which then recommended players to sign accordingly. Additionally, I played around with the Twitter developer API to 
obtain transfer rumors pertaining to specific players and teams. This in turn made me create a user feature 
so people could follow various players and teams and get twitter rumors.

The website mainly uses the data from the sql tables in the database but certain pages utilized additional 
logic. The team recommender for example, first analyzed a team's strengths and weaknesses by comparing their
various offensive and defensive stats in relation to teams near them in the league and all the teams as a whole.
This ranking resulted in a prioritization method which then chose the type of player a team should sign. If a team 
has a strong defense, it would recommend to sign prospective young talent as the team wouldn't need a 
top tier player to be immediately slotted into the team. All recommendations prefer to sign younger talents.

To obtain the data I used BeautifulSoup and pandas. I accessed the data from fbref and converted the information into 
panda dataframes. With these, I created additional columns from the various information before converting these dataframes into 
sql tables and putting it onto a database which my website obtains its information from.
I chose to use Flask as I was already familiar with python and its use of jinja templating was easy to use. This website uses the bootstrap framework
as it allows me to create responsive and clean websites with relative ease. The charts are used with chartJS as 
the templates were easy to understand and had a lot of features already built into the website.

In the future I want to obtain information from the 2021-2022 season and make the website update weekly with new information. 
An improved recommender for players such as midfielders and defenders is also something I want to work on later down the line.
         
Overall, through this website I was able to get a good taste of web development and web design. I feel a lot more confident in my HTML, CSS, and Javascript
capabilities and thoroughly enjoyed working on this project.
  
