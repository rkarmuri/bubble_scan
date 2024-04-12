# React App with Vite

This project was bootstrapped with [Vite](https://vitejs.dev/). It is a simple setup to get started with React and Vite.

## Getting Started

First, clone the repository and navigate into the project directory:

```bash
git clone <your-repository-url>
cd <your-project-name>
```

**Go to the bubblescan directory and run the React component using below commands**

```
cd bubblescan-client
npm install
npm install cors
npm run dev
```
**The React component is accessible at**
```bash
http://localhost:5173/
```

### You need to run the App server i.e `app.py` and Mock AI server `mock_ai.py` simultaneously to run the app
```bash
cd ServerCode\application
```
## Open two terminals and run the two servers using the commands below
# Flask Application Setup Guide

This guide provides step-by-step instructions for setting up a Flask application within a virtual environment. This ensures that your project dependencies are managed efficiently without affecting other Python projects.

## Prerequisites

Before you start, make sure you have Python installed on your system. Flask supports Python 3.6 and newer.

## Step 1: Go into ServerCode folder


```bash
cd ServerCode/application
```

## Step 2: Create the Virtual Environment

- **On macOS and Linux:**
```bash
python3 -m venv venv
```
- **On Windows:**
```bash
python -m venv venv
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

You can run your Flask applications using the `app.py` and `mock_ai.py`file as your entry point:

```bash
python3 app.py
python3 mock_ai.py
```

Your App server Flask application will be accessible at `http://127.0.0.1:5001/` and Mock AI application will be accessible at `http://127.0.0.1:5002/`.

## Step 7: Deactivate both the Virtual Environments

When you're done working on your project, you can deactivate the virtual environments by running:

```bash
deactivate
```

This command will return you to your system's default Python interpreter.

