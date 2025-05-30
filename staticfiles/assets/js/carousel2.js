// // Partner Logos Carousel - Üçüncü karusel
// class PartnerCarouselController {
//     constructor() {
//         this.gap = 115;
//         this.itemWidth = 110;
//         this.scrollAmount = this.itemWidth + this.gap;
//         this.autoplayDelay = 3200;
//         this.transitionDuration = 600;

//         this.carousel = document.getElementById('carousel3');
//         this.content = document.getElementById('content3');
//         this.next = document.getElementById('next3');
//         this.prev = document.getElementById('prev3');

//         if (!this.carousel || !this.content || !this.next || !this.prev) {
//             console.warn('Partner carousel elementləri tapılmadı');
//             return;
//         }

//         // State variables
//         this.isScrolling = false;
//         this.autoplayTimer = null;
//         this.startX = 0;
//         this.scrollLeft = 0;
//         this.isDragging = false;
//         this.scrollTimeout = null;
//         this.isInitialized = false;
//         this.singleWidth = 0;
//         this.resetInProgress = false;

//         this.init();
//     }

//     init() {
//         if (this.isInitialized) return;

//         // İçeriyi 3 dəfə təkrarlayırıq və əvvəlinə sonuncu elementi əlavə edirik
//         const originalContent = this.content.innerHTML;
//         const tempDiv = document.createElement('div');
//         tempDiv.innerHTML = originalContent;
//         const items = Array.from(tempDiv.children);

//         if (items.length === 0) return;

//         // Son elementi əvvələ əlavə edirik, sonra 3 kopya
//         const lastItem = items[items.length - 1].cloneNode(true);
//         const firstItem = items[0].cloneNode(true);

//         this.content.innerHTML = lastItem.outerHTML + originalContent + originalContent + originalContent + firstItem.outerHTML;

//         // Ölçüləri hesablayırıq
//         setTimeout(() => {
//             this.calculateDimensions();
//             this.setupEventListeners();
//             this.setupInitialPosition();
//             this.isInitialized = true;

//             // Autoplay-i başladırıq
//             setTimeout(() => this.startAutoplay(), 1000);
//         }, 100);
//     }

//     calculateDimensions() {
//         const totalItems = this.content.children.length;
//         const itemWidth = this.itemWidth + this.gap;
//         this.singleWidth = (totalItems - 2) * itemWidth / 3;
//         console.log(`Partner Carousel: singleWidth = ${this.singleWidth}, totalItems = ${totalItems}`);
//     }

//     setupInitialPosition() {
//         const itemWidth = this.itemWidth + this.gap;
//         this.carousel.style.scrollBehavior = 'auto';
//         this.carousel.scrollLeft = itemWidth;
//         this.carousel.style.cursor = 'grab';

//         setTimeout(() => {
//             this.carousel.style.scrollBehavior = 'smooth';
//         }, 50);
//     }

//     setupEventListeners() {
//         // Button events
//         this.next.addEventListener("click", (e) => {
//             e.preventDefault();
//             this.handleNextClick();
//         });

//         this.prev.addEventListener("click", (e) => {
//             e.preventDefault();
//             this.handlePrevClick();
//         });

//         // Drag events
//         this.carousel.addEventListener('mousedown', (e) => this.startDrag(e));
//         this.carousel.addEventListener('touchstart', (e) => this.startDrag(e), { passive: false });

//         this.carousel.addEventListener('mousemove', (e) => this.drag(e));
//         this.carousel.addEventListener('touchmove', (e) => this.drag(e), { passive: false });

//         this.carousel.addEventListener('mouseup', () => this.endDrag());
//         this.carousel.addEventListener('mouseleave', () => this.endDrag());
//         this.carousel.addEventListener('touchend', () => this.endDrag());

//         // Hover events
//         this.carousel.addEventListener('mouseenter', () => {
//             this.stopAutoplay();
//         });

//         this.carousel.addEventListener('mouseleave', () => {
//             if (!this.isDragging) {
//                 setTimeout(() => this.startAutoplay(), 500);
//             }
//         });

//         // Scroll event
//         this.carousel.addEventListener('scroll', () => {
//             this.handleScroll();
//         });
//     }

//     handleNextClick() {
//         this.stopAutoplay();
//         this.moveNext();
//         setTimeout(() => this.startAutoplay(), 1500);
//     }

//     handlePrevClick() {
//         this.stopAutoplay();
//         this.movePrev();
//         setTimeout(() => this.startAutoplay(), 1500);
//     }

//     handleScroll() {
//         if (this.scrollTimeout) {
//             clearTimeout(this.scrollTimeout);
//         }

//         this.scrollTimeout = setTimeout(() => {
//             if (!this.isDragging && !this.isScrolling && !this.resetInProgress) {
//                 this.checkPosition();
//             }
//         }, 150);
//     }

//     startAutoplay() {
//         if (!this.isInitialized) return;

//         this.stopAutoplay();

//         this.autoplayTimer = setInterval(() => {
//             if (!this.isScrolling && !this.isDragging && !document.hidden && !this.resetInProgress) {
//                 this.moveNext();
//             }
//         }, this.autoplayDelay);
//     }

//     stopAutoplay() {
//         if (this.autoplayTimer) {
//             clearInterval(this.autoplayTimer);
//             this.autoplayTimer = null;
//         }
//     }

//     checkPosition() {
//         if (!this.singleWidth || this.resetInProgress) return;

//         const currentScroll = this.carousel.scrollLeft;
//         const itemWidth = this.itemWidth + this.gap;
//         const maxScroll = this.carousel.scrollWidth - this.carousel.clientWidth;
//         const threshold = 30;

//         if (currentScroll >= maxScroll - threshold) {
//             this.resetPosition(itemWidth);
//         }
//         else if (currentScroll <= threshold) {
//             this.resetPosition(this.singleWidth + itemWidth);
//         }
//     }

//     resetPosition(newPosition) {
//         this.resetInProgress = true;
//         const wasScrollBehaviorSmooth = this.carousel.style.scrollBehavior === 'smooth';

//         this.carousel.style.scrollBehavior = 'auto';
//         this.carousel.scrollLeft = newPosition;

//         setTimeout(() => {
//             if (wasScrollBehaviorSmooth) {
//                 this.carousel.style.scrollBehavior = 'smooth';
//             }
//             this.resetInProgress = false;
//         }, 20);
//     }

//     moveNext() {
//         if (this.isScrolling || !this.isInitialized || this.resetInProgress) return;

//         this.isScrolling = true;
//         this.checkPosition();

//         setTimeout(() => {
//             this.carousel.style.scrollBehavior = 'smooth';
//             this.carousel.scrollBy({
//                 left: this.scrollAmount,
//                 behavior: 'smooth'
//             });

//             setTimeout(() => {
//                 this.checkPosition();
//                 this.isScrolling = false;
//             }, this.transitionDuration);
//         }, this.resetInProgress ? 100 : 0);
//     }

//     movePrev() {
//         if (this.isScrolling || !this.isInitialized || this.resetInProgress) return;

//         this.isScrolling = true;
//         this.checkPosition();

//         setTimeout(() => {
//             this.carousel.style.scrollBehavior = 'smooth';
//             this.carousel.scrollBy({
//                 left: -this.scrollAmount,
//                 behavior: 'smooth'
//             });

//             setTimeout(() => {
//                 this.checkPosition();
//                 this.isScrolling = false;
//             }, this.transitionDuration);
//         }, this.resetInProgress ? 100 : 0);
//     }

//     startDrag(e) {
//         this.isDragging = true;
//         this.stopAutoplay();
//         this.carousel.style.scrollBehavior = 'auto';

//         this.startX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
//         this.scrollLeft = this.carousel.scrollLeft;

//         this.carousel.style.cursor = 'grabbing';
//         e.preventDefault();
//     }

//     drag(e) {
//         if (!this.isDragging) return;
//         e.preventDefault();

//         const x = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX;
//         const walk = (x - this.startX) * 1.2;
//         this.carousel.scrollLeft = this.scrollLeft - walk;
//     }

//     endDrag() {
//         if (!this.isDragging) return;

//         this.isDragging = false;
//         this.carousel.style.cursor = 'grab';
//         this.carousel.style.scrollBehavior = 'smooth';

//         setTimeout(() => {
//             this.checkPosition();
//         }, 200);

//         setTimeout(() => this.startAutoplay(), 2000);
//     }

//     destroy() {
//         this.stopAutoplay();
//         if (this.scrollTimeout) {
//             clearTimeout(this.scrollTimeout);
//         }
//         this.isInitialized = false;
//         this.resetInProgress = false;
//     }
// }

// // Partner carousel yaratma və işə salma
// let partnerCarouselInstance = null;

// function initPartnerCarousel() {
//     if (document.getElementById('carousel3')) {
//         if (partnerCarouselInstance) {
//             partnerCarouselInstance.destroy();
//         }
//         partnerCarouselInstance = new PartnerCarouselController();
//     }
// }

// // Page visibility API
// document.addEventListener('visibilitychange', () => {
//     if (partnerCarouselInstance) {
//         if (document.hidden) {
//             partnerCarouselInstance.stopAutoplay();
//         } else {
//             setTimeout(() => partnerCarouselInstance.startAutoplay(), 1000);
//         }
//     }
// });

// // Initialization
// if (document.readyState === 'loading') {
//     document.addEventListener('DOMContentLoaded', () => {
//         setTimeout(initPartnerCarousel, 300);
//     });
// } else {
//     setTimeout(initPartnerCarousel, 300);
// }

// window.addEventListener('load', () => {
//     setTimeout(() => {
//         if (!partnerCarouselInstance) {
//             initPartnerCarousel();
//         }
//     }, 500);
// });