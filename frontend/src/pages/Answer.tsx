// src/pages/Answer.tsx
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useGame } from '../hooks/useGame';

export default function Answer() {
  const location = useLocation();
  const navigate = useNavigate();
  const guess = location.state?.guess;
  
  const { sendFeedback } = useGame();
  
  // Состояние, показывающее, открыта ли форма фидбека
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackName, setFeedbackName] = useState('');
  const [distQ, setDistQ] = useState('');

  if (!guess) {
    return (
      <div className="app-container">
        <h2>Сначала нужно сыграть!</h2>
        <button className="btn" onClick={() => navigate('/start')}>Играть</button>
      </div>
    );
  }

  const handleCorrect = () => {
    alert('Ура! Я так и знал!');
    navigate('/'); // Возвращаем в меню
  };

  const handleFeedbackSubmit = () => {
    sendFeedback({ name: feedbackName, distinguishingQuestion: distQ });
    alert('Спасибо! Я стану умнее.');
    navigate('/');
  };

  return (
    <div className="app-container">
      <h1 className="title">Я думаю, это...</h1>
      
      <h2>{guess.name || 'Иван Иванов'}</h2>
      
      {/* Если есть фото, выводим его, иначе заглушку */}
      <img 
        src={guess.photoUrl || "https://via.placeholder.com/150"} 
        alt="Персонаж" 
        className="character-image" 
      />

      {!showFeedback ? (
        <>
          <h3 style={{ marginTop: '20px' }}>Я угадал?</h3>
          <div className="btn-group">
            <button className="btn" onClick={handleCorrect}>Да, это он!</button>
            <button className="btn btn-secondary" onClick={() => setShowFeedback(true)}>Нет, ошибка</button>
          </div>
        </>
      ) : (
        <div style={{ marginTop: '20px', textAlign: 'left' }}>
          <h3>Ой! А кто это был?</h3>
          <input 
            value={feedbackName} 
            onChange={e => setFeedbackName(e.target.value)} 
            placeholder="Имя правильного персонажа" 
          />
          <input 
            value={distQ} 
            onChange={e => setDistQ(e.target.value)} 
            placeholder="Какой вопрос отличил бы его? (опц.)" 
          />
          <div className="btn-group">
            <button className="btn" onClick={handleFeedbackSubmit}>Отправить</button>
            <button className="btn btn-secondary" onClick={() => setShowFeedback(false)}>Отмена</button>
          </div>
        </div>
      )}
    </div>
  );
}