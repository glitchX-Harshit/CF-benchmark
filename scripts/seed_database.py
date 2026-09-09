import os
import yaml
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, JSON

Base = declarative_base()

class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(String, primary_key=True)
    version = Column(String)
    name = Column(String)
    prospect = Column(JSON)
    context = Column(JSON)
    objection = Column(JSON)
    desired_outcome = Column(JSON)
    expected_strategy = Column(JSON)
    undesired_behavior = Column(JSON)
    evaluation = Column(JSON)
    benchmark_responses = Column(JSON)

async def seed_database(db_url="sqlite+aiosqlite:///benchmark.db", scenarios_dir="data/scenarios"):
    engine = create_async_engine(db_url, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    scenarios_to_insert = []
    
    if os.path.exists(scenarios_dir):
        for filename in os.listdir(scenarios_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(scenarios_dir, filename)
                with open(filepath, 'r') as f:
                    data = yaml.safe_load(f)
                    scenario = Scenario(
                        id=data.get('id'),
                        version=data.get('version'),
                        name=data.get('name'),
                        prospect=data.get('prospect'),
                        context=data.get('context'),
                        objection=data.get('objection'),
                        desired_outcome=data.get('desired_outcome'),
                        expected_strategy=data.get('expected_strategy'),
                        undesired_behavior=data.get('undesired_behavior'),
                        evaluation=data.get('evaluation'),
                        benchmark_responses=data.get('benchmark_responses')
                    )
                    scenarios_to_insert.append(scenario)
                    
    async with async_session() as session:
        session.add_all(scenarios_to_insert)
        await session.commit()
        
    print(f"Successfully seeded {len(scenarios_to_insert)} scenarios.")

if __name__ == "__main__":
    asyncio.run(seed_database())
