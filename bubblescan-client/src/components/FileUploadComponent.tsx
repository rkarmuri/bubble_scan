import React, { useState, ChangeEvent, FormEvent } from 'react';

function FileUploadComponent() {
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const handlePDFChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setPdfFile(event.target.files[0]);
        }
    };

    // Helper function to clear the selected PDF file and success message
    const clearForm = () => {
        setPdfFile(null);
        setSuccessMessage(null);
    };

    // Helper function to submit the PDF file to the backend for text extraction
    const submitPDF = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const formData = new FormData();
        if (pdfFile) {
            formData.append('file', pdfFile);
        }

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("PDF file sent successfully");
                console.log(result.message);
                setSuccessMessage(result.message);
            } else {
                console.error('Failed to send PDF file');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <form encType='multipart/form-data' onSubmit={submitPDF} style={{ marginBottom: '15px' }}>
                    <input type="file" name='file' accept=".pdf" onChange={handlePDFChange} />
                    <div style={{ display: 'flex', marginTop: '10px' }}>
                        <button type="submit" style={{ marginRight: '10px', padding: '5px 10px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Upload</button>
                        <button type="button" onClick={clearForm} style={{ padding: '5px 10px', background: '#f44336', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Clear</button>
                    </div>
                </form>
                {successMessage && <p>{successMessage}</p>}
            </div>
        </>
    );
}

export default FileUploadComponent;
