import React, { useState } from "react";

function InputComponent() {
  const [inputValue, setInputValue] = useState("");
  // Use a single state variable to hold the latest submission.
  const [latestSubmission, setLatestSubmission] = useState<string>("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Update the latestSubmission with the current input value.
    setLatestSubmission(inputValue);
    setInputValue(""); // Clear the input field after submission.
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter some text"
        />
        <button type="submit">Submit</button>
      </form>
      {/* Display the latest submitted value */}
      {latestSubmission && <p>Latest Submission: {latestSubmission}</p>}
    </div>
  );
}

export default InputComponent;
