import os
import re
import streamlit as st
import logging
from crewai import Crew
from agents import Agents
from tasks import Tasks

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)


class ReviewCrew:
    """
    Class to handle the review process for a given file in a GitHub repository.
    """

    def __init__(self, owner, repo, path, output):
        """
        Initializes the ReviewCrew with the repository details.

        Parameters:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            path (str): The path of the file to review.
            output (output): The path of the single file with all the repo files reviewed.
        """
        self.owner = owner
        self.repo = repo
        self.path = path
        self.output = output
        self.output_placeholder = st.empty()

    def append_review_to_file(self, result):
        """
        Appends the explain and the review result to a markdown file.

        Parameters:
            result (str): The str containing the explain and the review results in markdown format.
        """
        # Create directory path using owner and repo
        dir_path = os.path.join(self.owner, self.repo)
        os.makedirs(dir_path, exist_ok=True)

        # Create a file with the current date as its name
        file_path = os.path.join(dir_path, self.output)

        try:
            with open(file_path, 'a') as file:
                file.write(f"\n\n# {self.repo} - {self.path}\n\n")
                file.write(result)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def run(self):
        """
        Runs the review process using the defined agents and tasks.
        """
        try:
            # The Agents
            agents = Agents()
            review_agent = agents.review_agent()
            content_agent = agents.content_agent()

            # The Tasks
            tasks = Tasks()
            content_task = tasks.content_task(
                agent=content_agent,
                owner=self.owner,
                repo=self.repo,
                path=self.path
            )
            review_task = tasks.review_task(
                agent=review_agent,
                repo=self.repo,
                path=self.path,
                context=[content_task]
            )

            # The Crew
            crew = Crew(
                agents=[content_agent, review_agent],
                tasks=[content_task, review_task],
                verbose=2,
                telemetry=False
            )

            # Run the crew
            kickoff_result = crew.kickoff()
            
            str_result = str(kickoff_result).strip()

            result = re.sub(r'^```markdown|```$', '', str_result, flags=re.DOTALL)

            self.output_placeholder.code(f"\n\nresult\n\n", language='bash')
            
            return result

        except Exception as e:
            print(f"Error running ReviewCrew: {e}")

