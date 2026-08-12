/**
 * Premium Service Pages JS
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialize AOS Animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100,
            easing: 'ease-out-cubic'
        });
    }

    // 2. Animated Counters
    const counters = document.querySelectorAll('.counter-value');
    if (counters.length > 0) {
        const speed = 200; // The lower the slower
        
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const updateCount = () => {
                        const target = +counter.getAttribute('data-target');
                        const count = +counter.innerText;
                        
                        // Lower inc to slow and higher to speed up
                        const inc = target / speed;
                        
                        // Check if target is reached
                        if (count < target) {
                            // Add inc to count and output in counter
                            counter.innerText = Math.ceil(count + inc);
                            // Call function every ms
                            setTimeout(updateCount, 20);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    updateCount();
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
});
