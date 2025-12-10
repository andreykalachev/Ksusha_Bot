document.addEventListener('DOMContentLoaded', () => {
    // --- Language Switching ---
    const langButtons = document.querySelectorAll('.lang-btn');
    const instagramLink = document.getElementById('instagram-link');
    
    // Check localStorage or default to 'ru'
    let currentLang = localStorage.getItem('siteLanguage') || 'ru';
    setLanguage(currentLang);

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-lang');
            setLanguage(lang);
        });
    });

    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('siteLanguage', lang);
        document.documentElement.lang = lang;

        // Update active button state
        langButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update text content
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                // Always use innerHTML to allow HTML tags like <br> in translations
                element.innerHTML = translations[lang][key];
            }
        });

        // Update Instagram Link
        if (translations[lang] && translations[lang].instagram_url) {
            if (instagramLink) {
                instagramLink.href = translations[lang].instagram_url;
            }
        }

        // Update Quiz Links
        const quizLinks = document.querySelectorAll('a[href^="quiz.html"]');
        quizLinks.forEach(link => {
            link.href = `quiz.html?lang=${lang}`;
        });

        // Update Carousel Text
        updateCarouselText(lang);
    }

    function updateCarouselText(lang) {
        document.querySelectorAll('.carousel-caption').forEach(caption => {
            const id = parseInt(caption.getAttribute('data-id'));
            if (id && typeof paintingsData !== 'undefined' && paintingsData[lang]) {
                // Search in both regions
                let painting = null;
                if (paintingsData[lang].europe) {
                    painting = paintingsData[lang].europe.find(p => p.id === id);
                }
                if (!painting && paintingsData[lang].russia) {
                    painting = paintingsData[lang].russia.find(p => p.id === id);
                }
                if (painting) {
                    caption.querySelector('h3').textContent = painting.name;
                }
            }
        });
    }

    // --- Mobile Menu ---
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }

    // --- Carousel ---
    const track = document.querySelector('.carousel-track');
    const nextButton = document.querySelector('.carousel-btn.next');
    const prevButton = document.querySelector('.carousel-btn.prev');
    
    // Use paintingsData if available, otherwise fallback (or empty)
    // We use 'en' as default source for structure, but text will be updated
    let paintingsSource = [];
    if (typeof paintingsData !== 'undefined' && paintingsData['en']) {
        // Combine both regions for carousel
        if (paintingsData['en'].europe) {
            paintingsSource = paintingsSource.concat(paintingsData['en'].europe);
        }
        if (paintingsData['en'].russia) {
            paintingsSource = paintingsSource.concat(paintingsData['en'].russia);
        }
    }

    if (track && paintingsSource.length > 0) {
        // Populate carousel
        paintingsSource.forEach(p => {
            const li = document.createElement('li');
            li.classList.add('carousel-slide');
            
            const img = document.createElement('img');
            img.src = `assets/paintings/${p.main_image}`;
            img.alt = p.name;
            img.loading = 'lazy';
            
            const caption = document.createElement('div');
            caption.classList.add('carousel-caption');
            caption.setAttribute('data-id', p.id);
            
            const h3 = document.createElement('h3');
            // Only Name is required for carousel as per request
            
            caption.appendChild(h3);
            
            li.appendChild(img);
            li.appendChild(caption);
            track.appendChild(li);
        });

        // Initial text update
        updateCarouselText(currentLang);

        const slides = Array.from(track.children);
        let currentIndex = 0;

        function updateCarousel() {
            if (slides.length === 0) return;
            
            // Get gap from computed styles
            const style = window.getComputedStyle(track);
            const gap = parseFloat(style.gap) || 0;

            // Calculate items per view based on CSS
            const containerWidth = track.parentElement.getBoundingClientRect().width;
            const slideWidth = slides[0].getBoundingClientRect().width;
            const itemsPerView = Math.round(containerWidth / slideWidth);
            
            // Limit index
            const maxIndex = slides.length - itemsPerView;
            if (currentIndex > maxIndex) currentIndex = maxIndex;
            if (currentIndex < 0) currentIndex = 0;

            // Calculate translation including gap
            const moveAmount = (slideWidth + gap) * currentIndex;
            track.style.transform = 'translateX(-' + moveAmount + 'px)';
        }

        window.addEventListener('resize', updateCarousel);

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                const containerWidth = track.parentElement.getBoundingClientRect().width;
                const slideWidth = slides[0].getBoundingClientRect().width;
                const itemsPerView = Math.round(containerWidth / slideWidth);
                
                if (currentIndex < slides.length - itemsPerView) {
                    currentIndex++;
                } else {
                    currentIndex = 0; // Loop back to start
                }
                updateCarousel();
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                const containerWidth = track.parentElement.getBoundingClientRect().width;
                const slideWidth = slides[0].getBoundingClientRect().width;
                const itemsPerView = Math.round(containerWidth / slideWidth);

                if (currentIndex > 0) {
                    currentIndex--;
                } else {
                    currentIndex = slides.length - itemsPerView; // Loop to end
                }
                updateCarousel();
            });
        }

        // --- Touch Support ---
        let touchStartX = 0;
        let touchEndX = 0;
        const swipeArea = track.parentElement; // Use container to avoid issues with moving element

        swipeArea.addEventListener('touchstart', e => {
            touchStartX = e.changedTouches[0].clientX;
        }, { passive: true });

        swipeArea.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].clientX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            const threshold = 50; // Minimum distance for swipe
            if (touchEndX < touchStartX - threshold) {
                // Swipe Left -> Next
                if (nextButton) nextButton.click();
            }
            if (touchEndX > touchStartX + threshold) {
                // Swipe Right -> Prev
                if (prevButton) prevButton.click();
            }
        }

        // --- Mouse Drag Support ---
        let isDragging = false;
        let dragStartX = 0;
        let dragCurrentX = 0;
        let dragStartScrollLeft = 0;

        swipeArea.addEventListener('mousedown', (e) => {
            isDragging = true;
            dragStartX = e.pageX;
            dragCurrentX = e.pageX;
            dragStartScrollLeft = currentIndex;
            swipeArea.style.cursor = 'grabbing';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            dragCurrentX = e.pageX;
        });

        document.addEventListener('mouseup', () => {
            if (!isDragging) return;
            isDragging = false;
            swipeArea.style.cursor = 'grab';
            
            const threshold = 50;
            const dragDistance = dragCurrentX - dragStartX;
            
            if (dragDistance < -threshold) {
                if (nextButton) nextButton.click();
            } else if (dragDistance > threshold) {
                if (prevButton) prevButton.click();
            }
        });

        swipeArea.style.cursor = 'grab';

        // --- Auto-play carousel ---
        let autoplayInterval;
        
        function startAutoplay() {
            autoplayInterval = setInterval(() => {
                if (nextButton) nextButton.click();
            }, 3000); // Every 3 seconds
        }
        
        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }
        
        // Start autoplay
        startAutoplay();
        
        // Pause on hover
        swipeArea.addEventListener('mouseenter', stopAutoplay);
        swipeArea.addEventListener('mouseleave', startAutoplay);
        
        // Pause on touch
        swipeArea.addEventListener('touchstart', stopAutoplay, { passive: true });
        swipeArea.addEventListener('touchend', () => {
            setTimeout(startAutoplay, 3000); // Resume after 3s
        }, { passive: true });
        
        setTimeout(updateCarousel, 100);
    }
    
    // --- Fade In Animation ---
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in, .section').forEach(section => {
        section.classList.add('fade-in-hidden');
        observer.observe(section);
    });
});
