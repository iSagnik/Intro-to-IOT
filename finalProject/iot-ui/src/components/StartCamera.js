import { useState } from "react";
import axios from "axios";

const StartCamera = ({ showOption, setShowOption, data, setData }) => {
  const [value, setValue] = useState("3");
  const [doorOpen, setDoorOpen] = useState(false);
  const [setupDone, setSetupDone] = useState(false);
  const [name, setName] = useState("");

  const handleNameChange = (e) => {
    setName(e.target.value);
  };
  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (value === "3") {
      setShowOption(0);
      setData(null);
      setSetupDone(false);
      return;
    }
    const url = "/handleStranger?option=" + value + "&name=" + name;
    axios.post(url).then((res) => {
      console.log(res.data);
      let alertMessage = "Request complete";
      if (res.data === false) {
        alertMessage = "Request not complete";
      }
      alert(alertMessage);
    });
    setDoorOpen(true);
  };

  const closeDoor = () => {
    //close door request
    const url = "/closeDoor";
    axios.post(url).then((res) => {
      console.log(res);
      let alertMessage = "Door Closed";
      if (res.data === false) {
        alertMessage = "Error, door not closed";
      }

      alert(alertMessage);
    });
    setShowOption(0);
    setData(null);
    setDoorOpen(false);
    setSetupDone(false);
  };
  const checkDoorStatus = () => {
    if (data && data["table"] === "Error") {
      setShowOption(0);
      setData(null);
      alert(data["msg"]);
      return;
    }
    if (data && (data["table"] === "Guests" || data["table"] === "Owners")) {
      setDoorOpen(true);
      setSetupDone(true);
    }
  };
  return (
    <div className="request-entry">
      <span>
        Please press q on the camera window to capture an image for validation
      </span>
      <br />
      {showOption === 4 && data === null && <span>Loading</span>}
      {showOption === 4 && !setupDone && checkDoorStatus()}
      {showOption === 4 && data && data["table"] !== "Stranger" && (
        <div className="entry">{data && data["msg"]}</div>
      )}
      {showOption === 4 && data && data["table"] === "Stranger" && (
        <div className="stranger-entry">
          <h3>A stranger is at the door.</h3>
          <form className="menu-form" onSubmit={handleSubmit}>
            <div>
              <input
                type="radio"
                value={"1"}
                onChange={handleChange}
                checked={value === "1"}
              />
              Add as guest and open the door
            </div>
            <div>
              <input
                type="radio"
                value={"2"}
                onChange={handleChange}
                checked={value === "2"}
              />
              Open the door
            </div>
            <div>
              <input
                type="radio"
                value={"3"}
                onChange={handleChange}
                checked={value === "3"}
              />
              Do Nothing
            </div>
            {value === "1" && (
              <label>
                Name: <input type="text" value={name} onChange={handleNameChange} />
              </label>
            )}
            <button type="submit">Submit</button>
          </form>
        </div>
      )}
      {showOption === 4 && doorOpen && (
        <div className="door-open">
          <h2>Door is open</h2>
          <button onClick={closeDoor}>Close Door</button>
        </div>
      )}
    </div>
  );
};

export default StartCamera;
