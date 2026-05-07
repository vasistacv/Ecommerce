/* Analytics Dashboard Charts - uses Chart.js CDN */
document.addEventListener('DOMContentLoaded', () => {
  // Revenue Chart
  const revenueCtx = document.getElementById('revenueChart');
  if (revenueCtx && window.chartData) {
    new Chart(revenueCtx, {
      type: 'line',
      data: {
        labels: window.chartData.labels || [],
        datasets: [{
          label: 'Revenue (₹)', data: window.chartData.revenue || [],
          borderColor: '#FF6B35', backgroundColor: 'rgba(255,107,53,0.1)',
          fill: true, tension: 0.4, borderWidth: 2, pointRadius: 3
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
    });
  }

  // Orders Chart
  const ordersCtx = document.getElementById('ordersChart');
  if (ordersCtx && window.chartData) {
    new Chart(ordersCtx, {
      type: 'bar',
      data: {
        labels: window.chartData.labels || [],
        datasets: [{
          label: 'Orders', data: window.chartData.orders || [],
          backgroundColor: 'rgba(155,114,207,0.6)', borderRadius: 6, barThickness: 20
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
    });
  }

  // Status Pie Chart
  const statusCtx = document.getElementById('statusChart');
  if (statusCtx && window.statusData) {
    const colors = ['#FF6B35','#9B72CF','#10B981','#F59E0B','#EF4444','#3B82F6','#6366F1','#EC4899'];
    new Chart(statusCtx, {
      type: 'doughnut',
      data: {
        labels: window.statusData.labels || [],
        datasets: [{ data: window.statusData.counts || [], backgroundColor: colors.slice(0, (window.statusData.labels||[]).length), borderWidth: 0 }]
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } }, cutout: '65%' }
    });
  }
});
