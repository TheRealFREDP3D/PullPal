#!/usr/bin/env python3
"""
PullPal - GitHub Pull Request Conversation Tool

This tool fetches and saves the complete conversation history from GitHub pull requests,
including PR details, issue comments, review comments, and reviews.

The tool uses a .env file to get the GitHub token. Create a .env file with:
GITHUB_TOKEN=your_token_here

Usage examples:
    # Fetch a single PR
    pullpal --pr 123

    # Fetch multiple PRs
    pullpal --prs 123,124,125

    # Fetch the 10 most recently updated PRs
    pullpal --latest 10

    # Specify a custom output directory
    pullpal --pr 123 --output-dir my_pr_data

    # Override token from .env file
    pullpal --pr 123 --token YOUR_GITHUB_TOKEN

    # Specify a different repository
    pullpal --owner username --repo repository --pr 123
"""

import argparse
import json
import os
import shutil
import sys
import time
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
GITHUB_API_BASE_URL = "https://api.github.com"
DEFAULT_REPO_OWNER = "octocat"  # Default repository owner
DEFAULT_REPO_NAME = "hello-world"  # Default repository name

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header() -> None:
    """Display the PullPal header from header.md file."""
    header_path = os.path.join(os.path.dirname(__file__), 'header.md')
    try:
        with open(header_path, 'r', encoding='utf-8') as f:
            header_content = f.read()

        # Get terminal width
        terminal_width = shutil.get_terminal_size().columns

        # Center each line of the header
        centered_header = '\n'.join(
            line.center(terminal_width) for line in header_content.split('\n')
        )

        print(centered_header)
    except FileNotFoundError:
        raise

def display_loading_bar(duration=5, width=50) -> None:
    """Display a loading bar that fills over the specified duration."""
    terminal_width = shutil.get_terminal_size().columns

    # Position the loading bar in the center
    padding = (terminal_width - width) // 2

    print("\n" * 2)
    print("Loading PullPal...".center(terminal_width))

    for i in range(width + 1):
        time.sleep(duration / width)
        progress = i / width
        bar = "█" * i + "░" * (width - i)
        percent = int(progress * 100)

        # Clear the current line and print the updated loading bar
        sys.stdout.write("\r" + " " * padding + f"[{bar}] {percent}%")
        sys.stdout.flush()

    print("\n" * 2)
    print("Ready!".center(terminal_width))
    time.sleep(0.5)

def get_headers(token: str) -> Dict[str, str]:
    """Get headers for GitHub API requests.

    Args:
        token: GitHub personal access token

    Returns:
        Dictionary of headers for GitHub API requests

    Examples:
        >>> headers = get_headers("my_token")
        >>> headers["Authorization"]
        'token my_token'
        >>> headers["Accept"]
        'application/vnd.github.v3+json'
    """
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def fetch_review_comments(owner: str, repo: str, pr_number: int, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch review comments from the pull request."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    comments = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comments.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return comments

def fetch_issue_comments(owner: str, repo: str, pr_number: int, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch issue comments from the pull request."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    comments = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comments.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return comments

def fetch_reviews(owner: str, repo: str, pr_number: int, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch reviews from the pull request."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    reviews = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        reviews.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return reviews

def fetch_pr_details(owner: str, repo: str, pr_number: int, headers: Dict[str, str]) -> Dict[str, Any]:
    """Fetch basic details about the pull request."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_conversation(owner: str, repo: str, pr_number: int, token: str) -> Dict[str, Any]:
    """Fetch the full conversation of a pull request.

    This function fetches all components of a pull request conversation:
    - PR details (title, description, etc.)
    - Review comments (comments on specific lines of code)
    - Issue comments (comments on the PR as a whole)
    - Reviews (approvals, change requests, etc.)

    Args:
        owner: GitHub repository owner (username or organization)
        repo: GitHub repository name
        pr_number: Pull request number
        token: GitHub personal access token

    Returns:
        Dictionary containing all components of the PR conversation

    Examples:
        >>> conversation = fetch_conversation("octocat", "hello-world", 123, "my_token")
        >>> sorted(conversation.keys())
        ['issue_comments', 'pr_details', 'review_comments', 'reviews']
        >>> conversation['pr_details']['number']
        123
    """
    headers = get_headers(token)
    return {
        "pr_details": fetch_pr_details(owner, repo, pr_number, headers),
        "review_comments": fetch_review_comments(owner, repo, pr_number, headers),
        "issue_comments": fetch_issue_comments(owner, repo, pr_number, headers),
        "reviews": fetch_reviews(owner, repo, pr_number, headers)
    }

def format_conversation_as_markdown(conversation: Dict[str, Any]) -> str:
    """Format the conversation as Markdown.

    This function takes a PR conversation dictionary and formats it as a Markdown document.
    The Markdown includes sections for PR details, description, comments, reviews, and review comments.

    Args:
        conversation: Dictionary containing PR conversation components

    Returns:
        Formatted Markdown string

    Examples:
        >>> conversation = {
        ...     "pr_details": {
        ...         "number": 123,
        ...         "title": "Fix bug",
        ...         "user": {"login": "octocat"},
        ...         "created_at": "2023-01-01T00:00:00Z",
        ...         "updated_at": "2023-01-02T00:00:00Z",
        ...         "state": "open",
        ...         "body": "This PR fixes a bug"
        ...     },
        ...     "issue_comments": [],
        ...     "reviews": [],
        ...     "review_comments": []
        ... }
        >>> md = format_conversation_as_markdown(conversation)
        >>> md.startswith("# PR #123: Fix bug")
        True
        >>> "**Author:** octocat" in md
        True
    """
    pr_details = conversation.get("pr_details", {})
    md = []

    # PR Title and metadata
    md.append(f"# PR #{pr_details.get('number')}: {pr_details.get('title')}\n")
    md.append(f"**Author:** {pr_details.get('user', {}).get('login')}")
    md.append(f"**Created:** {pr_details.get('created_at')}")
    md.append(f"**Updated:** {pr_details.get('updated_at')}")
    md.append(f"**State:** {pr_details.get('state')}\n")

    # PR Description
    if pr_details.get('body'):
        md.append("## Description\n")
        md.append(f"{pr_details.get('body')}\n")

    # Issue Comments
    issue_comments = conversation.get("issue_comments", [])
    if issue_comments:
        md.append("## Comments\n")
        for comment in issue_comments:
            md.append(f"### {comment.get('user', {}).get('login')} - {comment.get('created_at')}\n")
            md.append(f"{comment.get('body')}\n")

    # Reviews
    reviews = conversation.get("reviews", [])
    if reviews:
        md.append("## Reviews\n")
        for review in reviews:
            md.append(f"### {review.get('user', {}).get('login')} - {review.get('submitted_at')}\n")
            md.append(f"**State:** {review.get('state')}\n")
            if review.get('body'):
                md.append(f"{review.get('body')}\n")

    # Review Comments
    review_comments = conversation.get("review_comments", [])
    if review_comments:
        md.append("## Review Comments\n")
        for comment in review_comments:
            md.append(f"### {comment.get('user', {}).get('login')} - {comment.get('created_at')}\n")
            md.append(f"**Path:** {comment.get('path')}")
            md.append(f"**Line:** {comment.get('line')}\n")
            md.append(f"{comment.get('body')}\n")

    return "\n".join(md)

def save_conversation(conversation: Dict[str, Any], output_file: str, format_type: str = "md") -> None:
    """Save the conversation to a file in the specified format.

    This function saves a PR conversation to a file in either Markdown or JSON format.

    Args:
        conversation: Dictionary containing PR conversation components
        output_file: Path to the output file
        format_type: Output format, either "md" (default) or "json"

    Returns:
        None

    Examples:
        >>> conversation = {"pr_details": {"number": 123}}
        >>> # This would save to a file in practice
        >>> # save_conversation(conversation, "pr-123.md", "md")
        >>> # save_conversation(conversation, "pr-123.json", "json")
    """
    with open(output_file, "w", encoding="utf-8") as f:
        if format_type == "json":
            json.dump(conversation, f, indent=2)
        else:  # md format
            f.write(format_conversation_as_markdown(conversation))
    print(f"Conversation saved to {output_file}")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="PullPal - Fetch GitHub pull request conversations")
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token (overrides .env file)"
    )
    parser.add_argument(
        "--owner",
        default=DEFAULT_REPO_OWNER,
        help=f"Repository owner (default: {DEFAULT_REPO_OWNER})"
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO_NAME,
        help=f"Repository name (default: {DEFAULT_REPO_NAME})"
    )

    # PR selection options (mutually exclusive)
    pr_group = parser.add_mutually_exclusive_group(required=True)
    pr_group.add_argument(
        "--pr",
        type=int,
        help="Single pull request number to fetch"
    )
    pr_group.add_argument(
        "--prs",
        type=str,
        help="Comma-separated list of PR numbers to fetch (e.g., '1,2,3')"
    )
    pr_group.add_argument(
        "--latest",
        type=int,
        help="Fetch the N latest pull requests"
    )

    parser.add_argument(
        "--output-dir",
        default="pr-conversation",
        help="Output directory for conversation files (default: 'pr-conversation')"
    )
    parser.add_argument(
        "--output-file",
        help="Output file path for single PR (default: {repo}-{pr-number}.md)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "md"],
        default="md",
        help="Output format: json or md (markdown) (default: md)"
    )
    return parser.parse_args()

def fetch_latest_prs(owner: str, repo: str, count: int, headers: Dict[str, str]) -> List[int]:
    """Fetch the latest N pull request numbers.

    This function fetches the most recently updated pull requests from a repository.

    Args:
        owner: GitHub repository owner (username or organization)
        repo: GitHub repository name
        count: Number of PRs to fetch
        headers: GitHub API request headers

    Returns:
        List of PR numbers

    Examples:
        >>> headers = get_headers("my_token")
        >>> # This would make an API call in practice
        >>> # pr_numbers = fetch_latest_prs("octocat", "hello-world", 3, headers)
        >>> # print(pr_numbers)  # Example output: [125, 124, 123]
    """
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls?state=all&sort=updated&direction=desc&per_page={count}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return [pr["number"] for pr in response.json()]

def process_pr(owner: str, repo: str, pr_number: int, token: str, output_path: str, format_type: str = "md") -> None:
    """Process a single PR and save its conversation."""
    print(f"Fetching pull request #{pr_number} conversation from {owner}/{repo}...")
    try:
        conversation = fetch_conversation(owner, repo, pr_number, token)
        save_conversation(conversation, output_path, format_type)
        print(f"Successfully saved PR #{pr_number} conversation to {output_path}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred for PR #{pr_number}: {e}")
    except Exception as e:
        print(f"An error occurred for PR #{pr_number}: {e}")

def main() -> int:
    """Main entry point for the application."""
    try:
        # Clear screen and display header
        clear_screen()
        display_header()
        time.sleep(2)

        # Display loading bar
        display_loading_bar(duration=5)

        # Clear screen again before executing main code
        clear_screen()

        args = parse_args()

        # Get GitHub token from args or environment
        github_token = args.token or os.environ.get("GITHUB_TOKEN")
        if not github_token:
            print("Error: GitHub token not provided. Either use --token or set GITHUB_TOKEN in .env file.")
            sys.exit(1)

        # Ensure token is a string
        github_token = str(github_token)

        # Create output directory if it doesn't exist
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
            print(f"Created output directory: {args.output_dir}")

        # Get list of PR numbers to process
        pr_numbers = []
        headers = get_headers(github_token)

        # Determine file extension based on format
        file_ext = ".json" if args.format == "json" else ".md"

        if args.pr:
            # Single PR
            pr_numbers = [args.pr]
            # Use output_file if provided, otherwise use default in output_dir
            if args.output_file:
                output_path = args.output_file
            else:
                output_path = os.path.join(args.output_dir, f"{args.repo}-{args.pr}{file_ext}")
            process_pr(args.owner, args.repo, args.pr, github_token, output_path, args.format)
        else:
            # Multiple PRs
            if args.prs:
                # Parse comma-separated list
                pr_numbers = [int(pr.strip()) for pr in args.prs.split(',')]
            elif args.latest:
                # Fetch latest PRs
                pr_numbers = fetch_latest_prs(args.owner, args.repo, args.latest, headers)
                print(f"Found {len(pr_numbers)} latest PRs: {pr_numbers}")

            # Process each PR
            for pr_number in pr_numbers:
                output_path = os.path.join(args.output_dir, f"{args.repo}-{pr_number}{file_ext}")
                process_pr(args.owner, args.repo, pr_number, github_token, output_path, args.format)

            print(f"Processed {len(pr_numbers)} pull requests. Results saved in {args.output_dir}")
        return 0
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())


