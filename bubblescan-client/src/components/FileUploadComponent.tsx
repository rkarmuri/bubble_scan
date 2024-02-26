import React, { useState, useEffect, ChangeEvent } from "react";

interface FileWithPreview extends File {
  preview: string;
}

function FileUploadComponent() {
  const [uploadedFiles, setUploadedFiles] = useState<FileWithPreview[]>([]);

  // Log the state after it updates to confirm the update
  useEffect(() => {
    console.log("Updated Uploaded Files: ", uploadedFiles);
  }, [uploadedFiles]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const filesArray: FileWithPreview[] = Array.from(event.target.files).map(
        (file) => ({
          ...file,
          preview: URL.createObjectURL(file),
        })
      );

      // For debugging: Directly update state with all selected files
      setUploadedFiles((prevFiles) => [...prevFiles, ...filesArray]);
    }
  };

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
        <h6>Uploaded Files:</h6>
        {uploadedFiles.length > 0 ? (
          uploadedFiles.map((file, index) => (
            <div key={index}>
              {file.name} - {file.size} bytes
            </div>
          ))
        ) : (
          <p>No files uploaded yet.</p>
        )}
      </div>
      <button onClick={clearFiles}>Clear Files</button>
    </div>
  );
}

export default FileUploadComponent;
