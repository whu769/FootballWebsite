import requests
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import FbrefLeague as FL

class Fbref:
    baseLink = "https://fbref.com"
    compLink = "https://fbref.com/en/comps/"
    year = "2020-2021"

    def __init__(self):
        print("Initializing Fbref")
        self.obtainLeagueLinks()
        self.scrapeFbref()

    def obtainLeagueLinks(self):
        leagueLinks = []
        # should properly scrape the leaguelinks
        source = urllib.request.urlopen(Fbref.compLink)
        soup = BeautifulSoup(source, "lxml")
        # print(soup)
        topLeaguesHTML = soup.find(id="all_comps_club")
        # print(topLeaguesHTML.find("tbody"))
        topLeagueHistories = topLeaguesHTML.find("tbody").find_all("tr")[0:5]
        # self.scrapeFbref()
        historyEndings = []
        #print(topLeagueHistories)
        for item in topLeagueHistories:
            historyEndings.append(item.find('a', href=True)["href"])

        print(historyEndings)

        for ending in historyEndings:
            linkSource = urllib.request.urlopen(Fbref.baseLink+ending)
            soup = BeautifulSoup(linkSource, "lxml")
            #print(soup)
            tbody = soup.find("tbody")
            trs = soup.find_all("tr")[1:]
            #print(trs)
            for tr in trs:
                a = tr.find('a', href=True)
                if(a.text == Fbref.year):
                    #print("TRUE")
                    print(a["href"])
                    leagueLinks.append(Fbref.baseLink+a["href"])
                    break
        #print(leagueLinks)
        self.leagueLinks = leagueLinks

    def scrapeFbref(self):
        Leagues = []
        for lLink in self.leagueLinks:
            print("###################################################################################################")
            Leagues.append(FL.FbrefLeague(lLink))

        self.LeagueLst = Leagues

    # def createMegaDefDF(self):
    #     lstDF = []
    #     for league in self.LeagueLst:
    #         for team in league:
    #             lstDF.append(team.makeDefensiveTable())
    #
    #     megaDF = pd.concat(lstDF).reset_index(drop=True)
    #     #print(megaDF)
    #     return megaDF

    def createMegaTeamDFs(self):
        megaLeagueTable = []
        megaSquadStats = []
        megaTeamStandardStats = []
        megaTeamDefenseStats = []
        megaTeamOffenseStats = []
        megaTeamPassStats = []
        megaTeamGKStats = []
        megaTeamGSCStats = []
        megaTeamPossessionStats = []

        for league in self.LeagueLst:
            megaLeagueTable.append(league.getLeagueTable())
            megaSquadStats.append(league.getSquadStatsTable())
            for team in league.teams:
                megaTeamStandardStats.append(team.getStandardStats())
                megaTeamDefenseStats.append(team.getDefensiveStats())
                megaTeamOffenseStats.append(team.getOffensiveStats())
                megaTeamPassStats.append(team.getPassStats())
                megaTeamGKStats.append(team.getGKStats())
                megaTeamGSCStats.append(team.getGSCreationStats())
                megaTeamPossessionStats.append(team.getPossessionStats())

        MLT = pd.concat(megaLeagueTable).reset_index(drop=True)
        MSS = pd.concat(megaSquadStats).reset_index(drop= True)
        MTSS = pd.concat(megaTeamStandardStats).reset_index(drop = True)
        MTOS = pd.concat(megaTeamOffenseStats).reset_index(drop=True)
        MTDS = pd.concat(megaTeamDefenseStats).reset_index(drop=True)
        MTPS = pd.concat(megaTeamPassStats).reset_index(drop=True)
        MTGKS = pd.concat(megaTeamGKStats).reset_index(drop=True)
        MTGSCS = pd.concat(megaTeamGSCStats).reset_index(drop=True)
        MTPOSS = pd.concat(megaTeamPossessionStats).reset_index(drop=True)

        self.MLT = MLT
        self.MSS = MSS
        self.MTSS = MTSS
        self.MTOS = MTOS
        self.MTDS = MTDS
        self.MTPS = MTPS
        self.MTGKS = MTGKS
        self.MTGSCS = MTGSCS
        self.MTPOSS = MTPOSS

    def createRecommendorDFs(self):
        offenseLst = []
        defenseLst = []
        for league in self.LeagueLst:
            for team in league.teams:
                # print("###############################################################################################")
                # print(team.getTeamName())
                team.analyzeTeam()
                nonTeamOffense = self.MTOS[self.MTOS.get("team").str.contains(team.getTeamName()) == False]
                nonTeamDefense = self.MTDS[self.MTDS.get("team").str.contains(team.getTeamName()) == False]
                lst = team.generatePotentialSignings(nonTeamOffense, nonTeamDefense)
                offenseDF = lst[0]
                defenseDF = lst[1]
                offenseDF = offenseDF.assign(recommendedTeam = [team.getTeamName() for i in range(offenseDF.shape[0])])
                defenseDF = defenseDF.assign(recommendedTeam = [team.getTeamName() for i in range(defenseDF.shape[0])])
                offenseLst.append(offenseDF)
                defenseLst.append(defenseDF)

        self.offenseRec = pd.concat(offenseLst).reset_index(drop=True)
        self.defenseRec = pd.concat(defenseLst).reset_index(drop=True)

    def getMLT(self):
        return self.MLT

    def getMSS(self):
        return self.MSS

    def getMTSS(self):
        return self.MTSS

    def getMTOS(self):
        return self.MTOS

    def getMTDS(self):
        return self.MTDS

    def getMTPS(self):
        return self.MTPS

    def getMTGKS(self):
        return self.MTGKS

    def getMTGSCS(self):
        return self.MTGSCS

    def getMTPOSS(self):
        return self.MTPOSS

    def getOffenseRec(self):
        return self.offenseRec

    def getDefenseRec(self):
        return self.defenseRec
    #print("##################################################################")

# f = Fbref()
# lst = f.createMegaTeamDFs()