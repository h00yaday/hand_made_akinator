import React from 'react';

export default function ResultCard({ guess, onCorrect, onWrong }:{ guess:{name:string;description?:string;image?:string}|null; onCorrect:()=>void; onWrong:()=>void }){
  if(!guess) return null;
  return (
    <div id="game">
      <h2>Это {guess.name}?</h2>
      {guess.image && <img id="answer-image" src={guess.image} alt={guess.name} style={{maxWidth:220}} />}
      {guess.description && <p>{guess.description}</p>}
      <div style={{marginTop:12}}>
        <button className="answer-btn" onClick={onCorrect}>Да, это он</button>
        <button className="answer-btn" onClick={onWrong}>Нет, не он</button>
      </div>
    </div>
  );
}