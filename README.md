# FootballWebsite
Project involving webscraping and flask

ALL INFORMATION SCRAPED FROM FBREF.COM

This is a personal sideproject of mine that scraped data from the top 5 European Leagues (Premier League, La Liga, Serie A, Bundesliga, and Ligue 1) 
during the 2020-2021 league campaign.

Inside the scraping folder, there is the code to utilize beautifulsoup to obtain the proper links and scrape the 5 leagues. This information is formatted into
a pandas dataframe and converted into a db file. 

With this db file, I then created a simple flask application to visualize the data. The website has a home page, links to the separate leagues, links
to the separate teams, and finally links to the separate players. 

You can visit this website at: https://wh-fbstats.herokuapp.com/ and enjoy!

PAGE NAVIGATION
Home Page: 
  Has a top menu bar with the 5 leagues available (Premier League, La Liga, Ligue 1, Bundesliga, Serie A) and a link for terms (like a glossary for terms)
  Below are two tables. One is the top 20 scoreers from the five leagues with links directly to the players. The other is a table of the aggregated top 20 league table (ordered by   points gained).
League Page:
  Every league page has links to All Players, Top Players, Top Prospects. They have the full league table displayed as well ass top goalscorer, top assists, and team statistics. 
All Players Page:
  A page comprising of every player in the league. Table can be sorted, searched, etc.
Top Players & Top Prospects Page:
  Page that shows the top players in every position in the league. If it's top prospects, it shows the most promising players in every position in the league.
Team Page:
  The team page shows the league performance. There also has a team overview table which shows all of the players in the team's squad and various statistics. There is also a list 
  of the top goalscorers and assists. There are also attacking recommendations and defensive recommendations.
Team Graphs Page:
  The graphs page shows various graphs including squad age distribution, minute distribution, start distribution, and shot data comparisions within the league and a team's rivals.
Player Page:
  The player page displays their age, nationality, position, minutes played in the league, and the team the player is on. There are then multiple graphs of shot data, shot and    
  goal creation, defensive output, passing percentages, and passing frequency. All of these stats are compared against players of his position in the league and players in his 
  position in top teams to give a good comparison. If the player is a goalkeeper, there are bar graphs on passing type distribution, post-shot expected goals, and other 
  miscellaneous goalkeeping actions.
  
