/**
 * Premium Hero Slider - Vibhu Travel Hub
 * Swiper.js Initialization
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // Only initialize if the hero-swiper exists
    const swiperElement = document.querySelector('.hero-swiper');
    
    if (swiperElement) {
        // Initialize the Main Full-Screen Slider
        const heroSwiper = new Swiper('.hero-swiper', {
            // Elegant Fade + Horizontal Slide Combination
            effect: 'creative',
            creativeEffect: {
                prev: {
                    translate: ['-20%', 0, -1],
                    opacity: 0,
                },
                next: {
                    translate: ['20%', 0, 0],
                    opacity: 0,
                },
            },
            speed: 1500, // Smooth cinematic transitions (1500ms)
            grabCursor: true, // Support mouse drag
            
            // Infinite Looping
            loop: true,
            
            // Autoplay Configuration
            autoplay: {
                delay: 5000, // 5 seconds
                disableOnInteraction: false,
                pauseOnMouseEnter: true // Pause on hover, resume on leave
            },
            
            // Elegant Pagination Dots
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            
            // Keyboard accessibility
            keyboard: {
                enabled: true,
                onlyInViewport: false,
            },
            
            // Performance: preloading
            preloadImages: false,
            lazy: true,
            watchSlidesProgress: true,
        });
    }
});
