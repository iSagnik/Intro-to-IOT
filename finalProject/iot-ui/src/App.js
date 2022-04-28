import { useState } from "react";
import axios from "axios";
import Menu from "./components/MenuComponent";
import RemoveEntry from "./components/RemoveEntry";
import AddOwner from "./components/AddOwner";
import StartCamera from "./components/StartCamera";
import "./App.css";

const App = () => {
  const [showOption, setShowOption] = useState(0);
  const [data, setData] = useState(null);

  const requestEntry = () => {
    const url = "/requestEntry";
    axios.get(url).then((res) => {
      console.log(res.data);
      const data = res.data
      setData(data);
    });
  }
  return (
    <div className="App">
      <header>
        {" "}
        <h1>Smart Door Dashboard</h1>
      </header>
      <main>
        {showOption === 0 && <Menu setShowOption={setShowOption} requestEntry={requestEntry} />}
        {showOption === 1 && (
          <RemoveEntry setShowOption={setShowOption} table="Owners" />
        )}
        {showOption === 2 && (
          <RemoveEntry setShowOption={setShowOption} table="Guests" />
        )}
        {showOption === 3 && <AddOwner setShowOption={setShowOption} />}
        {showOption === 4 && <StartCamera showOption = {showOption} setShowOption={setShowOption} data = {data} setData={setData}/>}
      </main>
    </div>
  );
};

export default App;
