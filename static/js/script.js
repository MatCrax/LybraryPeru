document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize carousels with custom settings
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        new bootstrap.Carousel(carousel, {
            interval: 5000,
            wrap: true
        });
    });
    
    // Handle quantity input for add to cart forms
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        const minusBtn = input.previousElementSibling;
        const plusBtn = input.nextElementSibling;
        
        if (minusBtn && minusBtn.classList.contains('btn-minus')) {
            minusBtn.addEventListener('click', function() {
                if (input.value > 1) {
                    input.value = parseInt(input.value) - 1;
                }
            });
        }
        
        if (plusBtn && plusBtn.classList.contains('btn-plus')) {
            plusBtn.addEventListener('click', function() {
                input.value = parseInt(input.value) + 1;
            });
        }
    });
    
    // Handle purchase vs rental buttons
    const purchaseButtons = document.querySelectorAll('.btn-purchase');
    const rentalButtons = document.querySelectorAll('.btn-rental');
    
    purchaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form) {
                const rentalInput = form.querySelector('input[name="is_rental"]');
                if (rentalInput) {
                    rentalInput.value = 'false';
                }
            }
        });
    });
    
    rentalButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form) {
                const rentalInput = form.querySelector('input[name="is_rental"]');
                if (rentalInput) {
                    rentalInput.value = 'true';
                }
            }
        });
    });
    
    // Update cart item quantity and total
    const cartQuantityInputs = document.querySelectorAll('.cart-quantity');
    cartQuantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
    
    // Handle book search
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const searchInput = document.getElementById('searchInput');
            if (searchInput && searchInput.value.trim() === '') {
                event.preventDefault();
                alert('Please enter a search term');
            }
        });
    }
    
    // Scroll to top button
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.style.display = 'block';
            } else {
                scrollToTopBtn.style.display = 'none';
            }
        });
        
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
