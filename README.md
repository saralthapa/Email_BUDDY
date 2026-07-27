# 📧 emailBUDDY

An AI-powered Gmail assistant built using **Streamlit** and the **Groq API** (via LiteLLM). emailBUDDY provides a clean chat interface that allows you to generate intelligent, context-aware emails on behalf of the user and send them using the Gmail API and OAuth 2.0 authentication.

---

# 🚀 Features

* 🤖 AI-generated email composition
* 📩 Gmail API integration for sending emails
* 🔐 OAuth 2.0 authentication
* ⚡ Fast inference using Groq LLM (llama-3.1-8b-instant)
* 🎨 Clean, interactive Streamlit web UI
* 🔒 Secure API key and token management

---

# 🛠️ Tech Stack

* Python
* Streamlit (Web UI)
* LiteLLM (LLM Router)
* Groq API
* Gmail API & Google API Python Client
* Google OAuth 2.0
* python-dotenv

---

# 📁 Project Structure

```text
emailBUDDY/
│
├── emailBUDDY/
│   ├── __init__.py
│   ├── agent.py
│   ├── prompt.py
│   └── tools.py  
│
├── ui.py                 # Streamlit application entry point
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── credentials.json      # Excluded from GitHub for security
└── token.json            # Generated after authentication, excluded from GitHub
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/saralthapa/Email_buddy.git
cd emailBUDDY
```

### Create a virtual environment

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root to store your sensitive keys.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# 🔐 Gmail API Setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Gmail API**.
3. Configure the **OAuth Consent Screen** (add your testing email).
4. Create **OAuth Client Credentials** (Select **Desktop app**).
5. Download the OAuth credentials JSON file.
6. Save the downloaded file into the root of this project as exactly:

```text
credentials.json
```

7. Run the application once. The first time you ask emailBUDDY to send an email, it will open your browser to complete the Google authentication flow.

A `token.json` file will be generated automatically after successful authentication.

> **Security Note: Do not upload `.env`, `credentials.json`, or `token.json` to GitHub. The included `.gitignore` file automatically protects these files from being tracked.**

---

# ▶️ Running emailBUDDY

Start the interactive Streamlit web interface:

```bash
streamlit run ui.py
```

This will launch a local web server (usually at `http://localhost:8501`) and open your default browser.

---

# 📌 Workflow & Output

1. **User Input:** You enter a prompt in the Streamlit chat (e.g., "Send an email to John about the meeting tomorrow").
2. **AI Processing:** The Groq LLM processes your request and asks for missing details (subject, recipient, body).
3. **Confirmation:** The AI drafts the email and presents it to you for confirmation.
4. **Tool Execution:** Once you approve, the LLM triggers the `send_email` tool. The Streamlit UI will output the raw JSON tool call payload.
5. **Gmail API:** The `agent.py` script securely authenticates using your `token.json` and sends the email.
6. **Final Output:** The UI prints the success status and message ID returned by Gmail, and the AI gives you a final confirmation message.

---

# 🔒 Security

Protecting your sensitive data is a top priority. The repository is pre-configured to be public-ready. The following sensitive files are explicitly excluded from version control via `.gitignore`:

```text
.env
credentials.json
token.json
venv/
__pycache__/
```
Make sure you never force-add these files to your repository.

---

# 🚀 Future Enhancements

* ✨ Email summarisation
* 🌍 Multi-language replies
* 📝 Tone customization (Formal, Friendly, Professional)
* 📅 Google Calendar integration
* 📎 Attachment analysis
* ⭐ Priority email detection
* 💬 Conversation memory
* 📊 Email analytics dashboard

---

# 👨‍💻 Author

**Saral Thapa**

GitHub: https://github.com/saralthapa

---
# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.
