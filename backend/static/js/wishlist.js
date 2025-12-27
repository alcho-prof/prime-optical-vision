/**
 * Wishlist Page JavaScript
 * Handles wishlist item removal and notifications
 */

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // Handle remove button clicks
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;
            removeFromWishlist(productId, this);
        });
    });

    // Handle add to cart button clicks
    document.querySelectorAll('.btn-add-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
});

/**
 * Remove item from wishlist
 * @param {number} productId - The product ID to remove
 * @param {HTMLElement} button - The remove button element
 */
async function removeFromWishlist(productId, button) {
    const csrftoken = getCookie('csrftoken');
    const wishlistItem = button.closest('.wishlist-item');

    try {
        const response = await fetch(`/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (data.status === 'removed') {
            // Animate removal
            wishlistItem.style.opacity = '0';
            wishlistItem.style.transform = 'scale(0.8)';

            setTimeout(() => {
                wishlistItem.remove();

                // Check if wishlist is now empty
                const remainingItems = document.querySelectorAll('.wishlist-item');
                if (remainingItems.length === 0) {
                    location.reload(); // Reload to show empty state
                } else {
                    // Update count
                    const countEl = document.querySelector('.wishlist-count');
                    if (countEl) {
                        const count = remainingItems.length;
                        countEl.textContent = `${count} item${count !== 1 ? 's' : ''}`;
                    }
                }
            }, 300);

            showNotification('Removed from wishlist', 'info');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to remove item', 'error');
    }
}

/**
 * Add product to cart
 * @param {number} productId - The product ID to add to cart
 */
function addToCart(productId) {
    // TODO: Implement add to cart functionality
    showNotification('Add to cart functionality coming soon!', 'info');
}

/**
 * Show notification message
 * @param {string} message - The message to display
 * @param {string} type - The notification type (success, error, info)
 */
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
