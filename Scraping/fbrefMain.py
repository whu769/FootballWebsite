from sqlalchemy import create_engine
import Fbref


fbref = Fbref.Fbref()
fbref.scrapeFbref("2018-2019")
# fbref.scrapeFbref("2019-2020")
# fbref.scrapeFbref("2020-2021")
fbref.createMegaTeamDFs()
fbref.createRecommendorDFs()
engine = create_engine('sqlite:///fbref.db')
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

