// ============================================
// script.js - Study Planner JavaScript
// ============================================

// ---------- Modal Handling ----------
function openModal(id) {
  document.getElementById(id).classList.add('active');
  document.body.style.overflow = 'hidden';
}
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
  document.body.style.overflow = '';
}
// Close on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', function(e) {
    if (e.target === this) closeModal(this.id);
  });
});
// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => closeModal(m.id));
  }
});

// ---------- Live Search & Filter ----------
function filterTasks() {
  const search = (document.getElementById('searchInput')?.value || '').toLowerCase();
  const subject = (document.getElementById('subjectFilter')?.value || '').toLowerCase();
  const rows = document.querySelectorAll('.task-row');

  rows.forEach(row => {
    const name = (row.dataset.name || '').toLowerCase();
    const sub  = (row.dataset.subject || '').toLowerCase();
    const matchSearch  = !search  || name.includes(search);
    const matchSubject = !subject || sub === subject;
    row.style.display = (matchSearch && matchSubject) ? '' : 'none';
  });

  // Show/hide empty state
  const visible = [...rows].filter(r => r.style.display !== 'none').length;
  const emptyEl = document.getElementById('emptyState');
  if (emptyEl) emptyEl.style.display = visible === 0 ? 'block' : 'none';
}

document.getElementById('searchInput')?.addEventListener('input', filterTasks);
document.getElementById('subjectFilter')?.addEventListener('change', filterTasks);

// ---------- Auto-dismiss Flash Messages ----------
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(f => {
    f.style.transition = 'opacity 0.5s';
    f.style.opacity = '0';
    setTimeout(() => f.remove(), 500);
  });
}, 3000);

// ---------- Confirm Delete ----------
function confirmDelete(url, item) {
  if (confirm(`Are you sure you want to delete this ${item}? This cannot be undone.`)) {
    window.location.href = url;
  }
}

// ---------- Today's date for deadline min ----------
document.querySelectorAll('input[type="date"]').forEach(el => {
  if (!el.min) el.min = new Date().toISOString().split('T')[0];
});

// ---------- Highlight overdue rows ----------
document.querySelectorAll('.task-row').forEach(row => {
  const deadline = row.dataset.deadline;
  const status   = row.dataset.status;
  if (deadline && status === 'Pending') {
    if (new Date(deadline) < new Date()) {
      row.classList.add('overdue-row');
      const badge = row.querySelector('.task-badge');
      if (badge) {
        badge.className = 'badge badge-overdue';
        badge.textContent = '⚠ Overdue';
      }
    }
  }
});
