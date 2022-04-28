import { useState } from "react";
import axios from "axios";

const AddOwner = ({ setShowOption }) => {
  const [name, setName] = useState("");

  const handleChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const url = "/addOwner?name=" + name;
    axios.post(url).then((res) => {
      console.log(res.data);
      let alertMessage = "Owner added";
      if (res.data === false) {
        alertMessage = "Could not add owner. Check server logs for eror";
      } 
      alert(alertMessage);
    });
    setShowOption(0);
  };

  return (
    <div className="add-owner">
      <h1>Add an Owner</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Name: <input type="text" value={name} onChange={handleChange} />
        </label>
        <button type="submit">Add Owner</button>
      </form>
    </div>
  );
};

export default AddOwner;
