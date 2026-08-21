/**
 * GLOBAL PREMIUM MOTION & ANIMATION ENGINE - VIBHU TRAVEL HUB
 * Includes IntersectionObserver Reveal, Section Timelines, Parallax & Desktop 3D Tilt Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Reduced Motion & Device Check
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isMobile = window.innerWidth <= 768;

    // 2. Add Page Loaded Body Class
    requestAnimationFrame(() => {
        document.body.classList.add('page-loaded');
    });

    // 3. Grid Item Auto-Staggering
    const staggerContainers = document.querySelectorAll('.stagger-grid, [data-stagger-container]');
    staggerContainers.forEach(container => {
        const children = container.querySelectorAll('.reveal, .reveal-up, .reveal-scale, .stagger-item, .vth-fleet-card, .service-card-item, .destination-card, .place-card-ref, .col-lg-4, .col-md-6, .col-lg-3, .col-lg-2');
        children.forEach((child, index) => {
            if (!child.classList.contains('stagger-item') && !child.classList.contains('reveal')) {
                child.classList.add('stagger-item');
            }
            child.style.transitionDelay = `${(index % 6) * 100}ms`;
        });
    });

    // 4. Section Timeline Sequential Reveal Engine
    const revealSelector = '.reveal, .reveal-up, .reveal-down, .reveal-left, .reveal-right, .reveal-scale, .reveal-fade, .stagger-item, .dest-card-ref, .place-card-ref, [data-reveal]';
    const revealElements = document.querySelectorAll(revealSelector);

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const revealOptions = {
            root: null,
            rootMargin: '0px 0px -40px 0px',
            threshold: 0.08
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    target.classList.add('active', 'is-visible');
                    
                    const children = target.querySelectorAll(revealSelector);
                    children.forEach((child, idx) => {
                        setTimeout(() => {
                            child.classList.add('active', 'is-visible');
                        }, idx * 60);
                    });

                    observer.unobserve(target);
                }
            });
        }, revealOptions);

        revealElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight + 80 && rect.bottom > -80) {
                el.classList.add('active', 'is-visible');
                const children = el.querySelectorAll(revealSelector);
                children.forEach(child => child.classList.add('active', 'is-visible'));
            } else {
                revealObserver.observe(el);
            }
        });

        // Fast Scroll Safety Check
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            if (!scrollTimeout) {
                scrollTimeout = setTimeout(() => {
                    scrollTimeout = null;
                    revealElements.forEach(el => {
                        if (!el.classList.contains('is-visible')) {
                            const rect = el.getBoundingClientRect();
                            if (rect.top < window.innerHeight + 80 && rect.bottom > -80) {
                                el.classList.add('active', 'is-visible');
                            }
                        }
                    });
                }, 100);
            }
        }, { passive: true });
    } else {
        revealElements.forEach(el => el.classList.add('active', 'is-visible'));
    }

    // 5. Scroll Scrubbing & Parallax Engine (GPU Accelerated)
    if (!prefersReducedMotion && !isMobile) {
        const heroBg = document.querySelector('.vth-hero-bg-img');
        const parallaxBgs = document.querySelectorAll('.parallax-bg');
        let ticking = false;

        const updateScrollPhysics = () => {
            const currentScroll = window.scrollY;
            
            // Hero Parallax (subtle 0.12x rate)
            if (heroBg && currentScroll < 800) {
                const translateY = (currentScroll * 0.12).toFixed(1);
                heroBg.style.transform = `translate3d(0, ${translateY}px, 0)`;
            }

            // General Parallax Elements
            parallaxBgs.forEach(bg => {
                const rect = bg.parentElement ? bg.parentElement.getBoundingClientRect() : bg.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    const offset = ((window.innerHeight - rect.top) * 0.05).toFixed(1);
                    bg.style.transform = `translate3d(0, ${offset}px, 0)`;
                }
            });

            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateScrollPhysics);
                ticking = true;
            }
        }, { passive: true });
    }

    // 6. Desktop Subtle 3D Card Tilt Engine (±2.5deg max) for non-content cards
    if (!prefersReducedMotion && !isMobile) {
        const tiltCardSelector = '.vth-fleet-card, .hero-mini-card, .package-card, .blog-card';
        const tiltCards = document.querySelectorAll(tiltCardSelector);

        tiltCards.forEach(card => {
            let frameId = null;

            card.addEventListener('mousemove', (e) => {
                if (frameId) cancelAnimationFrame(frameId);

                frameId = requestAnimationFrame(() => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    const rotateX = (((y - centerY) / centerY) * -2.5).toFixed(2); // ±2.5deg max
                    const rotateY = (((x - centerX) / centerX) * 2.5).toFixed(2);  // ±2.5deg max

                    card.style.transform = `perspective(1000px) translateY(-7px) scale(1.015) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                });
            });

            card.addEventListener('mouseleave', () => {
                if (frameId) cancelAnimationFrame(frameId);
                card.style.transform = '';
            });
        });
    }

    // 7. Stats Counter Engine
    const statNumbers = document.querySelectorAll('.stat-number, .counter-value, .counter-number');
    if (statNumbers.length > 0 && 'IntersectionObserver' in window && !prefersReducedMotion) {
        const statsObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    let targetVal = el.getAttribute('data-target');
                    let rawText = el.innerText.trim();

                    if (!targetVal && rawText) {
                        const numericMatch = rawText.replace(/,/g, '').match(/(\d+)/);
                        if (numericMatch) targetVal = numericMatch[1];
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
});
