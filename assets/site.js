document.documentElement.classList.add('js');
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var els = document.querySelectorAll('.reveal');

  if(!('IntersectionObserver' in window) || reduce){
    els.forEach(function(e){e.classList.add('in')});
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(x){
        if(x.isIntersecting){ x.target.classList.add('in'); io.unobserve(x.target); }
      });
    },{threshold:0.12, rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e)});
  }

  var nav = document.querySelector('header.nav');
  if(nav){
    var onScroll = function(){
      if(window.scrollY > 8){ nav.classList.add('stuck'); } else { nav.classList.remove('stuck'); }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, {passive:true});
  }

  var steps = document.querySelectorAll('.step[data-s]');
  var ticks = document.querySelectorAll('.ptick[data-t]');
  if(steps.length && ticks.length && 'IntersectionObserver' in window){
    var sio = new IntersectionObserver(function(entries){
      entries.forEach(function(x){
        if(!x.isIntersecting) return;
        var n = x.target.getAttribute('data-s');
        ticks.forEach(function(t){ t.classList.toggle('on', t.getAttribute('data-t') === n); });
      });
    },{rootMargin:'-42% 0px -42% 0px'});
    steps.forEach(function(s){sio.observe(s)});
  }
})();
