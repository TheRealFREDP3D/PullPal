#!/usr/bin/env python3
"""
Example script to fetch specific pull requests from a repository.

This script demonstrates how to use PullPal to fetch specific pull requests
from a GitHub repository and save them as Markdown files.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import PullPal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pullpal.PullPal import fetch_conversation, save_conversation

# Load environment variables from .env file
load_dotenv()

def main():
    """Fetch specific pull requests from a repository."""
    # Configuration
    owner = "octocat"
    repo = "hello-world"
    pr_numbers = [123, 124, 125]  # List of PR numbers to fetch
    output_dir = "pr-conversations"
    
    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GitHub token not provided. Set GITHUB_TOKEN in .env file.")
        return 1
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Process each PR
    for pr_number in pr_numbers:
        output_path = os.path.join(output_dir, f"{repo}-{pr_number}.md")
        print(f"Fetching pull request #{pr_number} conversation from {owner}/{repo}...")
        try:
            conversation = fetch_conversation(owner, repo, pr_number, github_token)
            save_conversation(conversation, output_path, "md")
            print(f"Successfully saved PR #{pr_number} conversation to {output_path}")
        except Exception as e:
            print(f"An error occurred for PR #{pr_number}: {e}")
    
    print(f"Processed {len(pr_numbers)} pull requests. Results saved in {output_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
