from fastapi import HTTPException
from app.schemas.roadmap import RoadmapOutline,RoadmapStep
from app.db.models import Roadmap,RoadmapStep  as RoadmapStepModel
from .db import session


def create_roadmap(payload: RoadmapOutline):
    try:
        new_roadmap = Roadmap(
			name = payload.name,
			slug = payload.slug,
			description = payload.description,
			difficulty = payload.difficulty

		)
        session.add(new_roadmap)
        session.commit()
        
        session.refresh(new_roadmap)
        return new_roadmap
    except Exception as e:
        session.rollback()
        raise e
 
def create_roadmap_step(payload: RoadmapStep,roadmapid):
	try:
		step = RoadmapStepModel(
			title = payload.title,
			topic_slug = payload.topic_slug,
			description = payload.description,
			order_index = payload.order_index,
			roadmap_id = roadmapid

		)
		
		session.add(step)
		session.commit()
	
		session.refresh(step)
	
		return step
	except Exception as e:
			session.rollback()
			raise e
 
def get_roadmaps():
    try:
        roadmap_list = session.query(Roadmap).all()
        return roadmap_list
    except Exception as e:
        raise e
    
def get_roadmap_by_id(roadmap_id):
    try:
        roadmap = (
			session.query(Roadmap)
			.filter(Roadmap.id == roadmap_id).first()
    	)
        return roadmap
    

    except Exception as e:
        raise e

def get_roadmap_steps_by_id(roadmap_id):
    try:
        roadmap = (
			session.query(RoadmapStepModel)
			.filter(RoadmapStepModel.roadmap_id == roadmap_id)
			.order_by(RoadmapStepModel.order_index)
   			.all()
    	)
        return roadmap
    

    except Exception as e:
        raise e