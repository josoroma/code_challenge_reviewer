import logging
from crewai import Task, Agent

class Tasks:
    """
    Class to create and manage different types of tasks.
    """

    def review_task(self, agent: Agent, repo: str, path: str, context: str) -> Task:
        """
        Creates a review task for a given file.

        Parameters:
            agent (Agent): The agent responsible for performing the review.
            repo (str): The name of the repository.
            path (str): The file path.
            context (str): The context for the task.

        Returns:
            Task: Configured task for performing the review.
        """
        try:
            return Task(
                agent=agent,
                description=f"""
                    Review the given file and provide detailed feedback and a code review to ensure it adheres to industry code quality standards.

                    - File Input: Take the file path and file contents from content_agent.
                    
                    - Code Review Requirements:
                        - Code Quality: Assess the overall quality of the code.
                        - Bugs: Identify any bugs present in the code.
                        - Anti-Patterns: Point out any anti-patterns and suggest improvements.
                        - Improvements: Recommend general improvements.
                        - Compliance: Check for compliance with industry standards and best practices.
                        - Improvements: Make necessary improvements to the file content and return the updated content as updated_code.
                    
                    Output values to return

                    Return the following values in the Markdown content output:

                    Project Name: {repo}
                    Path: {path}
                    Explain This: Generate documentation for the code, explaining the entire code in a few lines.
                    Code Review: Provide detailed feedback on code quality, bugs, anti-patterns, improvements, and compliance.
                    Updated Code: Return the updated code of the file after making the necessary changes.
                    
                    Output Format

                    The returned attributes must be in Markdown format, with each section as an H2 heading (##) and the corresponding values as nested text.
                    
                    For "Explain This" and "Code Review", consolidate multiple explanations and reviews into a single cohesive output for each section.
                    
                    Enclose the entire output in triple backticks with the format specified as markdown, like this: ```markdown output``` .
                """,
                context=context,
                expected_output="NOTE: Return the entire output formatted as Markdown, enclosed within triple backticks like this: ```markdown output```"
            )
        except Exception as e:
            logging.error(f"Error creating review task: {e}")
            return None

    def get_file_path_task(self, agent: Agent, file_tree: str, repo_directory: str, repo_structure: str, repo_file_sample: str, repo_fullpath_sample: str, repo_output_sample: str) -> Task:
        """
        Creates a task to get the file path from a given tree structure.

        Parameters:
            agent (Agent): The agent responsible for performing the task.
            file_tree (str): The tree structure of the folder.
            repo_directory (str): The user input (file or folder name).

        Returns:
            Task: Configured task for extracting file paths.
        """
        try:
            return Task(
                agent=agent,
                description=f"""
                    You are given a tree structure of folder and repo_directory. First, you have to decide whether it is a folder or file from the given tree structure of a folder.

                    Follow this approach:

                    - If it's a file then return array with 1 element which contains the full path of that file in this folder structure.
                    - If it's a folder then return array of paths of sub files inside that folder. If there is a subfolder in given folder, then return paths for those files as well.
                    - If repo_directory is not present in given tree structure then just return an empty array.

                    Please return the FULL path of a given file in the given folder tree structure. For example, if the tree structure looks like this:

                    {repo_structure}

                    Then the full path of {repo_file_sample} will be "{repo_fullpath_sample}".

                    DON'T send every file content at once, send it one by one to review_agent.

                    Here is the tree structure of the folder:

                    {file_tree}

                    Here is user input:

                    {repo_directory}

                    NOTE: ONLY RETURN ARRAY OF PATHS WITHOUT ANY EXTRA TEXT IN RESPONSE.
                """,
                expected_output=f"""
                    ONLY an array of paths.
                    For example:
                    {repo_output_sample}
                """
            )
        except Exception as e:
            logging.error(f"Error creating file path task: {e}")
            return None

    def content_task(self, agent: Agent, owner: str, repo: str, path: str) -> Task:
        """
        Creates a task to fetch file content using the GitHub API.

        Parameters:
            agent (Agent): The agent responsible for performing the task.
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            path (str): The file path.

        Returns:
            Task: Configured task for fetching file content.
        """
        try:
            return Task(
                agent=agent,
                description=f"""
                    You are given a file path and you have to get the content of the file and file name using the GitHub API.

                    Here is the file path:

                    {path}

                    Here is the owner name:

                    {owner}

                    Here is the repo name:

                    {repo}

                    Don't return anything except the filename and content.
                """,
                expected_output="filename and content of the given file"
            )
        except Exception as e:
            logging.error(f"Error creating content task: {e}")
            return None