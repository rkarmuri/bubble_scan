import React, { useEffect, useState } from "react";
import ListGroup from "./components/ListGroup";
import InputComponent from "./components/InputComponent";
import FileUploadComponent from "./components/FileUploadComponent";
import "./App.css";

function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  // Fetch initial data from Flask
  useEffect(() => {
    fetch("http://localhost:5001/api/data")
      .then((response) => response.json())
      .then((data) => setData(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Function to send message to Flask
  const sendMessage = async () => {
    try {
      const res = await fetch("http://localhost:5001/api/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      console.error("Error sending message:", error);
      setResponse("Failed to send message.");
    }
  };

  return (
    <div>
      <h1>Welcome To Bubble Scan</h1>
      <h2>You can upload your files below</h2>
      <FileUploadComponent />
    </div>
  );
}

export default App;
