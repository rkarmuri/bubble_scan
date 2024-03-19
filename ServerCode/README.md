
# Flask Application Setup Guide

This guide provides step-by-step instructions for setting up a Flask application within a virtual environment. This ensures that your project dependencies are managed efficiently without affecting other Python projects.

## Prerequisites

Before you start, make sure you have Python installed on your system. Flask supports Python 3.6 and newer.

## Step 1: Go into ServerCode folder


```bash
cd serverCode
```

## Step 3: Activate the Virtual Environment

Before you can start using the virtual environment, you need to activate it. The command varies depending on your operating system.

- **On Windows:**

  ```cmd
  .\env\Scripts\activate
  ```

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

You'll know the virtual environment is activated because its name will appear at the beginning of the terminal prompt.

## Step 4: Install Flask or dependencies

With the virtual environment activated, install Flask using pip:

```bash
pip install Flask

pip3 install -r requirements.txt
```

## Step 5: Run Your Flask Application

You can run your Flask application by executing:

```bash
flask run
```

Or, if you're using the `app.py` file as your entry point:

```bash
python app.py
```

Your Flask application will be accessible at `http://127.0.0.1:5000/` by default.

## Step 7: Deactivate the Virtual Environment

When you're done working on your project, you can deactivate the virtual environment by running:

```bash
deactivate
```

This command will return you to your system's default Python interpreter.

