document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('mhMobileToggle');
  const navMenu = document.getElementById('mhNavMenu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', function () {
      navMenu.classList.toggle('is-active');
    });
  }

  // Mobile dropdown toggle handling
  const dropdowns = document.querySelectorAll('.mh-dropdown');
  dropdowns.forEach(function (dropdown) {
    const link = dropdown.querySelector('.mh-nav-link');
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 992) {
        e.preventDefault();
        dropdown.classList.toggle('is-open');
      }
    });
  });
});