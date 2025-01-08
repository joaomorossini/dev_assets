from textwrap import dedent
from crewai import Task
from app.agents_tools.composio_clickup import CreateTaskTool, CreateFolderlessListTool
from .agents import InitialPlanningAgents
from .tools import save_to_file
from ..templates.project_summary_template import PROJECT_SUMMARY_TEMPLATE
from ..templates.work_breakdown_template import WORK_BREAKDOWN_TEMPLATE
from ..templates.agility_story_template import AGILITY_STORY_EXAMPLE


class InitialPlanningTasks:

    def project_scope_analysis():
        return Task(
            description=dedent("""
            Read the project documents below, gather requirements, dates, deliverables, and constraints,
            then produce a high level 'Project Summary' using the provided template and save it to a markdown file.
            ---
            Project Documents:
            {project_documents}
            ---
            Additional Instructions:
            {additional_instructions}
            """),
            expected_output=dedent(f"""
            Below, you will find the project summary template, delimited by triple backticks.
            The template uses double vertical bars (||) as delimiters for placeholders.
            Replace the delimiters with the appropriate information.
            ```
            {PROJECT_SUMMARY_TEMPLATE}
            ```
            """),
            agent=InitialPlanningAgents.project_scope_analyst(),
            tools=[save_to_file],
        )

    def work_breakdown_analysis():
        return Task(
            description="Based on the project summary, break down the project into tasks and subtasks and save it to a markdown file",
            expected_output=dedent(f"""
            The tasks and subtasks should be sufficient to complete the project successfully.
            Below, you will find the work breakdown template, delimited by triple backticks.
            Replace the placeholders with the appropriate information.
            ```
            {WORK_BREAKDOWN_TEMPLATE}
            ```

            Your final output should be a list of tasks and subtasks.
            """),
            agent=InitialPlanningAgents.work_breakdown_analyst(),
            tools=[save_to_file],
        )

    def user_stories_writing():
        return Task(
            description="Use the task description field in the ClickUp API to write user stories for the project based on the project tasks and subtasks",
            expected_output=dedent(f"""
            Below, you will find an example of a user story, delimited by triple backticks.
            Use it as a guide to write user stories for the project.
            ```
            {AGILITY_STORY_EXAMPLE}

            Your final output should be a list of dictionaries, following the example format, which will be saved to a properly formatted json file.
            The output should be written in Brazilian Portuguese.
            ```
            """),
            agent=InitialPlanningAgents.user_story_writer(),
            tools=[save_to_file],
        )
    
    def create_clickup_tasks():
        return Task(
            description=dedent("""
            Create a new list with tasks in ClickUp based on the user stories for the project.

            ### ClickUp Structure
            -> Workspace: The highest level of organization in ClickUp. It contains all of your Spaces.
            --> Space: A collection of Folders and Lists. It's a way to group related work together.
            ---> Folder: Used to group Lists together.
            ----> List: Used to group tasks together. Lists can be either in a Folder or directly in a Space.
            -----> Task: The basic unit of work in ClickUp, assignable with due dates.
            ------> Subtask: A child task of a parent Task, assignable to different people.

            ### Default ClickUp IDs
            Use these IDs unless otherwise specified
            - 'Cogmo Workspace' (aka "team_id"): 12927880
            - 'Projetos' space id: 54804921
            - 'Agentes' folder id: 90131663060

            ### Your ClickUp user details:
            - id: 84141406
            - username: Ana Beatriz
            - email: ti@cogmo.com.br

            ### Active ClickUp Users (id, username, email)
            - 18951490, Gabriel Alberton, gabriel@cogmo.com.br
            - 48772077, Hélio Potelicki, helio@cogmo.com.br
            - 81918955, João Guilherme Silva Morossini, joaog.morossini@gmail.com
            - 82061927, Rafael Alves Magalhães, magalhaesrafael07@gmail.com

            ### IMPORTANT Guidelines
            - If you try and fail to update a task, delete the original task and create a new one with ALL of the original data, including subtasks, plus the desired changes
            - ALWAYS execute the previous step when required to modify task assignees
            - Before asking the user for any particular id, use the available tools to try to find the id yourself
            - After performing an action on ClickUp, check the response from the ClickUp API to make sure the action was successful
            - ALWAYS use 'date_to_timestamp' tool to convert dates from 'YYYY-MM-DD' to Unix milisecond timestamps when setting dates on ClickUp
            """),
            expected_output=dedent("""
            The tasks should be created in ClickUp based on the user stories. The user stories themselves should be included
            in the task description
            """),
            agent=InitialPlanningAgents.clickup_assistant(),
            tools=[CreateTaskTool(), CreateFolderlessListTool()],
        )