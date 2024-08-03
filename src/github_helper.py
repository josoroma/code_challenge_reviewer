import os
import requests
import streamlit as st

# Ensure environment variable is set for GITHUB_KEY
GITHUB_KEY = os.getenv('GITHUB_KEY')

# Our final path will be stored in this global variable
global_path = ""

def get_file_tree(owner, repo, path="", level=0):
    """
    Fetch and print the tree structure of a GitHub repository, ignoring specific folders.

    Parameters:
    - owner: The username of the repository owner.
    - repo: The name of the repository.
    - path: The path to fetch. Leave empty to fetch the root directory.
    - level: The current depth in the tree structure.

    Returns:
    - str: The tree structure as a string.
    """
    # Directories to ignore
    ignore_dirs = {'public', 'images', 'media', 'assets'}
    global global_path

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Add the Authorization header with the token
    headers = {'Authorization': f'token {GITHUB_KEY}'}

    try:
        # Make the request
        response = requests.get(api_url, headers=headers, verify=False)
        response.raise_for_status()
        items = response.json()

        if isinstance(items, list):
            for item in items:
                # Skip ignored directories
                if item['name'] in ignore_dirs:
                    continue

                item_name = f"{' ' * (level * 2)}- {item['name']}"

                st.code(item_name, language='bash')

                global_path += f"{item_name}\n"

                if item['type'] == 'dir':
                    get_file_tree(owner, repo, item['path'], level + 1)

        return global_path

    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return ""
    except ValueError:
        print("Error: Unable to parse the response from GitHub.")
        return ""
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return ""