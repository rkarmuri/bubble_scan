import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null); // File to be uploaded
  const [successMessage, setSuccessMessage] = useState<string>("");
  const [downloadLink, setDownloadLink] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setSuccessMessage("");
      setDownloadLink("");
    } else {
      alert("Please select a PDF file.");
      if (event.target && event.target.value) {
        event.target.value = ""; // Reset file input
      }
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a PDF file before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (response.ok) {
        setSuccessMessage("File uploaded successfully!");
        // Assume the response includes the path or name of the generated CSV file
        setDownloadLink(`http://localhost:5000/api/download/${result.message}`);
      } else {
        setSuccessMessage("Upload failed.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setSuccessMessage("Error during file upload.");
    }
  };

  const clearForm = () => {
    setFile(null);
    setSuccessMessage("");
    setDownloadLink("");
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    if (fileInput) fileInput.value = ""; // Reset file input safely with type casting
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          id="file-input"
          accept=".pdf"
          onChange={handleFileChange}
        />
        <button type="submit">Upload</button>
        <button
          type="button"
          onClick={clearForm}
          style={{ marginLeft: "10px" }}
        >
          Clear
        </button>
      </form>
      {successMessage && <p>{successMessage}</p>}
      {downloadLink && (
        <button onClick={() => (window.location.href = downloadLink)}>
          Download CSV
        </button>
      )}
    </div>
  );
}

export default FileUploadComponent;
