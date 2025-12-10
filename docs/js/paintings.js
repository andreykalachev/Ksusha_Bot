document.addEventListener('DOMContentLoaded', () => {
    // --- Language Switching ---
    const langButtons = document.querySelectorAll('.lang-btn');
    let currentLang = localStorage.getItem('siteLanguage') || 'ru';
    
    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('siteLanguage', lang);
        document.documentElement.lang = lang;

        langButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                element.innerHTML = translations[lang][key];
            }
        });
        
        renderGallery(); // Re-render to update text
    }

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            setLanguage(btn.getAttribute('data-lang'));
        });
    });

    // --- Gallery Logic ---
    const galleryGrid = document.getElementById('gallery-grid');
    const modal = document.getElementById('painting-modal');
    const modalClose = document.querySelector('.painting-modal-close');
    
    // Modal Elements
    const modalMainImage = document.getElementById('modal-main-image');
    const modalThumbnails = document.getElementById('modal-thumbnails');
    const modalTitle = document.getElementById('modal-title');
    const modalMaterials = document.getElementById('modal-materials');
    const modalSize = document.getElementById('modal-size');
    const modalYear = document.getElementById('modal-year');
    const modalPrice = document.getElementById('modal-price');
    const modalDescription = document.getElementById('modal-description');
    const prevBtn = document.getElementById('modal-prev-btn');
    const nextBtn = document.getElementById('modal-next-btn');

    let currentPainting = null;
    let currentImageIndex = 0;
    let currentImages = []; // Array of image paths for the current painting

    function renderGallery() {
        galleryGrid.innerHTML = '';
        const data = paintingsData[currentLang] || paintingsData['en'];

        // Render Europe section
        if (data.europe && data.europe.length > 0) {
            const europeHeader = document.createElement('h2');
            europeHeader.className = 'gallery-section-header';
            europeHeader.setAttribute('data-i18n', 'gallery_europe_title');
            europeHeader.textContent = translations[currentLang].gallery_europe_title;
            galleryGrid.appendChild(europeHeader);

            const sortedEurope = [...data.europe].sort((a, b) => {
                if (a.sold && !b.sold) return 1;
                if (!a.sold && b.sold) return -1;
                return 0;
            });

            sortedEurope.forEach(p => {
                const item = document.createElement('div');
                item.classList.add('gallery-item');
                if (p.sold) {
                    item.classList.add('sold');
                }
                
                const soldLabel = p.sold ? `<div class="sold-badge">${currentLang === 'ru' ? 'ПРОДАНО' : 'SOLD'}</div>` : '';
                
                item.innerHTML = `
                    <img src="assets/paintings/${p.main_image}" alt="${p.name} - ${p.materials}" loading="lazy">
                    ${soldLabel}
                    <div class="gallery-overlay">
                        <h3>${p.name}</h3>
                    </div>
                `;
                
                item.addEventListener('click', () => {
                    openModal(p);
                });
                
                galleryGrid.appendChild(item);
            });
        }

        // Render Russia section
        if (data.russia && data.russia.length > 0) {
            const russiaHeader = document.createElement('h2');
            russiaHeader.className = 'gallery-section-header';
            russiaHeader.setAttribute('data-i18n', 'gallery_russia_title');
            russiaHeader.textContent = translations[currentLang].gallery_russia_title;
            galleryGrid.appendChild(russiaHeader);

            const sortedRussia = [...data.russia].sort((a, b) => {
                if (a.sold && !b.sold) return 1;
                if (!a.sold && b.sold) return -1;
                return 0;
            });

            sortedRussia.forEach(p => {
                const item = document.createElement('div');
                item.classList.add('gallery-item');
                if (p.sold) {
                    item.classList.add('sold');
                }
                
                const soldLabel = p.sold ? `<div class="sold-badge">${currentLang === 'ru' ? 'ПРОДАНО' : 'SOLD'}</div>` : '';
                
                item.innerHTML = `
                    <img src="assets/paintings/${p.main_image}" alt="${p.name} - ${p.materials || 'Abstract painting'}" loading="lazy">
                    ${soldLabel}
                    <div class="gallery-overlay">
                        <h3>${p.name}</h3>
                    </div>
                `;
                
                item.addEventListener('click', () => {
                    openModal(p);
                });
                
                galleryGrid.appendChild(item);
            });
        }
    }

    function openModal(painting) {
        currentPainting = painting;
        
        // Update URL hash
        if (painting.slug) {
            window.history.pushState(null, '', `#${painting.slug}`);
        }
        
        // Update meta tags and schema for SEO
        updateMetaTags(painting);
        updateSchemaData(painting);
        
        // Prepare images array: Main image + Other images
        currentImages = [painting.main_image];
        if (painting.other_images && painting.other_images.length > 0) {
            currentImages = currentImages.concat(painting.other_images);
        }
        
        currentImageIndex = 0;
        updateModalImage();
        renderThumbnails();

        // Set Text Content
        modalTitle.textContent = painting.name;
        modalMaterials.textContent = painting.materials;
        modalSize.textContent = painting.size;
        modalYear.textContent = painting.year;
        
        if (painting.sold) {
            const soldText = currentLang === 'ru' ? 'ПРОДАНО' : 'SOLD';
            modalPrice.innerHTML = `<span class="sold-status">${soldText}</span>`;
            modalPrice.classList.add('sold');
        } else {
            modalPrice.textContent = painting.price;
            modalPrice.classList.remove('sold');
        }
        
        modalDescription.textContent = painting.description;

        // Update social links with personalized messages
        const pageUrl = `https://kseniialf.art/paintings.html#${painting.slug}`;
        
        // Telegram with pre-filled message
        const telegramText = currentLang === 'ru'
            ? `Здравствуйте! Интересует картина "${painting.name}" (${painting.size}, ${painting.price}). ${pageUrl}`
            : `Hello! Interested in "${painting.name}" (${painting.size}, ${painting.price}). ${pageUrl}`;
        const telegramBtn = modal.querySelector('.social-share-btn[title="Telegram"]');
        if (telegramBtn) {
            telegramBtn.href = `https://t.me/kseniialf?text=${encodeURIComponent(telegramText)}`;
        }
        
        // Instagram link based on language
        const instagramBtn = modal.querySelector('.social-share-btn[title="Instagram"]');
        if (instagramBtn && translations[currentLang]) {
            instagramBtn.href = translations[currentLang].instagram_url;
        }
        
        // Email with pre-filled subject and body
        const emailSubject = currentLang === 'ru'
            ? `Интересует картина "${painting.name}"`
            : `Interested in "${painting.name}" painting`;
        const emailBody = currentLang === 'ru'
            ? `Здравствуйте!%0A%0AМеня заинтересовала ваша картина "${painting.name}".%0A%0AПараметры:%0A- Размер: ${painting.size}%0A- Материалы: ${painting.materials}%0A- Цена: ${painting.price}%0A%0AХотелось бы узнать подробнее о возможности приобретения и условиях доставки.%0A%0AСсылка на картину: ${pageUrl}%0A%0AС уважением`
            : `Hello!%0A%0AI'm interested in your painting "${painting.name}".%0A%0ADetails:%0A- Size: ${painting.size}%0A- Materials: ${painting.materials}%0A- Price: ${painting.price}%0A%0AI would like to know more about purchasing and delivery options.%0A%0APainting link: ${pageUrl}%0A%0ABest regards`;
        const emailBtn = modal.querySelector('.social-share-btn[title="Email"]');
        if (emailBtn) {
            emailBtn.href = `mailto:hello@kseniialf.art?subject=${encodeURIComponent(emailSubject)}&body=${emailBody}`;
        }

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function updateModalImage() {
        modalMainImage.style.opacity = '0';
        setTimeout(() => {
            modalMainImage.src = `assets/paintings/${currentImages[currentImageIndex]}`;
            modalMainImage.onload = () => {
                modalMainImage.style.opacity = '1';
            };
        }, 200);

        // Update URL with image index
        if (currentPainting && currentPainting.slug) {
            const imageParam = currentImageIndex > 0 ? `?img=${currentImageIndex + 1}` : '';
            window.history.replaceState(null, '', `#${currentPainting.slug}${imageParam}`);
        }

        // Update active thumbnail
        const thumbs = modalThumbnails.querySelectorAll('img');
        thumbs.forEach((thumb, index) => {
            if (index === currentImageIndex) {
                thumb.classList.add('active');
            } else {
                thumb.classList.remove('active');
            }
        });
    }

    function renderThumbnails() {
        modalThumbnails.innerHTML = '';
        if (currentImages.length <= 1) {
            modalThumbnails.style.display = 'none';
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
            return;
        }

        modalThumbnails.style.display = 'flex';
        prevBtn.style.display = 'flex';
        nextBtn.style.display = 'flex';

        currentImages.forEach((imgSrc, index) => {
            const thumb = document.createElement('img');
            thumb.src = `assets/paintings/${imgSrc}`;
            thumb.addEventListener('click', () => {
                currentImageIndex = index;
                updateModalImage();
            });
            modalThumbnails.appendChild(thumb);
        });
    }

    // Modal Navigation
    prevBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + currentImages.length) % currentImages.length;
        updateModalImage();
    });

    nextBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % currentImages.length;
        updateModalImage();
    });

    // Close Modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        
        // Clear hash from URL
        window.history.pushState(null, '', window.location.pathname);
        
        // Reset meta tags to default
        resetMetaTags();
    }

    modalClose.addEventListener('click', closeModal);
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (!modal.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeModal();
        if (e.key === 'ArrowLeft') prevBtn.click();
        if (e.key === 'ArrowRight') nextBtn.click();
    });

    // --- Swipe Support for Mobile ---
    let touchStartX = 0;
    let touchEndX = 0;
    const swipeThreshold = 50;
    const imageWrapper = document.querySelector('.painting-modal-main-image-wrapper');

    if (imageWrapper) {
        imageWrapper.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        imageWrapper.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
    }

    function handleSwipe() {
        if (currentImages.length <= 1) return;
        const swipeDistance = touchEndX - touchStartX;
        if (Math.abs(swipeDistance) > swipeThreshold) {
            if (swipeDistance > 0) {
                prevBtn.click(); // Swipe Right -> Prev
            } else {
                nextBtn.click(); // Swipe Left -> Next
            }
        }
    }

    // Update or Reset Meta Tags for SEO
    function updateMetaTags(painting) {
        const baseUrl = 'https://kseniialf.art';
        const imageUrl = `${baseUrl}/assets/paintings/${painting.main_image}`;
        const pageUrl = `${baseUrl}/paintings.html#${painting.slug}`;
        const description = painting.description.substring(0, 160) + '...';
        
        document.title = `${painting.name} | Kseniia ALF`;
        
        // Update existing meta tags
        updateMetaTag('description', description);
        updateMetaTag('og:title', `${painting.name} | Kseniia ALF`, 'property');
        updateMetaTag('og:description', description, 'property');
        updateMetaTag('og:image', imageUrl, 'property');
        updateMetaTag('og:url', pageUrl, 'property');
        updateMetaTag('twitter:title', `${painting.name} | Kseniia ALF`, 'property');
        updateMetaTag('twitter:description', description, 'property');
        updateMetaTag('twitter:image', imageUrl, 'property');
        
        // Update canonical link
        let canonical = document.querySelector('link[rel="canonical"]');
        if (canonical) {
            canonical.href = pageUrl;
        }
    }
    
    function updateSchemaData(painting) {
        const baseUrl = 'https://kseniialf.art';
        const imageUrl = `${baseUrl}/assets/paintings/${painting.main_image}`;
        const pageUrl = `${baseUrl}/paintings.html#${painting.slug}`;
        
        const priceMatch = painting.price.match(/(\d+)/);
        const priceValue = priceMatch ? priceMatch[1] : '0';
        
        const schema = {
            "@context": "https://schema.org",
            "@type": "VisualArtwork",
            "name": painting.name,
            "description": painting.description,
            "image": imageUrl,
            "url": pageUrl,
            "creator": {
                "@type": "Person",
                "name": "Kseniia ALF",
                "url": "https://kseniialf.art"
            },
            "artMedium": painting.materials || "Acrylic on canvas",
            "artform": "Abstract painting",
            "dateCreated": painting.year,
            "width": painting.size,
            "offers": {
                "@type": "Offer",
                "price": priceValue,
                "priceCurrency": "EUR",
                "availability": "https://schema.org/InStock",
                "url": pageUrl
            }
        };
        
        const schemaScript = document.getElementById('schema-data');
        if (schemaScript) {
            schemaScript.textContent = JSON.stringify(schema, null, 2);
        }
    }
    
    function resetSchemaData() {
        const schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Kseniia ALF Art Gallery",
            "description": "Gallery of abstract paintings by Kseniia ALF",
            "url": "https://kseniialf.art/paintings.html",
            "author": {
                "@type": "Person",
                "name": "Kseniia ALF",
                "url": "https://kseniialf.art"
            }
        };
        
        const schemaScript = document.getElementById('schema-data');
        if (schemaScript) {
            schemaScript.textContent = JSON.stringify(schema, null, 2);
        }
    }
    
    function resetMetaTags() {
        document.title = 'Kseniia ALF | Галерея картин';
        const baseUrl = 'https://kseniialf.art';
        
        updateMetaTag('description', 'Галерея абстрактной живописи Ксении ALF. Картины, наполненные смыслом, эмоциями и цветом.');
        updateMetaTag('og:title', 'Kseniia ALF | Галерея картин', 'property');
        updateMetaTag('og:description', 'Авторская коллекция абстрактных картин Ксении ALF. Каждое полотно - это застывшая эмоция, энергия цвета и уникальная история для вашего интерьера.', 'property');
        updateMetaTag('og:image', `${baseUrl}/assets/paintings/1_eu_main_image.jpg`, 'property');
        updateMetaTag('og:url', `${baseUrl}/paintings.html`, 'property');
        updateMetaTag('twitter:title', 'Kseniia ALF | Галерея картин', 'property');
        updateMetaTag('twitter:description', 'Авторская коллекция абстрактных картин Ксении ALF. Каждое полотно - это застывшая эмоция, энергия цвета и уникальная история для вашего интерьера.', 'property');
        updateMetaTag('twitter:image', `${baseUrl}/assets/paintings/1_eu_main_image.jpg`, 'property');
        
        resetSchemaData();
        
        let canonical = document.querySelector('link[rel="canonical"]');
        if (canonical) {
            canonical.href = `${baseUrl}/paintings.html`;
        }
    }
    
    function updateMetaTag(attr, value, type = 'name') {
        let tag = document.querySelector(`meta[${type}="${attr}"]`);
        if (tag) {
            tag.content = value;
        }
    }
    
    // Check for hash on page load and open corresponding painting
    function checkHashAndOpenPainting() {
        const fullHash = window.location.hash.substring(1); // Remove #
        if (fullHash) {
            // Split slug and query params
            const [slug, queryString] = fullHash.split('?');
            const data = paintingsData[currentLang] || paintingsData['en'];
            let painting = null;
            
            // Search in both regions
            if (data.europe) {
                painting = data.europe.find(p => p.slug === slug);
            }
            if (!painting && data.russia) {
                painting = data.russia.find(p => p.slug === slug);
            }
            
            if (painting) {
                openModal(painting);
                
                // Check for image index in query params
                if (queryString) {
                    const params = new URLSearchParams(queryString);
                    const imgIndex = params.get('img');
                    if (imgIndex) {
                        const index = parseInt(imgIndex) - 1;
                        if (index >= 0 && index < currentImages.length) {
                            currentImageIndex = index;
                            updateModalImage();
                        }
                    }
                }
            }
        }
    }

    // Initial Setup
    setLanguage(currentLang);
    checkHashAndOpenPainting();
    
    // Mobile Menu
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }
});
