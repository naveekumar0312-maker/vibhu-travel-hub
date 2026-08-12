/**
 * Luxe Glassmorphism Navbar Interactions - Vibhu Travel Hub
 * Pure Vanilla JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Sticky Header Effect ---
    const headerWrapper = document.getElementById('luxeHeaderWrapper');
    
    if (headerWrapper) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                headerWrapper.classList.add('scrolled');
            } else {
                headerWrapper.classList.remove('scrolled');
            }
        });
    }

    // --- Mobile Menu Toggle ---
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const overlayBackground = document.querySelector('.mobile-overlay-background');
    const body = document.body;

    function toggleMobileMenu() {
        const isActive = mobileMenuToggle.classList.contains('is-active');
        
        if (isActive) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    function openMobileMenu() {
        mobileMenuToggle.classList.add('is-active');
        mobileMenuOverlay.classList.add('is-active');
        mobileMenuToggle.setAttribute('aria-expanded', 'true');
        mobileMenuOverlay.setAttribute('aria-hidden', 'false');
        
        // Lock body scroll
        body.style.overflow = 'hidden';
    }

    function closeMobileMenu() {
        mobileMenuToggle.classList.remove('is-active');
        mobileMenuOverlay.classList.remove('is-active');
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
        mobileMenuOverlay.setAttribute('aria-hidden', 'true');
        
        // Restore body scroll
        body.style.overflow = '';
        
        // Close all mobile dropdowns
        document.querySelectorAll('.mobile-dropdown-content').forEach(el => {
            el.classList.remove('is-open');
        });
        document.querySelectorAll('.mobile-dropdown-toggle i').forEach(icon => {
            icon.style.transform = 'rotate(0deg)';
        });
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }

    // Close when clicking overlay background
    if (overlayBackground) {
        overlayBackground.addEventListener('click', closeMobileMenu);
    }

    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenuOverlay && mobileMenuOverlay.classList.contains('is-active')) {
            closeMobileMenu();
        }
    });

    // Close on link click (only for standard links, not dropdown toggles)
    const mobileLinks = document.querySelectorAll('.mobile-nav-link, .mobile-dropdown-content a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // --- Mobile Dropdown Accordions ---
    const mobileDropdownToggles = document.querySelectorAll('.mobile-dropdown-toggle');
    
    mobileDropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const content = toggle.nextElementSibling;
            const icon = toggle.querySelector('i');
            const isOpen = content.classList.contains('is-open');
            
            // Close all others
            document.querySelectorAll('.mobile-dropdown-content').forEach(el => {
                if (el !== content) el.classList.remove('is-open');
            });
            document.querySelectorAll('.mobile-dropdown-toggle i').forEach(iEl => {
                if (iEl !== icon) iEl.style.transform = 'rotate(0deg)';
            });

            // Toggle current
            if (isOpen) {
                content.classList.remove('is-open');
                icon.style.transform = 'rotate(0deg)';
            } else {
                content.classList.add('is-open');
                icon.style.transform = 'rotate(180deg)';
            }
        });
    });

    // --- Button Ripple Effect ---
    const buttons = document.querySelectorAll('.luxe-book-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rippleContainer = this.querySelector('.ripple-container');
            if (!rippleContainer) return;

            const circle = document.createElement('span');
            const diameter = Math.max(this.clientWidth, this.clientHeight);
            const radius = diameter / 2;

            circle.style.width = circle.style.height = `${diameter}px`;
            circle.style.left = `${e.clientX - (this.getBoundingClientRect().left + radius)}px`;
            circle.style.top = `${e.clientY - (this.getBoundingClientRect().top + radius)}px`;
            circle.classList.add('ripple');

            const ripple = rippleContainer.querySelector('.ripple');
            if (ripple) {
                ripple.remove();
            }

            rippleContainer.appendChild(circle);
        });
    });

    // --- Smooth Scroll for Anchor Links (especially FAQ) ---
    const headerOffset = 90; // Offset for sticky navbar

    function scrollToTarget(targetId) {
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        }
    }

    document.querySelectorAll('a[href^="/#"], a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            let href = this.getAttribute('href');
            // Ignore simple "#" or links that just trigger modals
            if (href === '#' || href === '/#' || this.getAttribute('data-bs-toggle') === 'modal') return;

            let targetId = href.split('#')[1];

            // If we are already on a page containing this ID (like the homepage)
            if (targetId && document.getElementById(targetId)) {
                e.preventDefault();
                scrollToTarget(targetId);
                
                // Update URL without jumping
                if(history.pushState) {
                    history.pushState(null, null, '#' + targetId);
                } else {
                    window.location.hash = '#' + targetId;
                }
                
                // Update active navigation link visually
                document.querySelectorAll('.luxe-nav-link, .mobile-nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });

    // Handle hash on page load
    if (window.location.hash) {
        const targetId = window.location.hash.substring(1);
        if (document.getElementById(targetId)) {
            // Delay slightly to let page render
            setTimeout(() => {
                scrollToTarget(targetId);
                
                // Update active nav link
                document.querySelectorAll(`a[href="/#${targetId}"], a[href="#${targetId}"]`).forEach(link => {
                    link.classList.add('active');
                });
            }, 400);
        }
    }
});
