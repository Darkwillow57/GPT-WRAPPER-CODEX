import { OpenAI } from 'openai';
import multer from 'multer';
import fs from 'fs';

const upload = multer({ dest: '/tmp' });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export const config = {
  api: {
    bodyParser: false
  }
};

export default (req, res) => {
  upload.single('file')(req, res, async err => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    try {
      const fileStream = fs.createReadStream(req.file.path);
      const uploaded = await openai.files.create({
        file: fileStream,
        purpose: 'assistants'
      });
      fs.unlinkSync(req.file.path);
      res.status(200).json(uploaded);
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  });
};
