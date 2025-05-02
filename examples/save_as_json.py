#!/usr/bin/env python3
"""
Example script to fetch a pull request and save it as JSON.

This script demonstrates how to use PullPal to fetch a pull request
from a GitHub repository and save it as a JSON file for programmatic processing.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the path so we can import PullPal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pullpal.PullPal import fetch_conversation, save_conversation

# Load environment variables from .env file
load_dotenv()

def main():
    """Fetch a pull request and save it as JSON."""
    # Configuration
    owner = "octocat"
    repo = "hello-world"
    pr_number = 123
    output_dir = "pr-conversations"
    
    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GitHub token not provided. Set GITHUB_TOKEN in .env file.")
        return 1
    
    try:
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    except OSError as e:
        print(f"Error creating directory {output_dir}: {e}")
        return 1
    
    # Fetch and save the PR conversation
    output_path = os.path.join(output_dir, f"{repo}-{pr_number}.json")
    print(f"Fetching pull request #{pr_number} conversation from {owner}/{repo}...")
    try:
        conversation = fetch_conversation(owner, repo, pr_number, github_token)
        save_conversation(conversation, output_path, "json")
        print(f"Successfully saved PR #{pr_number} conversation to {output_path}")
        
        # Example of processing the JSON data
        print("\nExample of processing the JSON data:")
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Print some information from the PR
        print(f"PR Title: {data['pr_details']['title']}")
        print(f"PR Author: {data['pr_details']['user']['login']}")
        print(f"Number of comments: {len(data['issue_comments'])}")
        print(f"Number of reviews: {len(data['reviews'])}")
        print(f"Number of review comments: {len(data['review_comments'])}")
        
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
