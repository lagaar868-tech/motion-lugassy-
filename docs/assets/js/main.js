/* Lugassy Expertise — interactions légères */
(function () {
  document.documentElement.classList.add('js');

  // Année du pied de page
  var y = document.getElementById('annee');
  if (y) y.textContent = new Date().getFullYear();

  // En-tête : ombre au défilement
  var header = document.querySelector('.header');
  var onScroll = function () { header && header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Menu mobile
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('menu');
  function closeMenu() {
    if (!toggle) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Ouvrir le menu');
    nav.classList.remove('is-open');
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      nav.classList.toggle('is-open', open);
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  // Apparition des sections
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        // léger décalage entre éléments voisins
        var siblings = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.classList.contains('reveal'); });
        el.style.transitionDelay = Math.min(siblings.indexOf(el), 4) * 90 + 'ms';
        el.classList.add('is-visible');
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Lien actif dans le menu
  var links = document.querySelectorAll('.nav a[href^="#"]:not(.btn)');
  if ('IntersectionObserver' in window && links.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) { l.classList.toggle('is-active', l.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('main section[id]').forEach(function (s) { spy.observe(s); });
  }

  // Formulaire de contact
  // - Si data-endpoint contient une URL (ex. Formspree), envoi direct.
  // - Sinon, ouverture de la messagerie avec le message pré-rempli.
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = form.querySelector('.form__status');
  var TO = '[EMAIL]';

  function setStatus(msg, ok) { status.textContent = msg; status.className = 'form__status ' + (ok ? 'ok' : 'err'); }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var valid = true;
    form.querySelectorAll('[required]').forEach(function (f) {
      var bad = f.type === 'checkbox' ? !f.checked : !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      f.classList.toggle('is-invalid', bad);
      if (bad) valid = false;
    });
    if (!valid) { setStatus('Merci de compléter les champs obligatoires (*) et d’accepter les conditions.', false); return; }
    if (form._gotcha && form._gotcha.value) return; // anti-spam

    var data = new FormData(form);
    var endpoint = form.getAttribute('data-endpoint');
    if (endpoint) {
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true;
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error();
          form.reset(); setStatus('Merci, votre demande a bien été envoyée. Nous revenons vers vous rapidement.', true);
        })
        .catch(function () { setStatus('L’envoi a échoué. Vous pouvez nous écrire directement à ' + TO + '.', false); })
        .finally(function () { btn.disabled = false; });
    } else {
      var body = 'Nom : ' + data.get('nom') + '\nEmail : ' + data.get('email') + '\nTéléphone : ' + (data.get('telephone') || '—') + '\n\n' + data.get('message');
      window.location.href = 'mailto:' + TO + '?subject=' + encodeURIComponent('Demande de rendez-vous – ' + data.get('nom')) + '&body=' + encodeURIComponent(body);
      setStatus('Votre messagerie s’ouvre avec votre message pré-rempli.', true);
    }
  });
})();
