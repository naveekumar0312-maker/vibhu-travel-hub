/**
 * DYNAMIC UNIVERSAL DESTINATION ABOUT ANIMATION ENGINE
 * Vibhu Travel Hub — Works across ALL Destination Pages Dynamically
 */

document.addEventListener('DOMContentLoaded', function() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isMobile = window.innerWidth <= 768;

    // 1. Target ALL Destination About Sections Dynamically
    const aboutSections = document.querySelectorAll('#about-state, #about-preview, .destinations-about-section, .about-section, [id*="about-state"]');

    aboutSections.forEach(section => {
        // IntersectionObserver Viewport Reveal (15-20% Threshold)
        if ('IntersectionObserver' in window && !prefersReducedMotion) {
            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const target = entry.target;
                        target.classList.add('is-visible', 'active');

                        // Activate all descendant reveal elements
                        const children = target.querySelectorAll('.reveal-left, .reveal-right, .reveal, h2, p, .vth-eyebrow, .row.g-3.pt-3 > *');
                        children.forEach(child => child.classList.add('is-visible', 'active'));

                        obs.unobserve(target);
                    }
                });
            }, {
                root: null,
                rootMargin: '0px 0px -40px 0px',
                threshold: 0.15
            });

            observer.observe(section);
        } else {
            section.classList.add('is-visible', 'active');
        }

        // 2. Subtle GPU Scroll Scrubbing & Parallax for Destination Image & Content
        if (!prefersReducedMotion && !isMobile) {
            const aboutImg = section.querySelector('.position-relative img, .about-image-wrapper img, .about-hero-img');
            const heading = section.querySelector('h2');
            const textContent = section.querySelector('.about-text-content, p.lead');

            if (aboutImg || heading || textContent) {
                let ticking = false;

                const updateScrollPhysics = () => {
                    const rect = section.getBoundingClientRect();
                    if (rect.top < window.innerHeight && rect.bottom > 0) {
                        const scrollProgress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
                        const scrollOffset = (scrollProgress - 0.5);

                        // Image Parallax (5-8px shift)
                        if (aboutImg) {
                            const imgOffset = (scrollOffset * 16).toFixed(1);
                            aboutImg.style.transform = `translate3d(0, ${imgOffset}px, 0) scale(1.02)`;
                        }

                        // Heading Parallax (3-5px shift)
                        if (heading) {
                            const headOffset = (scrollOffset * 8).toFixed(1);
                            heading.style.transform = `translate3d(0, ${headOffset}px, 0)`;
                        }

                        // Text Parallax (2-4px shift)
                        if (textContent) {
                            const textOffset = (scrollOffset * 6).toFixed(1);
                            textContent.style.transform = `translate3d(0, ${textOffset}px, 0)`;
                        }
                    }
                    ticking = false;
                };

                window.addEventListener('scroll', () => {
                    if (!ticking) {
                        requestAnimationFrame(updateScrollPhysics);
                        ticking = true;
                    }
                }, { passive: true });
            }
        }
    });
});
