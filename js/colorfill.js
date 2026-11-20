/* Animação "a cor a encher": linhas -> colorido, região a região.
   Camadas: line.png (arte), color.jpg (colorido), time.png (quando cada pixel enche). */
(function(){
  var box=document.querySelector('[data-colorfill]'); if(!box) return;
  var base=box.getAttribute('data-colorfill'), cv=box.querySelector('canvas');
  var btn=box.querySelector('button'), ctx=cv.getContext('2d',{willReadFrequently:true});
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DUR=7000, W=640, H=876, line, col, tm, out, raf=0, played=false, done=false;
  function load(src){return new Promise(function(ok,no){var i=new Image();i.onload=function(){ok(i)};i.onerror=no;i.src=src;});}
  function px(img){var c=document.createElement('canvas');c.width=W;c.height=H;var x=c.getContext('2d');x.drawImage(img,0,0,W,H);return x.getImageData(0,0,W,H).data;}
  function draw(t){ // t entre 0 e 1
    var th=t*254, o=out.data, n=W*H;
    for(var i=0,p=0;i<n;i++,p+=4){
      var s=tm[p]<=th?col:line;
      o[p]=s[p];o[p+1]=s[p+1];o[p+2]=s[p+2];o[p+3]=255;
    }
    ctx.putImageData(out,0,0);
  }
  function play(){
    cancelAnimationFrame(raf); done=false; btn.disabled=true; var t0=null;
    function step(ts){ if(t0===null)t0=ts; var t=Math.min(1,(ts-t0)/DUR); draw(t);
      if(t<1){raf=requestAnimationFrame(step);} else {done=true;btn.disabled=false;btn.textContent='Play again';} }
    btn.textContent='Coloring…'; raf=requestAnimationFrame(step);
  }
  Promise.all([load(base+'-line.png'),load(base+'-color.jpg'),load(base+'-time.png')]).then(function(r){
    cv.width=W;cv.height=H; line=px(r[0]); col=px(r[1]); tm=px(r[2]); out=ctx.createImageData(W,H);
    if(reduce){ // sem movimento: botão alterna entre linhas e cor
      var on=false; draw(0); btn.textContent='Show colored page';
      btn.addEventListener('click',function(){on=!on;draw(on?1:0);btn.textContent=on?'Show line art':'Show colored page';});
      return;
    }
    draw(0); btn.textContent='Watch it fill with color';
    btn.addEventListener('click',play);
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es,ob){es.forEach(function(e){ if(e.isIntersecting&&!played){played=true;ob.disconnect();play();} });},{threshold:.6}).observe(cv);
    }
  });
})();
