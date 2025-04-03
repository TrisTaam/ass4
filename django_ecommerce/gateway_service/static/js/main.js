// API Endpoints
const API_BASE_URL = 'http://localhost:8000/api';
const ENDPOINTS = {
    books: `${API_BASE_URL}/books`,
    laptops: `${API_BASE_URL}/laptops`,
    mobiles: `${API_BASE_URL}/mobiles`,
    clothes: `${API_BASE_URL}/clothes`,
    cart: `${API_BASE_URL}/cart`,
    orders: `${API_BASE_URL}/orders`,
    auth: `${API_BASE_URL}/auth`,
};

// State Management
let cart = {
    items: [],
    total: 0
};

let currentUser = null;

// Authentication Functions
async function login(email, password) {
    try {
        const response = await fetch(`${ENDPOINTS.auth}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        currentUser = data.user;
        updateUI();
        showToast('Login successful', 'success');
        return true;
    } catch (error) {
        showToast('Login failed: ' + error.message, 'error');
        return false;
    }
}

async function register(userData) {
    try {
        const response = await fetch(`${ENDPOINTS.auth}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        showToast('Registration successful', 'success');
        return true;
    } catch (error) {
        showToast('Registration failed: ' + error.message, 'error');
        return false;
    }
}

function logout() {
    localStorage.removeItem('token');
    currentUser = null;
    updateUI();
    showToast('Logged out successfully', 'success');
}

// Product Functions
async function loadFeaturedProducts() {
    const featuredContainer = document.getElementById('featured-products');
    if (!featuredContainer) return;

    showLoading(featuredContainer);

    try {
        // Fetch products from different categories
        const [books, laptops, mobiles, clothes] = await Promise.all([
            fetch(ENDPOINTS.books).then(res => res.json()),
            fetch(ENDPOINTS.laptops).then(res => res.json()),
            fetch(ENDPOINTS.mobiles).then(res => res.json()),
            fetch(ENDPOINTS.clothes).then(res => res.json())
        ]);

        // Combine and shuffle products
        const allProducts = [...books, ...laptops, ...mobiles, ...clothes]
            .sort(() => Math.random() - 0.5)
            .slice(0, 8);

        // Clear loading and render products
        featuredContainer.innerHTML = allProducts.map(product => createProductCard(product)).join('');
    } catch (error) {
        console.error('Error loading featured products:', error);
        featuredContainer.innerHTML = '<p class="text-center">Failed to load products</p>';
    }
}

function createProductCard(product) {
    return `
        <div class="col-md-3 col-sm-6">
            <div class="product-card">
                <img src="${product.image_url}" alt="${product.name}" class="product-image">
                <div class="product-content">
                    <h5 class="product-title">${product.name}</h5>
                    <div class="product-rating">
                        ${createRatingStars(product.rating || 0)}
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="product-price">$${product.price.toFixed(2)}</span>
                        <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id}, '${product.type}')">
                            Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function createRatingStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    return `
        ${Array(fullStars).fill('<i class="fas fa-star"></i>').join('')}
        ${hasHalfStar ? '<i class="fas fa-star-half-alt"></i>' : ''}
        ${Array(emptyStars).fill('<i class="far fa-star"></i>').join('')}
    `;
}

// Cart Functions
async function addToCart(productId, productType) {
    if (!currentUser) {
        showToast('Please login to add items to cart', 'warning');
        return;
    }

    try {
        const response = await fetch(`${ENDPOINTS.cart}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({
                product_id: productId,
                product_type: productType,
                quantity: 1
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to add item to cart');
        }

        const updatedCart = await response.json();
        cart = updatedCart;
        updateCartUI();
        showToast('Item added to cart', 'success');
    } catch (error) {
        showToast('Failed to add item to cart: ' + error.message, 'error');
    }
}

async function updateCartQuantity(productId, productType, quantity) {
    try {
        const response = await fetch(`${ENDPOINTS.cart}/update`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({
                product_id: productId,
                product_type: productType,
                quantity: quantity
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to update cart');
        }

        const updatedCart = await response.json();
        cart = updatedCart;
        updateCartUI();
    } catch (error) {
        showToast('Failed to update cart: ' + error.message, 'error');
    }
}

async function removeFromCart(productId, productType) {
    try {
        const response = await fetch(`${ENDPOINTS.cart}/remove`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({
                product_id: productId,
                product_type: productType
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to remove item from cart');
        }

        const updatedCart = await response.json();
        cart = updatedCart;
        updateCartUI();
        showToast('Item removed from cart', 'success');
    } catch (error) {
        showToast('Failed to remove item from cart: ' + error.message, 'error');
    }
}

// UI Update Functions
function updateUI() {
    updateCartUI();
    updateAuthUI();
}

function updateCartUI() {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = cart.items.reduce((total, item) => total + item.quantity, 0);
    }

    const cartTotal = document.querySelector('.cart-total');
    if (cartTotal) {
        cartTotal.textContent = `$${cart.total.toFixed(2)}`;
    }

    const cartItems = document.querySelector('.cart-items');
    if (cartItems) {
        cartItems.innerHTML = cart.items.map(item => createCartItemHTML(item)).join('');
    }
}

function updateAuthUI() {
    const authLinks = document.querySelector('#userDropdown + .dropdown-menu');
    if (authLinks) {
        if (currentUser) {
            authLinks.innerHTML = `
                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                <li><a class="dropdown-item" href="/orders">Orders</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
            `;
        } else {
            authLinks.innerHTML = `
                <li><a class="dropdown-item" href="/login">Login</a></li>
                <li><a class="dropdown-item" href="/register">Register</a></li>
            `;
        }
    }
}

// Utility Functions
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast show bg-${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body text-white">
            ${message}
        </div>
    `;

    document.querySelector('.toast-container').appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function showLoading(container) {
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="loading-spinner"></div>
            <p class="mt-3">Loading...</p>
        </div>
    `;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Check authentication status
    const token = localStorage.getItem('token');
    if (token) {
        // Verify token and load user data
        fetch(`${ENDPOINTS.auth}/verify`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            currentUser = data.user;
            updateUI();
        })
        .catch(() => {
            localStorage.removeItem('token');
            updateUI();
        });
    }

    // Load cart data if user is authenticated
    if (currentUser) {
        fetch(`${ENDPOINTS.cart}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            cart = data;
            updateCartUI();
        })
        .catch(console.error);
    }

    // Handle newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = e.target.querySelector('input[type="email"]').value;
            try {
                const response = await fetch(`${API_BASE_URL}/newsletter/subscribe`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email }),
                });

                if (!response.ok) {
                    throw new Error('Failed to subscribe');
                }

                showToast('Successfully subscribed to newsletter', 'success');
                e.target.reset();
            } catch (error) {
                showToast('Failed to subscribe: ' + error.message, 'error');
            }
        });
    }

    // Handle search form submission
    const searchForm = document.querySelector('.navbar form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = e.target.querySelector('input[type="search"]').value;
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        });
    }
}); 