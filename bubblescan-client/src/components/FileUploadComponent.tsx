import React, { useState, useEffect, ChangeEvent } from "react";

interface FileWithPreview extends File {
  preview: string;
}

function FileUploadComponent() {
  const [uploadedFiles, setUploadedFiles] = useState<FileWithPreview[]>([]);

  useEffect(() => {
    console.log("Updated Uploaded Files: ", uploadedFiles);
  }, [uploadedFiles]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const filesArray: FileWithPreview[] = Array.from(event.target.files).map(
        (file) => {
          console.log(file.name, file.size); // Debugging line added
          return {
            ...file,
            preview: URL.createObjectURL(file),
          };
        }
      );

      setUploadedFiles((prevFiles) => [...prevFiles, ...filesArray]);
    }
  };

  const clearFiles = () => {
    uploadedFiles.forEach((file) => URL.revokeObjectURL(file.preview));
    setUploadedFiles([]);
  };

  const uploadFiles = async () => {
    const formData = new FormData();
    uploadedFiles.forEach(file => {
      formData.append('file', file); 
    });

    console.log(formData.has('file')); // Check if 'file' key exists in formData

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result.message); 
        clearFiles(); // Clear the files after successful upload
      } else {
        console.error('Upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
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
      <button onClick={uploadFiles}>Upload Files</button> {/* This button triggers the file upload */}
    </div>
  );
}

export default FileUploadComponent;
