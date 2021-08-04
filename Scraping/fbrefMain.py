from sqlalchemy import create_engine
import Fbref
import datetime
import time
import pandas as pd




seasonlst = ["2020-2021", "2019-2020", "2018-2019"]
# fbref = Fbref.Fbref()

# #Need to swap these when running
# fbref.scrapeFbref("2020-2021")
# fbref.scrapeFbref("2019-2020")
# fbref.scrapeFbref("2018-2019")

# # fbrefMain.counter+=1
# # print(fbrefMain.counter)
# fbref.createMegaTeamDFs()
# fbref.createRecommendorDFs()
# engine = create_engine('sqlite:///fbref.db')
# fbref.getMLT().to_sql("combined_leagues", engine, if_exists='append')
# fbref.getMSS().to_sql("team_overview", engine, if_exists='append')
# fbref.getMTSS().to_sql("player_overview", engine, if_exists='append')
# fbref.getMTOS().to_sql("player_offensive", engine, if_exists='append')
# fbref.getMTDS().to_sql("player_defensive", engine, if_exists='append')
# fbref.getMTPS().to_sql("player_passing", engine, if_exists='append')
# fbref.getMTGKS().to_sql("goalkeeping", engine, if_exists='append')
# fbref.getMTGSCS().to_sql("goal_shot_creation", engine, if_exists='append')
# fbref.getMTPOSS().to_sql("possession", engine, if_exists='append')
# fbref.getOffenseRec().to_sql("offense_rec", engine, if_exists='append')
# fbref.getDefenseRec().to_sql('defense_rec', engine, if_exists='append')
# fbref.getMLGSC().to_sql('team_gsc', engine, if_exists='append')
# fbref.getMLPS().to_sql('team_passing', engine, if_exists='append')

# for season in seasonlst:
#     print("Waiting 300 seconds")
#     time.sleep(300)
#     fbref.scrapeFbref(season)
# class fbrefMain:
#
#     def obtainDFs(self, fbref, year):
#         fbref.scrapeFbref(year)
#         fbref.createMegaTeamDFs()
#         fbref.createRecommendorDFs()
#         return [fbref.getMLT(), fbref.getMSS(), fbref.getMTSS(), fbref.getMTOS(), fbref.getMTDS, fbref.getMTPS,
#                 fbref.getMTGKS, fbref.getMTGSCS(), fbref.getMTPOSS(), fbref.getOffenseRec(), fbref.getDefenseRec()]


# fbref = Fbref.Fbref()
#
# test.obtainDFs(fbref, "2020-2021")
engine = create_engine('sqlite:///fbref.db')
for i in range(len(seasonlst)):
    fbref = Fbref.Fbref()
    print("30 second pause")
    time.sleep(30)
    fbref.scrapeFbref(seasonlst[i])
    fbref.createMegaTeamDFs()
    fbref.createRecommendorDFs()
    if(i == 0): #need to make all the lines replace
        fbref.getMLT().to_sql("combined_leagues", engine, if_exists='replace')
        fbref.getMSS().to_sql("team_overview", engine, if_exists='replace')
        fbref.getMTSS().to_sql("player_overview", engine, if_exists='replace')
        fbref.getMTOS().to_sql("player_offensive", engine, if_exists='replace')
        fbref.getMTDS().to_sql("player_defensive", engine, if_exists='replace')
        fbref.getMTPS().to_sql("player_passing", engine, if_exists='replace')
        fbref.getMTGKS().to_sql("goalkeeping", engine, if_exists='replace')
        fbref.getMTGSCS().to_sql("goal_shot_creation", engine, if_exists='replace')
        fbref.getMTPOSS().to_sql("possession", engine, if_exists='replace')
        fbref.getOffenseRec().to_sql("offense_rec", engine, if_exists='replace')
        fbref.getDefenseRec().to_sql('defense_rec', engine, if_exists='replace')
        fbref.getMLGSC().to_sql('team_gsc', engine, if_exists='replace')
        fbref.getMLPS().to_sql('team_passing', engine, if_exists='replace')
        fbref.getMLDS().to_sql('team_defense', engine, if_exists='replace')
        fbref.getMLSS().to_sql('team_shooting', engine, if_exists='replace')
        fbref.getMTPTS().to_sql('player_playtime', engine, if_exists='replace')
    else:
        fbref.getMLT().to_sql("combined_leagues", engine, if_exists='append')
        fbref.getMSS().to_sql("team_overview", engine, if_exists='append')
        fbref.getMTSS().to_sql("player_overview", engine, if_exists='append')
        fbref.getMTOS().to_sql("player_offensive", engine, if_exists='append')
        fbref.getMTDS().to_sql("player_defensive", engine, if_exists='append')
        fbref.getMTPS().to_sql("player_passing", engine, if_exists='append')
        fbref.getMTGKS().to_sql("goalkeeping", engine, if_exists='append')
        fbref.getMTGSCS().to_sql("goal_shot_creation", engine, if_exists='append')
        fbref.getMTPOSS().to_sql("possession", engine, if_exists='append')
        fbref.getOffenseRec().to_sql("offense_rec", engine, if_exists='append')
        fbref.getDefenseRec().to_sql('defense_rec', engine, if_exists='append')
        fbref.getMLGSC().to_sql('team_gsc', engine, if_exists='append')
        fbref.getMLPS().to_sql('team_passing', engine, if_exists='append')
        fbref.getMLDS().to_sql('team_defense', engine, if_exists='append')
        fbref.getMLSS().to_sql('team_shooting', engine, if_exists='append')
        fbref.getMTPTS().to_sql('player_playtime', engine, if_exists='append')
    


#Part taken from dbCreatorClass
print("FIXING INDICES")
# engine = create_engine('sqlite:///fbref.db')
cL = pd.read_sql('combined_leagues', engine).drop(columns=['index']).reset_index(drop=True)
cL.to_sql('combined_leagues', engine, if_exists='replace')

tO = pd.read_sql('team_overview', engine).drop(columns=['index']).reset_index(drop=True)
tO.to_sql('team_overview', engine, if_exists='replace')

player_overview = pd.read_sql('player_overview', engine).drop(columns=['index']).reset_index(drop=True)
player_overview.to_sql('player_overview', engine, if_exists='replace')

player_offensive = pd.read_sql('player_offensive', engine).drop(columns=['index']).reset_index(drop=True)
player_offensive.to_sql('player_offensive', engine, if_exists='replace')

player_defensive = pd.read_sql('player_defensive', engine).drop(columns=['index']).reset_index(drop=True)
player_defensive.to_sql('player_defensive', engine, if_exists='replace')

player_passing = pd.read_sql('player_passing', engine).drop(columns=['index']).reset_index(drop=True)
player_passing.to_sql('player_passing', engine, if_exists='replace')

goalkeeping = pd.read_sql('goalkeeping', engine).drop(columns=['index']).reset_index(drop=True)
goalkeeping.to_sql('goalkeeping', engine, if_exists='replace')

goal_shot_creation = pd.read_sql('goal_shot_creation', engine).drop(columns=['index']).reset_index(drop=True)
goal_shot_creation.to_sql('goal_shot_creation', engine, if_exists='replace')

possession = pd.read_sql('possession', engine).drop(columns=['index']).reset_index(drop=True)
possession.to_sql('possession', engine, if_exists='replace')

player_playtime = pd.read_sql('player_playtime', engine).drop(columns = ['index']).reset_index(drop=True)
player_playtime.to_sql('player_playtime', engine, if_exists='replace')

offense_rec = pd.read_sql('offense_rec', engine).drop(columns=['index']).reset_index(drop=True)
offense_rec.to_sql('offense_rec', engine, if_exists='replace')

defense_rec = pd.read_sql('defense_rec', engine).drop(columns=['index']).reset_index(drop=True)
defense_rec.to_sql('defense_rec', engine, if_exists='replace')

team_gsc = pd.read_sql('team_gsc', engine).drop(columns=['index']).reset_index(drop=True)
team_gsc.to_sql('team_gsc', engine, if_exists='replace')

team_passing = pd.read_sql('team_passing', engine).drop(columns=['index']).reset_index(drop=True)
team_passing.to_sql('team_passing', engine, if_exists='replace')

team_defense = pd.read_sql('team_defense', engine).drop(columns=['index']).reset_index(drop=True)
team_defense.to_sql('team_defense', engine, if_exists='replace')

team_shooting = pd.read_sql('team_shooting', engine).drop(columns=['index']).reset_index(drop=True)
team_shooting.to_sql('team_shooting', engine, if_exists='replace')
