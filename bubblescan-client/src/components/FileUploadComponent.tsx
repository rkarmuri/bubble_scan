import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null);
  const [successMessage, setSuccessMessage] = useState<string>("");
  const [downloadLink, setDownloadLink] = useState<string>("");
  const [fileId, setFileId] = useState<string>("");

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
            console.log("File ID:", result.file_id);
            setDownloadLink(`http://localhost:5001/api/download_csv/${result.file_id}`);
            setFileId(result.file_id);
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

  const handleDownloadCSV = async () => {
    try {
      const csvDownloadResponse = await fetch(downloadLink);

      if (csvDownloadResponse.ok) {
        const blob = await csvDownloadResponse.blob();
        const url = window.URL.createObjectURL(new Blob([blob]));
        const currentDate = new Date();
        const dateString = currentDate.toISOString().split('T')[0];
        const timeString = currentDate.toTimeString().split(' ')[0].replace(/:/g, '-');
        const filename = `data_${dateString}_${timeString}.csv`;

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        // Send acknowledgment to Flask
        const acknowledgmentResponse = await fetch(`http://localhost:5001/api/csv_acknowledgment/${fileId}`, {
          method: "POST",
        });

        if (acknowledgmentResponse.ok) {
          const acknowledgmentResult = await acknowledgmentResponse.json();
          if (acknowledgmentResult.status === "success") {
            console.log("CSV acknowledgment received from Flask");
            alert("CSV file downloaded successfully!");
          } else {
            console.error("Error: ", acknowledgmentResult.message);
          }
        } else {
          console.error("Error: Failed to send CSV acknowledgment to Flask");
        }
      } else {
        console.error("Error: Failed to download CSV");
      }
    } catch (error) {
      console.error("Error during CSV download:", error);
    }
  };

  const clearForm = () => {
    setFile(null);
    setSuccessMessage("");
    setDownloadLink("");
    setFileId("");
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
        <button onClick={handleDownloadCSV}>
          Download CSV
        </button>
      )}
    </div>
  );
}

export default FileUploadComponent;
