import { MouseEvent } from "react";

function ListGroup() {
  let items = ["New York", "San Francisco", "Tokyo", "London", "Paris"];

  //Event handler
  const handleCLick = (event: MouseEvent) => console.log(event);

  return (
    <>
      <h1>List</h1>
      {items.length === 0 && <p>No items found</p>}
      <ul className="list-group">
        {items.map((item, index) => (
          <li className="list-group-item" key={item} onClick={handleCLick}>
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
