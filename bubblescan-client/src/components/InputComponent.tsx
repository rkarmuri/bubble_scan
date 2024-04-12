import React, { useState } from "react";

function InputComponent() {
  const [inputValue, setInputValue] = useState("");
  const [latestSubmission, setLatestSubmission] = useState<string>("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLatestSubmission(inputValue);
    setInputValue("");
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
