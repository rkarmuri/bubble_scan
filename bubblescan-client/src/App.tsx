import ListGroup from "./components/ListGroup";
import InputComponent from "./components/InputComponent";
import FileUploadComponent from "./components/FileUploadComponent";
import "./App.css";

function App() {
  return (
    <div>
      <h1>Welcome To Bubble Scan</h1>
      <h2>What is your First and Last Name?</h2>
      <InputComponent />
      <h2>You can upload your files below</h2>
      <FileUploadComponent />
    </div>
  );
}

export default App;
