import React, { useState, ChangeEvent, FormEvent } from "react";

function FileUploadComponent() {
  const [jsonFile, setJsonFile] = useState<File | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [csvFileName, setCsvFileName] = useState<string | null>(null); // Track the CSV file name

  const handleJSONChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setJsonFile(event.target.files[0]);
    }
  };

  const clearForm = () => {
    setJsonFile(null);
    setSuccessMessage(null);
    setCsvFileName(null); // Also clear the CSV file name when clearing the form
  };

  const submitJSON = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData();
    if (jsonFile) {
      formData.append("file", jsonFile);
    }

    try {
      const response = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log("JSON file sent successfully");
        setSuccessMessage(result.message);
        setCsvFileName(result.message.split(': ')[1]); // Assuming the filename is in the response message
      } else {
        console.error("Failed to send JSON file");
        setSuccessMessage("Failed to send JSON file");
      }
    } catch (error) {
      console.error("Error:", error);
      setSuccessMessage("Error sending JSON file");
    }
  };

  const downloadCSV = () => {
    if (csvFileName) {
      // Triggering the download
      const a = document.createElement('a');
      a.href = `http://localhost:5000/api/download/${csvFileName}`;
      a.setAttribute('download', csvFileName);
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <form
        encType="multipart/form-data"
        onSubmit={submitJSON}
        style={{ marginBottom: "15px" }}
      >
        <input
          type="file"
          name="file"
          accept=".json"
          onChange={handleJSONChange}
        />
        <div style={{ display: "flex", marginTop: "10px" }}>
          <button
            type="submit"
            style={{
              marginRight: "10px",
              padding: "5px 10px",
              background: "#4CAF50",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Upload
          </button>
          <button
            type="button"
            onClick={clearForm}
            style={{
              padding: "5px 10px",
              background: "#f44336",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Clear
          </button>
        </div>
      </form>
      {successMessage && <p>{successMessage}</p>}
      {csvFileName && (
        <button
          onClick={downloadCSV}
          style={{
            marginTop: "10px",
            background: "#4CAF50",
            color: "white",
            padding: "5px 10px",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Download CSV
        </button>
      )}
    </div>
  );
}

export default FileUploadComponent;
