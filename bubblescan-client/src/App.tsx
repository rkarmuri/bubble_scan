import ListGroup from "./components/ListGroup";
import InputComponent from "./components/InputComponent";
import FileUploadComponent from "./components/FileUploadComponent";

function App() {
  return (
    <div>
      <h3>What is your First and Last Name?</h3>
      <InputComponent />
      <h3>You can upload your files below</h3>
      <FileUploadComponent />
    </div>
  );
}

export default App;
