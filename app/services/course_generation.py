from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser


import asyncio

from app.schemas.course import CourseOutline,DetailedChapter
from app.db.course import create_course,create_chapter
from app.utils.logger import get_logger

logger = get_logger(__name__)

llm = ChatGroq(
        temperature=0.3,
        model_name="openai/gpt-oss-20b",
        max_tokens=4000
    )


def generate_course_outline(name, target_audiunce="Beginner", difficulty="Easy", duration="2"):
    logger.info(f"Generating course outline for topic='{name}', audience='{target_audiunce}', "
                f"difficulty='{difficulty}', duration={duration} months")

    llm_chain = llm.with_structured_output(CourseOutline)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert course designer and educator. 
    Your task is to create a complete, well-structured course outline.

    Guidelines:
    - The course should have a logical progression.
    - Each chapter should build on the previous one.
    - Learning objectives must be actionable and clear.
    - Estimated durations should align with the total course duration.
    - Keep explanations concise, student-friendly, and practical."""),

        ("human", """Create a course outline for the topic: {course_topic}

    Requirements:
    - Target audience: {target_audience}
    - Course difficulty: {difficulty_level}
    - Total course duration: {course_duration} Months""")
    ])

    chain = prompt_template | llm_chain

    result = chain.invoke({
        "course_topic": name,
        "target_audience": target_audiunce,
        "difficulty_level": difficulty,
        "course_duration": duration
    })
    

    logger.info(f"Generated course outline with {len(result.chapters)} chapters")
    return result


def generate_chapter_content(chapter):
    logger.info(f"Expanding chapter {chapter.chapter_number}: '{chapter.title}'")
    
    parser = PydanticOutputParser(pydantic_object=DetailedChapter)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert programming instructor.
        Your task is to expand a course chapter into detailed lesson sections.

        Guidelines:
        - Divide the chapter into multiple sections of type: content, info, code, or tip.
        - CONTENT → main explanation of a concept, written simply for students.
        - INFO → short fact, rule, or important clarification.
        - CODE → code examples (must include "language" and "explanation").
        - TIP → best practices, pitfalls, or learning hacks.
        - Keep sections concise but informative.

        IMPORTANT:
        - Return ONLY valid JSON (no markdown, no ```json fences).
        - Escape quotes properly.
        - Do NOT use triple quotes. Use single or double quotes only.
        - Follow this schema strictly:

        {format_instructions}
        """),
        ("human", """Expand the following chapter into structured sections:

        Chapter {chapter_number}: {chapter_title}
        Description: {chapter_description}
        Learning Objectives: {learning_objectives}
        Estimated Duration: {estimated_duration} minutes
        """)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    # Option 1: Use the chain with parser directly and handle errors manually
    try:
        chain = prompt_template | llm | parser
        result = chain.invoke({
            "chapter_number": chapter.chapter_number,
            "chapter_title": chapter.title,
            "chapter_description": chapter.description,
            "learning_objectives": chapter.learning_objectives,
            "estimated_duration": chapter.estimated_duration
        })
    except Exception as e:
        logger.warning(f"Parser failed, attempting to fix: {e}")
        # If parsing fails, use OutputFixingParser
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        # Get the raw LLM output first
        chain_without_parser = prompt_template | llm
        raw_output = chain_without_parser.invoke({
            "chapter_number": chapter.chapter_number,
            "chapter_title": chapter.title,
            "chapter_description": chapter.description,
            "learning_objectives": chapter.learning_objectives,
            "estimated_duration": chapter.estimated_duration
        })
        # Now pass the string to the fixing parser
        result = fixing_parser.parse(raw_output.content)
    
    logger.info(f"Generated chapter content with {len(result.sections)} sections")
    return result


async def generate_course_handler(course):
    logger.info(f"Starting course generation for: {course.name}")

    # Step 1: Generate course outline
    result = generate_course_outline(
        course.name,
        course.target_audiunce,
        course.difficulty,
        course.duration,
    )
    # Step 2: Save course to DB
    course_obj = create_course(result)
    logger.info(f"Saved course '{course_obj.title}' with id={course_obj.id} to DB")

    # Step 3: Expand and save chapters with throttling
    for i, chapter in enumerate(result.chapters, start=1):
        chapter_content = generate_chapter_content(chapter)
        create_chapter(course_obj.id, chapter, chapter_content)
        logger.info(f"Saved chapter {chapter.chapter_number} ('{chapter.title}') to DB")

            
        # Rate limit: 3 chapters/minute → wait 20s after each chapter
        logger.info("Waiting 20s before next chapter...")
        await asyncio.sleep(20)  # spread out within the minute

    logger.info(f"Course generation complete for: {course.name}")
    return course_obj

