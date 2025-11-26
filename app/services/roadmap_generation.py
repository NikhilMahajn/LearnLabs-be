from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import asyncio

from app.utils.logger import get_logger
from app.schemas.roadmap import RoadmapOutline,RoadmapCreateRequest
from app.db.roadmap import create_roadmap,create_roadmap_step

logger = get_logger(__name__)

llm = ChatGroq(
        temperature=0.3,
        model_name="openai/gpt-oss-20b",
        max_tokens=4000
    )



def generate_roadmap(name: str, difficulty: str = "Beginner"):
    """
    Generate a complete learning roadmap using LLM with structured output.
    """

    logger.info(f"Generating roadmap for '{name}', difficulty='{difficulty}'")

    # Structured output model
    llm_chain = llm.with_structured_output(RoadmapOutline)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
		You are an expert tech educator who creates perfect learning roadmaps.
		Your task: generate a complete, clear, step-by-step roadmap.

		Guidelines:
		- Roadmap must follow a logical progression.
		- Split the roadmap into very clear, ordered steps.
		- Each step MUST have:
			• title
			• description
			• topic_slug (kebab-case)
			• order_index (1,2,3...)
		- Difficulty must influence the complexity of topics.
		- Steps should cover fundamentals → intermediate → advanced (if applicable).
		- Keep explanations concise and beginner-friendly.
		- Slug MUST be unique and SEO friendly (use kebab-case).
		"""),

        ("human", """
			Create a complete learning roadmap.

			Roadmap Title: {roadmap_name}
			Difficulty Level: {difficulty}

			Return data in structured format:
			- name
			- difficulty
			- slug
			- description
			- steps[] (title, description, topic_slug, order_index)
			""")
    ])

    chain = prompt_template | llm_chain

    result = chain.invoke({
        "roadmap_name": name,
        "difficulty": difficulty,
    })

    logger.info(f"Generated roadmap '{result.name}' with {len(result.steps)} steps.")

    return result
def generate_roadmap_handler(payload: RoadmapCreateRequest):
    logger.info(f"Roadmap generation request received | name='{payload.name}', difficulty='{payload.difficulty}'")

    try:
        
        logger.info("Invoking LLM to generate roadmap structure...")
        result = generate_roadmap(payload.name, payload.difficulty)
        logger.info(f"LLM generated roadmap outline with {len(result.steps)} steps")

        logger.info("Saving roadmap to database...")
        roadmap_obj = create_roadmap(result)
        logger.info(f"Roadmap saved | id={roadmap_obj.id}, slug='{roadmap_obj.slug}'")

        logger.info("Saving roadmap steps to database...")
        for step in result.steps:
            logger.debug(
                f"Creating step | order={step.order_index}, title='{step.title}', topic_slug='{step.topic_slug}'"
            )
            create_roadmap_step(step, roadmap_obj.id)

        logger.info(f"All {len(result.steps)} steps saved for roadmap id={roadmap_obj.id}")

        return roadmap_obj

    except Exception as e:
        logger.error(f"Error generating roadmap: {str(e)}", exc_info=True)
        raise
