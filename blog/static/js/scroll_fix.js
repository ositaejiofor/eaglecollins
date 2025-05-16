window.addEventListener("load", function() {
  if (window.location.hash) {
    const id = window.location.hash.substring(1);
    const el = document.getElementById(id);
    if (el) {
      const yOffset = -100; // Adjust to your header height
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }
});
