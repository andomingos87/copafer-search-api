/**
 * Search Products API - Documentation
 * Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initMobileMenu();
    initSmoothScroll();
    initCopyButtons();
    initHashNavigation();
});

/**
 * Initialize sidebar navigation
 */
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.doc-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            
            // Update active states
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Show section
            sections.forEach(s => s.classList.remove('active'));
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
                
                // Update URL hash without jumping
                history.pushState(null, '', `#${sectionId}`);
                
                // Scroll to top of content
                document.querySelector('.content-wrapper').scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
            
            // Close mobile menu if open
            closeMobileMenu();
        });
    });
}

/**
 * Handle hash navigation on page load
 */
function initHashNavigation() {
    const hash = window.location.hash.slice(1);
    if (hash) {
        const link = document.querySelector(`.nav-link[data-section="${hash}"]`);
        if (link) {
            link.click();
        }
    }
    
    // Listen for hash changes
    window.addEventListener('hashchange', () => {
        const newHash = window.location.hash.slice(1);
        if (newHash) {
            const link = document.querySelector(`.nav-link[data-section="${newHash}"]`);
            if (link) {
                link.click();
            }
        }
    });
}

/**
 * Initialize mobile menu
 */
function initMobileMenu() {
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
    
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
    });
    
    overlay.addEventListener('click', closeMobileMenu);
}

/**
 * Close mobile menu
 */
function closeMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Initialize smooth scrolling for internal links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.length > 1) {
                // Let navigation handle section switching
                return;
            }
        });
    });
}

/**
 * Initialize copy to clipboard buttons
 */
function initCopyButtons() {
    // Already handled by onclick, but add visual feedback
}

/**
 * Copy code to clipboard
 */
function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const code = codeBlock.querySelector('code');
    const text = code.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copiado!';
        button.style.background = 'rgba(16, 185, 129, 0.2)';
        button.style.borderColor = 'rgba(16, 185, 129, 0.5)';
        button.style.color = '#10b981';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
            button.style.borderColor = '';
            button.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Falha ao copiar:', err);
        
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            button.textContent = 'Copiado!';
            setTimeout(() => {
                button.textContent = 'Copiar';
            }, 2000);
        } catch (e) {
            button.textContent = 'Erro!';
            setTimeout(() => {
                button.textContent = 'Copiar';
            }, 2000);
        }
        
        document.body.removeChild(textarea);
    });
}

/**
 * Add scroll spy functionality
 */
function initScrollSpy() {
    const sections = document.querySelectorAll('.doc-section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('data-section') === id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, {
        rootMargin: '-50% 0px -50% 0px'
    });
    
    sections.forEach(section => observer.observe(section));
}

/**
 * Add keyboard navigation
 */
document.addEventListener('keydown', (e) => {
    // Press 'Escape' to close mobile menu
    if (e.key === 'Escape') {
        closeMobileMenu();
    }
    
    // Press '/' to focus search (if implemented)
    if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        // Future: focus search input
    }
});

/**
 * Add smooth reveal animation on scroll
 */
function initScrollAnimations() {
    const cards = document.querySelectorAll('.card, .feature-card, .endpoint-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        observer.observe(card);
    });
}

// Initialize scroll animations after a short delay
setTimeout(initScrollAnimations, 100);

/**
 * Switch cURL tabs between local and production
 */
function switchCurlTab(button, env) {
    const tabsContainer = button.closest('.curl-tabs');
    
    // Update button states
    tabsContainer.querySelectorAll('.curl-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
    
    // Update content visibility
    tabsContainer.querySelectorAll('.curl-tab-content').forEach(content => {
        content.classList.remove('active');
        if (content.getAttribute('data-env') === env) {
            content.classList.add('active');
        }
    });
}

/**
 * Sync all cURL tabs on the page (optional enhancement)
 * When user switches one tab, switch all tabs to the same environment
 */
function syncAllCurlTabs(env) {
    document.querySelectorAll('.curl-tabs').forEach(tabsContainer => {
        const buttons = tabsContainer.querySelectorAll('.curl-tab-btn');
        const contents = tabsContainer.querySelectorAll('.curl-tab-content');
        
        buttons.forEach((btn, index) => {
            btn.classList.remove('active');
            if ((env === 'local' && index === 0) || (env === 'prod' && index === 1)) {
                btn.classList.add('active');
            }
        });
        
        contents.forEach(content => {
            content.classList.remove('active');
            if (content.getAttribute('data-env') === env) {
                content.classList.add('active');
            }
        });
    });
}

/**
 * Console welcome message
 */
console.log('%c⚡ Search Products API', 'font-size: 24px; font-weight: bold; color: #10b981;');
console.log('%cDocumentação Técnica', 'font-size: 14px; color: #94a3b8;');

