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
        (file) => ({
          ...file,
          preview: URL.createObjectURL(file),
        })
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

    console.log(formData.has('file'));

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result.message); 
        clearFiles(); 
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
      <button onClick={uploadFiles}>Upload Files</button> {/* Add this button for uploading files */}
    </div>
  );
}

export default FileUploadComponent;
