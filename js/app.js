document.addEventListener('DOMContentLoaded', function () {
  var cfg = window.SITE_CONFIG || {};
  var PHONE = '917420880067', PHONE_DISPLAY = '+91 74208 80067';

  /* Fill Project, Developer and Relationship Manager fields from
     config.js (one place to change them). defaultValue is set too so
     form.reset() after a submit keeps the values. */
  [['project', cfg.PROJECT_NAME], ['developer', cfg.DEFAULT_DEVELOPER_NAME], ['manager_name', cfg.DEFAULT_MANAGER_NAME], ['manager_email', cfg.DEFAULT_MANAGER_EMAIL]]
    .forEach(function (p) {
      if (p[1]) document.querySelectorAll('[name="' + p[0] + '"]').forEach(function (el) { el.defaultValue = el.value = p[1]; });
    });


  /* Alternate prices stay blurred and locked on every visit; tapping one
     opens the enquiry form. (Earlier versions remembered an enquiry in
     localStorage and unlocked prices for good, so clear that old key.) */
  try { localStorage.removeItem('raahee_prices_unlocked'); } catch (e) {}

  /* Mobile nav */
  var toggle = document.getElementById('navToggle'), nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      toggle.setAttribute('aria-expanded', nav.classList.toggle('open') ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }

  /* Header shadow on scroll */
  var header = document.querySelector('.site-header');
  window.addEventListener('scroll', function () { header.classList.toggle('scrolled', window.scrollY > 40); }, { passive: true });

  /* Reveal on scroll */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }


  /* Amenity accordion (collapsed on phones, always open on desktop) */
  document.querySelectorAll('.acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (window.innerWidth > 900) return;
      var box = btn.closest('.acc');
      var open = box.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  var firstAcc = document.querySelector('.acc');
  if (firstAcc && window.innerWidth <= 900) { firstAcc.classList.add('open'); firstAcc.querySelector('.acc-btn').setAttribute('aria-expanded', 'true'); }

  /* Floor-plan tabs */
  var tabs = document.querySelectorAll('[data-plan-tab]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      document.querySelectorAll('.plan-panel').forEach(function (p) { p.hidden = p.id !== t.getAttribute('data-plan-tab'); });
    });
  });

  /* Lightbox */
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
  var pendingWa = null, modalForm = document.getElementById('modalForm');
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
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeModal(); closeLb(); }
  });
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
    var d = e.detail || {}, intent = overlay.dataset.intent;
    if (intent === 'whatsapp') {
      var url = 'https://wa.me/' + PHONE + '?text=' + encodeURIComponent(
        "Hi, I'm " + (d.name || '') + ". I'm interested in " + (d.interest || 'a home') + ' at ' + (d.project || 'Raahee Parna') + '. My number is ' + (d.phone || '') + '. Please share details.');
      if (pendingWa && !pendingWa.closed) pendingWa.location.href = url; else window.open(url, '_blank');
      pendingWa = null;
    }
  });

  /* Auto-open once after 15s */
  setTimeout(function () {
    var a = document.activeElement;
    if (!overlay.classList.contains('open') && !(a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))) openModal();
  }, 15000);

  document.getElementById('year').textContent = new Date().getFullYear();
});
