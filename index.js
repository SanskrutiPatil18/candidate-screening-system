import { useState } from "react";

export default function Home() {
  const [resume, setResume] = useState(null);
  const [role, setRole] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    await fetch("/resume/upload", { method: "POST", body: formData });
  };

  return (
    <div>
      <h1>AI Candidate Screening</h1>
      <input type="file" onChange={handleUpload} />
      <select onChange={(e) => setRole(e.target.value)}>
        <option>Backend Engineer</option>
        <option>AI/ML Engineer</option>
      </select>
      <button onClick={() => window.location.href="/interview"}>Start Interview</button>
    </div>
  );
}
