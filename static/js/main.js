/* ─── CareFlow JavaScript ─── */

document.addEventListener('DOMContentLoaded', function() {

    // ─── Auto-dismiss alerts ───
    document.querySelectorAll('.alert-dismissible').forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ─── Sidebar toggle for mobile ───
    var sidebar = document.getElementById('sidebar');
    if (sidebar) {
        // Close sidebar on outside click (mobile)
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                if (!sidebar.contains(e.target) && !e.target.closest('.menu-toggle')) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }

    // ─── Confirm delete actions ───
    document.querySelectorAll('[data-confirm]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // ─── Form auto-save to localStorage ───
    var forms = document.querySelectorAll('form[data-autosave]');
    forms.forEach(function(form) {
        var formId = form.dataset.autosave;
        var savedData = localStorage.getItem('careflow_form_' + formId);
        if (savedData) {
            var data = JSON.parse(savedData);
            Object.keys(data).forEach(function(key) {
                var input = form.querySelector('[name="' + key + '"]');
                if (input) input.value = data[key];
            });
        }
        form.addEventListener('input', function() {
            var data = {};
            new FormData(form).forEach(function(value, key) {
                data[key] = value;
            });
            localStorage.setItem('careflow_form_' + formId, JSON.stringify(data));
        });
        form.addEventListener('submit', function() {
            localStorage.removeItem('careflow_form_' + formId);
        });
    });

    // ─── Live clock in topbar ───
    var clockEl = document.getElementById('liveClock');
    if (clockEl) {
        function updateClock() {
            var now = new Date();
            clockEl.textContent = now.toLocaleTimeString('en-IN', {
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            });
        }
        updateClock();
        setInterval(updateClock, 1000);
    }

    // ─── Keyboard shortcut: Ctrl+K for search ───
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var searchInput = document.querySelector('input[name="search"]');
            if (searchInput) searchInput.focus();
        }
    });
});