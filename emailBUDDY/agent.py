"""
tool --> sends email --> subject, body, to
this credentials.json is having our consent to use email address that we setup
from google cloud console

so we need a method to use credentials.json and authorize the service

System prompt
agent --> tool wireup
done

"""

import traceback
import os
import base64
from email.message import EmailMessage

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail scope: send-only. If you later want to read/draft, add more scopes and
# delete token.json so the consent flow re-runs.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

load_dotenv()
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def _get_gmail_service():
    """Load cached OAuth credentials, refreshing or running the consent flow as needed."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_FILE}. Download an OAuth 2.0 'Desktop app' "
                    "client from the Google Cloud Console and save it there."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Opens a browser once for consent; token is cached to token.json afterward.
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email from the user's Gmail account.

    Args:
        to: Recipient email address.
        subject: Subject line of the email.
        body: Plain-text body content of the email.
    """
    try:
        service = _get_gmail_service()

        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject

        encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
        sent = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": encoded})
            .execute()
        )
        return {
            "status": "success",
            "message_id": sent.get("id"),
            "detail": f"Email sent to {to}.",
        }
   

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "detail": str(e)
    }


root_agent = Agent(
    name="email_agent",
    model=LiteLlm(model="groq/llama-3.1-8b-instant"),
    description="An agent that composes and sends emails on the user's behalf via Gmail.",
    instruction = """You are an email assistant.

You ONLY have the ability to SEND emails. You CANNOT read, check, or search the user's inbox, and you do not have any search tools. If the user asks you to check or read emails, politely inform them that you can only compose and send emails. Do not attempt to use any tools other than send_email.

When the user asks to send an email:

- Collect recipient, subject, and body.
- If anything is missing, ask for it.
- Show the draft.
- Ask for confirmation.
- Only after the user confirms, call send_email exactly once.
- Do not retry the tool if it fails.
- If the tool returns an error, report the error to the user.
      """  ,
    tools=[send_email],
)