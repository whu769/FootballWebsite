from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func
import sqlite3


app = Flask(__name__)

#Trying to connect to database
db_name = "fbref.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# viewed_season = "2020-2021"
current_season = '2020-2021'

#The various classes for the sql_tables in the db file



#Fbref tables from test2.db
class combinedLeagues(db.Model):
    __tablename__ = 'combined_leagues'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    MP = db.Column(db.Integer)
    W = db.Column(db.Integer)
    D = db.Column(db.Integer)
    L = db.Column(db.Integer)
    GF = db.Column(db.Integer)
    GA = db.Column(db.Integer)
    Pts = db.Column(db.Integer)
    xG = db.Column(db.Float)
    xGA = db.Column(db.Float)
    GD = db.Column(db.Integer)
    xGD = db.Column(db.Float)
    xGDP90 = db.Column(db.Float)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class teamOverview(db.Model):
    __tablename__ = 'team_overview'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    PlayersUsed = db.Column(db.Integer)
    Age = db.Column(db.Float)
    Possession = db.Column(db.Float)
    MP = db.Column(db.Integer)
    Gls = db.Column(db.Integer)
    Ast = db.Column(db.Integer)
    nPG = db.Column(db.Integer)
    PG = db.Column(db.Integer)
    PGAtt = db.Column(db.Integer)
    YCrd = db.Column(db.Integer)
    RCrd = db.Column(db.Integer)
    GlsP90 = db.Column(db.Float)
    AstP90 = db.Column(db.Float)
    GaAP90 = db.Column(db.Float)
    nPGP90 = db.Column(db.Float)
    nPGaAP90 = db.Column(db.Float)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    xA = db.Column(db.Float)
    npxGaA = db.Column(db.Float)
    xGP90 = db.Column(db.Float)
    xAP90 = db.Column(db.Float)
    xGaAP90 = db.Column(db.Float)
    npxGP90 = db.Column(db.Float)
    npxGaAP90 = db.Column(db.Float)
    league = db.Column(db.Text)
    season = db.Column(db.Text)

    
class playerOverview(db.Model):
    __tablename__ = 'player_overview'
    index = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    MP = db.Column(db.Integer)
    Starts = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Gls = db.Column(db.Integer)
    Ast = db.Column(db.Integer)
    nPG = db.Column(db.Integer)
    PG = db.Column(db.Integer)
    PGAtt = db.Column(db.Integer)
    YCrd = db.Column(db.Integer)
    RCrd = db.Column(db.Integer)
    GlsP90 = db.Column(db.Float)
    AstP90 = db.Column(db.Float)
    GaAP90 = db.Column(db.Float)
    nPGP90 = db.Column(db.Float)
    npGaAP90 = db.Column(db.Float)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    xA = db.Column(db.Float)
    npxGaA = db.Column(db.Float)
    xGP90 = db.Column(db.Float)
    xAP90 = db.Column(db.Float)
    xGaAP90 = db.Column(db.Float)
    npxGP90 = db.Column(db.Float)
    npxGaAP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class playerOffensive(db.Model):
    __tablename__ = 'player_offensive'
    index = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Gls = db.Column(db.Integer)
    Sh = db.Column(db.Integer)
    SoT = db.Column(db.Integer)
    SoTP = db.Column(db.Float)
    ShP90 = db.Column(db.Float)
    SoTP90 = db.Column(db.Float)
    GPSh = db.Column(db.Float)
    GPSoT = db.Column(db.Float)
    Dist = db.Column(db.Float)
    FK = db.Column(db.Integer)
    PK = db.Column(db.Integer)
    PKAtt = db.Column(db.Integer)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    npxGPSh = db.Column(db.Float)
    xG_diff = db.Column(db.Float)
    npxG_diff = db.Column(db.Float)
    GlsP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class playerDefensive(db.Model):
    __tablename__ = 'player_defensive'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Nation = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Tkl = db.Column(db.Integer)
    TklW = db.Column(db.Integer)
    Def3rd = db.Column(db.Integer)
    Mid3rd = db.Column(db.Integer)
    Att3rd = db.Column(db.Integer)
    TklDribble = db.Column(db.Integer)
    TklAttDribble = db.Column(db.Integer)
    TklPctDribble = db.Column(db.Float)
    Past = db.Column(db.Integer)
    Pressures = db.Column(db.Integer)
    PressureSuccess = db.Column(db.Integer)
    PressurePct = db.Column(db.Float)
    PDef3rd = db.Column(db.Integer)
    PMid3rd = db.Column(db.Integer)
    PAtt3rd = db.Column(db.Integer)
    Blocks = db.Column(db.Integer)
    ShotBlk = db.Column(db.Integer)
    ShSv = db.Column(db.Integer)
    BlkPass = db.Column(db.Integer)
    Int = db.Column(db.Integer)
    TklPlusInt = db.Column(db.Integer)
    Clr = db.Column(db.Integer)
    Err = db.Column(db.Integer)
    TklIntP90 = db.Column(db.Float)
    TklRate = db.Column(db.Float)
    BlkP90 = db.Column(db.Float)
    ClrP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    minutes = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class playerPassing(db.Model):
    __tablename__ = 'player_passing'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    TotalPasses = db.Column(db.Integer)
    AttPasses = db.Column(db.Integer)
    PassP = db.Column(db.Float)
    TotDist = db.Column(db.Integer)
    PrgDist = db.Column(db.Integer)
    SPTotal = db.Column(db.Integer)
    SPAtt = db.Column(db.Integer)
    SPP = db.Column(db.Float)
    MPTotal = db.Column(db.Integer)
    MPAtt = db.Column(db.Integer)
    MPP = db.Column(db.Float)
    LPTotal = db.Column(db.Integer)
    LPAtt = db.Column(db.Integer)
    LPP = db.Column(db.Float)
    Ast = db.Column(db.Integer)
    xA = db.Column(db.Float)
    KP = db.Column(db.Integer)
    FTP = db.Column(db.Integer)
    PPA = db.Column(db.Integer)
    CrsPA = db.Column(db.Integer)
    Prog = db.Column(db.Integer)
    KPP90 = db.Column(db.Float)
    FTP90 = db.Column(db.Float)
    ProgP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class goalkeeping(db.Model):
    __tablename__ = 'goalkeeping'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    GA = db.Column(db.Integer)
    PKA = db.Column(db.Integer)
    FK= db.Column(db.Integer)
    CK = db.Column(db.Integer)
    OG = db.Column(db.Integer)
    PSxG = db.Column(db.Float)
    PsxGPSoT = db.Column(db.Float)
    PassAtt = db.Column(db.Integer)
    ThrownPasses = db.Column(db.Integer)
    LaunchP = db.Column(db.Float)
    AvgLen = db.Column(db.Float)
    Crosses = db.Column(db.Integer)
    StoppedCross = db.Column(db.Integer)
    CrossStopP = db.Column(db.Float)
    OPAActions = db.Column(db.Integer)
    OPAAP90 = db.Column(db.Float)
    AvgDist = db.Column(db.Float)
    GAP90 = db.Column(db.Float)
    PSxG_diff = db.Column(db.Float)
    PSxG_dP90 = db.Column(db.Float)
    ThrownP = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class gsCreation(db.Model):
    __tablename__ = 'goal_shot_creation'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    SCA = db.Column(db.Integer)
    SCAP90 = db.Column(db.Float)
    SCA_PL = db.Column(db.Integer)
    SCA_PD = db.Column(db.Integer)
    SCA_Drib = db.Column(db.Integer)
    SCA_Sh = db.Column(db.Integer)
    SCA_Fld = db.Column(db.Integer)
    SCA_Def = db.Column(db.Integer)
    GCA = db.Column(db.Integer)
    GCAP90 = db.Column(db.Float)
    GCA_PL = db.Column(db.Integer)
    GCA_PD = db.Column(db.Integer)
    GCA_Drib = db.Column(db.Integer)
    GCA_Sh = db.Column(db.Integer)
    GCA_Fld = db.Column(db.Integer)
    GCA_Def = db.Column(db.Integer)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)

class possession(db.Model):
    __tablename__ = 'possession'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Touches = db.Column(db.Integer)
    TDP = db.Column(db.Integer)
    TD3rd = db.Column(db.Integer)
    TM3rd = db.Column(db.Integer)
    TA3rd = db.Column(db.Integer)
    TAP = db.Column(db.Integer)
    TLive = db.Column(db.Integer)
    DribSucc = db.Column(db.Integer)
    DribAtt = db.Column(db.Integer)
    DribSuccP = db.Column(db.Float)
    DribPlayers = db.Column(db.Integer)
    DribMegs = db.Column(db.Integer)
    Carries = db.Column(db.Integer)
    CarriesTD = db.Column(db.Integer) 
    CarriesPrgD = db.Column(db.Integer)
    CarriesProg = db.Column(db.Integer)
    Carries3rd = db.Column(db.Integer)
    CarriesCPA = db.Column(db.Integer)
    CarriesMis = db.Column(db.Integer)
    CarriesDis = db.Column(db.Integer)
    RecTarg = db.Column(db.Integer)
    RecNum = db.Column(db.Integer)
    RecP = db.Column(db.Float)
    RecProg = db.Column(db.Integer)
    DribP90 = db.Column(db.Float)
    TA3rdP90 = db.Column(db.Float)
    TAPP90 = db.Column(db.Float)
    Carries3rdP90 = db.Column(db.Float)
    CarriesCPAP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)


class offenseRec(db.Model):
    __tablename__ = "offense_rec"
    index = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Gls = db.Column(db.Integer)
    Sh = db.Column(db.Integer)
    SoT = db.Column(db.Integer)
    SoTP = db.Column(db.Float)
    ShP90 = db.Column(db.Float)
    SoTP90 = db.Column(db.Float)
    GPSh = db.Column(db.Float)
    GPSoT = db.Column(db.Float)
    Dist = db.Column(db.Float)
    FK = db.Column(db.Integer)
    PK = db.Column(db.Integer)
    PKAtt = db.Column(db.Integer)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    npxGPSh = db.Column(db.Float)
    xG_diff = db.Column(db.Float)
    npxG_diff = db.Column(db.Float)
    GlsP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    tier = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)
    recommendedTeam = db.Column(db.Text)

class defenseRec(db.Model):
    __tablename__ = "defense_rec"
    index = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.Text)
    Nation = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    Nineties = db.Column(db.Float)
    Tkl = db.Column(db.Integer)
    TklW = db.Column(db.Integer)
    Def3rd = db.Column(db.Integer)
    Mid3rd = db.Column(db.Integer)
    Att3rd = db.Column(db.Integer)
    TklDribble = db.Column(db.Integer)
    TklAttDribble = db.Column(db.Integer)
    TklPctDribble = db.Column(db.Float)
    Past = db.Column(db.Integer)
    Pressures = db.Column(db.Integer)
    PressureSuccess = db.Column(db.Integer)
    PressurePct = db.Column(db.Float)
    PDef3rd = db.Column(db.Integer)
    PMid3rd = db.Column(db.Integer)
    PAtt3rd = db.Column(db.Integer)
    Blocks = db.Column(db.Integer)
    ShotBlk = db.Column(db.Integer)
    ShSv = db.Column(db.Integer)
    BlkPass = db.Column(db.Integer)
    Int = db.Column(db.Integer)
    TklPlusInt = db.Column(db.Integer)
    Clr = db.Column(db.Integer)
    Err = db.Column(db.Integer)
    TklIntP90 = db.Column(db.Float)
    TklRate = db.Column(db.Float)
    BlkP90 = db.Column(db.Float)
    ClrP90 = db.Column(db.Float)
    Team = db.Column(db.Text)
    minutes = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    League = db.Column(db.Text)
    season = db.Column(db.Text)
    recommendedTeam = db.Column(db.Text)

@app.route("/", defaults={'viewed_season':'2020-2021'})
@app.route('/<viewed_season>')
def index(viewed_season):
    #print(viewed_season)
    #Good tester code to see if the db works
    # try:
    #     combinedLeague = combinedLeagues.query.filter_by(league='Premier League').order_by( combinedLeagues.Pts.desc()).all()
    #     cl_text = '<ul>'
    #     for cl in combinedLeague:
    #         cl_text += '<li>' + cl.Team + ', ' + str(cl.PTS) + '</li>'
    #     cl_text += '</ul>'
    #     return cl_text
    # except Exception as e:
    #     # e holds description of the error
    #     error_text = "<p>The error:<br>" + str(e) + "</p>"
    #     hed = '<h1>Something is broken.</h1>'
    #     return hed + error_text
    
    #KEEP THIS, IT'S LIKE LEGACY LOL
    # players = CombinedPlayer.query.order_by(CombinedPlayer.goals.desc()).limit(20)
    # cL = CombinedLeague.query.order_by(CombinedLeague.PTS.desc()).limit(20)
    # leagues = CombinedLeague.query.with_entities(CombinedLeague.League).distinct()
    # return render_template("index2.html", combinedLeague = cL, Leagues = leagues, Players = players)

    #this effort is ALL FBREF STUFF
    #try:
        #WHAT IS WRONG WITH THIS LINE?
    players = playerOverview.query.filter(playerOverview.season == viewed_season).order_by(playerOverview.Gls.desc()).limit(20)
    #print(players)
    # for player in players:
    #     print(player.season)
    cL = combinedLeagues.query.filter(combinedLeagues.season == viewed_season).order_by(combinedLeagues.Pts.desc()).limit(20)
    #print(type(cL))

    
    leagues = combinedLeagues.query.with_entities(combinedLeagues.League).distinct()
    return render_template("index3.html", combinedLeague = cL, Leagues = leagues, Player = players, season = viewed_season)
 

@app.route('/league/<League>')
def leagues(League, viewed_season = current_season):
    try:
        # Leagues = CombinedLeague.query.filter_by(League=League).order_by(CombinedLeague.PTS.desc()).all()
        # Teams = CombinedLeague.query.with_entities(CombinedLeague.Team).distinct()
        # Goals = advancedStats.query.filter_by(League=League).order_by(advancedStats.goals.desc()).all()
        # Assists = advancedStats.query.filter_by(League = League).order_by(advancedStats.assists.desc()).all()

        # bestOffensively = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.G.desc()).first()
        # bestDefensively = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.GA).first()
        # worstDefensively = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.GA.desc()).first()
        # worstOffensively = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.G).first()

        # overAchieved = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.xPTS_diff).first()
        # underAchieved = CombinedLeague.query.filter_by(League = League).order_by(CombinedLeague.xPTS_diff.desc()).first()
        
        # #DON'T NAME LISTS THE SAME THINGS AS COLUMN NAMES DUMBASS
        # return render_template('league2.html', League=Leagues, Team = Teams, Goals = Goals, Assists = Assists, bO = bestOffensively, bD = bestDefensively,
        # wO = worstOffensively, wD = worstDefensively, overAchieved = overAchieved, underAchieved = underAchieved)

        Leagues = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.Pts.desc()).all()
        Goals = playerOverview.query.filter(playerOverview.League == League, playerOverview.season == viewed_season).order_by(playerOverview.Gls.desc()).all()
        Assists = playerOverview.query.filter(playerOverview.League == League, playerOverview.season == viewed_season).order_by(playerOverview.Ast.desc()).all()

        bestOffensively = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.GF.desc()).first()
        bestDefensively = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.GA).first()
        worstDefensively = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.GA.desc()).first()
        worstOffensively = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.GF).first()
        highestGD = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == viewed_season).order_by(combinedLeagues.GD.desc()).first()
        return render_template('league3.html', League = Leagues, Goals = Goals, Assists = Assists, bO = bestOffensively, bD = bestDefensively, 
        wO = worstOffensively, wD = worstDefensively, hGD = highestGD)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/team/<Team>')
def teams(Team, viewed_season = current_season):
    try:
        #print(Team)
        # team = CombinedLeague.query.filter_by(Team = Team).first()
        # #print(team)
        # players = CombinedPlayer.query.filter_by(team_title=Team).order_by(CombinedPlayer.goals.desc()).all()
        # goals = advancedStats.query.filter_by(team_title = Team).order_by(advancedStats.goals.desc()).all()

        # assists = advancedStats.query.filter_by(team_title = Team).order_by(advancedStats.assists.desc()).all()

        # attackingSignings = offenseRec.query.filter_by(teamRecommend = Team).all()
        # defenseSignings = defenseRec.query.filter_by(teamRecommend = Team).all()
        # print(len(defenseSignings))
        # #print(offense)
        # #print(attackingPlayer) 
        # # dSignings = defenseSignings
        # return render_template('team2.html', Team = team, Player = players, Goals = goals, Assists = assists, aSignings = attackingSignings, dSignings = defenseSignings)

        team = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == viewed_season).first()
        tAdvanced = teamOverview.query.filter(teamOverview.Team == Team, teamOverview.season == viewed_season).first()
        players = playerOverview.query.filter(playerOverview.Team == Team, playerOverview.minutes != 0, playerOverview.season == viewed_season).order_by(playerOverview.minutes.desc()).all()
        goals = playerOffensive.query.filter(playerOffensive.Team == Team, playerOffensive.season == viewed_season).order_by(playerOffensive.Gls.desc()).all()
        assists = playerOverview.query.filter(playerOverview.Team == Team, playerOverview.season == viewed_season).order_by(playerOverview.Ast.desc()).all()
        aSignings = offenseRec.query.filter(offenseRec.recommendedTeam == Team, offenseRec.season == viewed_season).all()
        dSignings = defenseRec.query.filter(defenseRec.recommendedTeam == Team, defenseRec.season == viewed_season).all()

        
        return render_template("team3.html", Team = team, tO = tAdvanced, Player = players, Goals = goals, Assists = assists, aSignings = aSignings, dSignings = dSignings)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

def obtainTeamStats(team):
    teamDataList = []
    teamDataList.append(team.GlsP90)
    teamDataList.append(team.AstP90)
    teamDataList.append(team.xGP90)
    teamDataList.append(team.xAP90)
    return teamDataList

def obtainTeamAvgStats(teams):
    teamList = [[],[],[],[]]
    for team in teams:
        teamList[0].append(team.GlsP90)
        teamList[1].append(team.AstP90)
        teamList[2].append(team.xGP90)
        teamList[3].append(team.xAP90)
    
    lstAvg = []
    for lst in teamList:
        lstAvg.append(sum(lst)/len(lst))
    
    return lstAvg

@app.route('/team/<Team>/graphs')
def graphs(Team, viewed_season = current_season):
    try:
        #print("The page is working")
        team = teamOverview.query.filter(teamOverview.Team == Team, teamOverview.season == viewed_season).first()
        teams = teamOverview.query.filter(teamOverview.Team != Team, 
                    teamOverview.league == team.league, teamOverview.season == viewed_season).all()

        teamSeasons = teamOverview.query.filter(teamOverview.Team == Team).all()
        print(len(teamSeasons))
        # the db is messed up, indices are WRONG
        
        t1Teams = combinedLeagues.query.filter(combinedLeagues.League == team.league, combinedLeagues.season == viewed_season).limit(4)
        t1TLst = []
        for x in t1Teams:
            if(x.Team != team.Team):
                t1TLst.append(x.Team)
        t1teams = teamOverview.query.filter(teamOverview.Team.in_(t1TLst)).all()
        
        teamPlayers = playerOverview.query.filter(playerOverview.Team == Team, playerOverview.season == viewed_season).all()
        #print(type(teamPlayers))
        ageList = []
        ageDict = dict()
        minDict = dict()
        startDict = dict()
        for tP in teamPlayers:
            ageList.append(tP.Age)
            minDict[tP.Name] = tP.minutes
            startDict[tP.Name] = tP.Starts
            if(not(tP.Age in ageDict.keys())):
                ageDict[tP.Age] = 1
            else:
                ageDict[tP.Age] = ageDict[tP.Age] + 1
        
        teamStats = obtainTeamStats(team)
        leagueStats = (obtainTeamAvgStats(teams))
        
        t1LeagueStats = obtainTeamAvgStats(t1teams)
        
        teamLabels = ["GlsP90", "AstP90", "xGP90", "xAP90"]
        # print(list(minDict.keys()))
        # print(list(minDict))
        #print(list(ageDict.keys()))
        return render_template("teamGraph.html", ageLabels = sorted(list(ageDict.keys())), ageData = sorted(list(ageDict.values()))
        , minLabels = list(minDict.keys()), minData = list(minDict.values())
        , startLabels = list(startDict.keys()), startData = list(startDict.values()), Team = team, teamLabels = teamLabels, teamStats = teamStats
        , leagueStats = leagueStats, t1LeagueStats = t1LeagueStats)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

#returns a nested list w/ offense, defense, and passing stats
def obtainIndividualStats(pOffense, pDefense, pPass, pGSCreation):
    offenseLabels = ["SoTP90", "GlsP90", "ShP90", "GPSoT"] #, "npxGPSh"
    offenseData = []
    offenseData.append(pOffense.SoTP90)
    offenseData.append(pOffense.GlsP90)
    offenseData.append(pOffense.ShP90)
    offenseData.append(pOffense.GPSoT)
    #offenseData.append(pOffense.npxGPSh)
    #print(offenseData)
    # print(offenseLabels)

    #info for the defense radar
    defenseLabels = ["ClrP90", "BlkP90", "TklIntP90", "Tackles P90", "Successful Tackles P90", "Interceptions P90"]
    defenseData = []
    defenseData.append(pDefense.ClrP90)
    defenseData.append(pDefense.BlkP90)
    defenseData.append(pDefense.TklIntP90)
    defenseData.append(pDefense.Tkl / pDefense.Nineties)
    defenseData.append(pDefense.TklW / pDefense.Nineties)
    defenseData.append(pDefense.Int / pDefense.Nineties)
    #print(defenseData)

    #passing stuff
    passingLabels = ["PassP", "SPP", "MPP", "LPP"] #, "KPP90", "FTP90", "ProgP90"
    passingData = []
    passingData.append(pPass.PassP)
    passingData.append(pPass.SPP)
    passingData.append(pPass.MPP)
    passingData.append(pPass.LPP)

    passingLabels2 = ["SP90", "MP90", "LP90", "FT90", "KP90"]
    passingData2 = []
    passingData2.append(pPass.SPTotal / pPass.Nineties)
    passingData2.append(pPass.MPTotal / pPass.Nineties)
    passingData2.append(pPass.LPTotal / pPass.Nineties)
    passingData2.append(pPass.FTP90)
    passingData2.append(pPass.KPP90)

    gsCLabels = ["SCA_PL", "SCA_PD", "SCA_Drib", "SCA_Sh", "SCA_Fld", "SCA_Def"]
    gsCData = []
    gsCData.append(pGSCreation.SCA_PL / pGSCreation.Nineties)
    gsCData.append(pGSCreation.SCA_PD / pGSCreation.Nineties)
    gsCData.append(pGSCreation.SCA_Drib / pGSCreation.Nineties)
    gsCData.append(pGSCreation.SCA_Sh / pGSCreation.Nineties)
    gsCData.append(pGSCreation.SCA_Fld / pGSCreation.Nineties)
    gsCData.append(pGSCreation.SCA_Def / pGSCreation.Nineties)

    return [[offenseLabels, offenseData], [defenseLabels, defenseData], [passingLabels, passingData],
    [passingLabels2, passingData2], [gsCLabels, gsCData]]


def obtainAvgStats(teamDef, teamAtt, teamPass, teamGSC):
    teamDefData = [[],[],[],[],[],[]]
    teamDefAvgData = []
    # 0 = Clr, 1 = blk, 2 = Tkl+Int, 3 = Tklp90m, 4 =STP90, 5 = IntP90  
    for player in teamDef:
        if player.Nineties != 0:
            teamDefData[0].append(player.ClrP90)
            teamDefData[1].append(player.BlkP90)
            teamDefData[2].append(player.TklIntP90)
            teamDefData[3].append(player.Tkl / player.Nineties)
            teamDefData[4].append(player.TklW / player.Nineties)
            teamDefData[5].append(player.Int / player.Nineties)
    
    #print(teamDefData)
    for lst in teamDefData:
        teamDefAvgData.append(sum(lst) / len(lst))
    
    teamAttData = [[], [], [], []]
    teamAttAvgData = []
    for player in teamAtt:
        if player.minutes != 0: #this may affect the real values?
            teamAttData[0].append(player.SoTP90)
            teamAttData[1].append(player.GlsP90)
            teamAttData[2].append(player.ShP90)
            teamAttData[3].append(player.GPSoT)
    
    for lst in teamAttData:
        teamAttAvgData.append(sum(lst) / len(lst))
    
    teamPassData = [[], [], [], [], [], [], [], [], []]
    teamPassAvgData = []
    for player in teamPass:
        if player.minutes != 0:
            teamPassData[0].append(player.PassP)
            teamPassData[1].append(player.SPP)
            teamPassData[2].append(player.MPP)
            teamPassData[3].append(player.LPP)
            teamPassData[4].append(player.SPTotal / player.Nineties)
            teamPassData[5].append(player.MPTotal / player.Nineties)
            teamPassData[6].append(player.LPTotal / player.Nineties)
            teamPassData[7].append(player.FTP90)
            teamPassData[8].append(player.KPP90)

    for lst in teamPassData:
        teamPassAvgData.append(sum(lst) / len(lst))

    teamGSCData = [[],[],[],[],[],[]]
    teamGSCAvgData = []
    for player in teamGSC:
        teamGSCData[0].append(player.SCA_PL / player.Nineties)
        teamGSCData[1].append(player.SCA_PD / player.Nineties)
        teamGSCData[2].append(player.SCA_Drib / player.Nineties)
        teamGSCData[3].append(player.SCA_Sh / player.Nineties)
        teamGSCData[4].append(player.SCA_Fld / player.Nineties)
        teamGSCData[5].append(player.SCA_Def / player.Nineties)
    
    for lst in teamGSCData:
        teamGSCAvgData.append(sum(lst) / len(lst))


    return [teamDefAvgData, teamAttAvgData, teamPassAvgData, teamGSCAvgData]

def obtainGKStats(GKStats):
    #Passing segments
    gkPassLabels = ["Thrown", "Launched", "Short"]
    launchedPasses = int(GKStats.LaunchP / 100 * GKStats.PassAtt)
    shortPasses = GKStats.PassAtt - GKStats.ThrownPasses - launchedPasses
    gkPassData = [GKStats.ThrownPasses, launchedPasses, shortPasses]
    gkPassLst = [gkPassLabels, gkPassData]
    #GA / PSxG stuff
    gkShotLabels = ["GAP90", "PSxGP90","PSxG_dP90"]
    psxgP90 = GKStats.PSxG / GKStats.Nineties
    gkShotData = [GKStats.GAP90, psxgP90, GKStats.PSxG_dP90]
    gkShotLst = [gkShotLabels, gkShotData]

    #Misc stats
    gkMiscLabels = ["Cross Stop %", "AvgDist", "Out of Pen Box Actions P90"]
    gkMiscData = [GKStats.CrossStopP, GKStats.AvgDist, GKStats.OPAAP90]
    gkMiscLst = [gkMiscLabels, gkMiscData]
    
    return [gkPassLst, gkShotLst, gkMiscLst]

def obtainAvgGKStats(oppGKStats):
    gkShotStats = [[], [], []]
    gkAvgShotData = []
    #shot stuff
    for player in oppGKStats:
        gkShotStats[0].append(player.GAP90)
        gkShotStats[1].append(player.PSxG / player.Nineties)
        gkShotStats[2].append(player.PSxG_dP90)

    for lst in gkShotStats:
        gkAvgShotData.append(sum(lst) / len(lst))

    gkMiscStats = [[], [], []]
    gkAvgMiscData = []
    for player in oppGKStats:
        gkMiscStats[0].append(player.CrossStopP)
        gkMiscStats[1].append(player.AvgDist)
        gkMiscStats[2].append(player.OPAAP90)
    
    for lst in gkMiscStats:
        gkAvgMiscData.append(sum(lst) / len(lst))
    
    return [gkAvgShotData, gkAvgMiscData]

@app.route('/player/<Player>')
def players(Player, viewed_season = current_season):
    try:
        #print("The page is working")
        pO2 = playerOverview.query.filter_by(Name = Player).first()
        pO = playerOverview.query.filter(playerOverview.Name == Player, playerOverview.season == viewed_season).order_by(playerOverview.minutes.desc()).all()[0]
        print(pO.Team)
        print(pO2.Team)
        # for player in pO2:
        #     print(player.Gls)
        primaryPosition = pO.Position.split(",")[0]
        positions = pO.Position.split(",")
        if primaryPosition != "GK":
            pOffense = playerOffensive.query.filter(playerOffensive.Name == Player, playerOffensive.Team == pO.Team, playerOffensive.season == viewed_season).first()
            pDefense = playerDefensive.query.filter(playerDefensive.Name == Player, playerDefensive.Team == pO.Team, playerDefensive.season == viewed_season).first()
            pPass = playerPassing.query.filter(playerPassing.Name == Player, playerPassing.Team == pO.Team, playerPassing.season == viewed_season).first()
            pGSCreation = gsCreation.query.filter(gsCreation.Name == Player, gsCreation.Team == pO.Team, gsCreation.season == viewed_season).first()
            #print(pGSCreation.Name)
            
            #No longer used
            teamDef = playerDefensive.query.filter_by(Team = pO.Team).all()
            teamAtt = playerOffensive.query.filter_by(Team = pO.Team).all()
            teamPass = playerPassing.query.filter_by(Team = pO.Team).all()
            
            t1Def = playerDefensive.query.filter(playerDefensive.tier == 1, playerDefensive.Position == primaryPosition, playerDefensive.Nineties >= 8,
                    playerDefensive.season == viewed_season)
            t1Att = playerOffensive.query.filter(playerOffensive.tier == 1, playerOffensive.Position == primaryPosition, playerOffensive.Nineties >= 8,
                    playerOffensive.season == viewed_season)
            t1Pass = playerPassing.query.filter(playerPassing.tier == 1, playerPassing.Position == primaryPosition, playerPassing.Nineties >= 8,
                    playerPassing.season == viewed_season)
            t1GSC = gsCreation.query.filter(gsCreation.tier == 1, gsCreation.Position == primaryPosition, gsCreation.Nineties >= 8,
                    gsCreation.season == viewed_season)
            # for player in t1GSC:
            #     print(player.Name)

            
            oppDef = playerDefensive.query.filter(playerDefensive.Position == primaryPosition, playerDefensive.Nineties >= 8,
                    playerDefensive.season == viewed_season)
            oppAtt = playerOffensive.query.filter(playerOffensive.Position == primaryPosition, playerOffensive.Nineties >= 8,
                    playerOffensive.season == viewed_season)
            oppPass = playerPassing.query.filter(playerPassing.Position == primaryPosition, playerPassing.Nineties >= 8,
                    playerPassing.season == viewed_season)
            oppGSC = gsCreation.query.filter(gsCreation.Position == primaryPosition, gsCreation.Nineties >= 8,
                    gsCreation.season == viewed_season)
            
            playerData = obtainIndividualStats(pOffense, pDefense, pPass, pGSCreation)
            #teamData = obtainAvgStats(teamDef, teamAtt, teamPass)
            oppData = obtainAvgStats(oppDef, oppAtt, oppPass, oppGSC)
            t1Data = obtainAvgStats(t1Def, t1Att, t1Pass, t1GSC)
            #print(oppData[3])
            

            return render_template("player.html", pO = pO, pOLabels = playerData[0][0], pOData = playerData[0][1], pDLabels = playerData[1][0], pDData = playerData[1][1]
            , pPLabels = playerData[2][0], pPData = playerData[2][1], pPLabels2 = playerData[3][0], pPData2 = playerData[3][1], pDT1Data = t1Data[0]
            , pOT1Data = t1Data[1], pPT1Data = t1Data[2][0:4], pPT1Data2 = t1Data[2][4:], oPDData = oppData[0], oPOData = oppData[1],
            oPPData = oppData[2][0:4], oPPData2 = oppData[2][4:], pGSCLabels = playerData[4][0], pGSCData = playerData[4][1], pGSCT1Data = t1Data[3]
            , oppGSCData = oppData[3])
        else:
            GKStats = goalkeeping.query.filter(goalkeeping.Name == pO.Name, goalkeeping.season == viewed_season).first()
            oppGKStats = goalkeeping.query.filter(goalkeeping.minutes >= 1000, goalkeeping.Name != pO.Name, goalkeeping.season == viewed_season)
            oppT1GKStats = goalkeeping.query.filter(goalkeeping.minutes >= 1000, goalkeeping.Name != pO.Name, goalkeeping.tier == 1, goalkeeping.season == viewed_season)
            # for player in oppGKStats:
            #     print(player.Name)
            GKData = obtainGKStats(GKStats)
            oppGKData = obtainAvgGKStats(oppGKStats)
            oppGKT1Data = obtainAvgGKStats(oppT1GKStats)
            #print(GKData)
            #print(oppGKData)

            #print(GKData[1])
            #print(oppGKT1Data[0])
            return render_template("goalie.html", pO = pO, gkPassLabels = GKData[0][0], gkPassData = GKData[0][1]
            , gkShotLabels = GKData[1][0], gkShotData = GKData[1][1], oppgkShotData = oppGKData[0]
            , gkMiscLabels =GKData[2][0], gkMiscData = GKData[2][1], oppgkMiscData = oppGKData[1]
            , oppT1ShotData = oppGKT1Data[0], oppT1MiscData = oppGKT1Data[1])
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/terms')
def terms():
    try:
        return render_template("terms.html")
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/<League>/LeaguePlayers')
def LeaguePlayers(League, viewed_season = current_season):
    try:
        leaguePlayers = playerOverview.query.filter(playerOverview.League == League, playerOverview.minutes > 0, playerOverview.season == viewed_season).all()
    
        return render_template("leaguePlayers.html", lPlayers = leaguePlayers)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

def findBestFW(League, age, tier, minutes, viewed_season):
    #print("finding FW")
    #Shots/Goals Type FW
    fwOStats = playerOffensive.query.filter(playerOffensive.League == League, playerOffensive.Position.contains("FW"), playerOffensive.minutes >= minutes,
                playerOffensive.Age <= age, playerOffensive.tier >= tier, playerOffensive.season == viewed_season)
    #print(type(fwOStats))
    fwOPlayers = fwOStats.order_by(playerOffensive.Gls.desc(), playerOffensive.GlsP90.desc(), playerOffensive.xG.desc()).limit(10)
    # for player in fwOPlayers:
    #     print(player.Name)
    
    #Creative stuff
    fwCStats = gsCreation.query.filter(gsCreation.League == League, gsCreation.Position.contains("FW"), gsCreation.minutes >= minutes,
                gsCreation.Age <= age, gsCreation.tier >= tier, gsCreation.season == viewed_season)
    fwCPlayers = fwCStats.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)
    # for player in fwCPlayers:
    #     print(player.Name)


    #Haven't implemented the ball carrying stuff
    fwDStats = possession.query.filter(possession.League == League, possession.Position.contains("FW"), possession.minutes >= minutes,
                possession.Age <= age, possession.tier >= tier, possession.season == viewed_season)
    fwDPlayers = fwDStats.order_by(possession.DribP90.desc(), possession.DribSuccP.desc(), possession.TAPP90.desc(), possession.CarriesCPAP90.desc()).limit(10)
    # for player in fwDPlayers:
    #     print(player.Name)
    return [fwOPlayers, fwCPlayers, fwDPlayers]

def findBestMF(League, age, tier, minutes, viewed_season):
    #print("finding MF")
    #CAM section
    mfCStats = gsCreation.query.filter(gsCreation.League == League, gsCreation.Position.contains("MF"), gsCreation.minutes >= minutes,
                    gsCreation.Age <= age, gsCreation.tier >= tier, gsCreation.season == viewed_season)
    mfCPlayers = mfCStats.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)

    #Passing MF
    mfPStats = playerPassing.query.filter(playerPassing.League == League, playerPassing.Position.contains("MF"), playerPassing.minutes >= minutes,
                    playerPassing.Age <= age, playerPassing.tier >= tier, playerPassing.season == viewed_season)
    mfPPlayers = mfPStats.order_by(playerPassing.ProgP90.desc(), playerPassing.KPP90.desc(), playerPassing.FTP90.desc(), playerPassing.PassP.desc()).limit(10)

    #Defensive MF
    mfDStats = playerDefensive.query.filter(playerDefensive.League == League, playerDefensive.Position.contains("MF"), playerDefensive.minutes >= minutes,
                playerDefensive.Age <= age, playerDefensive.tier >= 1, playerDefensive.season == viewed_season)
    mfDPlayers = mfDStats.order_by(playerDefensive.TklIntP90.desc(), playerDefensive.TklRate.desc(), playerDefensive.PressurePct.desc()).limit(10)
    
    return [mfCPlayers, mfPPlayers, mfDPlayers]

def findBestDF(League, age, tier, minutes, viewed_season):
    #print("Finding DF")
    #offensive df
    dfOStats = playerOffensive.query.filter(playerOffensive.League == League, playerOffensive.Position == "DF", playerOffensive.minutes >= minutes
                , playerOffensive.Age <= age, playerOffensive.tier >= tier, playerOffensive.season == viewed_season)
    dfOPlayers = dfOStats.order_by(playerOffensive.Gls.desc(), playerOffensive.SoTP90.desc()).limit(10)
    # for player in dfOPlayers:
    #     print(player.Name)
    
    #Passing DF LPP90, 
    dfPStats = playerPassing.query.filter(playerPassing.League == League, playerPassing.Position == "DF", playerPassing.minutes >= minutes,
                playerPassing.Age <= age, playerPassing.tier >= tier, playerPassing.season == viewed_season)
    dfPPlayers = dfPStats.order_by(playerPassing.LPP.desc(), playerPassing.FTP90.desc(), playerPassing.ProgP90.desc()).limit(10)
    # for player in dfPPlayers:
    #     print(player.Name)

    #Not REALLY Satisfied with this one, data could be updated. Seems to be that 
    #defensive df
    dfDStats = playerDefensive.query.filter(playerDefensive.League == League, playerDefensive.Position == "DF", playerDefensive.minutes >= minutes,
                playerDefensive.Age <= age, playerDefensive.tier >= tier, playerDefensive.season == viewed_season)
    dfDPlayers = dfDStats.order_by(playerDefensive.TklRate.desc(), playerDefensive.TklIntP90.desc(), playerDefensive.BlkP90.desc(), playerDefensive.tier,).limit(10)
    # for player in dfDPlayers:
    #     print(player.Name)
    return [dfOPlayers, dfPPlayers, dfDPlayers]
@app.route('/<League>/TopPlayers')
def topplayers(League, viewed_season = current_season):
    try:
        players = playerOverview.query.filter(playerOverview.League == League, playerOverview.minutes > 0).all()
        # Three methods, forwards, midfielders, defenders

        #age under 50, tier 1 or higher, at least 1000 minutes
        fwList = findBestFW(League, 50, 1, 1000, viewed_season)
        mfList = findBestMF(League, 50, 1, 1000, viewed_season)
        dfList = findBestDF(League, 50, 1, 1000, viewed_season)

        return render_template("topplayers.html", League = players[0].League, fwList = fwList, mfList = mfList, dfList = dfList)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/<League>/TopProspects')
def topprospects(League, viewed_season = current_season):
    try:
        players = playerOverview.query.filter(playerOverview.League == League, playerOverview.minutes > 0, playerOverview.season == viewed_season).all()
        # Three methods, forwards, midfielders, defenders

        #age under 50, tier 1 or higher, at least 1000 minutes
        fwList = findBestFW(League, 23, 2, 700, viewed_season)
        mfList = findBestMF(League, 23, 2, 700, viewed_season)
        dfList = findBestDF(League, 23, 2, 700, viewed_season)

        return render_template("topprospects.html", League = players[0].League, fwList = fwList, mfList = mfList, dfList = dfList)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == "__main__":
    app.run(debug=True)