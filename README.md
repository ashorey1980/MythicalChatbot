# LLM Proxy Tester

A simple Streamlit app for testing LLM proxy endpoints.

## Features

- Configure LLM proxy endpoint URL
- OAuth authentication with Client ID and Secret
- Send prompts to the LLM
- Display responses in a friendly format
- View proxy metadata headers:
  - `x-llm-proxy-llm-provider`
  - `x-llm-proxy-llm-model`

## Usage

1. Install dependencies:
```bash
pip install streamlit requests
```

2. Run the app:
```bash
streamlit run app.py
```

3. Configure settings in the sidebar:
   - LLM Proxy Endpoint URL
   - Client ID
   - Client Secret

4. Enter your prompt and click "Send Request"

## API Format

The app sends requests in this format:
```json
POST {endpoint_url}
Headers:
  - Content-Type: application/json
  - client_id: {your_client_id}
  - client_secret: {your_client_secret}
Body:
  {
    "input": "your prompt here"
  }
```
