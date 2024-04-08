import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState(null); // File to be uploaded
  const [successMessage, setSuccessMessage] = useState("");
  const [downloadLink, setDownloadLink] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a file before submitting.");
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
        // Update the download link state with the new CSV file name
        setDownloadLink(`http://localhost:5000/api/download/${result.message}`);
      } else {
        setSuccessMessage("Upload failed.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setSuccessMessage("Error during file upload.");
    }
  };

  const handleDownload = () => {
    if (downloadLink) {
      window.location.href = downloadLink;
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {successMessage && <p>{successMessage}</p>}
      {downloadLink && <button onClick={handleDownload}>Download CSV</button>}
    </div>
  );
}

export default FileUploadComponent;
