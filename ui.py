import streamlit as st
import os
import json
from dotenv import load_dotenv
import litellm
from emailBUDDY.agent import send_email

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Email Agent", page_icon="✉️")

st.title("✉️ Email Agent UI")
st.markdown("I can help you compose and send emails via Gmail. Tell me what you'd like to send!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a helpful email assistant.
You ONLY have the ability to SEND emails. You CANNOT read, check, or search the user's inbox, and you do not have any search tools. If the user asks you to check or read emails, politely inform them that you can only compose and send emails.

When the user asks to send an email:
1. Collect recipient, subject, and body.
2. If anything is missing, ask for it.
3. Show the draft to the user and ask for confirmation.
4. Only after the user explicitly confirms, use the send_email tool.
5. If the user declines, do not send the email."""
        }
    ]

# Define the tools available to the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email from the user's Gmail account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject line of the email"
                    },
                    "body": {
                        "type": "string",
                        "description": "Plain-text body content of the email"
                    }
                },
                "required": ["to", "subject", "body"]
            }
        }
    }
]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if message["role"] == "tool":
                st.markdown(f"**Tool Output:**\n```json\n{message['content']}\n```")
            elif message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    st.markdown(f"**Executing Tool:** `{tool_call.function.name}`\n```json\n{tool_call.function.arguments}\n```")
            else:
                if message.get("content"):
                    st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # First LLM call
            response = litellm.completion(
                model="groq/llama-3.1-8b-instant",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # Check for tool calls
            if response_message.tool_calls:
                st.session_state.messages.append(response_message.model_dump())
                
                for tool_call in response_message.tool_calls:
                    st.markdown(f"**Executing Tool:** `{tool_call.function.name}`\n```json\n{tool_call.function.arguments}\n```")
                    
                    if tool_call.function.name == "send_email":
                        args = json.loads(tool_call.function.arguments)
                        # Execute the tool
                        tool_result = send_email(args.get("to"), args.get("subject"), args.get("body"))
                        
                        # Add tool response to history
                        st.session_state.messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "send_email",
                            "content": json.dumps(tool_result)
                        })
                        
                        st.markdown(f"**Tool Output:**\n```json\n{json.dumps(tool_result, indent=2)}\n```")
                
                # Second LLM call after tool execution
                second_response = litellm.completion(
                    model="groq/llama-3.1-8b-instant",
                    messages=st.session_state.messages
                )
                final_content = second_response.choices[0].message.content
                if final_content:
                    st.markdown(final_content)
                    st.session_state.messages.append({"role": "assistant", "content": final_content})
            else:
                if response_message.content:
                    st.markdown(response_message.content)
                    st.session_state.messages.append({"role": "assistant", "content": response_message.content})
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
