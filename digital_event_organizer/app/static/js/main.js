// Main JavaScript file for Digital Event Organizer

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

function togglePriceField(isPaid) {
    var priceDiv = document.getElementById('priceDiv');
    if (priceDiv) {
        priceDiv.style.display = isPaid === 'true' ? 'block' : 'none';
    }
}

console.log('Digital Event Organizer - Ready!');
