import { useState } from "react";
import "../App.css";

/**
 * 
 * Displays a menu
 */
const Menu = ({ setShowOption, requestEntry }) => {
  const [value, setValue] = useState("4");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(value);
    if (value === "1") {
      setShowOption(1);
    } else if (value === "2") {
      setShowOption(2);
    } else if (value === "3") {
      setShowOption(3);
    } else {
      setShowOption(4);
      requestEntry()
    }
  };


  return (
    <div>
      <div>
        <h2>Menu</h2>
        <h3>Choose an option:</h3>
        <form className="menu-form" onSubmit={handleSubmit}>
          <div>
            <input
              type="radio"
              value={"4"}
              onChange={handleChange}
              checked={value === "4"}
            />
            Request Entry
          </div>
          <div>
            <input
              type="radio"
              value={"1"}
              onChange={handleChange}
              checked={value === "1"}
            />
            Remove an owner
          </div>
          <div>
            <input
              type="radio"
              value={"2"}
              onChange={handleChange}
              checked={value === "2"}
            />
            Remove a guest
          </div>
          <div>
            <input
              type="radio"
              value={"3"}
              onChange={handleChange}
              checked={value === "3"}
            />
            Add an owner
          </div>

          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default Menu;