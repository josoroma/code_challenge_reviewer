setup:
	poetry install --no-root
	poetry env use `which python3.11`
	poetry shell

add:
	poetry add langchain langchain-community crewai 'crewai[tools]' requests

run:
	poetry run python -V
	poetry run which python
	PYTHONHTTPSVERIFY=0 poetry run python -m src.main -vv

clean:
	rm -rf `poetry env info -p`
	rm -rf poetry.lock