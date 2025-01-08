# Setup environnement

- Create a Virtual Environment 
```bash
python -m venv .venv
# or 
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

- Install Packages
```bash
pip install "fastapi[standard]"
```

- Install from requirements.txt
```bash
pip install -r requirements.txt
```

- Deactivate the Virtual Environment
```bash
deactivate
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

