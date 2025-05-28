// Carousel Class - Təkmilləşdirilmiş versiya
class CarouselController {
  constructor(options) {
    this.gap = options.gap || 115;
    this.itemWidth = options.itemWidth || 110;
    this.scrollAmount = this.itemWidth + this.gap;
    this.autoplayDelay = options.autoplayDelay || 2700;
    this.transitionDuration = options.transitionDuration || 800;

    this.carousel = document.getElementById(options.carouselId);
    this.content = document.getElementById(options.contentId);
    this.next = document.getElementById(options.nextId);
    this.prev = document.getElementById(options.prevId);

    if (!this.carousel || !this.content || !this.next || !this.prev) {
      console.warn(`Carousel elementləri tapılmadı: ${options.carouselId}`);
      return;
    }

    // State variables - hər carousel üçün ayrı
    this.isScrolling = false;
    this.autoplayTimer = null;
    this.startX = 0;
    this.scrollLeft = 0;
    this.isDragging = false;
    this.scrollTimeout = null;
    this.isInitialized = false;
    this.totalWidth = 0;

    this.init();
  }

  init() {
    if (this.isInitialized) return;

    // İçeriyi 3 dəfə təkrarlayırıq
    const originalContent = this.content.innerHTML;
    this.content.innerHTML =
      originalContent + originalContent + originalContent;

    // Ölçüləri hesablayırıq
    setTimeout(() => {
      this.calculateDimensions();
      this.setupEventListeners();
      this.setupInitialPosition();
      this.isInitialized = true;

      // Autoplay-i başladırıq
      setTimeout(() => this.startAutoplay(), 1000);
    }, 100);
  }

  calculateDimensions() {
    this.totalWidth = this.content.scrollWidth / 3;
    console.log(
      `Carousel ${this.carousel.id}: totalWidth = ${this.totalWidth}`
    );
  }

  setupInitialPosition() {
    this.carousel.style.scrollBehavior = 'auto';
    this.carousel.scrollLeft = this.totalWidth;
    this.carousel.style.cursor = 'grab';

    setTimeout(() => {
      this.carousel.style.scrollBehavior = 'smooth';
    }, 50);
  }

  setupEventListeners() {
    // Button events - arrow function istifadə edirik ki, 'this' düzgün işləsin
    this.next.addEventListener('click', (e) => {
      e.preventDefault();
      this.handleNextClick();
    });

    this.prev.addEventListener('click', (e) => {
      e.preventDefault();
      this.handlePrevClick();
    });

    // Drag events
    this.carousel.addEventListener('mousedown', (e) => this.startDrag(e));
    this.carousel.addEventListener('touchstart', (e) => this.startDrag(e), {
      passive: false,
    });

    this.carousel.addEventListener('mousemove', (e) => this.drag(e));
    this.carousel.addEventListener('touchmove', (e) => this.drag(e), {
      passive: false,
    });

    this.carousel.addEventListener('mouseup', () => this.endDrag());
    this.carousel.addEventListener('mouseleave', () => this.endDrag());
    this.carousel.addEventListener('touchend', () => this.endDrag());

    // Hover events
    this.carousel.addEventListener('mouseenter', () => {
      this.stopAutoplay();
    });

    this.carousel.addEventListener('mouseleave', () => {
      if (!this.isDragging) {
        setTimeout(() => this.startAutoplay(), 500);
      }
    });

    // Scroll event - debounced
    this.carousel.addEventListener('scroll', () => {
      this.handleScroll();
    });
  }

  handleNextClick() {
    this.stopAutoplay();
    this.moveNext();
    setTimeout(() => this.startAutoplay(), 1500);
  }

  handlePrevClick() {
    this.stopAutoplay();
    this.movePrev();
    setTimeout(() => this.startAutoplay(), 1500);
  }

  handleScroll() {
    if (this.scrollTimeout) {
      clearTimeout(this.scrollTimeout);
    }

    this.scrollTimeout = setTimeout(() => {
      if (!this.isDragging && !this.isScrolling) {
        this.checkPosition();
      }
    }, 100);
  }

  startAutoplay() {
    if (!this.isInitialized) return;

    this.stopAutoplay(); // Əvvəlki timer-i təmizləyirik

    this.autoplayTimer = setInterval(() => {
      if (!this.isScrolling && !this.isDragging && !document.hidden) {
        this.moveNext();
      }
    }, this.autoplayDelay);
  }

  stopAutoplay() {
    if (this.autoplayTimer) {
      clearInterval(this.autoplayTimer);
      this.autoplayTimer = null;
    }
  }

  checkPosition() {
    if (!this.totalWidth) {
      this.calculateDimensions();
    }

    const currentScroll = this.carousel.scrollLeft;
    const threshold = 50; // Həssaslıq üçün threshold

    if (currentScroll >= this.totalWidth * 2 - threshold) {
      // Sona çatdıq, əvvələ qayıdırıq
      this.carousel.style.scrollBehavior = 'auto';
      this.carousel.scrollLeft = this.totalWidth;
      setTimeout(() => {
        this.carousel.style.scrollBehavior = 'smooth';
      }, 10);
    } else if (currentScroll <= threshold) {
      // Əvvələ çatdıq, sona keçirik
      this.carousel.style.scrollBehavior = 'auto';
      this.carousel.scrollLeft = this.totalWidth;
      setTimeout(() => {
        this.carousel.style.scrollBehavior = 'smooth';
      }, 10);
    }
  }

  moveNext() {
    if (this.isScrolling || !this.isInitialized) return;

    this.isScrolling = true;
    this.carousel.style.scrollBehavior = 'smooth';

    // Scroll miqdarını dəqiq hesablayırıq
    this.carousel.scrollBy({
      left: this.scrollAmount,
      behavior: 'smooth',
    });

    setTimeout(() => {
      this.checkPosition();
      this.isScrolling = false;
    }, this.transitionDuration);
  }

  movePrev() {
    if (this.isScrolling || !this.isInitialized) return;

    this.isScrolling = true;
    this.carousel.style.scrollBehavior = 'smooth';

    this.carousel.scrollBy({
      left: -this.scrollAmount,
      behavior: 'smooth',
    });

    setTimeout(() => {
      this.checkPosition();
      this.isScrolling = false;
    }, this.transitionDuration);
  }

  startDrag(e) {
    this.isDragging = true;
    this.stopAutoplay();
    this.carousel.style.scrollBehavior = 'auto';

    this.startX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
    this.scrollLeft = this.carousel.scrollLeft;

    this.carousel.style.cursor = 'grabbing';
    e.preventDefault();
  }

  drag(e) {
    if (!this.isDragging) return;
    e.preventDefault();

    const x = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
    const walk = (x - this.startX) * 1.2; // Drag sürətini azaldırıq
    this.carousel.scrollLeft = this.scrollLeft - walk;
  }

  endDrag() {
    if (!this.isDragging) return;

    this.isDragging = false;
    this.carousel.style.cursor = 'grab';
    this.carousel.style.scrollBehavior = 'smooth';

    setTimeout(() => {
      this.checkPosition();
    }, 100);

    setTimeout(() => this.startAutoplay(), 2000);
  }

  destroy() {
    this.stopAutoplay();
    if (this.scrollTimeout) {
      clearTimeout(this.scrollTimeout);
    }
    this.isInitialized = false;
  }
}

// Global carousel instances
let carouselInstances = {};

// Carousel yaratma funksiyası
function createCarousel(id, config) {
  if (carouselInstances[id]) {
    carouselInstances[id].destroy();
  }

  carouselInstances[id] = new CarouselController(config);
  return carouselInstances[id];
}

// Səhifə yüklənəndə carousel-ları yaradırıq
function initializeCarousels() {
  // Partner logos carousel (brochure)
  if (document.getElementById('carousel')) {
    createCarousel('partner', {
      carouselId: 'carousel',
      contentId: 'content',
      nextId: 'next',
      prevId: 'prev',
      gap: 115,
      itemWidth: 110,
      autoplayDelay: 3000, // Bir az yavaşladırıq
      transitionDuration: 600,
    });
  }

  // Car logos carousel (about page)
  if (document.getElementById('carousel2')) {
    createCarousel('car', {
      carouselId: 'carousel2',
      contentId: 'content2',
      nextId: 'next2',
      prevId: 'prev2',
      gap: 115,
      itemWidth: 110,
      autoplayDelay: 3200, // Fərqli sürət
      transitionDuration: 600,
    });
  }
}

// Page visibility API
document.addEventListener('visibilitychange', () => {
  Object.values(carouselInstances).forEach((instance) => {
    if (document.hidden) {
      instance.stopAutoplay();
    } else {
      setTimeout(() => instance.startAutoplay(), 1000);
    }
  });
});

// DOM hazır olduqda başlat
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initializeCarousels, 300);
  });
} else {
  setTimeout(initializeCarousels, 300);
}

// Window load event - əmin olmaq üçün








window.addEventListener('load', () => {
  setTimeout(() => {
    // Əgər carousel-lar yaradılmayıbsa, yenidən cəhd et
    if (Object.keys(carouselInstances).length === 0) {
      initializeCarousels();
    }
  }, 500);
});


