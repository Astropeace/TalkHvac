import React, { useState } from "react";

function App() { 
  const [issue, setIssue] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [oemNumber, setOemNumber] = useState("");
  const [partInfo, setPartInfo] = useState("");

  const handleDiagnose = async () => {
    const response = await fetch("http://localhost:5000/diagnose", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ issue }),
    });

    const data = await response.json();
    setDiagnosis(data.response);
  };

  const handleFindPart = async () => {
    const response = await fetch(`http://localhost:5000/find_part?oem_number=${oemNumber}`);
    const data = await response.json();
    setPartInfo(JSON.stringify(data));
  };

  return (
    <div>
      <h1>HVAC Assistant</h1>
      <div>
        <h2>Diagnose Issue</h2>
        <input
          type="text"
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
          placeholder="Describe the HVAC issue"
        />
        <button onClick={handleDiagnose}>Diagnose</button>
        <p>{diagnosis}</p>
      </div>

      <div>
        <h2>Find Part</h2>
        <input
          type="text"
          value={oemNumber}
          onChange={(e) => setOemNumber(e.target.value)}
          placeholder="Enter OEM number"
        />
        <button onClick={handleFindPart}>Find Part</button>
        <p>{partInfo}</p>
      </div>
    </div>
  );
}

export default App;