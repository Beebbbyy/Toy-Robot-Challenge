/**
 * Theme Management System
 * Handles dark/light mode toggling with smooth transitions
 */

class ThemeManager {
    constructor() {
        this.theme = this.getStoredTheme() || this.getPreferredTheme();
        this.init();
    }

    /**
     * Initialize theme manager
     */
    init() {
        // Apply stored or preferred theme
        this.applyTheme(this.theme);

        // Create theme toggle button
        this.createThemeToggle();

        // Listen for system theme changes
        this.listenToSystemTheme();

        // Add ripple effect to all buttons
        this.addRippleEffectToButtons();
    }

    /**
     * Get theme from localStorage
     */
    getStoredTheme() {
        return localStorage.getItem('theme');
    }

    /**
     * Get preferred theme from system settings
     */
    getPreferredTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    /**
     * Apply theme to document
     */
    applyTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Dispatch theme change event
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }

    /**
     * Toggle between light and dark themes
     */
    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    /**
     * Listen to system theme changes
     */
    listenToSystemTheme() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        mediaQuery.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /**
     * Create theme toggle button
     */
    createThemeToggle() {
        // Create container
        const container = document.createElement('div');
        container.className = 'theme-toggle-container';
        container.setAttribute('aria-label', 'Theme toggle');

        // Create toggle button
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle';
        toggle.setAttribute('aria-label', `Switch to ${this.theme === 'light' ? 'dark' : 'light'} mode`);
        toggle.setAttribute('title', `Switch to ${this.theme === 'light' ? 'dark' : 'light'} mode`);

        // Create slider with icons
        const slider = document.createElement('div');
        slider.className = 'theme-toggle-slider';

        const sunIcon = document.createElement('span');
        sunIcon.className = 'theme-toggle-icon sun';
        sunIcon.textContent = '☀️';

        const moonIcon = document.createElement('span');
        moonIcon.className = 'theme-toggle-icon moon';
        moonIcon.textContent = '🌙';

        slider.appendChild(sunIcon);
        slider.appendChild(moonIcon);
        toggle.appendChild(slider);
        container.appendChild(toggle);

        // Add click handler
        toggle.addEventListener('click', () => {
            this.toggleTheme();
            toggle.setAttribute('aria-label', `Switch to ${this.theme === 'light' ? 'dark' : 'light'} mode`);
            toggle.setAttribute('title', `Switch to ${this.theme === 'light' ? 'dark' : 'light'} mode`);
        });

        // Add keyboard support
        toggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle.click();
            }
        });

        // Add to document
        document.body.appendChild(container);
    }

    /**
     * Add enhanced ripple effect to all buttons
     */
    addRippleEffectToButtons() {
        // Add ripple to existing buttons
        this.setupRippleEffects();

        // Watch for dynamically added buttons
        const observer = new MutationObserver(() => {
            this.setupRippleEffects();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Setup ripple effects on buttons
     */
    setupRippleEffects() {
        const buttons = document.querySelectorAll('.btn:not(.ripple-initialized)');

        buttons.forEach(button => {
            button.classList.add('ripple-initialized');

            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'btn-ripple';

                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';

                this.appendChild(ripple);

                // Remove ripple after animation
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    /**
     * Add smooth scroll behavior
     */
    enableSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Add entrance animations to sections
     */
    addEntranceAnimations() {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }
        );

        // Observe all sections
        document.querySelectorAll('section').forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            observer.observe(section);
        });
    }

    /**
     * Add particle effect on theme toggle (optional enhancement)
     */
    createThemeTransitionEffect() {
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9998';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');

        // Create particles
        const particles = [];
        for (let i = 0; i < 50; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 3 + 1,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                alpha: 1
            });
        }

        // Animate particles
        let animationId;
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.alpha -= 0.02;

                if (particle.alpha > 0) {
                    ctx.beginPath();
                    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
                    ctx.fillStyle = `rgba(59, 130, 246, ${particle.alpha})`;
                    ctx.fill();
                }
            });

            if (particles.every(p => p.alpha <= 0)) {
                cancelAnimationFrame(animationId);
                canvas.remove();
            } else {
                animationId = requestAnimationFrame(animate);
            }
        };

        animate();
    }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeManager = new ThemeManager();
    });
} else {
    window.themeManager = new ThemeManager();
}

// Export for module usage
export default ThemeManager;
