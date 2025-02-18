import { useState } from "react";
import axios from "axios";

export default function EmailForm() {
  const [prompt, setPrompt] = useState("");
  const [emailContent, setEmailContent] = useState("");

  const handleGenerate = async () => {
    const res = await axios.post("http://localhost:8000/email/generate", { prompt });
    setEmailContent(res.data.content);
  };

  return (
    <div className="p-6 bg-white shadow-md rounded-xl">
      <h2 className="text-xl font-bold">Generate Email</h2>
      <textarea
        className="w-full p-2 border rounded"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your email prompt..."
      />
      <button onClick={handleGenerate} className="mt-3 p-2 bg-blue-500 text-white rounded">
        Generate
      </button>
      {emailContent && <pre className="mt-3 p-3 bg-gray-100 rounded">{emailContent}</pre>}
    </div>
  );
}
