/* Main JS */
document.addEventListener('DOMContentLoaded', () => {
  // CSRF Token helper
  window.getCSRF = () => {
    const c = document.cookie.match(/csrftoken=([^;]+)/);
    return c ? c[1] : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  };

  // Auto-dismiss alerts
  document.querySelectorAll('.alert').forEach(a => {
    setTimeout(() => { a.style.opacity = '0'; a.style.transform = 'translateY(-10px)'; setTimeout(() => a.remove(), 300); }, 4000);
  });

  // Add to cart AJAX
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const form = btn.closest('form');
      if (!form) return;
      btn.innerHTML = '⏳ Adding...'; btn.disabled = true;
      try {
        const resp = await fetch(form.action, {
          method: 'POST', body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await resp.json();
        if (data.success) {
          btn.innerHTML = '✅ Added!';
          const badge = document.querySelector('.cart-badge');
          if (badge) badge.textContent = data.cart_count;
          setTimeout(() => { btn.innerHTML = '🛒 Add to Cart'; btn.disabled = false; }, 1500);
        }
      } catch { btn.innerHTML = '🛒 Add to Cart'; btn.disabled = false; }
    });
  });

  // Quantity controls
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.parentElement.querySelector('.qty-input');
      let val = parseInt(input.value) || 1;
      if (btn.dataset.action === 'inc') val++;
      else if (btn.dataset.action === 'dec' && val > 1) val--;
      input.value = val;
    });
  });

  // Search form
  const searchForm = document.querySelector('.nav-search');
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = searchForm.querySelector('input').value.trim();
      if (q) window.location.href = `/products/?q=${encodeURIComponent(q)}`;
    });
  }

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });

  // Star rating input
  document.querySelectorAll('.star-rating-input').forEach(container => {
    const stars = container.querySelectorAll('.star');
    const input = container.querySelector('input[type="hidden"]');
    stars.forEach(star => {
      star.addEventListener('click', () => {
        const val = star.dataset.value;
        input.value = val;
        stars.forEach(s => { s.classList.toggle('active', s.dataset.value <= val); });
      });
      star.addEventListener('mouseenter', () => {
        stars.forEach(s => { s.classList.toggle('hover', s.dataset.value <= star.dataset.value); });
      });
    });
    container.addEventListener('mouseleave', () => { stars.forEach(s => s.classList.remove('hover')); });
  });
});

// Format currency
function formatCurrency(amount) { return '₹' + parseFloat(amount).toLocaleString('en-IN', { minimumFractionDigits: 2 }); }
