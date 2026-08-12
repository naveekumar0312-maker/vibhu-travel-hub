document.addEventListener("DOMContentLoaded", function() {
    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100
        });
    }

    // Animated Counters
    const counters = document.querySelectorAll('.stat-number span');
    const speed = 200;

    const animateCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 15);
                } else {
                    counter.innerText = target;
                }
            };
            
            // Start animation when element is in viewport
            const rect = counter.getBoundingClientRect();
            if(rect.top < window.innerHeight && rect.bottom >= 0) {
                if(!counter.classList.contains('counted')) {
                    counter.classList.add('counted');
                    updateCount();
                }
            }
        });
    };

    window.addEventListener('scroll', animateCounters);
    animateCounters(); // Trigger on load
});
