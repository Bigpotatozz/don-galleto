document.addEventListener("DOMContentLoaded", function() {
    let toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        let bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    });
});