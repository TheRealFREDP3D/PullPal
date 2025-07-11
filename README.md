# PullPal

A powerful tool for fetching and saving complete GitHub pull request conversations, including PR details, issue comments, review comments, and reviews.

---  

[![Python Package](https://github.com/TheRealFREDP3D/PullPal/actions/workflows/python-package.yml/badge.svg)](https://github.com/TheRealFREDP3D/PullPal/actions/workflows/python-package.yml)[![Python Tests](https://github.com/TheRealFREDP3D/PullPal/actions/workflows/python-tests.yml/badge.svg)](https://github.com/TheRealFREDP3D/PullPal/actions/workflows/python-tests.yml)

## Features

- Fetch a single PR, multiple specific PRs, or the latest N PRs
- Save conversations in either Markdown or JSON format
- Uses GitHub token from `.env` file or command-line argument
- Handles pagination for large PRs with many comments
- Customizable output directory and file naming

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - python-dotenv

## Installation

### From PyPI (Recommended)

```bash
pip install pullpal
```

### From Source

1. Clone the repository
   ```bash
   git clone https://github.com/TheRealFREDP3D/PullPal.git
   cd PullPal
   ```

2. Install the package
   ```bash
   pip install -e .
   ```

3. Set up your GitHub token in a `.env` file or provide it via command line

## Usage

### Command Line

After installation, you can use PullPal from the command line:

```bash
# Make sure you have a .env file with your GitHub token
# GITHUB_TOKEN=your_github_token_here

# Fetch a single PR
pullpal --pr 123

# Fetch multiple PRs
pullpal --prs 123,124,125

# Fetch the 10 most recently updated PRs
pullpal --latest 10

# Specify a custom output directory
pullpal --pr 123 --output-dir my_pr_data

# Save in JSON format instead of Markdown
pullpal --pr 123 --format json

# Override the token from .env file
pullpal --pr 123 --token YOUR_GITHUB_TOKEN

# Specify a different repository
pullpal --owner username --repo repository --pr 123
```

### Python API

You can also use PullPal as a library in your Python code:

```python
from pullpal.PullPal import fetch_conversation, save_conversation

# Fetch a PR conversation
conversation = fetch_conversation("octocat", "hello-world", 123, "your_github_token")

# Save the conversation as Markdown
save_conversation(conversation, "pr-123.md", "md")

# Or save as JSON
save_conversation(conversation, "pr-123.json", "json")
```

## Output Format

By default, the script saves conversations in Markdown format with the following structure:

```markdown
# PR #123: Title of the PR

**Author:** username
**Created:** 2023-01-01T00:00:00Z
**Updated:** 2023-01-02T00:00:00Z
**State:** open

## Description

PR description text...

## Comments

### username - 2023-01-01T12:00:00Z

Comment text...

## Reviews

### username - 2023-01-01T13:00:00Z

**State:** APPROVED

Review text...

## Review Comments

### username - 2023-01-01T14:00:00Z

**Path:** path/to/file.py
**Line:** 42

Review comment text...
```

You can also save in JSON format for programmatic processing.

## Default Settings

- Output directory: `pr-conversation`
- Output file format: `{repo}-{pr-number}.md`
- Default repository owner: `octocat`
- Default repository name: `hello-world`

You can override these defaults using command-line arguments.

## Use Cases

- Archive PR discussions for future reference
- Create documentation from PR conversations
- Analyze PR patterns and communication
- Export GitHub data for offline use or migration
- Generate reports on PR activity

---

*PullPal was originally developed as part of the [Gemini-Code-Assist-PR-Poetry](https://github.com/TheRealFREDP3D/Gemini-Code-Assist-PR-Poetry) project, which collects poems generated by Gemini Code Assist in GitHub pull requests.*
