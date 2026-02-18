// Simple mock API for game flow. Replace with real fetch calls when backend is available.

type Question = { id: number; text: string };
type Guess = { name: string; description?: string; image?: string };

let _step = 0; // internal mock state

function delay(ms = 700) {
  return new Promise(res => setTimeout(res, ms));
}

export async function startGame(): Promise<{ type: 'question'; question: Question } | { type: 'guess'; guess: Guess }> {
  _step = 1;
  await delay();
  return { type: 'question', question: { id: 1, text: 'Он мужчина?' } };
}

export async function sendAnswer(answer: string): Promise<{ type: 'question'; question: Question } | { type: 'guess'; guess: Guess }> {
  await delay();
  _step++;
  // very simple branching mock
  if (_step === 2) {
    return { type: 'question', question: { id: 2, text: 'Он актёр?' } };
  }
  if (_step === 3) {
    return { type: 'question', question: { id: 3, text: 'Он из России?' } };
  }
  // after 4 steps, return a guess
  return {
    type: 'guess',
    guess: {
      name: 'Иван Иванов',
      description: 'Пример персонажа — заглушка',
      image: '/image/placeholder.jpg'
    }
  };
}

export async function sendFeedback(payload: { name: string; distinguishingQuestion?: string }): Promise<{ ok: boolean }> {
  await delay(500);
  // pretend success
  console.log('Feedback received', payload);
  return { ok: true };
}