# GPT Wrapper

A simple web interface for interacting with the OpenAI Assistants API. Pick the model, set temperature and top-p, upload files and export conversations.

## Netlify

Deploy this directory to Netlify. Set the environment variable `OPENAI_API_KEY` in your Netlify dashboard.

### Development

Install dependencies and run Netlify dev:

```bash
npm install
env OPENAI_API_KEY=yourkey npm start
```

This runs the site locally.

### Notes

The frontend fetches the available GPT models from OpenAI when it loads. When starting a new conversation the backend creates an assistant automatically using the selected model.
