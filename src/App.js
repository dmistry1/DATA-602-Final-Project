import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';

function App() {
  const [currentTime, setCurrretTime] = useState(0)

  useEffect(() => {
    fetch('/api/time').then(response => response.json()).then(data => {
      setCurrretTime(data.time)
    })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          This is where our final project is going to stay
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          <p>The current time is {currentTime} </p>
        </a>
      </header>
    </div>
  );
}

export default App;
