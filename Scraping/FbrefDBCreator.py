# import fbrefMain
# import Fbref
import time
import pandas as pd
import random
import datetime
from sqlalchemy import create_engine


engine = create_engine('sqlite:///fbref.db')
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

offense_rec = pd.read_sql('offense_rec', engine).drop(columns=['index']).reset_index(drop=True)
offense_rec.to_sql('offense_rec', engine, if_exists='replace')

defense_rec = pd.read_sql('defense_rec', engine).drop(columns=['index']).reset_index(drop=True)
defense_rec.to_sql('defense_rec', engine, if_exists='replace')

team_gsc = pd.read_sql('team_gsc', engine).drop(columns=['index']).reset_index(drop=True)
team_gsc.to_sql('team_gsc', engine, if_exists='replace')

team_passing = pd.read_sql('team_passing', engine).drop(columns=['index']).reset_index(drop=True)
team_passing.to_sql('team_passing', engine, if_exists='replace')

# fm = fbrefMain.fbrefMain()
#
# seasonlst = ["2020-2021", "2019-2020", "2018-2019"]
#
# lstOfLst = []
# for season in seasonlst:
#     randVal = random.randint(0, 30)
#     print(f"Obtaining {season} data after {60+randVal} delay. Time right now {datetime.datetime.now()}")
#     time.sleep(60 + randVal)
#     fbref = Fbref.Fbref()
#     # fbref.scrapeFbref()
#     lstOfLst.append(fm.obtainDFs(fbref, season))
#
#
# dfAggregate = []
# for i in range(len(lstOfLst[0])):
#     lst = []
#     for j in range(len(lstOfLst)):
#         lst.append(lstOfLst[j][i])
#     dfAggregate.append(lst)
#
# MLT = pd.concat(dfAggregate[0]).reset_index(drop=True)

