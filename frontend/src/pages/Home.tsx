// src/pages/Home.tsx
import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="app-container">
      <h1 className="title">Акинатор</h1>
      <h2>Я угадаю любого персонажа!</h2>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        Загадайте реального или вымышленного героя, и я задам вам несколько вопросов.
      </p>
      
      <Link to="/start">
        <button className="btn">Начать игру</button>
      </Link>
    </div>
  );
}