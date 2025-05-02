# Contributing to PullPal

Thank you for considering contributing to PullPal! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue with the following information:

- A clear, descriptive title
- A detailed description of the enhancement
- Any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run the tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository
2. Install the development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Create a `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

## Testing

Run the tests with:

```bash
python -m unittest discover tests
```

## Style Guide

This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
