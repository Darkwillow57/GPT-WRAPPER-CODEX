import { OpenAI } from 'openai';
import { IncomingForm } from 'formidable';
import fs from 'fs';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  const form = new IncomingForm({ uploadDir: '/tmp', keepExtensions: true });

  try {
    const file = await new Promise((resolve, reject) => {
      form.parse(event, (err, fields, files) => {
        if (err) return reject(err);
        const uploaded = files.file;
        if (Array.isArray(uploaded)) resolve(uploaded[0]);
        else resolve(uploaded);
      });
    });

    const stream = fs.createReadStream(file.filepath);
    const uploaded = await openai.files.create({ file: stream, purpose: 'assistants' });
    fs.unlinkSync(file.filepath);

    return {
      statusCode: 200,
      body: JSON.stringify(uploaded)
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
}
