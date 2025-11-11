# Contributing to sqlacodegen - Setup Guide

## Git Workflow for Contributing

### 1. **Fork the Repository** (on GitHub)
- Go to https://github.com/agronholm/sqlacodegen
- Click the "Fork" button in the top-right corner
- This creates a copy of the repository under your GitHub account

### 2. **Clone Your Fork** (to your local computer)
```bash
git clone git@github.com/YOUR-USERNAME/sqlacodegen
cd sqlacodegen
```

Replace `YOUR-USERNAME` with your actual GitHub username.

Example: `git clone git@github.com/Samplead/sqlacodegen`

### 3. **Add Upstream Remote** (optional but recommended)
This lets you sync with the original repository:
```bash
git remote add upstream https://github.com/agronholm/sqlacodegen.git
```

### 4. **Set Up Development Environment**

#### 4.1 **Add uv.lock to .gitignore**
Before starting development, add `uv.lock` to the `.gitignore` file:
```bash
echo "uv.lock" >> .gitignore
git add .gitignore
git commit -m "Add uv.lock to .gitignore"
```

#### 4.2 **Install dependencies using uv**
Use `uv` for managing the development environment:
```bash

# Install project dependencies
uv sync --all-extras
uv pip install -e .

# Install development dependencies
uv pip install tox pre-commit

# Install pre-commit hooks (code quality checks)
pre-commit install
```

### 5. **Create a Feature Branch**
Always create a new branch for your changes:
```bash
git checkout -b feature/declarative-str-enum-support
```

Use a descriptive name like `fix-mysql-type-mapping` or `add-postgresql-support`.

### 6. **Make Your Changes**
- Write your code
- Add tests if applicable
- Ensure your code follows PEP 8 standards

### 7. **Test Your Changes**
```bash
# Run all tests and code quality checks
tox

# Or run tests in parallel
tox -p
```

### 8. **Commit Your Changes**
```bash
git add .
git commit -m "Descriptive commit message

Fixes #123"  # If it fixes an issue
```

You can make multiple commits during development to save your progress.

### 9. **Squash Commits Before Creating PR**
Before opening a pull request, squash all your commits into a single commit:

```bash
# First, check how many commits you've made on your branch
git log --oneline origin/master..HEAD

# Squash the last N commits (replace N with the number of commits)
git rebase -i HEAD~N

# In the editor that opens:
# - Keep the first commit as "pick"
# - Change all other commits from "pick" to "squash" (or just "s")
# - Save and close the editor
# - Edit the final commit message in the next editor that opens

# Force push to your fork (this rewrites history on your branch)
git push origin my-feature-name --force
```

**Alternative using git reset:**
```bash
# Soft reset to combine all commits
git reset --soft origin/master
git commit -m "Your single commit message

Fixes #123"

# Force push to your fork
git push origin my-feature-name --force
```

### 10. **Push to Your Fork**
```bash
git push origin my-feature-name
```

### 11. **Create a Pull Request**
- Go to the original repository: https://github.com/agronholm/sqlacodegen
- Click "Pull Requests" → "New Pull Request"
- Click "compare across forks"
- Select your fork and branch
- Submit the PR with a clear description

## Summary

### Do this:
- **Fork** the repository on GitHub (creates your own copy)
- **Clone** your fork to your local machine
- **Branch** for each feature/fix
- **Push** to your fork
- **Pull Request** to the original repository

### Don't do this:
- Don't clone the original repository directly
- Don't work on the main/master branch
- Don't push directly to the original repository (you won't have permission anyway)

## Key Concept

You work on your own fork, and propose changes back to the original via pull requests. This is the standard open source contribution workflow!

## Additional Resources

- CONTRIBUTING.rst: https://github.com/agronholm/sqlacodegen/blob/master/CONTRIBUTING.rst
- Project Discussion Forum: https://github.com/agronholm/sqlacodegen/discussions
- Issue Tracker: https://github.com/agronholm/sqlacodegen/issues
