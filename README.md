# Crew Agents: Comprehensive Code Review Assistant

These Crew Agents are a powerful tool designed to perform thorough code reviews on your files, ensuring they adhere to industry standards. These agents help to: evaluate code quality, identify potential bugs, spot anti-patterns, and suggest improvements to enhance the overall quality and maintainability of your codebase.

### Features

- **Code Quality Assessment**: Evaluates the readability, maintainability, and efficiency of your code.

- **Bug Detection**: Identifies potential bugs or issues that could impact functionality or performance.

- **Anti-Pattern Detection**: Highlights any anti-patterns that may lead to suboptimal coding practices.

- **Improvement Recommendations**: Suggests areas for refactoring and optimization to improve code quality and performance.

- **Compliance Check**: Ensures your code follows best practices and guidelines specific to the technologies in use.

### Usage

The agent takes the file path and file contents from `content_agent` and performs the following tasks:

1. **Detailed Code Review**: Provides feedback if the file does not follow industry standards.

2. **Code Improvement**: Makes necessary changes to the file content and returns the updated content as `updated_code`.

### Markdown Output Format

These Crew Agents help to maintain high standards of code quality in your projects by providing detailed and actionable feedback on your code.

## .env

```
GITHUB_KEY=ghp_...
OPENAI_API_KEY=sk-p...
OPENAI_MODEL_NAME=gpt-4o-mini
```

## pyproject.toml

```
[tool.poetry]
name = "code_challenge_reviewer"
version = "1.0.0"
description = "Code Challenge Reviewer"
authors = ["Josoroma <pablo@josoroma.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "3.11,<=3.13"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## make

```
make setup
```

```
make add
```

```
make run
```

```
make clean
```

## If you feel curious about using Ollama

### Edit gents.py file

```
code agents.py
```

### Use the `mistral-nemo` Ollama Model

```
from langchain_community.llms import Ollama

#Initialize the model
model = Ollama(model="mistral-nemo")
```

### Add `llm=model` line to each Agent available

```
  def agent(self):
    return Agent(
        role='...',
        goal='...',
        backstory="...",
        allow_delegation=False,
        verbose=True,
        llm=model
    )
```

## Docs

- https://docs.crewai.com/core-concepts/Tasks/#overview-of-a-task

## Extending awesome idea and work from

- https://www.ionio.ai/blog/how-to-build-llm-agent-to-automate-your-code-review-workflow-using-crewai