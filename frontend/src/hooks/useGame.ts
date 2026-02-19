import { useState, useCallback } from 'react';
import * as api from '../api/gameApi';

export function useGame(){
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [question, setQuestion] = useState(null as null | { id:number; text:string });
  const [guess, setGuess] = useState(null as null | { name:string; description?:string; image?:string });
  const [finished, setFinished] = useState(false);

  const start = useCallback(async ()=>{
    setLoading(true); setError(null);
    try{
      const res = await api.startGame();
      if ((res as any).type === 'question') setQuestion((res as any).question);
      else if ((res as any).type === 'guess') setGuess((res as any).guess);
    }catch(e:any){ setError(e.message || 'Ошибка'); }
    setLoading(false);
  },[]);

  const answer = useCallback(async (ans:string)=>{
    setLoading(true); setError(null);
    try{
      const res = await api.sendAnswer(ans);
      if ((res as any).type === 'question') { setQuestion((res as any).question); setGuess(null); }
      else if ((res as any).type === 'guess') { setGuess((res as any).guess); setQuestion(null); }
    }catch(e:any){ setError(e.message || 'Ошибка при ответе'); }
    setLoading(false);
  },[]);

  const sendFeedback = useCallback(async (payload:{ name:string; distinguishingQuestion?:string })=>{
    setLoading(true); setError(null);
    try{
      const res = await api.sendFeedback(payload);
      if (res.ok) setFinished(true);
    }catch(e:any){ setError(e.message || 'Ошибка при отправке'); }
    setLoading(false);
  },[]);

  return { loading, error, question, guess, finished, start, answer, sendFeedback, setError };
}