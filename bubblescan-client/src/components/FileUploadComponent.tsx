import React, { useState } from "react";

function FileUploadComponent() {
<<<<<<< HEAD
  const [jsonFile, setJsonFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false); //tracks upload status
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [csvFileName, setCsvFileName] = useState<string | null>(null); // Track the CSV file name
=======
  const [file, setFile] = useState<File | null>(null); // File to be uploaded
  const [successMessage, setSuccessMessage] = useState<string>("");
  const [downloadLink, setDownloadLink] = useState<string>("");
>>>>>>> origin/sprint4ServerWork

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

<<<<<<< HEAD
  const clearForm = () => {
    setJsonFile(null);
    setSuccessMessage(null);
    setCsvFileName(null); // Also clear the CSV file name when clearing the form
    setIsUploading(false);
  };

  const submitJSON = async (event: FormEvent<HTMLFormElement>) => {
=======
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
>>>>>>> origin/sprint4ServerWork
    event.preventDefault();
    if (!file) {
      alert("Please select a PDF file before submitting.");
      return;
    }

    if(!jsonFile){
      setSuccessMessage("Please select a file before uploading.");
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/api/upload-json", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      const result = await response.json();

      if (response.ok) {
<<<<<<< HEAD
        //const result = await response.json();
        console.log("JSON file sent successfully");
        setSuccessMessage(result.message);
        setCsvFileName(result.csvFilename); // Adjust based on the actual response key for the CSV filename
=======
        setSuccessMessage("File uploaded successfully!");
        // Assume the response includes the path or name of the generated CSV file
        setDownloadLink(`http://localhost:5000/api/download/${result.message}`);
>>>>>>> origin/sprint4ServerWork
      } else {
        setSuccessMessage("Upload failed.");
      }
    } catch (error) {
<<<<<<< HEAD
      console.error("Error:", error);
      setSuccessMessage("Error sending JSON file");
    } finally {
      setIsUploading(false);
=======
      console.error("Error during file upload:", error);
      setSuccessMessage("Error during file upload.");
>>>>>>> origin/sprint4ServerWork
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
