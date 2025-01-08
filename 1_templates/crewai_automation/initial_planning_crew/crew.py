from crewai import Crew
from .tasks import InitialPlanningTasks
from .agents import InitialPlanningAgents
from ..templates.example_project_document import EXAMPLE_PROJECT_DOCUMENT

agents = [
    InitialPlanningAgents.project_scope_analyst(),
    InitialPlanningAgents.work_breakdown_analyst(),
    InitialPlanningAgents.user_story_writer(),
    InitialPlanningAgents.clickup_assistant(),
]

tasks = [
    InitialPlanningTasks.project_scope_analysis(),
    InitialPlanningTasks.work_breakdown_analysis(),
    InitialPlanningTasks.user_stories_writing(),
    InitialPlanningTasks.create_clickup_tasks(),
]


initial_planning_crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=2,
    embedder={
        "provider": "azure_openai",
        "config":{
            "model": 'text-embedding-3-large',
            "deployment_name": "text-embedding-3-large"
        }
    }    
)