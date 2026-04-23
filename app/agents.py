from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import tensorflow as tf

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, Sequence('agent_id_seq'), primary_key=True)
    name = Column(String(50), index=True)
    model_path = Column(String(255))

Base.metadata.create_all(bind=engine)

class AgentCreate(BaseModel):
    name: str
    model_path: str

class AgentUpdate(BaseModel):
    name: str = None
    model_path: str = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/agents/", response_model=Agent)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(name=agent.name, model_path=agent.model_path)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.get("/agents/{agent_id}", response_model=Agent)
def read_agent(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@app.put("/agents/{agent_id}", response_model=Agent)
def update_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.name is not None:
        db_agent.name = agent.name
    if agent.model_path is not None:
        db_agent.model_path = agent.model_path
    db.commit()
    db.refresh(db_agent)
    return db_agent

@app.delete("/agents/{agent_id}", response_model=dict)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(db_agent)
    db.commit()
    return {"detail": "Agent deleted"}