"""
FastMCP Google Tasks Server
"""

from fastmcp import FastMCP
from typing import List
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# ✅ Create MCP server
mcp = FastMCP("Google Tasks Manager")


# ✅ Google Tasks API setup
SCOPES = ['https://www.googleapis.com/auth/tasks']
script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_dir, 'credentials.json')
token_path = os.path.join(script_dir, 'token.pickle')


def get_tasks_service():
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    service = build('tasks', 'v1', credentials=creds)
    return service


# ✅ Read tasks MCP tool
@mcp.tool
def read_tasks(max_results: int = 10) -> List[dict]:
    """
    Fetch tasks from the default Google Tasks list.
    """
    service = get_tasks_service()

    results = service.tasks().list(
        tasklist='@default',
        maxResults=max_results,
        showCompleted=True
    ).execute()

    tasks = results.get('items', [])
    task_list = []

    for task in tasks:
        task_list.append({
            'id': task.get('id'),
            'title': task.get('title'),
            'notes': task.get('notes', ''),
            'status': task.get('status'),
            'due': task.get('due', None)
        })

    return task_list


# ✅ Create task MCP tool
@mcp.tool
def create_task(title: str, notes: str = "", due: str = None) -> dict:
    """
    Create a new task in the default Google Tasks list.
    """
    service = get_tasks_service()

    task_body = {
        'title': title,
        'notes': notes
    }
    if due:
        task_body['due'] = due  # Format: '2025-07-02T12:00:00.000Z'

    result = service.tasks().insert(
        tasklist='@default',
        body=task_body
    ).execute()

    return {
        'id': result.get('id'),
        'title': result.get('title'),
        'status': result.get('status'),
        'due': result.get('due', None)
    }


# ✅ Run MCP server
if __name__ == "__main__":
    mcp.run()