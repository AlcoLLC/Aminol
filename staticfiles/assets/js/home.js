

const swiper = new Swiper(".home-header .mySwiper", {
  loop: true,
  effect: "fade",
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".home-header .swiper-button-next",
    prevEl: ".home-header .swiper-button-prev",
  },
  pagination: {
    el: ".home-header .swiper-pagination",
    clickable: true,
  },
});


document.getElementById("scrollToTop").addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
 });

document.addEventListener("DOMContentLoaded", function () {
  const playButton = document.getElementById("playButton");
  const textContent = document.getElementById("textContent");
  const videoContainer = document.getElementById("videoContainer");
  const youtubeVideo = document.getElementById("youtubeVideo");

  if (playButton) {
    playButton.addEventListener("click", function () {
      textContent.classList.add("hidden");
      playButton.style.display = "none";
      videoContainer.style.display = "block";
      const videoSrc = youtubeVideo.src;
      youtubeVideo.src = videoSrc + "&autoplay=1";
    });
  }

  checkScroll();
  window.addEventListener("scroll", checkScroll);

  function checkScroll() {
    const sections = document.querySelectorAll(".section");
    sections.forEach((section) => {
      const sectionTop = section.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      if (sectionTop < windowHeight * 0.85) {
        section.classList.add("active");
      } else {
        section.classList.remove("active");
      }
    });
  }


  const swiperGallery = new Swiper(".gallery-section .labSwiper", {
    slidesPerView: 2.5,
    centeredSlides: true,
    spaceBetween: 20,
    loop: true,
    speed: 800,
    navigation: {
      nextEl: ".gallery-section .swiper-button-next",
      prevEl: ".gallery-section .swiper-button-prev",
    },
    breakpoints: {
      320: {
        slidesPerView: 1.3,
        spaceBetween: 15,
      },
      640: {
        slidesPerView: 1.8,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 2.2,
        spaceBetween: 20,
      },
    },
    on: {
      init: function() {
        updateSlideScaling();
      },
      slideChange: function () {
        updateSlideScaling();
      },
    },
  });

  function updateSlideScaling() {
    const slides = document.querySelectorAll(".gallery-section .swiper-slide");

    slides.forEach((slide) => {
      slide.classList.remove('active-slide');
    });

    setTimeout(() => {
      const activeSlide = document.querySelector(".gallery-section .swiper-slide-active");
      if (activeSlide) {
        activeSlide.classList.add('active-slide');
      }
    }, 50);
  }
});