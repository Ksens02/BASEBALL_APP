from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from pathlib import Path

# Database configuration
DATABASE_URL = "sqlite:///baseball.db"
DATABASE_PATH = Path(__file__).parent / "baseball.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session


class Person(SQLModel, table=True):
    """Represents a player in the baseball database."""
    playerID: str = Field(primary_key=True)
    ID: Optional[int] = None
    birthYear: Optional[int] = None
    birthMonth: Optional[int] = None
    birthDay: Optional[int] = None
    birthCity: Optional[str] = None
    birthCountry: Optional[str] = None
    birthState: Optional[str] = None
    deathYear: Optional[float] = None
    deathMonth: Optional[float] = None
    deathDay: Optional[float] = None
    deathCountry: Optional[str] = None
    deathState: Optional[str] = None
    deathCity: Optional[str] = None
    nameFirst: Optional[str] = None
    nameLast: Optional[str] = None
    nameGiven: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    debut: Optional[str] = None
    bbrefID: Optional[str] = None
    finalGame: Optional[str] = None
    retroID: Optional[str] = None
    
    # Relationships
    batting_stats: list["Batting"] = Relationship(back_populates="player")


class Team(SQLModel, table=True):
    """Represents a team and their performance in a specific year."""
    teamID: str = Field(primary_key=True)
    yearID: int = Field(primary_key=True)
    lgID: Optional[str] = None
    franchID: Optional[str] = None
    divID: Optional[str] = None
    Rank: Optional[int] = None
    G: Optional[int] = None
    Ghome: Optional[int] = None
    W: Optional[int] = None
    L: Optional[int] = None
    DivWin: Optional[str] = None
    WCWin: Optional[str] = None
    LgWin: Optional[str] = None
    WSWin: Optional[str] = None
    R: Optional[int] = None
    AB: Optional[int] = None
    H: Optional[int] = None
    doubles: Optional[int] = Field(None, alias="2B", title="2B")
    triples: Optional[int] = Field(None, alias="3B", title="3B")
    HR: Optional[int] = None
    BB: Optional[int] = None
    SO: Optional[int] = None
    SB: Optional[int] = None
    CS: Optional[int] = None
    HBP: Optional[int] = None
    SF: Optional[int] = None
    RA: Optional[int] = None
    ER: Optional[int] = None
    ERA: Optional[float] = None
    CG: Optional[int] = None
    SHO: Optional[int] = None
    SV: Optional[int] = None
    IPouts: Optional[int] = None
    HA: Optional[int] = None
    HRA: Optional[int] = None
    BBA: Optional[int] = None
    SOA: Optional[int] = None
    E: Optional[int] = None
    DP: Optional[int] = None
    FP: Optional[float] = None
    name: Optional[str] = None
    park: Optional[str] = None
    attendance: Optional[str] = None
    BPF: Optional[float] = None
    PPF: Optional[float] = None
    teamIDBR: Optional[str] = None
    teamIDlahman45: Optional[str] = None
    teamIDretro: Optional[str] = None
    
    # Relationships
    batting_stats: list["Batting"] = Relationship(back_populates="team")


class Batting(SQLModel, table=True):
    """Represents a player's batting statistics for a specific team and year."""
    playerID: str = Field(primary_key=True, foreign_key="person.playerID")
    yearID: int = Field(primary_key=True)
    stint: int = Field(primary_key=True)
    teamID: str = Field(foreign_key="team.teamID")
    lgID: Optional[str] = None
    G: Optional[int] = None
    AB: Optional[int] = None
    R: Optional[int] = None
    H: Optional[int] = None
    doubles: Optional[int] = Field(None, alias="2B", title="2B")
    triples: Optional[int] = Field(None, alias="3B", title="3B")
    HR: Optional[int] = None
    RBI: Optional[int] = None
    SB: Optional[int] = None
    CS: Optional[int] = None
    BB: Optional[int] = None
    SO: Optional[int] = None
    IBB: Optional[int] = None
    HBP: Optional[int] = None
    SH: Optional[int] = None
    SF: Optional[int] = None
    GIDP: Optional[int] = None
    
    # Relationships
    player: Optional[Person] = Relationship(back_populates="batting_stats")
    team: Optional[Team] = Relationship(back_populates="batting_stats")
