/**
 * GLOBAL ANIMATION SYSTEM - VIBHU TRAVEL HUB
 * Lightweight Vanilla JS Animation Engine using IntersectionObserver
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. REDUCED MOTION PREFERENCE CHECK
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 2. PAGE LOAD TRANSITION TRIGGER
    requestAnimationFrame(() => {
        document.body.classList.add('page-loaded');
    });

    const loadElements = document.querySelectorAll('.load-anim');
    loadElements.forEach((el, index) => {
        if (!el.style.animationDelay) {
            el.style.animationDelay = `${(index + 1) * 120}ms`;
        }
    });

    // 3. AUTOMATIC GRID CHILD STAGGERING (Must run before IntersectionObserver target collection)
    const staggerContainers = document.querySelectorAll('.stagger-grid, [data-stagger-container]');
    staggerContainers.forEach(container => {
        const children = container.querySelectorAll('.reveal, .reveal-scale, .stagger-item, .anim-card, .dest-card-ref, .place-card-ref, .col-lg-4, .col-md-6, .col-lg-3, .col-lg-2');
        children.forEach((child, index) => {
            if (!child.classList.contains('stagger-item') && !child.classList.contains('reveal')) {
                child.classList.add('stagger-item');
            }
            child.style.transitionDelay = `${(index % 6) * 90}ms`;
        });
    });

    // 4. SCROLL REVEAL ENGINE (INTERSECTION OBSERVER)
    const revealSelector = '.reveal, .reveal-up, .reveal-down, .reveal-left, .reveal-right, .reveal-scale, .reveal-zoom, .reveal-fade, .scale-reveal, .fade-reveal, .img-reveal, .stagger-item, .footer-reveal-item, .dest-card-ref, .place-card-ref, [data-reveal], [data-aos]';
    const revealElements = document.querySelectorAll(revealSelector);

    const childSelector = '.reveal, .reveal-up, .reveal-down, .reveal-left, .reveal-right, .reveal-scale, .reveal-zoom, .reveal-fade, .scale-reveal, .fade-reveal, .img-reveal, .stagger-item, .dest-card-ref, .place-card-ref, [data-reveal]';

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const revealOptions = {
            root: null,
            rootMargin: '0px 0px -50px 0px',
            threshold: 0.15
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    target.classList.add('active', 'aos-animate', 'is-visible');
                    
                    const children = target.querySelectorAll(childSelector);
                    children.forEach(child => {
                        child.classList.add('active', 'aos-animate', 'is-visible');
                    });

                    observer.unobserve(target);
                }
            });
        }, revealOptions);

        revealElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight + 100 && rect.bottom > -100) {
                el.classList.add('active', 'aos-animate', 'is-visible');
                const children = el.querySelectorAll(childSelector);
                children.forEach(child => {
                    child.classList.add('active', 'aos-animate', 'is-visible');
                });
            } else {
                revealObserver.observe(el);
            }
        });

        // Fast Scroll & Initial Check Safeguard
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            if (!scrollTimeout) {
                scrollTimeout = setTimeout(() => {
                    scrollTimeout = null;
                    revealElements.forEach(el => {
                        if (!el.classList.contains('active')) {
                            const rect = el.getBoundingClientRect();
                            if (rect.top < window.innerHeight + 100 && rect.bottom > -100) {
                                el.classList.add('active', 'aos-animate', 'is-visible');
                                const children = el.querySelectorAll(childSelector);
                                children.forEach(child => {
                                    child.classList.add('active', 'aos-animate', 'is-visible');
                                });
                            }
                        }
                    });
                }, 80);
            }
        }, { passive: true });
    } else {
        // Fallback: Make everything immediately visible
        revealElements.forEach(el => {
            el.classList.add('active', 'aos-animate', 'is-visible');
        });
    }

    // 5. UNIFIED COUNTER ANIMATION ENGINE
    const statNumbers = document.querySelectorAll('.stat-number, .counter-value, .counter-number, .stat-number span');
    if (statNumbers.length > 0 && 'IntersectionObserver' in window && !prefersReducedMotion) {
        const statsObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    let targetVal = el.getAttribute('data-target');
                    let rawText = el.innerText.trim();

                    if (!targetVal && rawText) {
                        const numericMatch = rawText.replace(/,/g, '').match(/(\d+)/);
                        if (numericMatch) {
                            targetVal = numericMatch[1];
                        }
                    }

                    if (targetVal) {
                        const target = parseInt(targetVal, 10);
                        const hasPlus = rawText.includes('+') || el.innerText.includes('+');
                        const suffix = hasPlus ? '+' : '';
                        const duration = 1400;
                        const startTime = performance.now();

                        const updateCount = (now) => {
                            const progress = Math.min((now - startTime) / duration, 1);
                            const easeOutQuad = 1 - (1 - progress) * (1 - progress);
                            const current = Math.floor(easeOutQuad * target);
                            el.innerText = current.toLocaleString() + suffix;
                            if (progress < 1) {
                                requestAnimationFrame(updateCount);
                            } else {
                                el.innerText = target.toLocaleString() + suffix;
                            }
                        };
                        requestAnimationFrame(updateCount);
                    }
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.2 });

        statNumbers.forEach(el => statsObserver.observe(el));
    }

    // 6. 3D HOVER TILT FOUNDATION LISTENER
    const tiltCards = document.querySelectorAll('.hover-tilt, .card-3d');
    if (!prefersReducedMotion && window.innerWidth > 768) {
        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -6; // max 6 deg
                const rotateY = ((x - centerX) / centerX) * 6;  // max 6 deg

                card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
            });
        });
    }
});
