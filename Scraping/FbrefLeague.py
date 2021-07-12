import requests
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import FbrefTeam as FbT

class FbrefLeague:
    baseLink = "https://fbref.com"

    def __init__(self, link):
        self.link = link
        leagueStr = self.link.rsplit('/', 1)[-1].split('-')
        self.leagueName = ' '.join(leagueStr[0:len(leagueStr) - 1])
        #print(self.link)
        #print(self.leagueName)
        #self.teams LIST OF ALL FBREFTEAM CLASSES EXIST
        self.scrape_league_site()
        self.makeLeagueTableDF()
        self.makeSquadStatsTable()

    #method opens the link and obtains a table of all the tables so future methods can be added to scrape the other tables
    # later down the line
    def scrape_league_site(self):
        source = urllib.request.urlopen(self.link)
        soup = BeautifulSoup(source, "lxml")
        #print(soup)
        tables = soup.find_all("table")
        self.tables = tables

    def makeLeagueTableDF(self):
        league_teams = []
        table = self.tables[0]

        #initializes all teams within the league
        leftTD = table.find("tbody").find_all('td', class_ ="left")#.find_all("a", href=True)
        linkLst = []
        for i in range(0,len(leftTD), 2):
            #print(leftTD[i])
            linkLst.append(leftTD[i])

        #make the list of teams
        for i in range(len(linkLst)):
            x = linkLst[i].find("a", href=True)
            #print(x['href'])
            league_teams.append(FbT.FbrefTeam(FbrefLeague.baseLink + x['href'], i+1, self.leagueName))

        self.teams = league_teams

        #obtain information from the league table and put into pd
        tableData = [] #holds all the row data
        rows = table.find("tbody").find_all("tr")
        for x in range(len(rows)):
            rowData = []
            rowData.append(self.teams[x].getTeamName())
            tds = rows[x].find_all("td", class_="right")
            for i in range(len(tds)):
                val = tds[i].get_text()
                if i in range(0,6) or i==7:
                    rowData.append(int(val))
                elif i in range(8, 10):
                    rowData.append(float(val))
                else:
                    continue
            self.teams[x].insertLeagueData(rowData)
            tableData.append(rowData)

        #print(tableData)


        #use data acquired to create the league pd
        pd_cols = ["Team", "MP", "W", "D", "L", "GF", "GA", "Pts", "xG", "xGA"]
        league_table_DF = pd.DataFrame(tableData, columns=pd_cols)
        gdSeries = league_table_DF["GF"] - league_table_DF["GA"]
        xgdSeries = league_table_DF["xG"] - league_table_DF["xGA"]
        league_table_DF = league_table_DF.assign(GD = gdSeries)
        league_table_DF = league_table_DF.assign(xGD = xgdSeries)
        xgdp90 = league_table_DF["xGD"] / league_table_DF["MP"]
        league_table_DF = league_table_DF.assign(xGDP90 = xgdp90)

        league_col = [self.leagueName for i in range(league_table_DF.shape[0])]
        league_table_DF = league_table_DF.assign(league=league_col)
        #print(league_table_DF)
        self.league_table = league_table_DF

    def makeSquadStatsTable(self):
        table = self.tables[2]
        tbody = table.find("tbody")
        teamOrder = self.league_table.sort_values(by="Team").reset_index(drop=True)["Team"].to_list() #Team names in alphabetical order
        #print(len(teamOrder))
        rows = tbody.find_all("tr")
        #print(rows)
        pd_table_list = []
        for x in range(len(rows)):
            rowData = []
            rowData.append(teamOrder[x])
            tds = rows[x].find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()

                if i in [0, 3, 7, 8, 9, 10, 11, 12, 13]:
                    rowData.append(int(val))
                elif i in [1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
                    rowData.append(float(val))
                else:
                    continue

            #print(x)
            tName = teamOrder[x]
            team = self.findTeam(tName)
            team.insertSquadData(rowData)
            pd_table_list.append(rowData)

        #print(pd_table_list)
        col_names = ["Team", "PlayersUsed", "Age", "Possession", "MP", "Gls", "Ast", "nPG", "PG", "PGAtt", "YCrd",
                     "RCrd", "GlsP90", "AstP90", "GaAP90", "nPGP90", "nPGaAP90", "xG", "npxG", "xA", "npxGaA",
                     "xGP90", "xAP90", "xGaAP90", "npxGP90", "npxGaAP90"]

        squadStatsPD = pd.DataFrame(pd_table_list, columns=col_names)
        league_col = [self.leagueName for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(league = league_col)
        #print(squadStatsPD)
        self.squadStatsDF = squadStatsPD

    def getLeagueTable(self):
        return self.league_table

    def getSquadStatsTable(self):
        return self.squadStatsDF

    def findTeam(self, teamName):
        for team in self.teams:
            if team.getTeamName() == teamName:
                return team

        print("Shouldn't be here")



# test = FbrefLeague("https://fbref.com/en/comps/9/Premier-League-Stats")
# #test.makeSquadStatsTable()
# print("###############################################")
# print("Creating teamDF's")
# testTeam = test.teams[16]
# playerOffensiveDFLst = []
# playerDefensiveDFLst = []
# for team in test.teams:
#     playerOffensiveDFLst.append(team.getOffensiveStats())
#     playerDefensiveDFLst.append(team.getDefensiveStats())
# attackingPlayers = pd.concat(playerOffensiveDFLst).reset_index(drop=True)
# defensivePlayers = pd.concat(playerDefensiveDFLst).reset_index(drop=True)
# #print(attackingPlayers)
# nonTeamAttack = attackingPlayers[attackingPlayers.get("team").str.contains(testTeam.getTeamName()) == False]
# nonTeamDefense = defensivePlayers[attackingPlayers.get("team").str.contains(testTeam.getTeamName()) == False]
#
# #print(nonChels)
# print("######################################################################")
# print(testTeam.getTeamName())
# testTeam.analyzeTeam()
# print(testTeam.xGA_diff)
# testTeam.generatePotentialSignings(nonTeamAttack, nonTeamDefense)
