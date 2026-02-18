import React, { useState } from 'react';
import { useGame } from '../hooks/useGame';
import QuestionCard from '../components/game/QuestionCard';
import ResultCard from '../components/game/ResultCard';
import Loader from '../components/common/Loader';
import ErrorToast from '../components/common/ErrorToast';

export default function Home(){
  const { loading, error, question, guess, finished, start, answer, sendFeedback, setError } = useGame();
  const [feedbackName, setFeedbackName] = useState('');
  const [distQ, setDistQ] = useState('');

  if (finished) return (
    <main id="game"><h2>Спасибо! Данные сохранены.</h2><button onClick={()=>window.location.reload()}>Играть снова</button></main>
  );

  return (
    <div>
      <header><h1>Акинатор</h1></header>
      <main>
        <button onClick={start} disabled={loading}>Старт</button>

        {loading && <Loader />}
        <ErrorToast message={error} onClose={()=>setError(null)} />

        {!loading && question && <QuestionCard question={question} onAnswer={answer} disabled={loading} />}

        {!loading && guess && (
          <div>
            <ResultCard guess={guess} onCorrect={()=>alert('Поздравляем!')} onWrong={()=>{/* show form below */}} />
            <div style={{marginTop:12}}>
              <div>Если это не правильный персонаж, укажите кто это был:</div>
              <input value={feedbackName} onChange={e=>setFeedbackName(e.target.value)} placeholder="Кто это был?" />
              <input value={distQ} onChange={e=>setDistQ(e.target.value)} placeholder="Какой вопрос отличает? (опц.)" />
              <button onClick={()=>sendFeedback({ name: feedbackName, distinguishingQuestion: distQ })}>Отправить</button>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}