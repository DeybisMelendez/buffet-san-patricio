// ============================================
// BOA POS - Common JavaScript
// Funciones comunes para toda la aplicación
// ============================================

// Prevenir reenvío de formularios al recargar página
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Inicializar dropdowns de navegación
document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.nav__dropdown');
  
  dropdowns.forEach(dropdown => {
    dropdown.addEventListener('mouseenter', function() {
      this.querySelector('.nav__dropdown-content').style.display = 'block';
    });
    
    dropdown.addEventListener('mouseleave', function() {
      this.querySelector('.nav__dropdown-content').style.display = 'none';
    });
  });
});

// Utilidad para mostrar/ocultar alertas
window.boa = window.boa || {};
window.boa.alerts = {
  hideAll: function() {
    const alertSection = document.querySelector('.alerts');
    if (alertSection) {
      alertSection.style.display = 'none';
    }
  },
  
  showAll: function() {
    const alertSection = document.querySelector('.alerts');
    if (alertSection) {
      alertSection.style.display = 'block';
    }
  }
};