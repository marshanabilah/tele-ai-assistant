import os
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from src.utils import SCOPES

def get_credentials(self):
        """
        Get and refresh Gmail API credentials
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

def read_email(self, email=""):
    """
    Read emails from Gmail based on a query
    """

    creds = self.get_credentials()
    service = build("gmail", "v1", credentials=creds)

    query = ""
    if email:
        query += f' from:{email}'

    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query)
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return "No messages found."
        
        email_data = []
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            email_data.append(msg)
        
        return email_data
    except Exception as error:
        return f"An error occurred: {error}"

def _run(self,
        from_date: str,
        to_date: str,
        email: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.read_emails(email)