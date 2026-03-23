
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import engine, Batting, People, Teams

app = FastAPI()

@app.get("/years")
async def get_years():
    with Session(engine) as session:
        years = session.exec(select(Teams.yearID).distinct().order_by(Teams.yearID)).all()
    return {"years": years}

@app.get("/teams")
async def get_teams(year: int):
    with Session(engine) as session:
        teams = session.exec(select(Teams.teamID, Teams.name, Teams.lgID, Teams.divID).where(Teams.yearID == year)).all()
    team_list = [{"id": team_id, "name": name, "league": league, "division": division} for team_id, name, league, division in teams]
    return {"teams": team_list}

@app.get("/players")
async def get_players(year: int, team: str):
    with Session(engine) as session:
        players = session.exec(
            select(People.nameFirst, People.nameLast)
            .join(Batting, Batting.playerID == People.playerID)
            .where((Batting.yearID == year) & (Batting.teamID == team))
            .distinct()
        ).all()
    player_list = [{"first_name": first, "last_name": last} for first, last in players]
    return {"players": player_list}



app.mount("/", StaticFiles(directory="static", html=True), name="static")
