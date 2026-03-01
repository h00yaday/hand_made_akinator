import React from 'react';
// Вот правильный путь до вашей папки со стилями:
import './styles/App.css'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import Home from './pages/Home';
import StartGame from './pages/StartGame'; 
import Answer from './pages/Answer';       

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/start" element={<StartGame />} />
        <Route path="/answer" element={<Answer />} />
      </Routes>
    </Router>
  );
}