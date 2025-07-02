
# 🗒️ FastMCP Google Tasks Server

Manage Google Tasks using a simple FastMCP API server for Gemini-CLI

## 🚀 Features

- Fetch tasks
- Create tasks with notes and due dates

## 🔧 Setup

### Install Dependencies

```bash
pip install uv
cd gemini-tasks-mcp
uv venv
uv pip install
```

### Generate Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **Google Tasks API**.
3. Go to **APIs & Services → Credentials**.
4. Click **“Create Credentials” → “OAuth client ID” → Application type: Desktop App**.
5. Download `credentials.json` and place it in the project folder.


### Gemini-CLI Configuration

```bash
cd ~/.gemini
nano settings.json
```

```json
"mcpServers": {
    "gmailReader": {
      "command": "uv",
      "args": ["run", "main.py"],
      "cwd": "<<full-path>>/gemini-tasks-mcp",
      "timeout": 20000
    },
}
```