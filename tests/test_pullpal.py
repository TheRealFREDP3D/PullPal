#!/usr/bin/env python3
"""
Tests for PullPal.

This module contains tests for the PullPal module.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import PullPal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pullpal.PullPal import (
    fetch_conversation,
    fetch_issue_comments,
    fetch_latest_prs,
    fetch_pr_details,
    fetch_review_comments,
    fetch_reviews,
    format_conversation_as_markdown,
    get_headers,
    save_conversation,
)


class TestPullPal(unittest.TestCase):
    """Tests for PullPal."""

    def test_get_headers(self):
        """Test get_headers function."""
        token = "test_token"
        headers = get_headers(token)
        self.assertEqual(headers["Authorization"], "token test_token")
        self.assertEqual(headers["Accept"], "application/vnd.github.v3+json")

    @patch('pullpal.PullPal.requests.get')
    def test_fetch_pr_details(self, mock_get):
        """Test fetch_pr_details function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"number": 123, "title": "Test PR"}
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_pr_details("owner", "repo", 123, {})

        # Check the result
        self.assertEqual(result["number"], 123)
        self.assertEqual(result["title"], "Test PR")

        # Check that the correct URL was called
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls/123",
            headers={}
        )

    @patch('pullpal.PullPal.requests.get')
    def test_fetch_review_comments(self, mock_get):
        """Test fetch_review_comments function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "body": "Test comment"}]
        mock_response.links = {}
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_review_comments("owner", "repo", 123, {})

        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["body"], "Test comment")

        # Check that the correct URL was called
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls/123/comments",
            headers={}
        )

    @patch('pullpal.PullPal.requests.get')
    def test_fetch_issue_comments(self, mock_get):
        """Test fetch_issue_comments function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "body": "Test issue comment"}]
        mock_response.links = {}
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_issue_comments("owner", "repo", 123, {})

        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["body"], "Test issue comment")

        # Check that the correct URL was called
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues/123/comments",
            headers={}
        )

    @patch('pullpal.PullPal.requests.get')
    def test_fetch_reviews(self, mock_get):
        """Test fetch_reviews function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "state": "APPROVED"}]
        mock_response.links = {}
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_reviews("owner", "repo", 123, {})

        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["state"], "APPROVED")

        # Check that the correct URL was called
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls/123/reviews",
            headers={}
        )

    @patch('pullpal.PullPal.fetch_pr_details')
    @patch('pullpal.PullPal.fetch_review_comments')
    @patch('pullpal.PullPal.fetch_issue_comments')
    @patch('pullpal.PullPal.fetch_reviews')
    def test_fetch_conversation(self, mock_reviews, mock_issue_comments, mock_review_comments, mock_pr_details):
        """Test fetch_conversation function."""
        # Mock the responses
        mock_pr_details.return_value = {"number": 123, "title": "Test PR"}
        mock_review_comments.return_value = [{"id": 1, "body": "Test review comment"}]
        mock_issue_comments.return_value = [{"id": 2, "body": "Test issue comment"}]
        mock_reviews.return_value = [{"id": 3, "state": "APPROVED"}]

        # Call the function
        result = fetch_conversation("owner", "repo", 123, "test_token")

        # Check the result
        self.assertEqual(result["pr_details"]["number"], 123)
        self.assertEqual(result["pr_details"]["title"], "Test PR")
        self.assertEqual(len(result["review_comments"]), 1)
        self.assertEqual(result["review_comments"][0]["id"], 1)
        self.assertEqual(len(result["issue_comments"]), 1)
        self.assertEqual(result["issue_comments"][0]["id"], 2)
        self.assertEqual(len(result["reviews"]), 1)
        self.assertEqual(result["reviews"][0]["id"], 3)

    def test_format_conversation_as_markdown(self):
        """Test format_conversation_as_markdown function."""
        # Create a test conversation
        conversation = {
            "pr_details": {
                "number": 123,
                "title": "Test PR",
                "user": {"login": "testuser"},
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "state": "open",
                "body": "This is a test PR"
            },
            "issue_comments": [
                {
                    "user": {"login": "commenter"},
                    "created_at": "2023-01-03T00:00:00Z",
                    "body": "This is a comment"
                }
            ],
            "reviews": [
                {
                    "user": {"login": "reviewer"},
                    "submitted_at": "2023-01-04T00:00:00Z",
                    "state": "APPROVED",
                    "body": "LGTM"
                }
            ],
            "review_comments": [
                {
                    "user": {"login": "reviewer"},
                    "created_at": "2023-01-04T00:00:00Z",
                    "path": "file.py",
                    "line": 42,
                    "body": "Nice code"
                }
            ]
        }

        # Format the conversation
        markdown = format_conversation_as_markdown(conversation)

        # Check the result
        self.assertIn("# PR #123: Test PR", markdown)
        self.assertIn("**Author:** testuser", markdown)
        self.assertIn("**Created:** 2023-01-01T00:00:00Z", markdown)
        self.assertIn("**Updated:** 2023-01-02T00:00:00Z", markdown)
        self.assertIn("**State:** open", markdown)
        self.assertIn("## Description", markdown)
        self.assertIn("This is a test PR", markdown)
        self.assertIn("## Comments", markdown)
        self.assertIn("### commenter - 2023-01-03T00:00:00Z", markdown)
        self.assertIn("This is a comment", markdown)
        self.assertIn("## Reviews", markdown)
        self.assertIn("### reviewer - 2023-01-04T00:00:00Z", markdown)
        self.assertIn("**State:** APPROVED", markdown)
        self.assertIn("LGTM", markdown)
        self.assertIn("## Review Comments", markdown)
        self.assertIn("### reviewer - 2023-01-04T00:00:00Z", markdown)
        self.assertIn("**Path:** file.py", markdown)
        self.assertIn("**Line:** 42", markdown)
        self.assertIn("Nice code", markdown)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_conversation_json(self, mock_json_dump, mock_open):
        """Test save_conversation function with JSON format."""
        # Create a test conversation
        conversation = {"pr_details": {"number": 123}}

        # Call the function
        save_conversation(conversation, "test.json", "json")

        # Check that the file was opened correctly
        mock_open.assert_called_once_with("test.json", "w", encoding="utf-8")

        # Check that json.dump was called with the conversation
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        self.assertEqual(args[0], conversation)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('pullpal.PullPal.format_conversation_as_markdown')
    def test_save_conversation_markdown(self, mock_format, mock_open):
        """Test save_conversation function with Markdown format."""
        # Create a test conversation and mock the format function
        conversation = {"pr_details": {"number": 123}}
        mock_format.return_value = "# Markdown content"

        # Call the function
        save_conversation(conversation, "test.md", "md")

        # Check that the file was opened correctly
        mock_open.assert_called_once_with("test.md", "w", encoding="utf-8")

        # Check that format_conversation_as_markdown was called
        mock_format.assert_called_once_with(conversation)

        # Check that the formatted content was written to the file
        file_handle = mock_open()
        file_handle.write.assert_called_once_with("# Markdown content")

    @patch('pullpal.PullPal.requests.get')
    def test_fetch_latest_prs(self, mock_get):
        """Test fetch_latest_prs function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"number": 123},
            {"number": 124},
            {"number": 125}
        ]
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_latest_prs("owner", "repo", 3, {})

        # Check the result
        self.assertEqual(result, [123, 124, 125])

        # Check that the correct URL was called
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls?state=all&sort=updated&direction=desc&per_page=3",
            headers={}
        )

if __name__ == "__main__":
    unittest.main()
