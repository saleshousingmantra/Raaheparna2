/* Raahee Parna: page behaviour (menu, motion, lightbox, enquiry popup) */
document.addEventListener('DOMContentLoaded', function () {
  var cfg = window.SITE_CONFIG || {};
  var PHONE = '917420880067';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Fill Project, Developer and Relationship Manager fields from config.js */
  [['project', cfg.PROJECT_NAME], ['developer', cfg.DEFAULT_DEVELOPER_NAME], ['manager_name', cfg.DEFAULT_MANAGER_NAME], ['manager_email', cfg.DEFAULT_MANAGER_EMAIL]]
    .forEach(function (p) {
      if (p[1]) document.querySelectorAll('[name="' + p[0] + '"]').forEach(function (el) { el.defaultValue = el.value = p[1]; });
    });

  /* Earlier versions remembered an enquiry and unlocked prices for good */
  try { localStorage.removeItem('raahee_prices_unlocked'); } catch (e) {}

  /* Reading progress line (sits just under the floating header) + header shadow */
  var prog = document.getElementById('progress'), nav = document.querySelector('.nav');
  function onScroll() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var pct = h > 0 ? Math.min(1, window.scrollY / h) : 0;
    if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 30);
    if (prog && nav) {
      var r = nav.getBoundingClientRect();
      prog.style.top = (r.bottom + 6) + 'px';
      prog.style.left = (r.left + 18) + 'px';
      prog.style.width = Math.max(0, (r.width - 36) * pct) + 'px';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* Mobile menu */
  var toggle = document.getElementById('navToggle'), links = document.getElementById('mainNav');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      toggle.setAttribute('aria-expanded', links.classList.toggle('open') ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }

  /* Reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* Count-up for the key facts */
  var counts = document.querySelectorAll('[data-count]');
  if (counts.length && 'IntersectionObserver' in window && !reduceMotion) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        co.unobserve(en.target);
        var el = en.target, txt = el.textContent.trim(), m = txt.match(/^([\d.]+)(.*)$/);
        if (!m) return;
        var end = parseFloat(m[1]), suffix = m[2], dec = (m[1].split('.')[1] || '').length, t0 = null;
        (function step(ts) {
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / 1300, 1), e = 1 - Math.pow(1 - p, 3);
          el.textContent = (end * e).toFixed(dec) + suffix;
          if (p < 1) window.requestAnimationFrame(step); else el.textContent = txt;
        })(performance.now());
      });
    }, { threshold: .6 });
    counts.forEach(function (el) { co.observe(el); });
  }

  /* Image lightbox */
  var lb = document.getElementById('lightbox'), lbImg = document.getElementById('lbImg'), lbCap = document.getElementById('lbCap');
  document.querySelectorAll('[data-zoom]').forEach(function (el) {
    el.addEventListener('click', function () {
      lbImg.src = el.getAttribute('data-zoom'); lbImg.alt = el.getAttribute('data-alt') || '';
      lbCap.textContent = el.getAttribute('data-alt') || '';
      lb.classList.add('open'); document.body.style.overflow = 'hidden';
    });
  });
  function closeLb() { lb.classList.remove('open'); document.body.style.overflow = ''; }
  lb.addEventListener('click', closeLb);

  /* Enquiry popup */
  var overlay = document.getElementById('modalOverlay'), interest = document.getElementById('modal-interest');
  var modalForm = document.getElementById('modalForm'), pendingWa = null;
  function openModal(plan, intent) {
    overlay.dataset.intent = intent || 'enquire';
    if (plan) interest.value = plan;
    document.getElementById('modalTitle').textContent = intent === 'whatsapp' ? 'Chat with us on WhatsApp' : 'Get Price & Brochure';
    overlay.classList.add('open'); document.body.style.overflow = 'hidden';
    setTimeout(function () { document.getElementById('modal-name').focus(); }, 100);
  }
  function closeModal() { overlay.classList.remove('open'); document.body.style.overflow = ''; }
  document.getElementById('modalClose').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeModal(); closeLb(); } });
  document.querySelectorAll('[data-open-modal]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (el.getAttribute('data-intent') === 'call') { window.location.href = 'tel:+' + PHONE; return; }
      openModal(el.getAttribute('data-plan'), el.getAttribute('data-intent'));
    });
  });
  modalForm.addEventListener('submit', function () {
    if (overlay.dataset.intent === 'whatsapp') pendingWa = window.open('', '_blank');
  });
  modalForm.addEventListener('enquirySubmitted', function (e) {
    var d = e.detail || {};
    if (overlay.dataset.intent === 'whatsapp') {
      var url = 'https://wa.me/' + PHONE + '?text=' + encodeURIComponent(
        "Hi, I'm " + (d.name || '') + ". I'm interested in " + (d.interest || 'a home') + ' at ' + (d.project || 'Raahee Parna') + '. My number is ' + (d.phone || '') + '. Please share details.');
      if (pendingWa && !pendingWa.closed) pendingWa.location.href = url; else window.open(url, '_blank');
      pendingWa = null;
    }
  });

  /* Open the popup once, 15 seconds after the page loads */
  setTimeout(function () {
    var a = document.activeElement;
    if (!overlay.classList.contains('open') && !(a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))) openModal();
  }, 15000);

  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();
});
