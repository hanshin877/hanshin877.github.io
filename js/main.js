'use strict';

// mobile nav toggle
const navToggle = document.getElementById('nav-toggle');
const mainNav = document.getElementById('main-nav');
if (navToggle && mainNav) {
  navToggle.addEventListener('click', () => mainNav.classList.toggle('open'));
}

// smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (mainNav) mainNav.classList.remove('open');
  });
});

// active nav on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('#main-nav a.nav1st');
window.addEventListener('scroll', () => {
  const y = window.scrollY + 100;
  sections.forEach(sec => {
    if (y >= sec.offsetTop && y < sec.offsetTop + sec.offsetHeight) {
      navLinks.forEach(l => {
        const li = l.closest('li');
        li.classList.toggle('active', l.getAttribute('href') === '#' + sec.id);
      });
    }
  });
  // back to top
  const sTop = document.getElementById('sTop');
  if (sTop) sTop.classList.toggle('visible', window.scrollY > 400);
});

// back to top
const sTop = document.getElementById('sTop');
if (sTop) {
  sTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// contact form
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('.form-submit');
    btn.textContent = '전송 중...';
    btn.disabled = true;
    setTimeout(() => {
      alert('메시지가 전송되었습니다. 감사합니다!');
      form.reset();
      btn.textContent = '메시지 보내기';
      btn.disabled = false;
    }, 1000);
  });
}
