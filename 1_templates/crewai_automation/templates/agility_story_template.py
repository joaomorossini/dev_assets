from textwrap import dedent

# Reference: https://github.com/danielmiessler/fabric/blob/main/patterns/agility_story/system.md

AGILITY_STORY_EXAMPLE = dedent("""
"Topic": "Automating data quality automation",
"Story": "As a user, I want to be able to create a new user account so that I can access the system.",
"Criteria": "Given that I am a user, when I click the 'Create Account' button, then I should be prompted to enter my email address, password, and confirm password. When I click the 'Submit' button, then I should be redirected to the login page."
""")