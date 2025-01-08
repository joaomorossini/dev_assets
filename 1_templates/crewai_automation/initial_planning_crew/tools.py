from langchain.tools import tool
from datetime import datetime

@tool
def save_to_file(content: str, title: str, file_extension: str = "md"):
    """
    Save the content to a markdown file.
    Args:
        content (str): The properly formatted content to save to the markdown file.
        title (str): The title of the markdown file, in snake case.
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{title}_{current_time}"
    file_path = f"app/automations/initial_planning_crew/outputs/{filename}.{file_extension}"
    with open(file_path, "w") as f:
        f.write(content)