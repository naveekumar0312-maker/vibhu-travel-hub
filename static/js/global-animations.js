/**
 * GLOBAL ANIMATION SYSTEM - VIBHU TRAVEL HUB
 * IntersectionObserver & Page Load Animation Handler
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. PAGE LOAD ANIMATION TRIGGER
    requestAnimationFrame(() => {
        document.body.classList.add('page-loaded');
    });

    // Stagger load elements if present
    const loadElements = document.querySelectorAll('.load-anim');
    loadElements.forEach((el, index) => {
        if (!el.style.animationDelay) {
            el.style.animationDelay = `${(index + 1) * 150}ms`;
        }
    });

    // 2. AUTOMATIC GRID STAGGERING
    const staggerContainers = document.querySelectorAll('.stagger-grid, [data-stagger-container]');
    staggerContainers.forEach(container => {
        const children = container.querySelectorAll('.reveal, .reveal-scale, .stagger-item, .anim-card, .col-lg-4, .col-md-6, .col-lg-3');
        children.forEach((child, index) => {
            if (!child.classList.contains('stagger-item') && !child.classList.contains('reveal')) {
                child.classList.add('stagger-item');
            }
            child.style.transitionDelay = `${(index % 6) * 120}ms`;
        });
    });

    // 3. SCROLL REVEAL (INTERSECTION OBSERVER)
    const revealSelector = '.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-item';
    const revealElements = document.querySelectorAll(revealSelector);

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -40px 0px',
            threshold: 0.12
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
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

    // 4. NAV LINK ACTIVE & SMOOTH HOVER EFFECTS
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            link.classList.add('hovered');
        });
        link.addEventListener('mouseleave', () => {
            link.classList.remove('hovered');
        });
    });

    // 5. ACCORDION ICON ROTATION ENHANCEMENT
    const accordionButtons = document.querySelectorAll('.accordion-button');
    accordionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.add('animating');
            setTimeout(() => btn.classList.remove('animating'), 350);
        });
    });

    // 6. STATISTICS COUNTER ANIMATION
    const statNumbers = document.querySelectorAll('.stat-number, .counter-number');
    if (statNumbers.length > 0 && 'IntersectionObserver' in window && !prefersReducedMotion) {
        const statsObserverOptions = {
            threshold: 0.2
        };
        const statsObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const text = el.innerText.trim();
                    const match = text.match(/^(\d+)(.*)$/);
                    if (match) {
                        const target = parseInt(match[1], 10);
                        const suffix = match[2];
                        const duration = 1500;
                        const startTime = performance.now();
                        const updateCount = (now) => {
                            const progress = Math.min((now - startTime) / duration, 1);
                            const easeOutQuad = 1 - (1 - progress) * (1 - progress);
                            const current = Math.floor(easeOutQuad * target);
                            el.innerText = current + suffix;
                            if (progress < 1) {
                                requestAnimationFrame(updateCount);
                            } else {
                                el.innerText = target + suffix;
                            }
                        };
                        requestAnimationFrame(updateCount);
                    }
                    observer.unobserve(el);
                }
            });
        }, statsObserverOptions);

        statNumbers.forEach(el => statsObserver.observe(el));
    }
});
