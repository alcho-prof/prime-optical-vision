/**
 * Product List Wishlist Functionality
 * Handles adding/removing products from wishlist with database persistence
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

// Initialize wishlist functionality
document.addEventListener('DOMContentLoaded', async function () {
    const wishlistIcons = document.querySelectorAll('.wishlist-icon');
    const csrftoken = getCookie('csrftoken');
    const isAuthenticated = document.body.dataset.userAuthenticated === 'true';

    // Get user's wishlist from server
    let userWishlist = [];
    if (isAuthenticated) {
        try {
            const response = await fetch('/wishlist/api/items/');
            if (response.ok) {
                const data = await response.json();
                userWishlist = data.product_ids || [];
            }
        } catch (error) {
            console.error('Error loading wishlist:', error);
        }
    }

    // Function to update wishlist icon
    function updateWishlistIcon(icon, productId, inWishlist) {
        const heartSpan = icon.querySelector('span');
        if (inWishlist) {
            heartSpan.textContent = '♥';  // Filled heart
            heartSpan.style.color = '#e74c3c';  // Red color
            icon.title = 'Remove from Wishlist';
        } else {
            heartSpan.textContent = '♡';  // Empty heart
            heartSpan.style.color = '#333';  // Default color
            icon.title = 'Add to Wishlist';
        }
    }

    // Initialize wishlist icons
    wishlistIcons.forEach(icon => {
        const productCard = icon.closest('.product-card');
        const productId = icon.dataset.productId || productCard.dataset.productId;

        if (productId) {
            icon.dataset.productId = productId;
            const inWishlist = userWishlist.includes(parseInt(productId));
            updateWishlistIcon(icon, productId, inWishlist);

            // Add click event
            icon.addEventListener('click', async function (e) {
                e.preventDefault();
                e.stopPropagation();

                if (isAuthenticated) {
                    const productId = this.dataset.productId;

                    try {
                        const response = await fetch(`/wishlist/toggle/${productId}/`, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken,
                                'Content-Type': 'application/json',
                            },
                        });

                        const data = await response.json();

                        if (response.ok) {
                            updateWishlistIcon(this, productId, data.in_wishlist);

                            if (data.in_wishlist) {
                                userWishlist.push(parseInt(productId));
                                showNotification('Added to wishlist ♥', 'success');
                            } else {
                                userWishlist = userWishlist.filter(id => id !== parseInt(productId));
                                showNotification('Removed from wishlist', 'info');
                            }

                            updateWishlistCount();
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        showNotification('Failed to update wishlist', 'error');
                    }
                } else {
                    // Redirect to login if not authenticated
                    showNotification('Please login to add items to wishlist', 'info');
                    setTimeout(() => {
                        window.location.href = '/accounts/login/?next=' + window.location.pathname;
                    }, 1500);
                }
            });
        }
    });

    // Update wishlist count in navigation
    function updateWishlistCount() {
        const wishlistBadge = document.querySelector('.icon-link[title="Wishlist"] .icon-badge');
        if (wishlistBadge) {
            const count = userWishlist.length;
            if (count > 0) {
                wishlistBadge.textContent = count;
                wishlistBadge.style.display = 'block';
            } else {
                wishlistBadge.style.display = 'none';
            }
        }
    }

    // Show notification
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `wishlist-notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: ${type === 'success' ? '#d4edda' : type === 'info' ? '#d1ecf1' : '#f8d7da'};
            color: ${type === 'success' ? '#155724' : type === 'info' ? '#0c5460' : '#721c24'};
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            font-weight: 500;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // Initial count update
    updateWishlistCount();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .wishlist-icon {
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    
    .wishlist-icon:hover {
        transform: scale(1.2);
    }
    
    .wishlist-icon:active {
        transform: scale(0.9);
    }
`;
document.head.appendChild(style);
