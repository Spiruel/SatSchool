# SatSchool

SatSchool "Working with Data" module.

## Getting Started

If you wish to deploy this webapp on your own computer, follow the instructions below:

### 1. Prerequisites

This project uses `uv` for fast Python package management. If you don't have it installed, you can get it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup Environment

Create a virtual environment and install dependencies from `requirements.txt`:

```bash
uv venv
uv pip install -r requirements.txt
```

### 3. Earth Engine Authentication

To use Google Earth Engine, you need to authenticate your machine. Run the following command and follow the instructions in your browser:

```bash
earthengine authenticate
```

### 4. Project Configuration

The Earth Engine project ID is centrally defined in `config.py`. If you are using your own project, update this value:

```python
# config.py
EE_PROJECT = 'your-project-id'
```

### 5. Running the Application locally

Launch the Streamlit app using `uv`:

```bash
uv run streamlit run app.py
```

## Deployment

If deploying to Streamlit Cloud, you should add your Earth Engine credentials to Streamlit Secrets:
`EARTHENGINE_TOKEN = "YOUR_TOKEN_HERE"`

## Questions?

Samuel Bancroft
spiruel@gmail.com
