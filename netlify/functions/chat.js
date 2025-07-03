import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const {
      message,
      thread_id,
      assistant_id,
      model,
      temperature,
      top_p
    } = JSON.parse(event.body || '{}');

    let threadId = thread_id;
    if (!threadId) {
      const thread = await openai.beta.threads.create();
      threadId = thread.id;
    }

    let assistantId = assistant_id;
    if (!assistantId) {
      const assistant = await openai.beta.assistants.create({
        model,
        instructions: 'Personal assistant'
      });
      assistantId = assistant.id;
    }

    await openai.beta.threads.messages.create(threadId, {
      role: 'user',
      content: message
    });

    const run = await openai.beta.threads.runs.create(threadId, {
      assistant_id: assistantId,
      model,
      temperature,
      top_p
    });

    let runStatus;
    do {
      await new Promise((r) => setTimeout(r, 1000));
      runStatus = await openai.beta.threads.runs.retrieve(threadId, run.id);
    } while (runStatus.status !== 'completed' && runStatus.status !== 'failed');

    if (runStatus.status === 'failed') {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Run failed' })
      };
    }

    const messages = await openai.beta.threads.messages.list(threadId);
    const lastMessage = messages.data[0];

    return {
      statusCode: 200,
      body: JSON.stringify({
        reply: lastMessage.content[0].text.value,
        thread_id: threadId,
        assistant_id: assistantId
      })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
}
