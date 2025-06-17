# VGQuiz

VGQuiz is a website built to test your knowledge on video games.

## Tech Stack

* Python
* Django
* Unpoly
* Bootstrap
* SQLite

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). This is used to manage the project and project dependencies. Once uv is installed, run the following bash commands from the repository root.

```
# create a venv with the correct Python version and dependencies for the project
uv sync

# create the database
uv run src/manage.py migrate

# create a super user
uv run src/manage.py createsuperuser

# serve the application - leave this running in a separate terminal window
uv run src/manage.py runserver

# load quizzes
uv run bin/load_quizzes.py
```

At this point, you can navigate to the following URLs to interact with the application.

http://localhost:8000 (the homepage)

http://localhost:8000/api/docs (OpenAPI endpoints document)

http://localhost:8000/admin (Django Admin powered UI, log in with the super user created previously)


Happy coding!
