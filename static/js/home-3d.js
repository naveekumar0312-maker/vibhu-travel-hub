/**
 * VIBHU TRAVEL HUB - HOME PAGE 3D MOTION & INTERACTION ENGINE
 */

document.addEventListener('DOMContentLoaded', () => {
    const isMobile = window.innerWidth <= 768;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 1. DESKTOP MOUSE-BASED 3D PARALLAX FOR HERO VISUAL
    if (!isMobile && !prefersReducedMotion) {
        const heroSection = document.querySelector('.hero-ref-section');
        const heroVisual = document.querySelector('.hero-visual-wrapper');

        if (heroSection && heroVisual) {
            let mouseX = 0;
            let mouseY = 0;
            let targetX = 0;
            let targetY = 0;
            let ticking = false;

            const handleMouseMove = (e) => {
                const rect = heroSection.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                targetX = ((y - centerY) / centerY) * -2.5; // Max 2.5deg
                targetY = ((x - centerX) / centerX) * 2.5;

                if (!ticking) {
                    requestAnimationFrame(updateHeroParallax);
                    ticking = true;
                }
            };

            const updateHeroParallax = () => {
                mouseX += (targetY - mouseX) * 0.1;
                mouseY += (targetX - mouseY) * 0.1;

                heroVisual.style.transform = `perspective(1000px) rotateX(${mouseY.toFixed(2)}deg) rotateY(${mouseX.toFixed(2)}deg) translateZ(10px)`;
                ticking = false;
            };

            heroSection.addEventListener('mousemove', handleMouseMove);
            heroSection.addEventListener('mouseleave', () => {
                targetX = 0;
                targetY = 0;
                requestAnimationFrame(updateHeroParallax);
            });
        }

        // 2. INTERACTIVE CARD 3D TILT
        const tiltCards = document.querySelectorAll('.dest-card-ref, .place-card-ref, .fleet-showcase-container, .why-point-item');
        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -2.5;
                const rotateY = ((x - centerX) / centerX) * 2.5;

                card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
            });
        });
    }

    // 3. INLINE BOOK YOUR TRIP FORM PRE-FILL & MODAL LAUNCH
    const bookStripForm = document.getElementById('bookStripForm');
    if (bookStripForm) {
        bookStripForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('stripName')?.value || '';
            const phone = document.getElementById('stripPhone')?.value || '';
            const date = document.getElementById('stripDate')?.value || '';

            // Pre-fill existing #enquiryModal fields
            const modalName = document.getElementById('enquiryName');
            const modalPhone = document.getElementById('enquiryPhone');
            const modalDate = document.getElementById('enquiryTravelDate');

            if (modalName) modalName.value = name;
            if (modalPhone) modalPhone.value = phone;
            if (modalDate) modalDate.value = date;

            // Launch Modal
            const enquiryModalEl = document.getElementById('enquiryModal');
            if (enquiryModalEl && typeof bootstrap !== 'undefined') {
                const modalInstance = bootstrap.Modal.getOrCreateInstance(enquiryModalEl);
                modalInstance.show();
            }
        });
    }
});
