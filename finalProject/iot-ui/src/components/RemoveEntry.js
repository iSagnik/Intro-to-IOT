import { useState, useEffect } from "react";
import axios from "axios";

const RemoveEntry = ({ setShowOption, table }) => {
  const [entries, setEntries] = useState([]);
  const [value, setValue] = useState("");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (value === "") {
      alert("Please select an entry");
      return;
    }
    const url = "/removeTableEntry?tableName=" + table + "&name=" + value;
    axios.post(url).then((res) => {
      console.log(res.data);
      let alertMessage = value + " removed from " + table + "table";
      if (res.data === false) {
        alertMessage = "Could not remove entry. Check server logs for eror";
      }
      alert(alertMessage);
    });
    setShowOption(0);
  };
  useEffect(() => {
    function getEntries() {
      const url = "/getEntries?tableName=" + table;
      axios.get(url).then((res) => {
        console.log(res);
        const resEntries = res.data;
        setEntries(resEntries);
      });
    }
    getEntries();
  }, []);

  return (
    <div className="remove-entry">
      <h1>Remove an entry from {table}</h1>

      {entries && entries.length > 0 && (
        <>
          {" "}
          <h2>Entries</h2>
          <h3>Choose an entry:</h3>
          <form className="menu-form" onSubmit={handleSubmit}>
            <div>
              {entries &&
                entries.map((entry, idx) => {
                  return (
                    <div>
                      <input
                        type="radio"
                        key={idx}
                        value={entry}
                        onChange={handleChange}
                        checked={value === entry}
                      />
                      {entry}
                    </div>
                  );
                })}
            </div>
            <button type="submit">Submit</button>
          </form>
        </>
      )}
      {entries && entries.length === 0 && (
        <span>No {table} in the database</span>
      )}
    </div>
  );
};

export default RemoveEntry;
