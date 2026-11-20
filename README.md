# Student Task Management System with CI/CD using GitHub Actions

A beginner-friendly lab project built with Python Flask, SQLite, HTML and CSS.

## Features
- Add student assignments/tasks with subject, due date and priority
- View all, pending and completed tasks
- Mark tasks as completed
- Delete tasks
- Health-check endpoint at `/health`
- Automated tests and GitHub Actions CI workflow

## Requirements
- Python 3.10 or newer
- Git
- GitHub account

## Run locally
```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## GitHub Actions CI/CD setup
1. Create a new GitHub repository named `student-task-manager`.
2. Upload/push this project's files to the repository's `main` branch.
3. Open the **Actions** tab in GitHub.
4. The workflow in `.github/workflows/ci-cd.yml` runs automatically on every push and pull request to `main`.
5. The `test` job installs dependencies and runs unit tests.
6. The `deploy` job runs only after tests pass on a push to `main`.

### Important deployment note
The workflow includes a deployment placeholder because actual deployment requires a hosting provider (for example Render, Railway or an institutional server) and its credentials. Add the provider's official deployment action/commands and store credentials in **GitHub repository → Settings → Secrets and variables → Actions**. Never commit passwords or API tokens.

## CI/CD flow
```text
Developer pushes code to GitHub
             |
             v
       GitHub Actions
             |
             v
     Install dependencies
             |
             v
        Run unit tests
             |
       Tests passed?
        /       \\
      No         Yes
      |           |
  Stop pipeline  Deploy job
                  |
              Application
```

## Project structure
```text
student_task_manager/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        └── ci-cd.yml
```

## Lab viva explanation
**Objective:** Design and implement a student task management system and automate testing/deployment workflow using GitHub Actions.

**CI (Continuous Integration):** Whenever code is pushed or a pull request is opened against `main`, GitHub Actions installs Python dependencies and runs automated unit tests.

**CD (Continuous Delivery/Deployment):** After successful tests on a push to `main`, the deploy job runs. In this starter project it is a placeholder; connect a hosting provider to perform a real deployment.

**Conclusion:** The application helps students organize academic tasks, while GitHub Actions automates quality checks and provides a foundation for deployment.
