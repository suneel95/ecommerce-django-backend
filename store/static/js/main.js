// Optional: small interactions (e.g. confirm before remove, number input limits)
// Kept minimal - no frameworks.

document.addEventListener('DOMContentLoaded', function () {
    // Optional: confirm when removing from cart
    var removeLinks = document.querySelectorAll('a[href*="remove"]');
    removeLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (!confirm('Remove this item from cart?')) {
                e.preventDefault();
            }
        });
    });
});
