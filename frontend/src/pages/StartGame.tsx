// src/pages/StartGame.tsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGame } from '../hooks/useGame';

export default function StartGame() {
  const navigate = useNavigate();
  const { loading, error, question, guess, start, answer } = useGame();

  useEffect(() => {
    start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // Если Акинатор угадал, перебрасываем на страницу с ответом
    if (guess && !loading) {
      navigate('/answer', { state: { guess } });
    }
  }, [guess, loading, navigate]);

  if (loading) return <div className="app-container"><h2>Думаю... 🤔</h2></div>;
  if (error) return <div className="app-container"><h2>Ошибка: {error}</h2></div>;

  return (
    <div className="app-container">
      <h1 className="title">Вопрос</h1>
      
      {question ? (
        <>
          <h2 style={{ fontSize: '1.5rem', margin: '20px 0' }}>{question.text}</h2>
          <div className="btn-group">
            <button className="btn" onClick={() => answer('yes')}>Да</button>
            <button className="btn btn-secondary" onClick={() => answer('dont_know')}>Не знаю</button>
            <button className="btn" style={{ background: '#e53935' }} onClick={() => answer('no')}>Нет</button>
          </div>
        </>
      ) : (
        <h2>Загрузка вопроса...</h2>
      )}
    </div>
  );
}