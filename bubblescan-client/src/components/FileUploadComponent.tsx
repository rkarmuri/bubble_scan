import React, { useState, ChangeEvent } from "react";

interface FileWithPreview extends File {
  preview: string;
}

function FileUploadComponent() {
  const [uploadedFiles, setUploadedFiles] = useState<FileWithPreview[]>([]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const filesArray: FileWithPreview[] = Array.from(event.target.files).map(
        (file) => ({
          ...file,
          preview: URL.createObjectURL(file),
        })
      );

      // Assuming you'll handle PDF files for upload
      const pdfFiles = filesArray.filter(
        (file) => file.type === "application/pdf"
      );
      setUploadedFiles((prevFiles) => [...prevFiles, ...pdfFiles]);
    }
  };

  // Remember to revoke the object URLs to avoid memory leaks
  const clearFiles = () => {
    uploadedFiles.forEach((file) => URL.revokeObjectURL(file.preview));
    setUploadedFiles([]);
  };

  return (
    <div>
      <input
        type="file"
        accept="application/pdf"
        multiple
        onChange={handleFileChange}
      />
      <div>
        <h3>Uploaded PDF Files:</h3>
        {uploadedFiles.map((file, index) => (
          <div key={index}>
            {file.name} - {file.size} bytes
          </div>
        ))}
      </div>
      <button onClick={clearFiles}>Clear Files</button>
    </div>
  );
}

export default FileUploadComponent;
