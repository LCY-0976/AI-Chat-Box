import streamlit as st
import requests
from database import get_data, save_api_response, clear_data
from datetime import datetime

FASTAPI_URL = "http://127.0.0.1:8000/"

def extract_message_text(ai_response):
    """Extract plain text from AI JSON response"""
    if isinstance(ai_response, dict):
        # Try common JSON response patterns
        if 'message' in ai_response:
            return ai_response['message']
        elif 'response' in ai_response:
            return ai_response['response']
        elif 'content' in ai_response:
            return ai_response['content']
        elif 'text' in ai_response:
            return ai_response['text']
        else:
            # If no known key, return the first string value found
            for value in ai_response.values():
                if isinstance(value, str):
                    return value
            # If no string found, return the whole dict as string
            return str(ai_response)
    else:
        # If it's already a string, return as is
        return str(ai_response)

st.title("Expert Chat 🔥")
st.write("Chat with an expert! All conversations are saved. 😊")

# Display conversation history
st.subheader("📝 Conversation History")
conversation_data = get_data()

if conversation_data:
    # Display conversations in reverse order (newest first)
    for entry in reversed(conversation_data[-10:]):  # Show last 10 conversations
        with st.expander(f"💬 {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"):
            data = entry.data
            if 'original' in data and 'processed' in data:
                st.write(f"**You:** {data['original']}")
                # Extract plain text from JSON response
                ai_text = extract_message_text(data['processed'])
                st.write(f"**AI:** {ai_text}")
else:
    st.info("No conversation history yet. Start chatting below!")

st.divider()

# Chat interface
st.subheader("💭 New Message")
user_input = st.text_input("Enter your message:")

col1, col2 = st.columns(2)

with col1:
    if st.button("💖 Psychologist Response", use_container_width=True):
        if user_input:
            with st.spinner("Getting psychologist response..."):
                try:
                    response = requests.post(
                        FASTAPI_URL + "api/psychologist",
                        json={
                            "user_text": user_input,
                            "role": "You are a super professional psychologist. Please respond in JSON format with a 'message' field containing your response."
                        }
                    )
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Make sure FastAPI server is running on port 8000.")
                    st.stop()
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if response has error
                if 'error' in result:
                    st.error(f"❌ Server error: {result['error']}")
                elif 'original' in result and 'processed' in result:
                    # Save to database (keeps JSON format)
                    save_api_response(result)
                    
                    # Display as plain text to user
                    ai_text = extract_message_text(result['processed'])
                    st.success(f"**You:** {result['original']}")
                    st.success(f"**Psychologist:** {ai_text}")
                    
                    # Auto-refresh to show updated history
                    st.rerun()
                else:
                    st.error(f"❌ Unexpected response format: {result}")
            else:
                st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
        else:
            st.warning("Please enter a message first")

with col2:
    if st.button("💙 Physicist Response", use_container_width=True):
        if user_input:
            with st.spinner("Getting physicist response..."):
                try:
                    response = requests.post(
                        FASTAPI_URL + "api/physicist",
                        json={
                            "user_text": user_input,
                            "role": "You are a super professional physicist. Please respond in JSON format with a 'message' field containing your response."
                        }
                    )
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Make sure FastAPI server is running on port 8000.")
                    st.stop()
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if response has error
                if 'error' in result:
                    st.error(f"❌ Server error: {result['error']}")
                elif 'original' in result and 'processed' in result:
                    # Save to database (keeps JSON format)
                    save_api_response(result)
                    
                    # Display as plain text to user
                    ai_text = extract_message_text(result['processed'])
                    st.success(f"**You:** {result['original']}")
                    st.success(f"**Physicist:** {ai_text}")
                    
                    # Auto-refresh to show updated history
                    st.rerun()
                else:
                    st.error(f"❌ Unexpected response format: {result}")
            else:
                st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
        else:
            st.warning("Please enter a message first")

# Add a clear history button
st.divider()
if st.button("🗑️ Clear Chat History", type="secondary"):
    if st.session_state.get('confirm_clear', False):
        st.info("Clear history successfully")
        st.session_state.confirm_clear = False
    else:
        st.session_state.confirm_clear = True
        clear_data()
        st.warning("Click again to confirm clearing all chat history")