
# CodeCheck – Python Code Analysis Tool

CodeCheck is a Python-based static code analysis tool designed to
inspect Python source files and identify basic code quality issues.

## Features

- Python source file reading
- Syntax validation using Python AST
- Detection of imports and functions
- Detection of classes and loops
- Conditional statement analysis
- Nested control structure analysis

## Technologies Used

- Python
- Abstract Syntax Tree (AST)
- Pytest
- Git and GitHub

## Project Structure

```text
CodeCheck/
├── analyzer/
│   ├── __init__.py
│   ├── file_reader.py
│   ├── syntax_checker.py
│   ├── code_analyzer.py
│   └── report_generator.py
├── tests/
├── sample_files/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd CodeCheck
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

## Testing

Run automated tests:

```bash
pytest -v
```

## Project Status

Currently under development.

## Author

Mohammed Fahis M

GitHub: https://github.com/fahis1099

LinkedIn: https://linkedin.com/in/mohammed-fahis
```

Note: This README describes the current implemented features and planned report generation separately. We'll update it as development progresses.

# Step 4 – Initialize Git

Open the VS Code terminal in your CodeCheck directory.

Check Git:

```powershell
git --version
```

Initialize the repository:

```powershell
git init
```

Configure your identity if you haven't already:

```powershell
git config --global user.name "Mohammed Fahis"
git config --global user.email "fahis1099@gmail.com"
```

Check the files:

```powershell
git status
```

# Step 5 – First commit

Add all project files:

```powershell
git add .
```

Create your first commit:

```powershell
git commit -m "Initial project setup with file reader and syntax checker"
```

A commit is a snapshot of your project at a particular point in development.

# Step 6 – Connect GitHub

Copy the HTTPS repository URL from the GitHub repository you created.

It should look like:

```text
https://github.com/fahis1099/CodeCheck.git
```

Run:

```powershell
git branch -M main

git remote add origin https://github.com/fahis1099/CodeCheck.git

git push -u origin main
```

VS Code or Git Credential Manager may ask you to authenticate with GitHub.

---

# Our Git workflow from now on

Whenever we complete a major feature, we'll create a meaningful commit.

| Development stage | Commit message |
|---|---|
| Initial setup | `Initial project setup` |
| Syntax checker | `Implement Python syntax validation` |
| Code analyzer | `Add AST-based code analysis` |
| Unused imports | `Add unused import detection` |
| Reports | `Implement code quality report generation` |
| Testing | `Add automated unit tests` |
| Documentation | `Update project documentation` |

This will demonstrate incremental development rather than uploading the entire project in one commit.

## Your task now

Complete Steps 1–6.

<box border radius="lg" padding={3} gap={2}>
  **GitHub setup checklist**
  {@body const items=["Created public CodeCheck repository","Created .gitignore","Created README.md","Initialized local Git repository","Created initial commit","Successfully pushed to GitHub"]}
  {@body const [checks,setChecks]=DIL.useState(items.map(()=>false))}
  {#each items as item,i}
    <checkbox checked={checks[i]} onChange={v=>setChecks(old=>old.map((x,j)=>i===j?v:x))}>{item}</checkbox>
  {/each}
  <text color="secondary" size="xs">{checks.filter(Boolean).length} of 6 completed</text>
</box>

**Send me your GitHub repository link once you've pushed it.** I'll review the repository structure and README before we continue building the Code Analyzer.