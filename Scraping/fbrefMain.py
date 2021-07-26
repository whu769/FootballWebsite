from sqlalchemy import create_engine
import Fbref




seasonlst = ["2020-2021", "2019-2020", "2018-2019"]
fbref = Fbref.Fbref()

#Need to swap these when running
# fbref.scrapeFbref("2020-2021")
# fbref.scrapeFbref("2019-2020")
# fbref.scrapeFbref("2018-2019")

# fbrefMain.counter+=1
# print(fbrefMain.counter)
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
fbref.getMLGSC().to_sql('team_gsc', engine, if_exists='append')
fbref.getMLPS().to_sql('team_passing', engine, if_exists='append')

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
