
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
            select(People.playerID, People.nameFirst, People.nameLast)
            .join(Batting, Batting.playerID == People.playerID)
            .where((Batting.yearID == year) & (Batting.teamID == team))
            .distinct()
        ).all()
    player_list = [{"player_id": pid, "first_name": first, "last_name": last} for pid, first, last in players]
    return {"players": player_list}


@app.get("/player/{player_id}")
async def get_player_stats(player_id: str):
    with Session(engine) as session:
        # Get player bio information
        player = session.exec(
            select(People)
            .where(People.playerID == player_id)
        ).first()
        
        if not player:
            return {"error": "Player not found"}
        
        # Get all career batting stats (aggregated across all years and teams)
        batting_records = session.exec(
            select(Batting)
            .where(Batting.playerID == player_id)
            .order_by(Batting.yearID)
        ).all()
        
        # Aggregate career stats
        career_stats = {
            "G": 0, "AB": 0, "R": 0, "H": 0, "doubles": 0, "triples": 0,
            "HR": 0, "RBI": 0, "SB": 0, "CS": 0, "BB": 0, "SO": 0,
            "IBB": 0, "HBP": 0, "SH": 0, "SF": 0, "GIDP": 0
        }
        
        for record in batting_records:
            career_stats["G"] += record.G or 0
            career_stats["AB"] += record.AB or 0
            career_stats["R"] += record.R or 0
            career_stats["H"] += record.H or 0
            career_stats["doubles"] += record.doubles or 0
            career_stats["triples"] += record.triples or 0
            career_stats["HR"] += record.HR or 0
            career_stats["RBI"] += record.RBI or 0
            career_stats["SB"] += record.SB or 0
            career_stats["CS"] += record.CS or 0
            career_stats["BB"] += record.BB or 0
            career_stats["SO"] += record.SO or 0
            career_stats["IBB"] += record.IBB or 0
            career_stats["HBP"] += record.HBP or 0
            career_stats["SH"] += record.SH or 0
            career_stats["SF"] += record.SF or 0
            career_stats["GIDP"] += record.GIDP or 0
        
        # Calculate batting average and other rates
        avg = round(career_stats["H"] / career_stats["AB"], 3) if career_stats["AB"] > 0 else 0
        obp = round((career_stats["H"] + career_stats["BB"] + career_stats["HBP"]) / 
                   (career_stats["AB"] + career_stats["BB"] + career_stats["HBP"] + career_stats["SF"]), 3) \
              if (career_stats["AB"] + career_stats["BB"] + career_stats["HBP"] + career_stats["SF"]) > 0 else 0
        slg = round((career_stats["H"] + career_stats["doubles"] + 2*career_stats["triples"] + 3*career_stats["HR"]) / 
                   career_stats["AB"], 3) if career_stats["AB"] > 0 else 0
        
        return {
            "player": {
                "player_id": player.playerID,
                "first_name": player.nameFirst,
                "last_name": player.nameLast,
                "birth_year": player.birthYear,
                "birth_city": player.birthCity,
                "birth_state": player.birthState,
                "birth_country": player.birthCountry,
                "height": player.height,
                "weight": player.weight,
                "bats": player.bats,
                "throws": player.throws,
                "debut": player.debut,
                "final_game": player.finalGame
            },
            "career_stats": career_stats,
            "calculated_stats": {
                "batting_average": avg,
                "obp": obp,
                "slg": slg
            }
        }


app.mount("/", StaticFiles(directory="static", html=True), name="static")
