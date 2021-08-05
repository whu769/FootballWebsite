from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func
import sqlite3
import numpy as np


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
    GFP90 = db.Column(db.Float)
    GAP90 = db.Column(db.Float)
    xGP90 = db.Column(db.Float)
    xGAP90 = db.Column(db.Float)
    League = db.Column(db.Text)
    season = db.Column(db.Text)
    tier = db.Column(db.Integer)

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
    tier = db.Column(db.Integer)

class teamDefense(db.Model):
    __tablename__ = 'team_defense'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    PlayersUsed = db.Column(db.Integer)
    Nineties = db.Column(db.Integer)
    TklTot = db.Column(db.Integer)
    TklW = db.Column(db.Integer)
    TklD3 = db.Column(db.Integer)
    TklM3 = db.Column(db.Integer)
    TklA3 = db.Column(db.Integer)
    TklDribTot = db.Column(db.Integer)
    TklDribAtt = db.Column(db.Integer)
    TklDribP = db.Column(db.Float)
    TklDribFail = db.Column(db.Integer)
    PressTot = db.Column(db.Integer)
    PressSucc = db.Column(db.Integer)
    PressP = db.Column(db.Float)
    PressD3 = db.Column(db.Integer)
    PressM3 = db.Column(db.Integer)
    PressA3 = db.Column(db.Integer)
    BlkTot = db.Column(db.Integer)
    BlkSh = db.Column(db.Integer)
    BlkShSv = db.Column(db.Integer)
    BlkPass = db.Column(db.Integer)
    Int = db.Column(db.Integer)
    IntTkl = db.Column(db.Integer)
    Clr = db.Column(db.Integer)
    Err = db.Column(db.Integer)
    TklTotalP = db.Column(db.Float)
    PressD3P = db.Column(db.Float)
    PressM3P = db.Column(db.Float)
    PressA3P = db.Column(db.Float)
    ErrP90 = db.Column(db.Float)
    league = db.Column(db.Text)
    season = db.Column(db.Text)
    tier = db.Column(db.Integer)



class teamGSC(db.Model):
    __tablename__ = 'team_gsc'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    PlayersUsed = db.Column(db.Integer)
    Nineties = db.Column(db.Integer)
    SCA = db.Column(db.Integer)
    SCA90 = db.Column(db.Float)
    SCAPL = db.Column(db.Integer)
    SCAPD = db.Column(db.Integer)
    SCADrib = db.Column(db.Integer)
    SCASh = db.Column(db.Integer)
    SCAFld = db.Column(db.Integer)
    SCADef = db.Column(db.Integer)
    GCA = db.Column(db.Integer)
    GCA90 = db.Column(db.Float)
    GCAPL = db.Column(db.Integer)
    GCAPD = db.Column(db.Integer)
    GCADrib = db.Column(db.Integer)
    GCASh = db.Column(db.Integer)
    GCAFld = db.Column(db.Integer)
    GCADef = db.Column(db.Integer)
    league = db.Column(db.Text)
    season = db.Column(db.Text)
    tier = db.Column(db.Integer)

class teamPassing(db.Model):
    __tablename__ = 'team_passing'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    PlayersUsed = db.Column(db.Integer)
    Nineties = db.Column(db.Integer)
    CmpPasses = db.Column(db.Integer)
    AttPasses = db.Column(db.Integer)
    CmpP = db.Column(db.Float)
    TotDist = db.Column(db.Integer)
    PrgDist = db.Column(db.Integer)
    ShortCmp = db.Column(db.Integer)
    ShortAtt = db.Column(db.Integer)
    ShortCmpP = db.Column(db.Float)
    MedCmp = db.Column(db.Integer)
    MedAtt = db.Column(db.Integer)
    MedCmpP = db.Column(db.Float)
    LongCmp = db.Column(db.Integer)
    LongAtt = db.Column(db.Integer)
    LongCmpP = db.Column(db.Float)
    Ast = db.Column(db.Integer)
    xA = db.Column(db.Float)
    xA_diff = db.Column(db.Float)
    KP = db.Column(db.Integer)
    FinalThird = db.Column(db.Integer)
    PPA = db.Column(db.Integer)
    CrsPA = db.Column(db.Integer)
    Prog = db.Column(db.Integer)
    passP = db.Column(db.Float)
    KPP90 = db.Column(db.Float)
    FTP90 = db.Column(db.Float)
    PPAP90 = db.Column(db.Float)
    CrsPAP90 = db.Column(db.Float)
    ProgP90 = db.Column(db.Float)
    league = db.Column(db.Text)
    season = db.Column(db.Text)
    tier = db.Column(db.Integer)

class teamShooting(db.Model):
    __tablename__ = 'team_shooting'
    index = db.Column(db.Integer, primary_key = True)
    Team = db.Column(db.Text)
    PlayersUsed = db.Column(db.Integer)
    Nineties = db.Column(db.Integer)
    Gls = db.Column(db.Integer)
    Sh = db.Column(db.Integer)
    SoT = db.Column(db.Integer)
    SoTP = db.Column(db.Float)
    SoTP90 = db.Column(db.Float)
    GPSh = db.Column(db.Float)
    GPSoT = db.Column(db.Float)
    Dist = db.Column(db.Float)
    FK = db.Column(db.Integer)
    PKMade = db.Column(db.Integer)
    PKAtt = db.Column(db.Integer)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    npxGPSh = db.Column(db.Float)
    xG_diff = db.Column(db.Float)
    npxG_diff = db.Column(db.Float)
    league = db.Column(db.Text)
    season = db.Column(db.Text)
    tier = db.Column(db.Integer)
    
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

class playerPlaytime(db.Model):
    __tablename__ = 'player_playtime'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    Country = db.Column(db.Text)
    Position = db.Column(db.Text)
    Age = db.Column(db.Integer)
    MP = db.Column(db.Integer)
    MNpMP = db.Column(db.Integer)
    MinP = db.Column(db.Float)
    Nineties = db.Column(db.Float)
    Starts = db.Column(db.Integer)
    MNpStarts = db.Column(db.Integer)
    Subs = db.Column(db.Integer)
    MNpSubs = db.Column(db.Integer)
    unSub = db.Column(db.Integer)
    PPM = db.Column(db.Float)
    onG = db.Column(db.Integer)
    onGA = db.Column(db.Integer)
    onxG = db.Column(db.Float)
    onxGA = db.Column(db.Float)
    onGP90 = db.Column(db.Float)
    onGAP90 = db.Column(db.Float)
    onxGP90 = db.Column(db.Float)
    onxGAP90 = db.Column(db.Float)
    team = db.Column(db.Text)
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
        # aSignings = offenseRec.query.filter(offenseRec.recommendedTeam == Team, offenseRec.season == viewed_season).all()
        # dSignings = defenseRec.query.filter(defenseRec.recommendedTeam == Team, defenseRec.season == viewed_season).all()

        #test analyzeTeam method
        # analysis_lst = analyzeTeam(Team)
        # analysis_pts = analysis_lst[0]
        # analysis_indices = analysis_lst[1]

        # print(analysis_lst)
        #generateSignings(Team)
        
        analysis_lst = analyzeTeam(Team)
        analysis_pts = analysis_lst[0]
        analysis_indices = analysis_lst[1]
        teamDict = analysis_lst[2]

        best_category = teamDict[analysis_indices[0]]
        worst_category = teamDict[analysis_indices[len(analysis_indices)-1]]
        bc_val = analysis_pts[analysis_indices[0]]
        wc_val = analysis_pts[analysis_indices[len(analysis_indices)-1]]

        def genMsg(val, category):
            if val in range(-2,3):
                return f"{category} is at or hovering around their competitors"
            elif val < -2 and val > -5:
                return f"{category} is below their competitors and could use improvements"
            elif val < -5:
                return f"{category} is considerably below their competitors and need improvement"
            elif val > 2 and val < 5:
                return f"{category} is above their competitors"
            else:
                return f"{category} is considerably above their competitors"
        
        bc_msg = genMsg(bc_val, best_category)
        wc_msg = genMsg(wc_val, worst_category)
        print(bc_msg)
        print(wc_msg)
        # print(best_category)
        # print(worst_category)
        #should write method that based off category shows some stats compared to other teams

        
        return render_template("team3.html", Team = team, tO = tAdvanced, Player = players, Goals = goals, Assists = assists, bc = best_category, wc = worst_category,
                                bc_msg = bc_msg, wc_msg = wc_msg)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

#method to look through the team's general stats GSC, Defense, Passing, shooting and categorizes them
def analyzeTeam(Team):
    #Later on, possibly separate into 4 inner methods for passing, gsc, defense, shooting
    
    #Obtain all information regarding specifically the team
    team_standard = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == current_season).all()
    team_overview = teamOverview.query.filter(teamOverview.Team == Team, teamOverview.season == current_season).all()
    team_gsc = teamGSC.query.filter(teamGSC.Team == Team, teamGSC.season == current_season).all()
    team_defense = teamDefense.query.filter(teamDefense.Team == Team, teamDefense.season == current_season).all()
    team_passing = teamPassing.query.filter(teamPassing.Team == Team, teamPassing.season == current_season).all()
    team_shooting = teamShooting.query.filter(teamShooting.Team == Team, teamShooting.season == current_season).all()

    league = team_gsc[0].league #league the team is in
    tier = team_gsc[0].tier #tier the team is in
    team = team_gsc[0].Team

    #Opponent information (Same tier competitors, AVG tier, and everyone else)
    opp_gsc_query = teamGSC.query.filter(teamGSC.Team != Team, teamGSC.season == current_season, teamGSC.league == league)
    opp_defense_query = teamDefense.query.filter(teamDefense.Team != Team, teamDefense.season == current_season, teamDefense.league == league)
    opp_passing_query = teamPassing.query.filter(teamPassing.Team != Team, teamPassing.season == current_season, teamPassing.league == league)
    opp_shooting_query = teamShooting.query.filter(teamShooting.Team != Team, teamShooting.season == current_season, teamShooting.league == league)
    opp_team_overview = combinedLeagues.query.filter(combinedLeagues.Team != Team, combinedLeagues.season == current_season, combinedLeagues.League == league)
    
    
    #print("Tier: " + str(tier))
    def assessGSC(team_gsc, opp_gsc_query, tier):
        team_gsc_vals = [team_gsc[0].GCA90, team_gsc[0].SCA90, (team_gsc[0].GCA90/team_gsc[0].SCA90)]
        #print(f'{team_gsc[0].Team} values: {team_gsc_vals}')
        #T1 gsc (tier avg, individual tier, everyone else)
        gca_lst = [] #list to compare all of the things mentioned above
        sca_lst = []
        gsp_lst = []
        tier_opp_gsc = opp_gsc_query.filter(teamGSC.tier == tier)
        tier_opp_gca_avg = (tier_opp_gsc.with_entities(func.sum(teamGSC.GCA90).label("GCA90Sum")).first().GCA90Sum) / len(tier_opp_gsc.all())
        tier_opp_sca_avg = (tier_opp_gsc.with_entities(func.sum(teamGSC.SCA90).label("SCA90Sum")).first().SCA90Sum) / len(tier_opp_gsc.all())
        tier_opp_gsp_avg = (tier_opp_gsc.with_entities(func.sum(teamGSC.GCA90 / teamGSC.SCA90).label("GSPSum")).first().GSPSum) / len(tier_opp_gsc.all())

        
        #appends gca_lst 
        if(tier_opp_gca_avg > team_gsc[0].GCA90):
            gca_lst.append(-1)
        elif(tier_opp_gca_avg < team_gsc[0].GCA90):
            gca_lst.append(1)
        else:
            gca_lst.append(0)

        #appends sca_lst
        if(tier_opp_sca_avg > team_gsc[0].SCA90):
            sca_lst.append(-1)
        elif(tier_opp_sca_avg < team_gsc[0].SCA90):
            sca_lst.append(1)
        else:
            sca_lst.append(0)
        
        if(tier_opp_gsp_avg > team_gsc_vals[2]):
            gsp_lst.append(-1)
        elif(tier_opp_gsp_avg < team_gsc_vals[2]):
            gsp_lst.append(1)
        else:
            gsp_lst.append(0)

        #print("Tier Avg")
        for team in tier_opp_gsc.all():
            # print(team.Team)
            opp_gca = team.GCA90
            opp_sca = team.SCA90
            opp_gsp = opp_gca / opp_sca
            if(opp_gca > team_gsc[0].GCA90):
                gca_lst.append(-1)
            elif(opp_gca < team_gsc[0].GCA90):
                gca_lst.append(1)
            else:
                gca_lst.append(0)

            if(opp_sca > team_gsc[0].SCA90):
                sca_lst.append(-1)
            elif(opp_sca < team_gsc[0].SCA90):
                sca_lst.append(1)
            else:
                sca_lst.append(0)
            
            if(opp_gsp > team_gsc_vals[2]):
                gsp_lst.append(-1)
            elif(opp_gsp < team_gsc_vals[2]):
                gsp_lst.append(1)
            else:
                gsp_lst.append(0)

        #print("League Avg")
        league_opp_gca_avg = (opp_gsc_query.with_entities(func.sum(teamGSC.GCA90).label("GCA90Sum")).first().GCA90Sum) / len(opp_gsc_query.all())
        league_opp_sca_avg = (opp_gsc_query.with_entities(func.sum(teamGSC.SCA90).label("SCA90Sum")).first().SCA90Sum) / len(opp_gsc_query.all())
        league_opp_gsp_avg = (opp_gsc_query.with_entities(func.sum(teamGSC.GCA90 / teamGSC.SCA90).label("GSPSum")).first().GSPSum) / len(opp_gsc_query.all())
        
        if(league_opp_gca_avg > team_gsc[0].GCA90):
            gca_lst.append(-1)
        elif(league_opp_gca_avg < team_gsc[0].GCA90):
            gca_lst.append(1)
        else:
            gca_lst.append(0)
        
        if(league_opp_sca_avg > team_gsc[0].SCA90):
            sca_lst.append(-1)
        elif(league_opp_sca_avg < team_gsc[0].SCA90):
            sca_lst.append(1)
        else:
            sca_lst.append(0)
        
        if(league_opp_gsp_avg > team_gsc_vals[2]):
            gsp_lst.append(-1)
        elif(league_opp_gsp_avg < team_gsc_vals[2]):
            gsp_lst.append(1)
        else:
            gsp_lst.append(0)
        
        # print(gca_lst)
        # print(sca_lst)
        # print(gsp_lst)
        # print([sum(gca_lst) , sum(sca_lst) , sum(gsp_lst)])
        results_lst = [sum(gca_lst) , sum(sca_lst) , sum(gsp_lst)]
        return results_lst
    
    def assessDefense(team_standard, team_defense, opp_defense_query, opp_team_overview,tier):
        # t.TklTotalP, t.ErrP90, GAP90, xGAP90
        team_def_vals = [team_defense[0].TklTotalP, team_defense[0].ErrP90, team_standard[0].GAP90, team_standard[0].xGAP90]
        #print(f'{team_standard[0].Team} values: {team_def_vals}')

        tklP_lst = []
        err_lst = []
        ga_lst = []
        xga_lst = []

        tier_opp_defense = opp_defense_query.filter(teamDefense.tier == tier)
        tier_opp_tkl_avg = (tier_opp_defense.with_entities(func.sum(teamDefense.TklTotalP).label("TklSum")).first().TklSum) / (len(tier_opp_defense.all()))
        tier_opp_err_avg = (tier_opp_defense.with_entities(func.sum(teamDefense.ErrP90).label("ErrSum")).first().ErrSum) / (len(tier_opp_defense.all()))

        tier_opp_ga = opp_team_overview.filter(combinedLeagues.tier == tier)
        tier_opp_ga_avg = tier_opp_ga.with_entities(func.sum(combinedLeagues.GAP90).label('GASum')).first().GASum / len(tier_opp_ga.all())
        tier_opp_xga_avg = tier_opp_ga.with_entities(func.sum(combinedLeagues.xGAP90).label('xGASum')).first().xGASum / len(tier_opp_ga.all())
        
        # print(len(tier_opp_defense.all()))
        # print(tier_opp_tkl_avg)
        #print("Tier avg")
        if(tier_opp_tkl_avg > team_def_vals[0]):
            tklP_lst.append(1)
        elif(tier_opp_tkl_avg < team_def_vals[0]):
            tklP_lst.append(-1)
        else:
            tklP_lst.append(0)

        if(tier_opp_err_avg > team_def_vals[1]):
            err_lst.append(1)
        elif(tier_opp_err_avg < team_def_vals[1]):
            err_lst.append(-1)
        else:
            err_lst.append(0)
        
        if(tier_opp_ga_avg > team_def_vals[2]):
            ga_lst.append(1)
        elif(tier_opp_ga_avg < team_def_vals[2]):
            ga_lst.append(-1)
        else:
            ga_lst.append(0)
        
        if(tier_opp_xga_avg > team_def_vals[3]):
            xga_lst.append(1)
        elif(tier_opp_xga_avg < team_def_vals[3]):
            xga_lst.append(-1)
        else:
            xga_lst.append(0)
        
        for team in tier_opp_defense.all():
            #print(team.Team)

            if(team.TklTotalP > team_def_vals[0]):
                tklP_lst.append(1)
            elif(team.TklTotalP < team_def_vals[0]):
                tklP_lst.append(-1)
            else:
                tklP_lst.append(0)
            
            if(team.ErrP90 > team_def_vals[1]):
                err_lst.append(1)
            elif(team.ErrP90 < team_def_vals[1]):
                err_lst.append(-1)
            else:
                err_lst.append(0)
        
        for team in tier_opp_ga.all():
            # print(team.Team)
            if(team.GAP90 > team_def_vals[2]):
                ga_lst.append(1)
            elif(team.GAP90 < team_def_vals[2]):
                ga_lst.append(-1)
            else:
                ga_lst.append(0)

            if(team.xGAP90 > team_def_vals[3]):
                xga_lst.append(1)
            elif(team.xGAP90 < team_def_vals[3]):
                xga_lst.append(-1)
            else:
                xga_lst.append(0)


        # print("League avg")
        opp_tkl_avg = (opp_defense_query.with_entities(func.sum(teamDefense.TklTotalP).label("TklSum")).first().TklSum) / (len(opp_defense_query.all()))
        opp_err_avg = (opp_defense_query.with_entities(func.sum(teamDefense.ErrP90).label('ErrSum')).first().ErrSum) / (len(opp_defense_query.all()))
        opp_ga_avg = opp_team_overview.with_entities(func.sum(combinedLeagues.GAP90).label('GASum')).first().GASum / len(opp_team_overview.all())
        opp_xga_avg = opp_team_overview.with_entities(func.sum(combinedLeagues.xGAP90).label('xGASum')).first().xGASum / len(opp_team_overview.all())
        #print(opp_tkl_avg)
        if (opp_tkl_avg > team_def_vals[0]):
            tklP_lst.append(1)
        elif(opp_tkl_avg < team_def_vals[0]):
            tklP_lst.append(-1)
        else:
            tklP_lst.append(0)
        
        if(opp_err_avg > team_def_vals[1]):
            err_lst.append(1)
        elif(opp_err_avg < team_def_vals[1]):
            err_lst.append(-1)
        else:
            err_lst.append(0)
        
        if(opp_ga_avg > team_def_vals[2]):
            ga_lst.append(1)
        elif(opp_ga_avg < team_def_vals[2]):
            ga_lst.append(-1)
        else:
            ga_lst.append(0)
        
        if(opp_xga_avg > team_def_vals[3]):
            xga_lst.append(1)
        elif(opp_xga_avg < team_def_vals[3]):
            xga_lst.append(-1)
        else:
           xga_lst.append(0)



        # print(tklP_lst)
        # print(err_lst)
        # print(ga_lst)
        # print(xga_lst)
        # print([sum(tklP_lst), sum(err_lst), sum(ga_lst), sum(xga_lst)])
        results_lst = [sum(tklP_lst), sum(err_lst), sum(ga_lst), sum(xga_lst)]
        return results_lst
    
    def assessPassing(team_passing, opp_passing_query, tier):
        team_pass_vals = [team_passing[0].passP, team_passing[0].KPP90, team_passing[0].FTP90]
        # print(f'{team_passing[0].Team} values: {team_pass_vals}')

        passP_lst = []
        kp_lst = []
        ftp_lst = []

        tier_passing = opp_passing_query.filter(teamPassing.tier == tier)
        tier_passP_avg = tier_passing.with_entities(func.sum(teamPassing.passP).label('passSum')).first().passSum / len(tier_passing.all())
        tier_kpp_avg = tier_passing.with_entities(func.sum(teamPassing.KPP90).label("kpSum")).first().kpSum / len(tier_passing.all())
        tier_ftp_avg = tier_passing.with_entities(func.sum(teamPassing.FTP90).label("ftpSum")).first().ftpSum / len(tier_passing.all())

        #print(tier_passP_avg)
        #print(tier_kpp_avg)

        #print("Tier avg")
        if(tier_passP_avg > team_pass_vals[0]):
            passP_lst.append(-1)
        elif(tier_passP_avg < team_pass_vals[0]):
            passP_lst.append(1)
        else:
            passP_lst.append(0)


        if(tier_kpp_avg > team_pass_vals[1]):
            kp_lst.append(-1)
        elif(tier_kpp_avg < team_pass_vals[1]):
            kp_lst.append(1)
        else:
            kp_lst.append(0)

        if(tier_ftp_avg > team_pass_vals[2]):
            ftp_lst.append(-1)
        elif(tier_ftp_avg < team_pass_vals[2]):
            ftp_lst.append(1)
        else:
            ftp_lst.append(0)
        
        for team in tier_passing.all():
            #print(team.Team)

            if(team.passP > team_pass_vals[0]):
                passP_lst.append(-1)
            elif(team.passP < team_pass_vals[0]):
                passP_lst.append(1)
            else:
                passP_lst.append(0)

            if(team.KPP90 > team_pass_vals[1]):
                kp_lst.append(-1)
            elif(team.KPP90 < team_pass_vals[1]):
                kp_lst.append(1)
            else:
                kp_lst.append(0)
            
            if(team.FTP90 > team_pass_vals[2]):
                ftp_lst.append(-1)
            elif(team.FTP90 < team_pass_vals[2]):
                ftp_lst.append(1)
            else:
                ftp_lst.append(0)
        
        #print("League avg")
        opp_passP_avg = opp_passing_query.with_entities(func.sum(teamPassing.passP).label('passSum')).first().passSum / len(opp_passing_query.all())
        opp_kpp_avg = opp_passing_query.with_entities(func.sum(teamPassing.KPP90).label('kpSum')).first().kpSum / len(opp_passing_query.all())
        opp_ftp_avg = opp_passing_query.with_entities(func.sum(teamPassing.FTP90).label('ftpSum')).first().ftpSum / len(opp_passing_query.all())
        #print(opp_passP_avg)
        
        if(opp_passP_avg > team_pass_vals[0]):
            passP_lst.append(-1)
        elif(opp_passP_avg < team_pass_vals[0]):
            passP_lst.append(1)
        else:
            passP_lst.append(0)

        if(opp_kpp_avg > team_pass_vals[1]):
            kp_lst.append(-1)
        elif(opp_kpp_avg < team_pass_vals[1]):
            kp_lst.append(1)
        else:
            kp_lst.append(0)

        if(opp_ftp_avg > team_pass_vals[2]):
            ftp_lst.append(-1)
        elif(opp_ftp_avg < team_pass_vals[2]):
            ftp_lst.append(1)
        else:
            ftp_lst.append(0)
        
        # print(passP_lst)
        # print(kp_lst)
        # print(ftp_lst)
        # print([sum(passP_lst), sum(kp_lst), sum(ftp_lst)])
        results_lst = [sum(passP_lst), sum(kp_lst), sum(ftp_lst)]
        return results_lst

    def assessShooting(team_shooting, opp_shooting_query, tier):
        team_shot_vals = [team_shooting[0].SoTP90, team_shooting[0].GPSoT, team_shooting[0].xG_diff]
        # print(f'{team_shooting[0].Team} values: {team_shot_vals}')

        sotp_lst = []
        gpsot_lst = []
        xgd_lst = []

        tier_shooting = opp_shooting_query.filter(teamShooting.tier == tier)
        tier_sotp_avg = tier_shooting.with_entities(func.sum(teamShooting.SoTP90).label('sotpSum')).first().sotpSum / len(tier_shooting.all())
        tier_gpsot_avg = tier_shooting.with_entities(func.sum(teamShooting.GPSoT).label('gpsotSum')).first().gpsotSum / len(tier_shooting.all())
        tier_xgd_avg = tier_shooting.with_entities(func.sum(teamShooting.xG_diff).label('xgdSum')).first().xgdSum / len(tier_shooting.all())
        # print(tier_sotp_avg)
        # print(tier_gpsot_avg)

        if(tier_sotp_avg < team_shot_vals[0]):
            sotp_lst.append(1)
        elif(tier_sotp_avg > team_shot_vals[0]):
            sotp_lst.append(-1)
        else:
            sotp_lst.append(0)
        
        if(tier_gpsot_avg < team_shot_vals[1]):
            gpsot_lst.append(1)
        elif(tier_gpsot_avg > team_shot_vals[1]):
            gpsot_lst.append(-1)
        else:
            gpsot_lst.append(0)
        
        if(tier_xgd_avg < team_shot_vals[2]):
            xgd_lst.append(1)
        elif(tier_xgd_avg > team_shot_vals[2]):
            xgd_lst.append(-1)
        else:
            xgd_lst.append(0)
        
        for team in tier_shooting.all():
            #print(team.Team)
            # print(team.SoTP90)

            if(team.SoTP90 < team_shot_vals[0]):
                sotp_lst.append(1)
            elif(team.SoTP90 > team_shot_vals[0]):
                sotp_lst.append(-1)
            else:
                sotp_lst.append(0)
            
            if(team.GPSoT < team_shot_vals[1]):
                gpsot_lst.append(1)
            elif(team.GPSoT > team_shot_vals[1]):
                gpsot_lst.append(-1)
            else:
                gpsot_lst.append(0)
            
            if(team.xG_diff < team_shot_vals[2]):
                xgd_lst.append(1)
            elif(team.xG_diff > team_shot_vals[2]):
                xgd_lst.append(-1)
            else:
                xgd_lst.append(0)
        
        lg_sotp_avg = opp_shooting_query.with_entities(func.sum(teamShooting.SoTP90).label('sotpSum')).first().sotpSum / len(opp_shooting_query.all())
        lg_gpsot_avg = opp_shooting_query.with_entities(func.sum(teamShooting.GPSoT).label('gpsotSum')).first().gpsotSum / len(opp_shooting_query.all())
        lg_xgd_avg = opp_shooting_query.with_entities(func.sum(teamShooting.xG_diff).label('xgdSum')).first().xgdSum / len(opp_shooting_query.all())
        # print(lg_sotp_avg)
        # print(lg_gpsot_avg)
        # print(lg_xgd_avg)
        
        
        if(lg_sotp_avg < team_shot_vals[0]):
            sotp_lst.append(1)
        elif(lg_sotp_avg > team_shot_vals[0]):
            sotp_lst.append(-1)
        else:
            lg_lst.append(0)
        
        if(lg_gpsot_avg < team_shot_vals[1]):
            gpsot_lst.append(1)
        elif(lg_gpsot_avg > team_shot_vals[1]):
            gpsot_lst.append(-1)
        else:
            gpsot_lst.append(0)
        
        if(lg_xgd_avg < team_shot_vals[2]):
            xgd_lst.append(1)
        elif(lg_xgd_avg > team_shot_vals[2]):
            xgd_lst.append(-1)
        else:
            xgd_lst.append(0)

        # print(sotp_lst)
        # print(gpsot_lst)
        # print(xgd_lst)
        # print([sum(sotp_lst), sum(gpsot_lst), sum(xgd_lst)])
        results_lst = [sum(sotp_lst), sum(gpsot_lst), sum(xgd_lst)]
        return results_lst
        
    gsc_lst = assessGSC(team_gsc, opp_gsc_query, tier)
    shot_lst = assessShooting(team_shooting, opp_shooting_query, tier)
    pass_lst = assessPassing(team_passing, opp_passing_query, tier)
    def_lst = assessDefense(team_standard, team_defense, opp_defense_query, opp_team_overview, tier)

    overall_lst = [sum(gsc_lst), sum(shot_lst), sum(pass_lst), sum(def_lst)] #ORDER: GSC, SHOT, PASS, DEF
    #print(overall_lst)

    def createIndexLst(overall_lst):
        overall_copy = [val for val in overall_lst]
        overall_copy = list(set(overall_copy))
        overall_copy.sort()
        overall_copy.reverse()
        #print(overall_copy)

        index_lst = []
        for val in overall_copy:
            
            for i in range(len(overall_lst)):
                if overall_lst[i] == val:
                    index_lst.append(i)

        # print(index_lst)
        return index_lst
    
    index_lst = createIndexLst(overall_lst)
    teamDict = {0 : 'Goal Shot Creation', 1 : 'Shooting', 2 : 'Passing', 3 : 'Defense'} #legend
    # best_category = teamDict[index_lst[0]]
    # worst_category = teamDict[index_lst[len(index_lst) - 1]]
    # print(f'Best category: {best_category}')
    # print(f'Worst category: {worst_category}')
    
    #need to return overall list, index list which will ultimately set up a more personalized recommendor
    return [overall_lst, index_lst, teamDict]

def recommendGSC(Team, priority):
    team = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == current_season).first()
    #Want two options. If GSC is not a priority fix, find prospects. If it is, find proven good players. All tiers balls to the wall
    gsc_players = gsCreation.query.filter(gsCreation.Team != Team, gsCreation.season == current_season)
    players = []
    if priority == "high": #Find the best CAM/Winger/Creative player <32yrs, >1000min
        potential_signings = gsc_players.filter(gsCreation.Age <= 32, gsCreation.minutes >= 1000, gsCreation.tier >= team.tier)
        cams = potential_signings.filter(gsCreation.Position.contains("MF"))
        cams = cams.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)
        fws = potential_signings.filter(gsCreation.Position.contains("FW"))
        fws = fws.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)
        players = [cams, fws]
    elif priority == "med": #Find good player tier below age cap, <28yrs >1000min
        potential_signings = gsc_players.filter(gsCreation.Age <= 28, gsCreation.minutes >= 1000, gsCreation.tier > team.tier)
        cams = potential_signings.filter(gsCreation.Position.contains("MF"))
        cams = cams.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)
        fws = potential_signings.filter(gsCreation.Position.contains("FW"))
        fws = fws.order_by(gsCreation.GCAP90.desc(), gsCreation.SCAP90.desc()).limit(10)
        players = [cams, fws]
    else: #find an upcoming prospect <24yrs <700min
        potential_signings = gsc_players.filter(gsCreation.Age <= 24, gsCreation.minutes >= 700, gsCreation.tier > team.tier)
        cams = potential_signings.filter(gsCreation.Position.contains("MF"))
        cams = cams.order_by(gsCreation.SCAP90.desc(), gsCreation.GCAP90.desc()).limit(10)
        fws = potential_signings.filter(gsCreation.Position.contains("FW"))
        fws = fws.order_by(gsCreation.SCAP90.desc(), gsCreation.GCAP90.desc()).limit(10)
        players = [cams, fws]
    
    # for lst in players:
    #     print("-------------------------------------------------------")
    #     for player in lst:
    #         print(player.Name)
    
    return players

def recommendStriker(Team, priority):
    team = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == current_season).first()

    strikers = playerOffensive.query.filter(playerOffensive.Team != Team, playerOffensive.season == current_season)
    players = []
    
    if priority == "high": #<32yrs, >1000min
        potential_signings = strikers.filter(playerOffensive.Age <= 32, playerOffensive.minutes >= 1000, playerOffensive.tier >= team.tier)
        st = potential_signings.order_by(playerOffensive.Gls.desc(), playerOffensive.GlsP90.desc(), playerOffensive.xG.desc()).limit(10)
        players.append(st)
    elif priority == "med": #Find good player tier below age cap, <28yrs >1000min
        potential_signings = strikers.filter(playerOffensive.Age <= 28, playerOffensive.minutes >= 1000, playerOffensive.tier > team.tier)
        st = potential_signings.order_by(playerOffensive.GlsP90.desc(), playerOffensive.xG.desc(), playerOffensive.Gls.desc()).limit(10)
        players.append(st)
    else: #find an upcoming prospect <24yrs <700min
        potential_signings = strikers.filter(playerOffensive.Age <= 24, playerOffensive.minutes >= 700, playerOffensive.tier > team.tier)
        st = potential_signings.order_by(playerOffensive.ShP90.desc(), playerOffensive.SoTP90.desc(), playerOffensive.xG.desc()).limit(10)
        players.append(st)
    
    # for player in players[0]:
    #     print(player.Name)
    
    return players

def recommendMF(Team, priority):
    team = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == current_season).first()
    
    mf = playerPassing.query.filter(playerPassing.Team != Team, playerPassing.season == current_season, playerPassing.Position.contains("MF"))
    players = []

    if priority == "high": # <32yrs, >1000min
        potential_signings = mf.filter(playerPassing.tier >= team.tier, playerPassing.Age <= 32, playerPassing.minutes >= 1000)
        mfs = potential_signings.order_by(playerPassing.ProgP90.desc(), playerPassing.KPP90.desc(), playerPassing.FTP90.desc(), playerPassing.PassP.desc()).limit(10)
        players.append(mfs)
    elif priority == "med": #Find good player tier below age cap, <28yrs >1000min
        potential_signings = mf.filter(playerPassing.tier > team.tier, playerPassing.Age <= 28, playerPassing.minutes >= 1000)
        mfs = potential_signings.order_by(playerPassing.ProgP90.desc(), playerPassing.KPP90.desc(), playerPassing.FTP90.desc(), playerPassing.PassP.desc()).limit(10)
        players.append(mfs)
    else: #find an upcoming prospect <24yrs <700min
        potential_signings = mf.filter(playerPassing.tier > team.tier, playerPassing.Age <= 24, playerPassing.minutes >= 700)
        mfs = potential_signings.order_by(playerPassing.ProgP90.desc(), playerPassing.KPP90.desc(), playerPassing.FTP90.desc(), playerPassing.PassP.desc()).limit(10)
        players.append(mfs)
    
    # for player in players[0]:
    #     print(player.Name)
    
    return players

def recommendDef(Team, priority):
    team = combinedLeagues.query.filter(combinedLeagues.Team == Team, combinedLeagues.season == current_season).first()
    
    cdms = playerDefensive.query.filter(playerDefensive.Team != Team, playerDefensive.season == current_season, playerDefensive.Position.contains("MF"))
    defs = playerPlaytime.query.filter(playerPlaytime.team != Team, playerPlaytime.season == current_season, playerPlaytime.Position == ("DF"))
    players = []

    #split between cdm and a df probably
    if priority == "high": # <32yrs, >1000min
        cdms = cdms.filter(playerDefensive.tier >= team.tier, playerDefensive.Age <= 32, playerDefensive.minutes >= 1000)
        cdms = cdms.order_by(playerDefensive.TklIntP90.desc(), playerDefensive.TklRate.desc(), playerDefensive.PressurePct.desc()).limit(10)
        defs = defs.filter(playerPlaytime.tier >= team.tier, playerPlaytime.Age <= 32, playerPlaytime.minutes >= 1000)
        defs = defs.order_by(playerPlaytime.onGAP90, playerPlaytime.onxGAP90).limit(10)
        players = [defs, cdms]
    elif priority == "med": #Find good player tier below age cap, <28yrs >1000min
        cdms = cdms.filter(playerDefensive.tier > team.tier, playerDefensive.Age <= 28, playerDefensive.minutes >= 1000)
        cdms = cdms.order_by(playerDefensive.TklIntP90.desc(), playerDefensive.TklRate.desc(), playerDefensive.PressurePct.desc()).limit(10)
        defs = defs.filter(playerPlaytime.tier > team.tier, playerPlaytime.Age <= 28, playerPlaytime.minutes >= 1000)
        defs = defs.order_by(playerPlaytime.onGAP90, playerPlaytime.onxGAP90).limit(10)
        players = [defs, cdms]
    else: #find an upcoming prospect <24yrs <700min
        cdms = cdms.filter(playerDefensive.tier > team.tier, playerDefensive.Age <= 24, playerDefensive.minutes >= 700)
        cdms = cdms.order_by(playerDefensive.TklIntP90.desc(), playerDefensive.TklRate.desc(), playerDefensive.PressurePct.desc()).limit(10)
        defs = defs.filter(playerPlaytime.tier > team.tier, playerPlaytime.Age <= 24, playerPlaytime.minutes >= 700)
        defs = defs.order_by(playerPlaytime.onGAP90, playerPlaytime.onxGAP90).limit(10)
        players = [defs, cdms]

    # for lst in players:
    #     print("-------------------------------------------------------")
    #     for player in lst:
    #         print(player.Name)

    return players

def generateSignings(Team):
    analysis_lst = analyzeTeam(Team)
    #print(analysis_lst)
    analysis_pts = analysis_lst[0]
    analysis_indices = analysis_lst[1]
    teamDict = analysis_lst[2]

    def determineRecommender(Team, index, val):
        priority_lst = ["high", "med", "low"]
        priority = ""

        if val < -2:
            priority = priority_lst[0]
        elif val > 5:
            priority = priority_lst[2]
        else:
            priority = priority_lst[1]
        
        #print(priority)
        
        if index == 0:
            #print("GSC")
            lst = recommendGSC(Team , priority)
        elif index == 1:
            #print("STRIKER")
            lst = recommendStriker(Team, priority)
        elif index == 2:
            #print("MF")
            lst = recommendMF(Team, priority)
        else:
            #print("DF")
            lst = recommendDef(Team, priority)
        
        return lst

    
    rec_dict = dict()
    for i in range(len(analysis_indices)):
        rec_dict[i] = determineRecommender(Team, i, analysis_pts[i])

    #0, 1, 2, 3 for keys, players as vals
    #print(rec_dict)
    return rec_dict
    
    

def createLeagueAvgs(League):
    # given the current season, compile all of the 20 teams in the league and create averages 
    # sort the GCA's, SCA's and create the parameters. 
    
    league_gsc = teamGSC.query.filter(teamGSC.league == League, teamGSC.season == current_season)
    league_gca = league_gsc.order_by(teamGSC.GCA90).all()
    league_sca = league_gsc.order_by(teamGSC.SCA90).all()

    gsc_dict = dict()
    for x in league_gca:
        # print(f'{x.Team} : {x.GCA90}')
        # print(f'{x.Team} : {x.SCA90}')
        # print(f'{x.Team} : {x.GCA90 / x.SCA90}')
        gsc_dict[x.Team] = [x.GCA90, x.SCA90, (x.GCA90/x.SCA90)]
    
    # for k, v in gsc_dict.items():
    #     print(f'{k}: GCA-{v[0]} SCA-{v[1]} Proportion-{v[2]}')

    #Defense, pressures
    league_GA = combinedLeagues.query.filter(combinedLeagues.League == League, combinedLeagues.season == current_season).order_by(
        combinedLeagues.GA).all()
    league_defense = teamDefense.query.filter(teamDefense.league == League, teamGSC.season == current_season)

    defense_dict = dict()
    for team in league_GA:
        t = league_defense.filter(teamDefense.Team == team.Team).first()
        defense_dict[team.Team] = [t.TklTotalP, t.PressD3P, t.PressM3P, t.PressA3P, t.ErrP90]

    # for k, v in defense_dict.items():
    #     print(f'{k}: {v[0]} {v[1]} {v[2]} {v[3]} {v[4]}')

    #league shooting
    league_shooting = teamShooting.query.filter(teamShooting.league == League, teamShooting.season == current_season).order_by(teamShooting.Gls).all()
    shooting_dict = dict()
    for team in league_shooting:
        # print(team.SoTP90)
        shooting_dict[team.Team] = [team.Gls, team.xG, team.npxG, team.SoTP90, team.xG_diff, team.npxG_diff]

    # for k, v in shooting_dict.items():
    #     print(f'{k}: {v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]}')

    league_passing = teamPassing.query.filter(teamPassing.league == League, teamPassing.season == current_season).order_by(teamPassing.CmpP.desc()).all()
    passing_dict = dict()

    for team in league_passing:
        passing_dict[team.Team] = [team.KPP90, team.FTP90, team.PPAP90, team.CrsPAP90, team.ProgP90]
    
    # for k, v in passing_dict.items():
    #     print(f'{k}: {v[0]} {v[1]} {v[2]} {v[3]} {v[4]}')

    dict_list = [gsc_dict, defense_dict, passing_dict, shooting_dict]

    return dict_list

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
        # print(pO.Team)
        # print(pO2.Team)
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

@app.route('/<League>/Stats')
def leaguestats(League):

    league_stats = createLeagueAvgs(League)
    gsc_dict = league_stats[0]
    shooting_dict = league_stats[3]
    passing_dict = league_stats[2]
    defense_dict = league_stats[1]

   
    #Goal Shot Creation Things
    gca_lst = [x[0] for x in gsc_dict.values()]
    sca_lst = [x[1] for x in gsc_dict.values()]
    gsprop_lst = [x[2] * 100 for x in gsc_dict.values()]

    #Shooting Things
    gls_lst = [x[0] for x in shooting_dict.values()]
    xG_lst = [x[1] for x in shooting_dict.values()]
    xG_diff_lst = [x[4] for x in shooting_dict.values()]
    # print(gls_lst)
    # print(test_list)
    # print(gsc_dict.keys())

    #Passing
    kp_lst = [x[0] for x in passing_dict.values()]
    ftp_lst = [x[1] for x in passing_dict.values()]
    ppa_lst = [x[2] for x in passing_dict.values()]
    crspa_lst = [x[3] for x in passing_dict.values()]
    #print(kp_lst)

    #Defense
    #t.TklTotalP, t.PressD3P, t.PressM3P, t.PressA3P
    tklP_lst = [x[0] for x in defense_dict.values()]
    d3pP_lst = [x[1] for x in defense_dict.values()]
    m3pP_lst = [x[2] for x in defense_dict.values()]
    a3pP_lst = [x[3] for x in defense_dict.values()]


    gsc_lists = [gca_lst , sca_lst, gsprop_lst]
    shot_lists = [gls_lst, xG_lst, xG_diff_lst]
    pass_lists = [kp_lst, ftp_lst, ppa_lst, crspa_lst]
    defense_lists = [tklP_lst, d3pP_lst, m3pP_lst, a3pP_lst]
    
    return render_template('leaguestats.html', League = League, gscLabels = list(gsc_dict.keys()), gcaData = gsc_lists[0], scaData = gsc_lists[1], gspropData = gsc_lists[2],
                            shotLabels = list(shooting_dict.keys()), glsData = shot_lists[0], xGData = shot_lists[1], xGDiffData = shot_lists[2]
                            , passLabels = list(passing_dict.keys()), kpData = pass_lists[0], ftpData = pass_lists[1], ppaData = pass_lists[2], crsData = pass_lists[3]
                            , defenseLabels = list(defense_dict.keys()), tklPData = defense_lists[0], d3pData = defense_lists[1], m3pData = defense_lists[2], a3pData = defense_lists[3])

if __name__ == "__main__":
    app.run(debug=True)