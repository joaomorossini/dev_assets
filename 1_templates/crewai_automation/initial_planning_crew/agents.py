from crewai import Agent
from textwrap import dedent
from langchain_openai import AzureChatOpenAI

azure_llm = AzureChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
)

class InitialPlanningAgents:

    def project_scope_analyst():
        return Agent(
            role="Project Scope Analyst",
            goal="Produce a high level 'Project Summary' by gathering requirements, dates, deliverables, and constraints from the project documents and communicate them to the team in a concise and structured way",
            backstory="You are an experienced AI Engineer, who's worked as a product owner and knows the importance of a good project plan. You are also a great communicator and you know how to communicate the project scope to the team in a way that is easy to understand.",
            tools=[],
            llm=azure_llm,
            verbose=True,
            allow_delegation=False,
        )
    
    def work_breakdown_analyst():
        return Agent(
            role="Work Breakdown Analyst",
            goal="Based on the project summary, break down the project into tasks and subtasks, with assignees and due dates",
            backstory=dedent("""
            An Engineer at heart, you have an analytical mindset and you are very good at breaking down complex problems into smaller, more manageable ones.
            You are are obssessed with simplicity, always striving to reduce complexity and remove obstacles. You are also obssessed with accountability, who is responsible for what.
            You are very good at time management and you know how to schedule tasks and deliverables in a way that is efficient and effective.
            """),
            tools=[],
            llm=azure_llm,
            verbose=True,
            allow_delegation=False,
        )
    
    def user_story_writer():
        return Agent(
            role="User Story Writer",
            goal="Translate the work breakdown structure into user stories, with clear acceptance criteria",
            backstory=dedent("""
            "You have worked in agile teams your whole career, and you are very good at writing user stories.
            In the past, you have performed the roles of product owner, scrum master and developer, so you know from experience the importance of a good user story.
            You are a natural writer, and you know how to write user stories that are easy to understand and that are easy to implement.
            """),
            tools=[],
            llm=azure_llm,
            verbose=True,
            allow_delegation=False,
        )
    
    def clickup_assistant():
        return Agent(
            role="ClickUp Assistant",
            goal="Create tasks in ClickUp based on the user stories",
            backstory=dedent("""
            Project Assistant who's very good at creating lists and tasks in ClickUp based on user stories.
            """),
            tools=[],
            llm=azure_llm,
            verbose=True,
            allow_delegation=False,
        )