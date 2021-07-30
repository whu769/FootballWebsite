import requests
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import FbrefTeam as FbT
import time
import random

class FbrefLeague:
    baseLink = "https://fbref.com"

    def __init__(self, link, year):
        self.link = link

        leagueStr = self.link.rsplit('/', 1)[-1].split('-')
        if(len(leagueStr) > 3):
            self.leagueName = ' '.join(leagueStr[2:len(leagueStr) - 1])
        else:
            self.leagueName = ' '.join(leagueStr[0:len(leagueStr) - 1])
        #print(self.leagueName)
        self.season = year
        #print(self.link)
        #print(self.leagueName)
        #self.teams LIST OF ALL FBREFTEAM CLASSES EXIST

        self.scrape_league_site()
        #print(self.tables)
        self.makeLeagueTableDF()
        self.makeSquadStatsTable()
        self.makeSquadGSCTable()
        self.makeSquadShootingTable()
        self.makeSquadPassingTable()
        self.makeSquadDefenseTable()

        #print(self.leagueName)

    #method opens the link and obtains a table of all the tables so future methods can be added to scrape the other tables
    # later down the line
    def scrape_league_site(self):
        source = urllib.request.urlopen(self.link)
        soup = BeautifulSoup(source, "lxml")
        #print(soup)
        tables = soup.find_all("table")
        self.tables = tables
        #print(self.tables)

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
            league_teams.append(FbT.FbrefTeam(FbrefLeague.baseLink + x['href'], i+1, self.leagueName, self.season))

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

        season_col = [self.season for i in range(league_table_DF.shape[0])]
        league_table_DF = league_table_DF.assign(season=season_col)
        #print(league_table_DF)
        
        
        #make a dict w/ teamname as keys and the tier as values, implement into all of the other tables
        tier_dict = dict()
        for i in range(len(self.teams)):
            if i in range(0,4):
                tier_dict[self.teams[i].getTeamName()] = 1
            elif i in range(4, 8):
                tier_dict[self.teams[i].getTeamName()] = 2
            elif i in range(8, 14):
                tier_dict[self.teams[i].getTeamName()] = 3
            else:
                tier_dict[self.teams[i].getTeamName()] = 4
        
        self.tier_dict = tier_dict
        
        #print(list(tier_dict.values()))
        tier_col = list(tier_dict.values())
        league_table_DF = league_table_DF.assign(tier = tier_col)
        self.league_table = league_table_DF
        # for team in self.teams:
        #     print(team.getTeamName())

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

        season_col = [self.season for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(season=season_col)

        # print(squadStatsPD["Team"].to_list())
        tier_col = []
        for team in squadStatsPD["Team"].to_list():
            tier_col.append(self.tier_dict[team])
        
        squadStatsPD = squadStatsPD.assign(tier = tier_col)
        #print(tier_col)
        #print(squadStatsPD)
        self.squadStatsDF = squadStatsPD

    def makeSquadGSCTable(self):
        table = self.tables[14]
        #print(table)
        tbody = table.find("tbody")
        teamOrder = self.league_table.sort_values(by="Team").reset_index(drop=True)[
            "Team"].to_list()  # Team names in alphabetical order
        #print(teamOrder)
        # print(len(teamOrder))
        rows = tbody.find_all("tr")
        pd_table_list = []
        for x in range(len(rows)):
            rowData = []
            rowData.append(teamOrder[x])
            tds = rows[x].find_all("td")
            # print(tds)
            for i in range(len(tds)):
                val = tds[i].get_text()
                #print(val)
                if i in [0, 2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17]:
                    rowData.append(int(val))
                elif i in [1, 3, 11]:
                    rowData.append(float(val))
                else:
                    continue

            # print(x)
            tName = teamOrder[x]
            team = self.findTeam(tName)
            team.insertSquadData(rowData)
            pd_table_list.append(rowData)

        col_names = ["Team", "PlayersUsed", "Nineties", "SCA", "SCA90", "SCAPL", "SCAPD", "SCADrib", "SCASh", "SCAFld"
            , "SCADef", "GCA", "GCA90", "GCAPL", "GCAPD", "GCADrib", "GCASh", "GCAFld", "GCADef"]

        squadStatsPD = pd.DataFrame(pd_table_list, columns=col_names)

        league_col = [self.leagueName for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(league=league_col)

        season_col = [self.season for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(season=season_col)
        #print(squadStatsPD)

        tier_col = []
        for team in squadStatsPD["Team"].to_list():
            tier_col.append(self.tier_dict[team])
        
        squadStatsPD = squadStatsPD.assign(tier = tier_col)

        self.squadGSCDF = squadStatsPD

    def makeSquadShootingTable(self):
        table = self.tables[8]
        # print(table)
        tbody = table.find("tbody")
        teamOrder = self.league_table.sort_values(by="Team").reset_index(drop=True)[
            "Team"].to_list()  # Team names in alphabetical order
        # print(teamOrder)
        # print(len(teamOrder))
        rows = tbody.find_all("tr")
        pd_table_list = []
        for x in range(len(rows)):
            rowData = []
            rowData.append(teamOrder[x])
            tds = rows[x].find_all("td")
            # print(tds)
            for i in range(len(tds)):
                val = tds[i].get_text()
                # print(val)
                if i in [0,2,3,4,11,12,13]:
                    rowData.append(int(val))
                elif i in [1,5,6,7,8,9,10, 14, 15, 16, 17,18]:
                    rowData.append(float(val))
                else:
                    continue

            # print(x)
            tName = teamOrder[x]
            team = self.findTeam(tName)
            team.insertSquadData(rowData)
            pd_table_list.append(rowData)

        col_names = ["Team", "PlayersUsed", "Nineties", "Gls", "Sh", "SoT", "SoTP", "SoTP90", "SoTP90", "GPSh", "GPSoT",
                     'Dist', 'FK', 'PKMade', 'PKAtt','xG', 'npxG', 'npxGPSh', 'xG_diff', 'npxG_diff']

        squadStatsPD = pd.DataFrame(pd_table_list, columns=col_names)

        league_col = [self.leagueName for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(league=league_col)

        season_col = [self.season for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(season=season_col)
        # print(squadStatsPD)

        tier_col = []
        for team in squadStatsPD["Team"].to_list():
            tier_col.append(self.tier_dict[team])
        
        squadStatsPD = squadStatsPD.assign(tier = tier_col)

        self.squadShootingDF = squadStatsPD

    def makeSquadPassingTable(self):
        table = self.tables[10]
        #print(table)
        tbody = table.find("tbody")
        teamOrder = self.league_table.sort_values(by="Team").reset_index(drop=True)[
            "Team"].to_list()  # Team names in alphabetical order
        # print(teamOrder)
        # print(len(teamOrder))
        rows = tbody.find_all("tr")
        pd_table_list = []
        for x in range(len(rows)):
            rowData = []
            rowData.append(teamOrder[x])
            tds = rows[x].find_all("td")
            # print(tds)
            for i in range(len(tds)):
                val = tds[i].get_text()
                # print(val)
                if i in [0,2,3,5,6,7,8,10,11,13, 14, 16,19,20,21,22,23]:
                    rowData.append(int(val))
                elif i in [1,4,9,12,15,17,18]:
                    rowData.append(float(val))
                else:
                    continue

            # print(x)
            tName = teamOrder[x]
            team = self.findTeam(tName)
            team.insertSquadData(rowData)
            pd_table_list.append(rowData)

        col_names = ["Team", "PlayersUsed", "Nineties", "CmpPasses", "AttPasses", "CmpP", "TotDist", "PrgDist", "ShortCmp",
                     "ShortAtt", "ShortCmpP", "MedCmp", "MedAtt", "MedCmpP", "LongCmp", "LongAtt", "LongCmpP",
                     "Ast", "xA", "xA_diff", "KP", "FinalThird", "PPA", "CrsPA", "Prog"]

        squadStatsPD = pd.DataFrame(pd_table_list, columns=col_names)
        #print(squadStatsPD)

        passP = squadStatsPD["CmpPasses"] / squadStatsPD["AttPasses"]
        KPP90 = squadStatsPD["KP"] / squadStatsPD["Nineties"]
        FTP90 = squadStatsPD["FinalThird"] / squadStatsPD["Nineties"]
        PPAP90 = squadStatsPD["PPA"] / squadStatsPD["Nineties"]
        CrsPAP90 = squadStatsPD["CrsPA"] / squadStatsPD["Nineties"]
        ProgP90 = squadStatsPD["Prog"] / squadStatsPD["Nineties"]
        squadStatsPD = squadStatsPD.assign(passP = passP)
        squadStatsPD = squadStatsPD.assign(KPP90 = KPP90)
        squadStatsPD = squadStatsPD.assign(FTP90 = FTP90)
        squadStatsPD = squadStatsPD.assign(PPAP90 = PPAP90)
        squadStatsPD = squadStatsPD.assign(CrsPAP90 = CrsPAP90)
        squadStatsPD = squadStatsPD.assign(ProgP90 = ProgP90)



        league_col = [self.leagueName for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(league=league_col)

        season_col = [self.season for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(season=season_col)
        #print(squadStatsPD)

        tier_col = []
        for team in squadStatsPD["Team"].to_list():
            tier_col.append(self.tier_dict[team])
        
        squadStatsPD = squadStatsPD.assign(tier = tier_col)


        self.squadPassingDF = squadStatsPD

    def makeSquadDefenseTable(self):
        table = self.tables[16]
        #print(table)
        tbody = table.find("tbody")
        teamOrder = self.league_table.sort_values(by="Team").reset_index(drop=True)[
            "Team"].to_list()  # Team names in alphabetical order
        # print(teamOrder)
        # print(len(teamOrder))
        rows = tbody.find_all("tr")
        pd_table_list = []
        for x in range(len(rows)):
            rowData = []
            rowData.append(teamOrder[x])
            tds = rows[x].find_all("td")
            # print(tds)
            for i in range(len(tds)):
                val = tds[i].get_text()
                # print(val)
                if i in [0,2,3,4,5,6,7,8,10,11,12,14,15,16,17,18,19,20,21,22,23,24]:
                    rowData.append(int(val))
                elif i in [1,9,13]:
                    rowData.append(float(val))
                else:
                    continue
            
            # print(x)
            tName = teamOrder[x]
            team = self.findTeam(tName)
            team.insertSquadData(rowData)
            pd_table_list.append(rowData)
        
        col_names = ["Team", "PlayersUsed", "Nineties", "TklTot", "TklW", "TklD3", "TklM3", "TklA3", "TklDribTot",
                     "TklDribAtt", "TklDribP", "TklDribFail", "PressTot", "PressSucc", "PressP", "PressD3", "PressM3",
                     "PressA3", "BlkTot", "BlkSh", "BlkShSv", "BlkPass", "Int", "IntTkl", "Clr", "Err"]
        squadStatsPD = pd.DataFrame(pd_table_list, columns=col_names)
        

        TklTotalP = squadStatsPD["TklW"] / squadStatsPD["TklTot"]
        PressD3P = squadStatsPD["PressD3"] / squadStatsPD["PressTot"]
        PressM3P = squadStatsPD["PressM3"] / squadStatsPD["PressTot"]
        PressA3P = squadStatsPD["PressA3"] / squadStatsPD["PressTot"]
        ErrP90 = squadStatsPD["Err"] / squadStatsPD["Nineties"]
        squadStatsPD = squadStatsPD.assign(TklTotalP = TklTotalP)
        squadStatsPD = squadStatsPD.assign(PressD3P = PressD3P)
        squadStatsPD = squadStatsPD.assign(PressM3P = PressM3P)
        squadStatsPD = squadStatsPD.assign(PressA3P = PressA3P)
        squadStatsPD = squadStatsPD.assign(ErrP90 = ErrP90)

        league_col = [self.leagueName for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(league=league_col)

        season_col = [self.season for i in range(squadStatsPD.shape[0])]
        squadStatsPD = squadStatsPD.assign(season=season_col)

        tier_col = []
        for team in squadStatsPD["Team"].to_list():
            tier_col.append(self.tier_dict[team])
        
        squadStatsPD = squadStatsPD.assign(tier = tier_col)

        #print(squadStatsPD)
        self.squadDefenseDF = squadStatsPD

    #Getter methods
    def getLeagueTable(self):
        return self.league_table

    def getSquadStatsTable(self):
        return self.squadStatsDF

    def getSquadGSCTable(self):
        return self.squadGSCDF

    def getSquadShootingTable(self):
        return self.squadShootingDF

    def getSquadPassingTable(self):
        return self.squadPassingDF
    
    def getSquadDefenseTable(self):
        return self.squadDefenseDF

    def findTeam(self, teamName):
        for team in self.teams:
            if team.getTeamName() == teamName:
                return team

        print("Shouldn't be here")



# test = FbrefLeague("https://fbref.com/en/comps/9/Premier-League-Stats", "2020-2021")
# test.makeSquadDefenseTable()
# test.makeSquadPassingTable()
# test.makeSquadShootingTable()
# test.makeSquadGSCTable()
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
