import React from 'react';

export default function ErrorToast({ message, onClose }:{ message:string|null; onClose?:()=>void }){
  if(!message) return null;
  return (
    <div style={{position:'fixed',right:16,top:16,background:'#fff3f2',padding:12,borderRadius:8,boxShadow:'0 6px 18px rgba(0,0,0,0.08)'}}>
      <div style={{color:'#9b2c2c'}}>{message}</div>
      <button onClick={onClose} style={{marginTop:8}}>Закрыть</button>
    </div>
  );
}