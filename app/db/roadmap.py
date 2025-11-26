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
    
def get_roadmap_by_id(roadmap_id: int):
    try:
        roadmap = (
            session.query(Roadmap)
            .filter(Roadmap.id == roadmap_id)
            .first()
        )

        if not roadmap:
            return None

        roadmap_dict = {
			"id": roadmap.id,
            "name": roadmap.name,
            "slug": roadmap.slug,
            "description": roadmap.description,
            "difficulty": roadmap.difficulty
		}
        steps = (
			session.query(RoadmapStepModel)
			.filter(RoadmapStepModel.roadmap_id == roadmap_id)
			.order_by(RoadmapStepModel.order_index)
   			.all()
    	)
        roadmap_dict["steps"] = [
            {
                "id": step.id,
				"roadmap_id": step.roadmap_id,
				"title": step.title,
				"description": step.description,
				"topic_slug": step.topic_slug,
				"order_index": step.order_index,
				"course_id": step.course_id
    		} for step in steps]

        return roadmap_dict

    except Exception as e:
        print("Error fetching roadmap:", e)
        raise e
    finally:
        session.close()
        
def get_roadmap_by_slug(roadmap_slug: str):
    try:
        roadmap = (
            session.query(Roadmap)
            .filter(Roadmap.slug == roadmap_slug)
            .first()
        )

        if not roadmap:
            return None

        roadmap_dict = {
			"id": roadmap.id,
            "name": roadmap.name,
            "slug": roadmap.slug,
            "description": roadmap.description,
            "difficulty": roadmap.difficulty
		}
        steps = (
			session.query(RoadmapStepModel)
			.filter(RoadmapStepModel.roadmap_id == roadmap.id)
			.order_by(RoadmapStepModel.order_index)
   			.all()
    	)
        roadmap_dict["steps"] = [
            {
                "id": step.id,
				"roadmap_id": step.roadmap_id,
				"title": step.title,
				"description": step.description,
				"topic_slug": step.topic_slug,
				"order_index": step.order_index,
				"course_id": step.course_id
    		} for step in steps]

        return roadmap_dict
    
    except Exception as e:
        print("Error fetching roadmap:", e)
        raise e
    finally:
        session.close()

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