# Setup environnement

- Create a Virtual Environment 
```bash
# on windows
python -m venv .venv
# or on mac os
python3 -m venv .venv
```

- Activate the Virtual Environment
```bash
source .venv/bin/activate
```

- Check the Virtual Environment is Active
```bash
which python
```

- Upgrade pip
```bash
python -m pip install --upgrade pip
```

- Deactivate the Virtual Environment
```bash
deactivate
```

- Remove/delete a virtualenv? 
```bash
deactivate
sudo rm -rf .venv
```

- Init git
```bash
git init
```

- Add .gitignore
```bash
echo "*" > .venv/.gitignore
```

- Add these in .gitignore project
```
__pycache__
.env
env
test_db.db
```

- Init commit
```bash
git add .
git commit -m"Init project"
```

# Github
- Create a repo as public 
chatwithdocs

- push an existing repository from the command line
```bash
git remote add origin https://github.com/coumarane/chatwithdocs.git
git branch -M main
git push -u origin main
```

# Python environments in VS Code
- Select and activate an environment
Command from the Command Palette (⇧⌘P), and select `Python: Select Interpreter` choose the recommanded (it is from the current workspace)


# Install FastApi
- Install Packages
```bash
pip install "fastapi[standard]"
```

- Generate the requirements.txt file.
```bash
pip freeze > requirements.txt
```

- Install from requirements.txt
```bash
pip install -r requirements.txt
```

# Example
- Create a file app.py and this code:
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

- Run the code
```bash
fastapi dev app.py

# or
uvicorn app.main:app --reload
```


# Database Postgresql
```bash
pip install asyncpg sqlalchemy databases alembic psycopg2
# dev mode
pip install asyncpg sqlalchemy databases alembic psycopg2-binary
```

# Database Migrations
```bash
alembic revision --autogenerate -m "Init database schemas"
alembic upgrade head
```

* asyncpg: Asyncpg is a database interface library designed specifically for PostgreSQL and Python/asyncio. (https://magicstack.github.io/asyncpg/current/)
* sqlalchemy: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. (https://www.sqlalchemy.org/)
* alembic: Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. (https://alembic.sqlalchemy.org/en/latest/)
* databases: Databases gives you simple asyncio support for a range of databases. (https://pypi.org/project/databases/)
* psycopg2 0r psycopg2-binary (only for dev mode): Psycopg is the most popular PostgreSQL database adapter for the Python programming language. (https://pypi.org/project/psycopg2/)

# Api Structure
- app
  -- .env                     # gitignored
  -- api
    ---- routes               # FastAPI or Flask route handlers (API endpoints)
  -- core                     # Application-wide utilities, configurations, and core logic
  -- domain                   # Core business models (SQLAlchemy models, Pydantic domain models, enums, etc.)
  -- repositories             # Database access and query logic (e.g., CRUD operations)
  -- services                 # Business logic and application services
  -- schemas                  # Pydantic schemas for request validation and response serialization
  -- templates                # HTML templates (if using templating engines like Jinja2)
  -- main.py                     # Application entry point
- test                        # Unit and integration tests
- migrations                  # Database migration files (e.g., Alembic)

4. Access the Application:
* Open a browser or use a tool like `curl` to access `http://localhost:8000`.

**Using .env in Docker**
* The --env-file option in the docker run command loads your .env file into the container's environment variables.
* Ensure sensitive data in .env (like database credentials) is excluded from version control using .gitignore.

# Test Unitaire
```bash
pytest
```