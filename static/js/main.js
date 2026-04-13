// ─── Sidebar Toggle ──────────────────────────────────────────────────────────
const sidebar = document.getElementById('sidebar');
const toggle  = document.getElementById('sidebarToggle');

if (toggle && sidebar) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
  // Close on outside click (mobile)
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && e.target !== toggle) {
        sidebar.classList.remove('open');
      }
    }
  });
}

// ─── Auto-dismiss flash alerts ───────────────────────────────────────────────
document.querySelectorAll('.alert-pill').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .5s, transform .5s';
    el.style.opacity = '0';
    el.style.transform = 'translateY(-6px)';
    setTimeout(() => el.remove(), 500);
  }, 4500);
});

// ─── Table row hover highlight ───────────────────────────────────────────────
document.querySelectorAll('.student-row').forEach(row => {
  row.addEventListener('mouseenter', () => row.style.background = '#f8fafc');
  row.addEventListener('mouseleave', () => row.style.background = '');
});
