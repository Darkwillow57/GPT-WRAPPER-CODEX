import { OpenAI } from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message, thread_id, assistant_id, model, temperature, top_p } = JSON.parse(req.body);

    let threadId = thread_id;

    if (!threadId) {
      const thread = await openai.beta.threads.create();
      threadId = thread.id;
    }

    await openai.beta.threads.messages.create(threadId, {
      role: 'user',
      content: message
    });

    const run = await openai.beta.threads.runs.create(threadId, {
      assistant_id: assistant_id,
      model: model || undefined,
      temperature: temperature,
      top_p: top_p
    });

    let runStatus;
    do {
      await new Promise(r => setTimeout(r, 1000));
      runStatus = await openai.beta.threads.runs.retrieve(threadId, run.id);
    } while (runStatus.status !== 'completed' && runStatus.status !== 'failed');

    if (runStatus.status === 'failed') {
      return res.status(500).json({ error: 'Run failed' });
    }

    const messages = await openai.beta.threads.messages.list(threadId);
    const lastMessage = messages.data[0];

    res.status(200).json({
      reply: lastMessage.content[0].text.value,
      thread_id: threadId
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
