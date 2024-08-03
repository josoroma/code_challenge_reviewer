setup:
	poetry install --no-root
	poetry env use `which python3.11`
	poetry shell

add:
	poetry add streamlit langchain langchain-community crewai 'crewai[tools]' requests python-dotenv watchdog

run:
	poetry run python -V
	poetry run which python
	poetry run -vv streamlit run app.py

clean:
	rm -rf `poetry env info -p`
	rm -rf poetry.lock