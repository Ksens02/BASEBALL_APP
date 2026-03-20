
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
        teams = session.exec(select(Teams.name, Teams.lgID, Teams.divID).where(Teams.yearID == year)).all()
    team_list = [{"name": name, "league": league, "division": division} for name, league, division in teams]
    return {"teams": team_list}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
