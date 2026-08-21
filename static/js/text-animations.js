/**
 * GLOBAL PREMIUM TEXT ANIMATION SYSTEM - VIBHU TRAVEL HUB
 * Handles Character Splitting, Word Blur-In, Clip-Path Reveals & SEO Preservation
 */

document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) return;

    // 1. Hero Heading Character Splitter (SEO Safe - Keeps aria-label)
    const heroTitles = document.querySelectorAll('.hero-main-title, .hero-title, .text-split');
    heroTitles.forEach(title => {
        if (title.getAttribute('data-vth-split')) return;
        const text = title.textContent.trim();
        if (!text) return;

        title.setAttribute('aria-label', text);
        title.setAttribute('data-vth-split', 'true');
        
        let charIndex = 0;
        const words = text.split(' ');
        title.innerHTML = words.map(word => {
            const wordHtml = word.split('').map(char => {
                charIndex++;
                const delay = (charIndex * 35).toFixed(0);
                return `<span class="vth-char" style="transition-delay: ${delay}ms;">${char}</span>`;
            }).join('');
            return `<span class="vth-word-wrap" style="display: inline-block; white-space: nowrap;">${wordHtml}</span>`;
        }).join(' ');
    });

    // 2. Hero Subtitle & Description Word Splitter
    const blurSubtitles = document.querySelectorAll('.text-blur, .hero-desc-anim');
    blurSubtitles.forEach(sub => {
        if (sub.getAttribute('data-vth-split')) return;
        const text = sub.textContent.trim();
        if (!text) return;

        sub.setAttribute('aria-label', text);
        sub.setAttribute('data-vth-split', 'true');

        const words = text.split(/\s+/);
        sub.innerHTML = words.map((word, idx) => {
            const delay = (idx * 80).toFixed(0);
            return `<span class="vth-word" style="transition-delay: ${delay}ms;">${word}&nbsp;</span>`;
        }).join('');
    });

    // 3. IntersectionObserver Text Reveal Engine
    const textSelector = '.hero-main-title, .hero-title, .text-split, .text-blur, .hero-desc-anim, .text-clip, .text-mask, .special-dest-title';
    const textElements = document.querySelectorAll(textSelector);

    if ('IntersectionObserver' in window) {
        const textObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible', 'active');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            rootMargin: '0px 0px -40px 0px',
            threshold: 0.1
        });

        textElements.forEach(el => textObserver.observe(el));
    } else {
        textElements.forEach(el => el.classList.add('is-visible', 'active'));
    }
});
