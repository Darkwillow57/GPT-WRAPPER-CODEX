# GPT Wrapper

A simple web interface for interacting with the OpenAI Assistants API. Pick the model, set temperature and top-p, upload files and export conversations.

## Netlify

Deploy this directory to Netlify and set the environment variable `OPENAI_API_KEY` in your Netlify dashboard. Netlify installs dependencies automatically during deployment.

### Optional local development

If you want to test locally you can install dependencies and run Netlify dev:

```bash
npm install
env OPENAI_API_KEY=yourkey npm start
```

### Notes

The frontend fetches the available GPT models from OpenAI when it loads. When starting a new conversation the backend creates an assistant automatically using the selected model.

### Resetting your repository

If you lost the files in your GitHub repo, simply copy this project back or clone it again. Once `OPENAI_API_KEY` is set, Netlify will deploy normally.
