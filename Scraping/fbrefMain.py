from sqlalchemy import create_engine
import Fbref


fbref = Fbref.Fbref()
fbref.createMegaTeamDFs()
fbref.createRecommendorDFs()
engine = create_engine('sqlite:///fbref.db')
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

