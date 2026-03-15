"""
Simple Streamlit app to test LLM proxy endpoint
"""
import streamlit as st
import requests
import json
import anthropic
import os

# Custom CSS for clean interface
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }

    /* Style the title */
    .main .block-container h1:first-of-type {
        font-size: 1.5rem;
        font-weight: 500;
        color: #202124;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("Mythical Enterprise Chatbot")

def summarize_response(user_prompt, llm_response):
    """Use Claude to extract just the answer from the LLM response"""
    try:
        # Check if ANTHROPIC_API_KEY is available
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return llm_response  # Return original if no API key

        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Given this user prompt:
"{user_prompt}"

And this LLM response:
"{llm_response}"

Extract and present ONLY the direct answer to the user's prompt. Remove any preamble, explanations, or extra formatting. Just provide the core answer."""
            }]
        )

        # Extract the text from Claude's response
        for block in response.content:
            if block.type == "text":
                return block.text

        return llm_response  # Fallback to original
    except Exception as e:
        return llm_response  # Return original on error

# Settings Section
st.sidebar.header("⚙️ Settings")

LLM_PROXY_URL = st.sidebar.text_input(
    "LLM Proxy Endpoint URL",
    value="",
    placeholder="https://llm-gateway-6qzbeu.h37dvc.usa-e2.cloudhub.io/MythicalLLMProxy/responses",
    help="Enter your LLM proxy endpoint URL"
)

CLIENT_ID = st.sidebar.text_input(
    "Client ID",
    value="",
    placeholder="your-client-id",
    help="Enter your OAuth client ID"
)

CLIENT_SECRET = st.sidebar.text_input(
    "Client Secret",
    type="password",
    value="",
    placeholder="your-client-secret",
    help="Enter your OAuth client secret"
)

st.sidebar.markdown("---")

# Prompt input
prompt = st.text_area(
    "Enter your prompt:",
    height=150,
    placeholder="What would you like to ask the LLM?"
)

# Submit button
if st.button("Send Request", type="primary"):
    if not prompt:
        st.warning("Please enter a prompt")
    elif not LLM_PROXY_URL:
        st.warning("Please enter an LLM proxy endpoint URL")
    elif not CLIENT_ID or not CLIENT_SECRET:
        st.warning("Please enter both Client ID and Client Secret")
    else:
        with st.spinner("Calling LLM proxy..."):
            try:
                # Prepare request
                headers = {
                    "Content-Type": "application/json",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET
                }

                payload = {
                    "input": prompt
                }

                # Make request
                response = requests.post(
                    LLM_PROXY_URL,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                # Display response
                st.success("✅ Response received!")

                # Show the LLM response
                st.subheader("LLM Response")
                if response.status_code == 200:
                    try:
                        response_data = response.json()

                        # Extract the text from the response structure
                        raw_response = None

                        # Check if response is an array (new structure)
                        if isinstance(response_data, list):
                            # Find the message object in the array
                            for item in response_data:
                                if isinstance(item, dict) and item.get("type") == "message":
                                    content = item.get("content", [])
                                    if isinstance(content, list):
                                        # Find the output_text item
                                        for content_item in content:
                                            if isinstance(content_item, dict) and content_item.get("type") == "output_text":
                                                raw_response = content_item.get("text", "")
                                                break
                                    break

                        # Fallback to checking common field names
                        if not raw_response and isinstance(response_data, dict):
                            if "information" in response_data:
                                raw_response = response_data["information"]
                            elif "response" in response_data:
                                raw_response = response_data["response"]
                            elif "output" in response_data:
                                raw_response = response_data["output"]
                            elif "content" in response_data:
                                # Content might be a list (array structure)
                                content = response_data["content"]
                                if isinstance(content, list):
                                    # Find the message object in the content array
                                    for item in content:
                                        if isinstance(item, dict) and item.get("type") == "message":
                                            msg_content = item.get("content", [])
                                            if isinstance(msg_content, list):
                                                # Find the output_text item
                                                for content_item in msg_content:
                                                    if isinstance(content_item, dict) and content_item.get("type") == "output_text":
                                                        raw_response = content_item.get("text", "")
                                                        break
                                            break
                                else:
                                    raw_response = content

                        # If raw_response is still a list, extract the text from it
                        if isinstance(raw_response, list):
                            for item in raw_response:
                                if isinstance(item, dict) and item.get("type") == "message":
                                    msg_content = item.get("content", [])
                                    if isinstance(msg_content, list):
                                        # Find the output_text item
                                        for content_item in msg_content:
                                            if isinstance(content_item, dict) and content_item.get("type") == "output_text":
                                                text = content_item.get("text", "")
                                                if text:
                                                    raw_response = text
                                                    break
                                    if isinstance(raw_response, str):
                                        break


                        # Display the response
                        if raw_response:
                            st.write(raw_response)
                        else:
                            # Show the whole response if no text field is found
                            st.warning("Could not extract text field. Showing full response:")
                            st.json(response_data)

                        # Display token usage and cost
                        if "usage" in response_data:
                            st.subheader("Usage & Cost")
                            usage = response_data["usage"]

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                input_tokens = usage.get("input_tokens", 0)
                                st.metric("Input Tokens", f"{input_tokens:,}")

                            with col2:
                                output_tokens = usage.get("output_tokens", 0)
                                st.metric("Output Tokens", f"{output_tokens:,}")

                            with col3:
                                total_tokens = input_tokens + output_tokens
                                st.metric("Total Tokens", f"{total_tokens:,}")

                            # Calculate approximate cost
                            # Assuming Claude pricing (adjust based on your actual model)
                            # Input: $3 per 1M tokens, Output: $15 per 1M tokens (Claude Sonnet 4 example)
                            input_cost = (input_tokens / 1_000_000) * 3.00
                            output_cost = (output_tokens / 1_000_000) * 15.00
                            total_cost = input_cost + output_cost

                            st.markdown(f"**Approximate Cost:** ${total_cost:.6f}")
                            st.caption("*Cost calculated based on standard pricing. Actual cost may vary.*")

                    except json.JSONDecodeError:
                        st.text(response.text)
                else:
                    st.error(f"Error: Status code {response.status_code}")
                    st.text(response.text)

                # Display specific headers
                st.subheader("Proxy Metadata")
                col1, col2 = st.columns(2)

                with col1:
                    provider = response.headers.get("x-llm-proxy-llm-provider", "Not provided")
                    st.metric("Provider", provider)

                with col2:
                    model = response.headers.get("x-llm-proxy-llm-model", "Not provided")
                    st.metric("Model", model)

                # Show all response headers (collapsible)
                with st.expander("View All Response Headers"):
                    st.json(dict(response.headers))

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# Instructions
with st.sidebar:
    st.markdown("### Instructions")
    st.markdown("""
    1. Enter your LLM proxy endpoint URL
    2. Add your Client ID and Client Secret
    3. Type your prompt
    4. Click 'Send Request'
    5. View the response and proxy metadata
    """)
