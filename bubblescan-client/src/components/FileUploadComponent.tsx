import React, { useState, ChangeEvent, FormEvent } from "react";

function FileUploadComponent() {
  const [jsonFile, setJsonFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false); //tracks upload status
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
    setIsUploading(false);
  };

  const submitJSON = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if(!jsonFile){
      setSuccessMessage("Please select a file before uploading.");
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    if (jsonFile) {
      formData.append("file", jsonFile);
    }

    try {
      const response = await fetch("http://localhost:5000/api/upload-json", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        //const result = await response.json();
        console.log("JSON file sent successfully");
        setSuccessMessage(result.message);
        setCsvFileName(result.csvFilename); // Adjust based on the actual response key for the CSV filename
      } else {
        console.error("Failed to send JSON file");
        setSuccessMessage("Failed to send JSON file");
      }
    } catch (error) {
      console.error("Error:", error);
      setSuccessMessage("Error sending JSON file");
    } finally {
      setIsUploading(false);
    }
  };

  const downloadCSV = () => {
    if (csvFileName) {
      window.location.href = `http://localhost:5000/api/download/${csvFileName}`;
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
