To publish your tool **[PullPal](https://github.com/TheRealFREDP3D/pullpal)** to PyPI so it can be installed using `pip install pullpal`, you’ll need to:

* Prepare your Python package correctly
* Build the distribution files
* Upload them to [PyPI](https://pypi.org/)

Here’s a **step-by-step guide** with explanations and commands.

---

## ✅ Step 1: Structure Your Project Correctly

Your project already looks pretty good, but you need to make sure the structure looks something like this:

```bash
pullpal/
├── pullpal/             # Your actual package code
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_basic.py
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.cfg           # optional, but useful
├── setup.py            # optional with pyproject.toml
```

---

## ✅ Step 2: Create `pyproject.toml`

Create a `pyproject.toml` in the root directory:

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pullpal"
version = "0.1.0"
description = "PullPal - PR Suggestion Archivist Tool"
readme = "README.md"
requires-python = ">=3.8"
license = { file = "LICENSE" }
authors = [
  { name="Frederick Pellerin", email="youremail@example.com" }
]
dependencies = [
  "requests",
  "rich",
  "typer"
]

[project.urls]
"Homepage" = "https://github.com/TheRealFREDP3D/pullpal"

[project.scripts]
pullpal = "pullpal.main:app"
```

> This will make `pullpal` available as a CLI command if your `main.py` contains a Typer app like `app = typer.Typer()`.

---

## ✅ Step 3: Add `__init__.py`

Your `pullpal` folder should have an `__init__.py`, even if it's empty:

```bash
touch pullpal/__init__.py
```

---

## ✅ Step 4: Build Your Package

Make sure you’re in your root folder (where `pyproject.toml` is).

```bash
pip install build
python -m build
```

This will generate:

```
dist/
├── pullpal-0.1.0.tar.gz
└── pullpal-0.1.0-py3-none-any.whl
```

---

## ✅ Step 5: Upload to PyPI

### a. Create a PyPI Account

* Register on [https://pypi.org/account/register/](https://pypi.org/account/register/)
* Generate an API token at [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)

> Store the token securely. You’ll use it in the `.pypirc` file or `twine`.

### b. Install `twine`

```bash
pip install twine
```

### c. Upload your package

```bash
twine upload dist/*
```

You’ll be prompted for your PyPI username and password (or token if using API token with username `__token__`).

---

## ✅ Step 6: Test It!

Install it from PyPI to make sure it works:

```bash
pip install pullpal
pullpal --help
```

---

## 🧪 Optional: Test on TestPyPI First

To avoid messing up the real PyPI if it’s your first time, use [TestPyPI](https://test.pypi.org):

```bash
twine upload --repository testpypi dist/*
```

Then test install with:

```bash
pip install --index-url https://test.pypi.org/simple/ pullpal
```

---

## 🧠 Extra Tips

* Use [GitHub Actions](https://packaging.python.org/en/latest/tutorials/packaging-projects/#automating-publishing) to automate your releases.
* Set up `bumpversion` or `hatch` to manage versions cleanly.
* Consider adding a `MANIFEST.in` if you want to include extra files like examples or configs.

---

## 🧵 Resources for Learning More

* 🔧 [Python Packaging User Guide](https://packaging.python.org/)
* 🧪 [TestPyPI guide](https://packaging.python.org/en/latest/guides/using-testpypi/)
* 🧵 [Publishing on PyPI Tutorial (Official)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
* 📦 [Typer Docs for CLI tools](https://typer.tiangolo.com/)

---

Want me to review your current `pyproject.toml` or help generate it from your code? Drop a file or paste `main.py`, I’ll tailor it for you.
