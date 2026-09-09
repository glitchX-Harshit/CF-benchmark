from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.api.deps import get_db
from app.models.scenario import Scenario
from app.schemas.scenario import ScenarioCreate, ScenarioUpdate, ScenarioResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()

@router.post("", response_model=ScenarioResponse)
async def create_scenario(
    scenario_in: ScenarioCreate,
    db: AsyncSession = Depends(get_db)
):
    scenario = Scenario(**scenario_in.model_dump())
    db.add(scenario)
    await db.commit()
    await db.refresh(scenario)
    return scenario

@router.get("", response_model=PaginatedResponse[ScenarioResponse])
async def list_scenarios(
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * size
    query = select(Scenario).offset(offset).limit(size)
    result = await db.execute(query)
    scenarios = result.scalars().all()
    
    return PaginatedResponse(
        items=list(scenarios),
        total=len(scenarios),
        page=page,
        size=size
    )

@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    query = select(Scenario).where(Scenario.id == scenario_id)
    result = await db.execute(query)
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    return scenario

@router.patch("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: uuid.UUID,
    scenario_in: ScenarioUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Scenario).where(Scenario.id == scenario_id)
    result = await db.execute(query)
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    update_data = scenario_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
        
    await db.commit()
    await db.refresh(scenario)
    return scenario

@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    query = select(Scenario).where(Scenario.id == scenario_id)
    result = await db.execute(query)
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    await db.delete(scenario)
    await db.commit()
    return {"status": "success"}
