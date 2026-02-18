import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

// --- ДОБАВЛЯЕМ СТИЛИ ЗДЕСЬ ---
import './styles/home_page.css'
import './styles/start_game.css'
import './styles/answer.css'
// -----------------------------

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)