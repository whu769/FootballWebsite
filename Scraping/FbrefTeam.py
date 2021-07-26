import requests
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import time
import random


class FbrefTeam:
    tier1 = [1, 2, 3, 4]
    tier2 = [5, 6, 7, 8]
    tier3 = [9, 10, 11, 12, 13, 14]
    tier4 = [15, 16, 17, 18, 19, 20]
    tiers = [tier1, tier2, tier3, tier4]

    def __init__(self, link, position, leagueName, season):
        self.link = link
        #(self.link)
        nameStr = self.link.rsplit('/', 1)[-1].split('-')
        self.team = ' '.join(nameStr[0:len(nameStr) - 1])
        self.leagueName = leagueName
        #print(self.leagueName)
        self.season = season

        #fix the links
        # newlink = self.link.rsplit('/', 1)
        # nLP1 = newlink[0]
        # nLP2 = newlink[1]
        # self.link = (nLP1 + f'/{self.season}/'+nLP2)
        # print(self.link)
        #tier bit
        self.position = position
        for i in range(len(FbrefTeam.tiers)):
            tier = FbrefTeam.tiers[i]
            if self.position in tier:
                self.tier = (i+1)

        print(self.team)
        #print("Scraping")
        self.scrape_site()

        self.makeStandardTable()
        self.makeDefensiveTable()
        self.makeOffensiveTable()
        self.makePassingTable()
        self.makeGKTable()
        self.makeGSCreationTable()
        self.makePossessionTable()


        self.leagueData = []
        self.squadData = []


    def scrape_site(self):
        # time.sleep(random.randint(5, 10))
        source = urllib.request.urlopen(self.link)
        soup = BeautifulSoup(source, "lxml")
        # print(soup)
        tables = soup.find_all("table")
        # if(self.getTeamName() == "Wolfsburg"):
        #     #print(soup)
        #     print(tables)
        self.tables = tables

    def getTeamName(self):
        return self.team

    def makeStandardTable(self):
        table = self.tables[0]
        #print(table)
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            tds = row.find_all("td")
            #print(len(tds))
            for i in range(len(tds)):
                val = tds[i].get_text()
                #print(val)
                if val == "":
                    val = "0"

                if i in [0, 1]:
                    # if(i == 0):
                    #     val = val.split(" ")[1]
                    playerStats.append(val)
                elif i in [2, 3, 4, 7, 8, 9, 10, 11, 12, 13]:
                    playerStats.append(int(val))
                elif i in range(14, 28) or i == 6:
                    playerStats.append(float(val))
            teamStats.append(playerStats)
        #print(teamStats[0])
        col_names = ["Name", "Country", "Position", "Age", "MP", "Starts", "Nineties", "Gls", "Ast", "nPG","PG", "PGAtt",
                     "YCrd", "RCrd", "GlsP90", "AstP90", "GaAP90", "nPGP90", "npGaAP90", "xG", "npxG", "xA", "npxGaA",
                     "xGP90", "xAP90", "xGaAP90", "npxGP90", "npxGaAP90"]
        pd_table = pd.DataFrame(teamStats, columns=col_names)
        #print(pd_table)
        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team = team_col)
        pd_table = pd_table.assign(tier = tier_col)
        pd_table = pd_table.assign(minutes = minutes_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season = season_col)

        #print(pd_table)
        self.standardTable = pd_table


    def makeDefensiveTable(self):
        defensiveTable = self.tables[8] #index 8 is the defensive action
        #print(defensiveTable)
        defenseRows = defensiveTable.find("tbody").find_all("tr")
        #print(defenseRows[0])
        teamStats = []
        for row in defenseRows:
            playerStats = []
            name = row.find('a').find_all(text=True)[0]
            playerStats.append(name)
            #print(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                #print(tds[i].get_text())

                val = tds[i].get_text()
                if(val == ""):
                    #print(name)
                    #print(tds[i])
                    val = "0"

                if(i in [0, 1]):
                    # if(i==0):
                    #     val = val.split(" ")[1]
                    playerStats.append(val)
                elif(i in [3, 11, 15]):
                    playerStats.append(float(val))
                elif(i == len(tds) - 1):
                    pass
                else:
                    playerStats.append(int(val))
            teamStats.append(playerStats)
            #print(playerStats)
            #print("#################################################################################")
        #print(teamStats)
        cols = ["Name", "Nation", "Position", "Age", "Nineties", "Tkl", "TklW", "Def3rd", "Mid3rd", "Att3rd",
                   "TklDribble", "TklAttDribble", "TklPctDribble", "Past", "Pressures", "PressureSuccess",
                   "PressurePct", "PDef3rd", "PMid3rd", "PAtt3rd", "Blocks", "ShotBlk", "ShSv", "BlkPass",
                   "Int", "TklPlusInt", "Clr", "Err"]
        teamDefenseDF = pd.DataFrame(teamStats, columns = cols)
        #print(teamDefenseDF)
        TklIntP90 = teamDefenseDF["TklPlusInt"] / teamDefenseDF["Nineties"]
        TklRate = teamDefenseDF["TklW"] / teamDefenseDF["Tkl"]
        BlkP90 = teamDefenseDF["Blocks"] / teamDefenseDF["Nineties"]
        ClrP90 = teamDefenseDF["Clr"] / teamDefenseDF["Nineties"]
        minutes = teamDefenseDF["Nineties"] * 90
        TeamCol = [self.team for i in range(teamDefenseDF.shape[0])]
        teamDefenseDF = teamDefenseDF.assign(TklIntP90 = TklIntP90)
        teamDefenseDF = teamDefenseDF.assign(TklRate=TklRate)
        teamDefenseDF = teamDefenseDF.assign(BlkP90=BlkP90)
        teamDefenseDF = teamDefenseDF.assign(ClrP90=ClrP90)
        teamDefenseDF = teamDefenseDF.assign(team = TeamCol)
        teamDefenseDF = teamDefenseDF.assign(minutes = minutes)

        tier_series = [self.tier for i in range(teamDefenseDF.shape[0])]
        teamDefenseDF = teamDefenseDF.assign(tier = tier_series)
        league_col = [self.leagueName for i in range(teamDefenseDF.shape[0])]
        teamDefenseDF = teamDefenseDF.assign(league=league_col)

        season_col = [self.season for i in range(teamDefenseDF.shape[0])]
        teamDefenseDF = teamDefenseDF.assign(season=season_col)

        self.teamDefDF = teamDefenseDF
        #print(self.teamDF)

    def makeOffensiveTable(self):
        table = self.tables[4]
        #print(table)
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()
                if(val == ""):
                    val = "0"


                if i in [0, 1]:
                    # if i == 0:
                    #     val = val.split(" ")[1]
                    playerStats.append(val)
                elif i in [2, 4, 5, 6, 13, 14, 15]:
                    playerStats.append(int(val))
                elif i in [3, 7, 8, 9, 10, 11, 12, 16, 17, 18]:
                    playerStats.append(float(val))
            teamStats.append(playerStats)
        #print(teamStats)
        col_names = ["Name", "Country", "Position", "Age", "Nineties", "Gls", "Sh", "SoT", "SoTP", "ShP90", "SoTP90",
                     "GPSh", "GPSoT", "Dist", "FK", "PK", "PKAtt", "xG", "npxG", "npxGPSh"]

        pd_table = pd.DataFrame(teamStats, columns=col_names)
        g_xG_diff = pd_table["Gls"] - pd_table["xG"]
        npg_npxG_diff = (pd_table["Gls"] - pd_table["PK"])  - pd_table["npxG"]
        gls_p90 = pd_table["Gls"] / pd_table["Nineties"]
        pd_table = pd_table.assign(xG_diff = g_xG_diff)
        pd_table = pd_table.assign(npxG_diff = npg_npxG_diff)
        pd_table = pd_table.assign(GlsP90 = gls_p90)

        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team=team_col)
        pd_table = pd_table.assign(tier=tier_col)
        pd_table = pd_table.assign(minutes=minutes_col)
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season=season_col)

        self.offensiveTable = pd_table

    def makePassingTable(self):
        table = self.tables[5]
        #print(table)
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        #print(tbody)
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            #print(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()

                if (val == ""):
                    val = "0"

                if i in [0, 1]:
                    playerStats.append(val)
                elif i in [2, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 18, 21, 22, 23, 24, 25]:
                    playerStats.append(int(val))
                elif i in [3, 6, 11, 14, 17, 19]:
                    playerStats.append(float(val))
            teamStats.append(playerStats)
            #print(playerStats)
        col_names = ["Name", "Country", "Position", "Age", "Nineties", "TotalPasses", "AttPasses", "PassP", "TotDist",
                     "PrgDist", "SPTotal", "SPAtt", "SPP", "MPTotal", "MPAtt", "MPP", "LPTotal", "LPAtt", "LPP", "Ast",
                     "xA", "KP", "FTP", "PPA", "CrsPA", "Prog"]
        pd_table = pd.DataFrame(teamStats, columns=col_names)
        #print(pd_table)
        #need to add KPP90, team, league, minutes, FTP90, ProgP90, minutes

        KPP90 = pd_table["KP"] / pd_table["Nineties"]
        FTP90 = pd_table["FTP"] / pd_table["Nineties"]
        ProgP90 = pd_table["Prog"] / pd_table["Nineties"]

        pd_table = pd_table.assign(KPP90 = KPP90)
        pd_table = pd_table.assign(FTP90=FTP90)
        pd_table = pd_table.assign(ProgP90=ProgP90)

        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team=team_col)
        pd_table = pd_table.assign(tier=tier_col)
        pd_table = pd_table.assign(minutes=minutes_col)
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season=season_col)

        #(pd_table)
        self.passTable = pd_table

    def makeGKTable(self):
        table = self.tables[3]
        tbody = table.find("tbody")
        #print(tbody)
        trs = tbody.find_all("tr")
        # print(tbody)
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            # print(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()

                if (val == ""):
                    val = "0"

                if i in [0, 1]:
                    playerStats.append(val)
                elif i in [2, 4, 5, 6, 7, 8, 16, 17, 23, 24, 26]:
                    playerStats.append(int(val))
                elif i in [3, 9, 10, 18, 19, 25, 27, 28]:
                    playerStats.append(float(val))
            teamStats.append(playerStats)
        #print(teamStats)
        #need to add GAP90, PSxG+/-, PSxG_GADiffP90, thrownPercentage
        col_names = ["Name", "Country", "Position", "Age", "Nineties", "GA", "PKA", "FK", "CK", "OG", "PSxG", "PsxGPSoT"
            ,"PassAtt", "ThrownPasses", "LaunchP", "AvgLen", "Crosses", "StoppedCross", "CrossStopP", "OPAActions"
            ,"OPAAP90", "AvgDist"]

        pd_table = pd.DataFrame(teamStats, columns=col_names)
        #print(pd_table)

        GAP90 = pd_table["GA"] / pd_table["Nineties"]
        PSxG_diff = pd_table["PSxG"] - (pd_table["GA"] - pd_table["OG"])
        pd_table = pd_table.assign(GAP90 = GAP90)
        pd_table = pd_table.assign(PSxG_diff = PSxG_diff)

        PSxG_dP90 = pd_table["PSxG_diff"] / pd_table["Nineties"]
        thrownP = pd_table["ThrownPasses"] / pd_table["PassAtt"]

        pd_table = pd_table.assign(PSxG_dP90 = PSxG_dP90)
        pd_table = pd_table.assign(ThrownP = thrownP)

        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team=team_col)
        pd_table = pd_table.assign(tier=tier_col)
        pd_table = pd_table.assign(minutes=minutes_col)
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season=season_col)

        #print(pd_table)
        self.GKTable = pd_table

    def makeGSCreationTable(self):
        table = self.tables[7]
        tbody = table.find("tbody")
        # print(tbody)
        trs = tbody.find_all("tr")
        # print(tbody)
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            # print(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()

                if (val == ""):
                    val = "0"

                if i in [0, 1]:
                    playerStats.append(val)
                elif i in [2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19]:
                    playerStats.append(int(val))
                elif i in [3, 5, 13]:
                    playerStats.append(float(val))
            teamStats.append(playerStats)

        #print(teamStats)
        col_names = ["Name", "Country", "Position", "Age", "Nineties", "SCA", "SCAP90", "SCA_PL", "SCA_PD", "SCA_Drib"
                     , "SCA_Sh", "SCA_Fld", "SCA_Def", "GCA", "GCAP90", "GCA_PL", "GCA_PD", "GCA_Drib", "GCA_Sh",
                     "GCA_Fld", "GCA_Def"]

        pd_table = pd.DataFrame(teamStats, columns=col_names)
        #print(pd_table)
        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team=team_col)
        pd_table = pd_table.assign(tier=tier_col)
        pd_table = pd_table.assign(minutes=minutes_col)
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season=season_col)

        #print(pd_table)
        self.GSCreationTable = pd_table

    def makePossessionTable(self):
        table = self.tables[9]
        tbody = table.find("tbody")
        # print(tbody)
        trs = tbody.find_all("tr")
        # print(tbody)
        teamStats = []
        for row in trs:
            playerStats = []
            name = row.find("a").find_all(text=True)[0]
            playerStats.append(name)
            # print(name)
            tds = row.find_all("td")
            for i in range(len(tds)):
                val = tds[i].get_text()

                if (val == ""):
                    val = "0"

                if i in [0,1]:
                    playerStats.append(val)
                elif i in [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27]:
                    playerStats.append(int(val))
                elif i in [3, 13, 26]:
                    playerStats.append(float(val))

            teamStats.append(playerStats)
        col_names = ["Name", "Country", "Position", "Age", "Nineties", "Touches", "TDP", "TD3rd", "TM3rd", "TA3rd", "TAP"
                     ,"TLive", "DribSucc", "DribAtt", "DribSuccP", "DribPlayers", "DribMegs", "Carries", "CarriesTD"
                    ,"CarriesPrgD", "CarriesProg", "Carries3rd", "CarriesCPA", "CarriesMis", "CarriesDis", "RecTarg"
                    ,"RecNum", "RecP", "RecProg"]

        pd_table = pd.DataFrame(teamStats, columns=col_names)
        # print(pd_table)

        DribP90 = pd_table["DribAtt"] / pd_table["Nineties"]
        TA3rdP90 = pd_table["TA3rd"] / pd_table["Nineties"]
        TAPP90 = pd_table["TAP"] / pd_table["Nineties"]
        Carries3rdP90 = pd_table["Carries3rd"] / pd_table["Nineties"]
        CarriesCPAP90 = pd_table["CarriesCPA"] / pd_table["Nineties"]

        pd_table = pd_table.assign(DribP90 = DribP90)
        pd_table = pd_table.assign(TA3rdP90 = TA3rdP90)
        pd_table = pd_table.assign(TAPP90 = TAPP90)
        pd_table = pd_table.assign(Carries3rdP90 = Carries3rdP90)
        pd_table = pd_table.assign(CarriesCPAP90 = CarriesCPAP90)

        team_col = [self.team for i in range(pd_table.shape[0])]
        tier_col = [self.tier for i in range(pd_table.shape[0])]
        minutes_col = pd_table["Nineties"] * 90
        pd_table = pd_table.assign(team=team_col)
        pd_table = pd_table.assign(tier=tier_col)
        pd_table = pd_table.assign(minutes=minutes_col)
        league_col = [self.leagueName for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(league=league_col)

        season_col = [self.season for i in range(pd_table.shape[0])]
        pd_table = pd_table.assign(season=season_col)

        self.possessionTable = pd_table

#--------------------------------------------------------------GETTER METHODS-------------------------------------------------
    def getStandardStats(self):
        return self.standardTable

    def getDefensiveStats(self):
        return self.teamDefDF

    def getOffensiveStats(self):
        return self.offensiveTable

    def getPassStats(self):
        return self.passTable

    def getGKStats(self):
        return self.GKTable

    def getGSCreationStats(self):
        return self.GSCreationTable

    def getPossessionStats(self):
        return self.possessionTable

    def insertLeagueData(self, lstOfInfo):
        self.leagueData = lstOfInfo
        #print(lstOfInfo)

    def insertSquadData(self, lstOfInfo):
        self.squadData = lstOfInfo
        #print(lstOfInfo)

    def getLeagueData(self):
        #print(self.leagueData)
        return self.leagueData

    def getSquadData(self):
        #print(self.squadData)
        return self.squadData

    def analyzeTeam(self):
        #log = []
        teamData = self.getLeagueData()
        teamOverview = self.getSquadData()
        self.xG_diff = teamData[5] - teamData[8]
        self.xGA_diff = teamData[6] - teamData[9]
        self.squadAge = teamOverview[2]
        self.playersUsed = teamOverview[1]

    def generatePotentialSignings(self, attackingDF, defensiveDF):

        # otherDF  = dataframe of list of players that dont include the team players itself. Playeroverview DF
        offenseDFRec = self.generateAttackingSignings(attackingDF)
        defenseDFRec = self.generateDefensiveSignings(defensiveDF)
        return [offenseDFRec, defenseDFRec]


    def generateAttackingSignings(self, otherDF):
        # check xG diff for potenatial attacking players
        #print(self.xG_diff)
        otherDF = otherDF[otherDF.get("season") == self.season]
        if (self.xG_diff < 0): #signings
            if(self.tier == 1):
                upperAgeBound = self.squadAge + 2
                shooters = otherDF[(otherDF.get("minutes") >= 700) & (otherDF.get("tier") >= self.tier) & (
                            otherDF.get("Age") <= upperAgeBound)]
                # (otherDF[otherDF.get("tier") >= 1]) & (otherDF[otherDF.get("Age") <= self.squadAge]
                shooters = shooters.sort_values(by=["GlsP90"], ascending=False).reset_index(drop=True).head(10)
            elif(self.tier == 2):
                upperAgeBound = self.squadAge + 3
                shooters = otherDF[((otherDF.get("minutes") >= 700) & (otherDF.get("tier") >= self.tier) & (
                        otherDF.get("Age") <= upperAgeBound)) | ((otherDF.get("tier") < self.tier) &
                                                                 (otherDF.get("minutes") < 700))]
                # (otherDF[otherDF.get("tier") >= 1]) & (otherDF[otherDF.get("Age") <= self.squadAge]
                shooters = shooters.sort_values(by=["tier", "GlsP90"], ascending=False).reset_index(drop=True).head(10)
            elif(self.tier == 3 or self.tier == 4):
                upperAgeBound = self.squadAge + 4
                shooters = otherDF[((otherDF.get("minutes") >= 700) & (otherDF.get("tier") >= self.tier) & (
                        otherDF.get("Age") <= upperAgeBound)) | ((otherDF.get("tier") < self.tier) &
                        (otherDF.get("minutes") < 700)) | ((otherDF.get("Age") > 32))]
                shooters = shooters.sort_values(by=["tier", "GlsP90"], ascending=False).reset_index(drop=True).head(10)
            #print(shooters)
        else: #potential talent, searching for talent instead
            tierThreshold = 0
            if (self.tier in [1, 2, 3]):
                tierThreshold = self.tier + 1
            else:
                tierThreshold = self.tier
            shooters = otherDF[(otherDF.get("minutes") >= 500) & (otherDF.get("tier") >= tierThreshold) & (
                    otherDF.get("Age") <= 23)]
            shooters = shooters.sort_values(by=["SoTP90", "GlsP90"], ascending=False).reset_index(drop=True).head(10)
            #print(shooters)

        return shooters


    def generateDefensiveSignings(self, otherDF):
        #print(self.xGA_diff)
        otherDF = otherDF[otherDF.get("season") == self.season]
        if (self.xGA_diff < 0):
            #buy some defenders
            upperAgeBound = self.squadAge + 3
            if(self.tier == 1):
                defenders = otherDF[((otherDF.get("TklRate") != None) & (otherDF.get("minutes") >= 700)
                                     & (otherDF.get("tier") >= self.tier) & (otherDF.get("Age") <= upperAgeBound))]
                defenders = defenders.sort_values(by=["TklIntP90", "TklRate", "BlkP90", "ClrP90"], ascending=False) \
                    .reset_index(drop=True).head(10)
            elif(self.tier == 2):
                defenders = otherDF[((otherDF.get("TklRate") != None) & (otherDF.get("minutes") >= 700)
                                     & (otherDF.get("tier") >= self.tier) & (otherDF.get("Age") <= upperAgeBound)) |
                                    ((otherDF.get("tier") < self.tier) & (otherDF.get("minutes") < 1500)
                                     & (otherDF.get("Age") < upperAgeBound) & (otherDF.get("minutes") > 600)
                                     & (otherDF.get("Position").str.contains("DF")))]
                defenders = defenders.sort_values(by=["TklIntP90", "TklRate", "BlkP90", "ClrP90"], ascending=False) \
                    .reset_index(drop=True).head(10)
            else:
                defenders = otherDF[((otherDF.get("TklRate") != None) & (otherDF.get("minutes") >= 700)
                                     & (otherDF.get("tier") >= self.tier) & (otherDF.get("Age") <= upperAgeBound)) |
                                    ((otherDF.get("tier") < self.tier) & (otherDF.get("minutes") < 700)
                                     & (otherDF.get("Age") < 23) & (otherDF.get("Position").str.contains("DF"))) |
                                    ((otherDF.get("Age") > 33) & (otherDF["tier"] < self.tier)
                                     & (otherDF.get("Position").str.contains("DF")))]
                defenders = defenders.sort_values(by=["TklIntP90", "TklRate", "BlkP90", "ClrP90"], ascending=False) \
                    .reset_index(drop=True).head(10)



            #print(defenders)
        else:
            tierThreshold = 0
            if(self.tier in [1,2,3]):
                tierThreshold = self.tier + 1
            else:
                tierThreshold = self.tier
            defenders = otherDF[((otherDF.get("Age") <= 24) & (otherDF.get("tier") >= tierThreshold)
                                 & (otherDF.get("minutes") >= 500) & (otherDF.get("Position").str.contains("DF")))]
            defenders = defenders.sort_values(by= ["TklIntP90", "TklRate", "BlkP90", "ClrP90"], ascending=False)\
                .reset_index(drop=True).head(10)
            #print(defenders)
        return defenders


# chels = FbrefTeam("https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats", 4, "Premier League")
# chels.makePossessionTable()
# chels.makeGSCreationTable()
# chels.makeGKTable()
# print(chels.getStandardStats())
# print(chels.getDefensiveStats())
# chels.setupAssessment()

#x = FbrefTeamClass("https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats")

# z = FbrefTeam("https://fbref.com/en/squads/1d2fe027/2019-2020/SPAL-Stats", 20, "Serie A", "2019-2020")
# print(z.link)

