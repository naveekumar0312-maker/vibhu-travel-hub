/**
 * GLOBAL ANIMATION SYSTEM - VIBHU TRAVEL HUB
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. PAGE LOAD ANIMATIONS
    // Add page-loaded class to body to trigger initial CSS animations
    document.body.classList.add('page-loaded');

    // Select elements that need to fade up on load immediately
    const loadElements = document.querySelectorAll('.load-anim');
    loadElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 150}ms`;
        el.classList.add('fade-in-up-load');
    });

    // 2. SCROLL REVEAL (INTERSECTION OBSERVER)
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -50px 0px', // Trigger slightly before it comes into view
            threshold: 0.15
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // Stop observing once animated to prevent repeating animations on scroll up
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        revealElements.forEach(el => {
            revealObserver.observe(el);
        });
    } else {
        // Fallback for older browsers or reduced motion preference
        revealElements.forEach(el => {
            el.classList.add('active');
        });
    }
});
