import os
import requests
import base64
from langchain_community.tools import tool

# Ensure environment variable is set for GITHUB_KEY
GITHUB_KEY = os.getenv('GITHUB_KEY')

if not GITHUB_KEY:
    raise EnvironmentError("GITHUB_KEY environment variable not set")

class Tools():
    @staticmethod
    @tool("get file contents from given file path")
    def get_file_contents(path, owner, repo):
        """
        Fetches the content of a given file from GitHub using the provided path, owner, and repository name.

        Parameters:
            path (str): The file path or URL.
            owner (str): The owner of the repository.
            repo (str): The name of the repository.

        Returns:
            str: The content of the file or an error message.
        """
        # Construct the API URL
        if path.startswith("https://"):
            api_url = path
        else:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

        # Add the Authorization header with the token
        headers = {
            'Authorization': f'token {GITHUB_KEY}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            file_content = response.json()

            # Check the size of the file
            if file_content['size'] > 1000000:  # 1MB in bytes
                return "Skipped: File size is greater than 1 MB."

            # Decode the Base64 encoded content
            content_decoded = base64.b64decode(file_content['content'])

            # Convert bytes to string
            content_str = content_decoded.decode('utf-8')

            # Check the number of lines in the file
            if len(content_str.split('\n')) > 500:
                return "Skipped: File contains more than 500 lines."

            return content_str

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
        except KeyError:
            return "Error: Unexpected response structure from GitHub API"
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"