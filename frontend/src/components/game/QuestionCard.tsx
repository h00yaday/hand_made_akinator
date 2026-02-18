import React from 'react';

export default function QuestionCard({ question, onAnswer, disabled }:{ question:{id:number;text:string}|null; onAnswer:(a:string)=>void; disabled?:boolean }){
  if(!question) return null;
  return (
    <div id="game">
      <h2 id="current-question">{question.text}</h2>
      <div style={{marginTop:12}}>
        <button className="answer-btn" data-answer="yes" onClick={()=>onAnswer('yes')} disabled={disabled}>Да</button>
        <button className="answer-btn" data-answer="no" onClick={()=>onAnswer('no')} disabled={disabled}>Нет</button>
        <button className="answer-btn" data-answer="unknown" onClick={()=>onAnswer('unknown')} disabled={disabled}>Не знаю</button>
      </div>
    </div>
  );
}