import os
import sys
import ast
from constants import APP_REPO_FILE_SAMPLE, APP_REPO_FULLPATH_SAMPLE, APP_REPO_OUTPUT, APP_REPO_PATH, APP_REPO_STRUCTURE, APP_REPO_URL
import streamlit as st
from datetime import datetime
import logging
import warnings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure PYTHONPATH includes src directory
sys.path.append(os.getenv('PYTHONPATH'))

from src.agents import Agents, StreamToExpander
from src.github_helper import get_file_tree
from src.review_crew import ReviewCrew
from src.tasks import Tasks


class App:
    def __init__(self):
        self.github_url = APP_REPO_URL
        
        self.repo_directory = APP_REPO_PATH
        self.repo_structure = APP_REPO_STRUCTURE
        self.repo_output_sample = APP_REPO_OUTPUT

        self.repo_file_sample = APP_REPO_FILE_SAMPLE 
        self.repo_fullpath_sample = APP_REPO_FULLPATH_SAMPLE

        self.setup_session_state()
        self.setup_logging()

    def setup_session_state(self):
        """Initialize session state if it doesn't exist."""
        if 'form_submitted' not in st.session_state:
            st.session_state.form_submitted = False

    def setup_logging(self):
        """Configure logging to suppress warnings and info messages."""
        warnings.filterwarnings("ignore")
        
        logging.basicConfig(level=logging.CRITICAL)
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)
        logging.getLogger("crewai").setLevel(logging.CRITICAL)
        logging.getLogger("requests").setLevel(logging.CRITICAL)
        logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)
    
    def display_header(self):
        """Display the main header of the app."""
        st.subheader("GitHub Repository Directory Review", divider="rainbow", anchor=False)

    def fetch_repo_tree(self):
        """Fetch the tree structure of the GitHub repository."""
        try:
            split_url = self.github_url.split('/')
            owner = split_url[3]
            repo = split_url[4]
            
            repo_tree = get_file_tree(owner=owner, repo=repo)
            
            st.code(repo_tree, language="bash")
            
            return owner, repo, repo_tree
        except Exception as e:
            st.error(f"Error: Unable to retrieve the repository tree. {str(e)}")
            return None, None, None

    def run_path_task(self, repo_tree):
        """Execute the path task to get file paths."""
        path_agent = Agents().path_agent()
        path_task = Tasks().get_file_path_task(
            agent=path_agent, file_tree=repo_tree, 
            repo_directory=self.repo_directory, 
            repo_structure=self.repo_structure, 
            repo_file_sample=self.repo_file_sample, 
            repo_fullpath_sample=self.repo_fullpath_sample,
            repo_output_sample=self.repo_output_sample
        )
        try:
            task_output = path_task.execute_sync()
            paths_str = str(task_output)
            paths = ast.literal_eval(paths_str)
            return paths
        except (ValueError, SyntaxError):
            st.error("Error: Unable to parse the paths string.")
            return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None

    def review_files(self, owner, repo, paths):
        """Review the files at the given paths."""
        output_placeholder = ""
        output = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.md"
        
        for path in paths:
            review_crew = ReviewCrew(owner=owner, repo=repo, path=path, output=output)
            result = review_crew.run()
            
            output_placeholder += result + "\n\n"
            
            st.markdown(f"\n\n{result}\n\n")

        return output_placeholder
    
    def handle_submit(self):
        st.session_state.form_submitted = True

    def reset_form(self):
        st.session_state.form_submitted = False

    def display_sidebar_form(self, form_container):
        """Display the form in the sidebar for user input."""
        with form_container:
            with st.sidebar:
                with st.form(key='settings_form'):
                    self.github_url = st.text_input("GitHub URL", self.github_url.strip())
                    
                    self.repo_directory = st.text_input("Repo Directory", self.repo_directory.strip())
                    self.repo_structure = st.text_area("Repo Structure Sample", self.repo_structure.strip(), height=125)
                    
                    self.repo_file_sample = st.text_input("File Sample", self.repo_file_sample.strip())
                    self.repo_fullpath_sample = st.text_input("Full Path Sample", self.repo_fullpath_sample.strip())
                    
                    self.repo_output_sample = st.text_input("Array Output Sample", self.repo_output_sample.strip())

                    st.form_submit_button(label="Submit", on_click=self.handle_submit, disabled=st.session_state.form_submitted)

                st.write('Made with love by Jos❤️roma')

    def display_app(self, form_container):
        if st.session_state.form_submitted:
            form_container.button(label="Re-run", on_click=self.reset_form)
            output_placeholder = ""
            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=360):
                    sys.stdout = StreamToExpander(st)

                    # Extract owner and repository name from GitHub URL
                    split_url = self.github_url.split('/')
                    owner = split_url[3]
                    repo = split_url[4]

                    try:
                        # Get the tree structure of the GitHub repository
                        owner, repo, repo_tree = self.fetch_repo_tree()
                        if not repo_tree:
                            return

                        # Get array of full paths of given files
                        paths = self.run_path_task(repo_tree)
                        if not paths:
                            return

                        output_placeholder = self.review_files(owner, repo, paths)

                    except (ValueError, SyntaxError):
                        st.error("Error: Unable to parse the paths string.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

                status.update(label="✅ Code Review Ready!", state="complete", expanded=False)
            
            self.reset_form()
            st.subheader("Output", anchor=False, divider="rainbow")
            st.markdown(f"\n\n{output_placeholder}\n\n")

    def main(self):
        """Main function to execute the review process."""
        form_container = st.container()
        self.display_sidebar_form(form_container)
        self.display_header()
        self.display_app(form_container)


if __name__ == "__main__":
    try:
        app = App()
        app.main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        exit(1)
