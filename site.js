document.documentElement.classList.add('js');
// Scroll reveal. Content is visible by default: the .reveal-ready class that hides .reveal elements is only
// added once the observer exists, and any failure reveals everything rather than leaving it hidden.
(function(){
    var els=document.querySelectorAll('.reveal');
    function showAll(){els.forEach(function(e){e.classList.add('in')})}
    try{
      if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion:reduce)').matches){showAll();return;}
      var io=new IntersectionObserver(function(en){
        en.forEach(function(x){
          if(!x.isIntersecting)return;
          var el=x.target,sibs=el.parentNode?el.parentNode.querySelectorAll(':scope > .reveal'):[];
          var i=Array.prototype.indexOf.call(sibs,el);
          el.style.transitionDelay=(Math.min(i<0?0:i,4)*60)+'ms';
          el.classList.add('in');io.unobserve(el);
        });
      },{threshold:0,rootMargin:'0px 0px -10% 0px'});
      els.forEach(function(e){io.observe(e)});
      document.documentElement.classList.add('reveal-ready');
      // keyboard focus or an anchor jump into a not-yet-revealed block shows it at once
      document.addEventListener('focusin',function(e){var r=e.target.closest&&e.target.closest('.reveal');if(r)r.classList.add('in')});
      window.addEventListener('hashchange',function(){var t=document.getElementById(location.hash.slice(1));if(t){(t.closest('.reveal')||t).classList.add('in');t.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in')})}});
    }catch(err){document.documentElement.classList.remove('reveal-ready');showAll();}
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
// Booking links ship hidden with a placeholder href and are only revealed once a real
// calendar URL is in place, so a half-configured site never shows a dead button.
(function(){
    document.querySelectorAll('[data-booking]').forEach(function(a){
      var href=a.getAttribute('href')||'';
      if(href&&href.indexOf('REPLACE-ME')===-1)a.hidden=false;
    });
  })();
