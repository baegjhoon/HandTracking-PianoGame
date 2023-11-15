import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Home from "./pages/Home";
import MusicSelect from "./pages/MusicSelect";

import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/music-select" element={<MusicSelect />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
