# FootballWebsite
Project involving webscraping and flask

ALL INFORMATION SCRAPED FROM FBREF.COM

This is a personal sideproject of mine that scraped data from the top 5 European Leagues (Premier League, La Liga, Serie A, Bundesliga, and Ligue 1) 
during the 2020-2021 league campaign.

Inside the scraping folder, there is the code to utilize beautifulsoup to obtain the proper links and scrape the 5 leagues. This information is formatted into
a pandas dataframe and converted into a db file. 

With this db file, I then created a simple flask application to visualize the data. The website has a home page, links to the separate leagues, links
to the separate teams, and finally links to the separate players. 
