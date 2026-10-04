document.documentElement.classList.add('js');
(function(){
    var els=document.querySelectorAll('.reveal');
    if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion:reduce)').matches){
      els.forEach(function(e){e.classList.add('in')});return;
    }
    var io=new IntersectionObserver(function(en){
      en.forEach(function(x){
        if(!x.isIntersecting)return;
        var el=x.target,sibs=el.parentNode?el.parentNode.querySelectorAll(':scope > .reveal'):[];
        var i=Array.prototype.indexOf.call(sibs,el);
        el.style.transitionDelay=(Math.min(i<0?0:i,4)*60)+'ms';
        el.classList.add('in');io.unobserve(el);
      });
    },{threshold:0.12,rootMargin:'0px 0px -12% 0px'});
    els.forEach(function(e){io.observe(e)});
  })();
// mobile menu
(function(){
    var btn=document.querySelector('.menu-btn'),nav=document.getElementById('primary-nav');
    if(!btn||!nav)return;
    function set(open){nav.classList.toggle('open',open);btn.setAttribute('aria-expanded',open?'true':'false')}
    btn.addEventListener('click',function(){set(!nav.classList.contains('open'))});
    nav.addEventListener('click',function(e){if(e.target.tagName==='A')set(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open')){set(false);btn.focus()}});
    document.addEventListener('click',function(e){if(nav.classList.contains('open')&&!e.target.closest('header.nav'))set(false)});
  })();
