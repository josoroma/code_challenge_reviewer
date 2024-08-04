from crewai import Task


class Tasks:
    """
    Class to create and manage different types of tasks.
    """

    def review_task(self, agent, repo, path, context):
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

                    - Take the file path and file contents from `content_agent`.
                    - Provide a detailed code review with feedback on the following aspects:
                       * Code Quality
                       * Bugs
                       * Anti-Patterns
                       * Improvements
                       * Compliance
                    - Make necessary improvements to the file content and return the updated content as `updated_code`.

                    Return the following values in the markdown content output:

                    - project_name: {repo}.
                    - path: {path}.
                    - explain_this: generate documentation for this code, explain the entire code in a few lines.
                    - code_review: detailed explain the code review for this code, provide feedback on the code quality, bugs, anti-patterns, improvements, and compliance.
                    - updated_code: updated code of file after making code review and changes.

                    The attributes returned must be in markdown format, as heading h2 or ## and the value as its nested text.

                    The `updated_code` output string must be a string in python format. This `updated_code` output string should be involved by backticks such as ```python updated_code_output ```.
                    
                    Only return the explained and reviewed file content. If there are multiple explains and reviews, return the entire reviewed file content in markdown format.

                    Task output must be a string in markdown format. This string should not be involved by any type of backticks such as ```markdown output ```, just avoid that.
                """,
                context=context,
                expected_output="Only return the string output in markdown format and ensure the markdown content is accurate and well-structured."
            )
        except Exception as e:
            print(f"Error creating review task: {e}")
            return None

    def get_file_path_task(self, agent, file_tree, repo_directory, repo_structure, repo_file_sample, repo_fullpath_sample, repo_output_sample):
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
            print(f"Error creating file path task: {e}")
            return None

    def content_task(self, agent, owner, repo, path):
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
            print(f"Error creating content task: {e}")
            return None
