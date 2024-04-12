import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null);
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
      const response = await fetch("http://localhost:5001/api/upload", {
        method: "POST",
        body: formData,
      });
      // const result = await response.json();

      if (response.ok) {
        const result = await response.json();
        if (result.status === "success") {
          setSuccessMessage("File uploaded successfully!");
          if (result.file_id) {
            setDownloadLink(`http://localhost:5001/api/download_csv/output_${result.file_id}.csv`);
          } else {
            setSuccessMessage("Error: CSV filename not found in the response.");
          }
        } else {
          setSuccessMessage("Error: " + result.message);
        }
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
    if (fileInput) fileInput.value = ""; 
  };

  console.log("Download link:", downloadLink);

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
