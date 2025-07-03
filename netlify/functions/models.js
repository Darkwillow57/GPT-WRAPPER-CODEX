import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function handler(event) {
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const list = await openai.models.list();
    const models = list.data
      .filter((m) => m.id.startsWith('gpt-'))
      .map((m) => m.id);
    return {
      statusCode: 200,
      body: JSON.stringify({ models })
    };
  } catch (e) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: e.message })
    };
  }
}
