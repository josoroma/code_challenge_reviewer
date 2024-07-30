import ast
from datetime import datetime
import logging
import warnings
from agents import Agents
from github_helper import get_file_tree
from review_crew import ReviewCrew
from tasks import Tasks

def main():
    """
    Main function to execute the review process on a given GitHub repository.
    """
    # Take input from user
    github_url = "https://github.com/josoroma/New-Kidz-On-The-Grid"
    user_input = "app/(pages)/blog"

    # Extract owner and repository name from GitHub URL
    split_url = github_url.split('/')
    owner = split_url[3]
    repo = split_url[4]

    try:
        # Get the tree structure of the GitHub repository
        repo_tree = get_file_tree(owner=owner, repo=repo)
    except Exception as e:
        print(f"Error: Unable to retrieve the repository tree. {str(e)}")
        return

    # Get array of full paths of given files
    path_agent = Agents().path_agent()
    path_task = Tasks().get_file_path_task(agent=path_agent, file_tree=repo_tree, user_input=user_input)

    try:
        # Execute the path task and get the result as a string
        task_output = path_task.execute_sync()
        paths_str = str(task_output)

        # Parse the paths string into a list
        paths = ast.literal_eval(paths_str)

        output = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.md"

        # Traverse the paths one by one and review them using ReviewCrew
        for path in paths:
            review_crew = ReviewCrew(owner=owner, repo=repo, path=path, output=output)
            review_crew.run()

    except (ValueError, SyntaxError):
        print("Error: Unable to parse the paths string.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Suppress warnings
    warnings.filterwarnings("ignore")

    # Configure logging to suppress warnings and info messages
    logging.basicConfig(level=logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logging.getLogger("crewai").setLevel(logging.CRITICAL)
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)

    main()