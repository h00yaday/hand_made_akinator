import React, { useState } from 'react';
import Loader from '../common/Loader';
import ErrorToast from '../common/ErrorToast';
import { sendFeedback } from '../../api/gameApi';

type Guess = { name: string; description?: string; image?: string };

type Props = {
  guess: Guess;
  onPlayAgain: () => void;
};

export default function ResultCard({ guess, onPlayAgain }: Props) {
  const [accepted, setAccepted] = useState<boolean | null>(null); // null = decision not made, true = guessed right, false = guessed wrong
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // feedback form state
  const [realName, setRealName] = useState('');
  const [distinguishingQuestion, setDistinguishingQuestion] = useState('');
  const [sentOk, setSentOk] = useState(false);

  async function handleYes() {
    setLoading(true);
    setError(null);
    try {
      // Optionally you could call an API to confirm the guess — here we just show success
      await new Promise(res => setTimeout(res, 500));
      setAccepted(true);
    } catch (e) {
      setError('Не удалось подтвердить. Попробуйте ещё.');
    } finally {
      setLoading(false);
    }
  }

  function handleNo() {
    setAccepted(false);
  }

  async function handleSubmitFeedback(e?: React.FormEvent) {
    if (e) e.preventDefault();
    setError(null);
    if (!realName.trim()) {
      setError('Пожалуйста, введите имя персонажа.');
      return;
    }
    setLoading(true);
    try {
      const payload: { name: string; distinguishingQuestion?: string } = { name: realName.trim() };
      if (distinguishingQuestion.trim()) payload.distinguishingQuestion = distinguishingQuestion.trim();
      const res = await sendFeedback(payload);
      if (res.ok) {
        setSentOk(true);
      } else {
        setError('Сервер вернул ошибку. Попробуйте позже.');
      }
    } catch (err) {
      setError('Ошибка сети. Проверьте соединение.');
    } finally {
      setLoading(false);
    }
  }

  // render
  if (accepted === true) {
    return (
      <div className="result-card">
        <h2>Ура! Я угадал 🎉</h2>
        <p>Спасибо за игру.</p>
        <button onClick={onPlayAgain}>Играть снова</button>
      </div>
    );
  }

  if (accepted === false) {
    return (
      <div className="result-card feedback">
        <h2>Похоже, я ошибся</h2>
        <p>Помогите нам улучшить игру — расскажите, кто был на самом деле.</p>

        {error && <ErrorToast message={error} onClose={() => setError(null)} />}

        {sentOk ? (
          <div className="feedback-sent">
            <p>Спасибо! Мы учтём ваш ответ.</p>
            <button onClick={onPlayAgain}>Играть снова</button>
          </div>
        ) : (
          <form onSubmit={handleSubmitFeedback} className="feedback-form">
            <label>
              Кто это был?
              <input
                value={realName}
                onChange={e => setRealName(e.target.value)}
                placeholder="Имя персонажа"
                disabled={loading}
              />
            </label>

            <label>
              Какой вопрос отличает вашего персонажа? (опционально)
              <input
                value={distinguishingQuestion}
                onChange={e => setDistinguishingQuestion(e.target.value)}
                placeholder="Например: Он женщина?"
                disabled={loading}
              />
            </label>

            <div className="actions">
              <button type="submit" disabled={loading}>Отправить</button>
              <button type="button" onClick={onPlayAgain} disabled={loading}>Пропустить / Играть снова</button>
            </div>

            {loading && <Loader />}
          </form>
        )}
      </div>
    );
  }

  // default: show the guess card with yes/no actions
  return (
    <div className="result-card guess">
      <h3>Я думаю, это:</h3>
      <div className="guess-body">
        {guess.image && <img src={guess.image} alt={guess.name} style={{ maxWidth: 200 }} />}
        <div className="guess-info">
          <h2>{guess.name}</h2>
          {guess.description && <p>{guess.description}</p>}
        </div>
      </div>

      {error && <ErrorToast message={error} onClose={() => setError(null)} />}

      <div className="actions">
        <button onClick={handleYes} disabled={loading}>Да, это он</button>
        <button onClick={handleNo} disabled={loading}>Нет, не он</button>
      </div>

      {loading && <Loader />}
    </div>
  );
}