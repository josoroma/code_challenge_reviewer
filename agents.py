from crewai import Agent
from tools import Tools


class Agents:
    """
    Class to create and manage different types of agents.
    """

    def review_agent(self):
        """
        Creates a review agent for code reviews.
        
        Returns:
            Agent: Configured agent for performing code reviews.
        """
        try:
            return Agent(
                role='Senior Software Developer',
                goal='Perform detailed code reviews on the provided file to ensure it adheres to industry code quality standards. The code review should focus on the following aspects: evaluate code quality, identify bugs, spot anti-patterns, recommend improvements and ensure compliance.',
                backstory="You are a Senior Software Developer at a leading tech company, responsible for maintaining high code quality standards across the organization. As part of your role, you are tasked with conducting thorough code reviews on given file contents. Your goal is to ensure the code meets industry standards and follows best practices specific to the technologies in use.",
                allow_delegation=False,
                verbose=True,
            )
        except Exception as e:
            print(f"Error creating review agent: {e}")
            return None

    def path_agent(self):
        """
        Creates a path agent for extracting file paths.
        
        Returns:
            Agent: Configured agent for extracting file paths.
        """
        try:
            return Agent(
                role="File Path Extractor",
                goal="Get the tree structure of folder and return full paths of the given file or files of given folder in array format",
                backstory="You're a file path extractor who has created several file paths from given tree structures",
                allow_delegation=False,
                verbose=True,
            )
        except Exception as e:
            print(f"Error creating path agent: {e}")
            return None

    def content_agent(self):
        """
        Creates a content agent for fetching file content using GitHub API.
        
        Returns:
            Agent: Configured agent for fetching file content using GitHub API.
        """
        try:
            return Agent(
                role="GitHub API Expert",
                goal="Get the content of given file using GitHub API",
                backstory="You're a GitHub API expert who has extracted many file contents using GitHub's API",
                verbose=True,
                allow_delegation=False,
                tools=[Tools.get_file_contents],
            )
        except Exception as e:
            print(f"Error creating content agent: {e}")
            return None
