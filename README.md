# Setup environnement

- Create a Virtual Environment 
python -m venv .venv
or 
python3 -m venv .venv

- Activate the Virtual Environment
source .venv/bin/activate

- Check the Virtual Environment is Active
which python

- Upgrade pip
python -m pip install --upgrade pip

- Install Packages
pip install "fastapi[standard]"

- Install from requirements.txt
pip install -r requirements.txt

- Deactivate the Virtual Environment
deactivate

- Init git
git init

- Add .gitignore
echo "*" > .venv/.gitignore

- Add these in .gitignore project
__pycache__
.env
env
test_db.db

# Github
- Create a repo as public 
chatwithdocs

- push an existing repository from the command line
git remote add origin https://github.com/coumarane/chatwithdocs.git
git branch -M main
git push -u origin main