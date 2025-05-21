
document.addEventListener("DOMContentLoaded", function () {
  const playButton = document.getElementById("playButton");
  const textContent = document.getElementById("textContent");
  const videoContainer = document.getElementById("videoContainer");
  const youtubeVideo = document.getElementById("youtubeVideo");

  playButton.addEventListener("click", function () {
    textContent.classList.add("hidden");

    playButton.style.display = "none";

    videoContainer.style.display = "block";

    const videoSrc = youtubeVideo.src;

    youtubeVideo.src = videoSrc + "&autoplay=1";
  });

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
    slidesPerView: "auto",
    centeredSlides: true,
    spaceBetween: 30,
    loop: true,
    speed: 800,
    navigation: {
      nextEl: ".gallery-section .swiper-button-next",
      prevEl: ".gallery-section .swiper-button-prev",
    },
    breakpoints: {
      320: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 20,
      },
    },
    on: {
      slideChange: function () {
        const slides = document.querySelectorAll(
          ".gallery-section .swiper-slide"
        );

        slides.forEach((slide) => {
          const img = slide.querySelector("img");
          img.style.width = "100%";
        });

        setTimeout(() => {
          const activeSlide = document.querySelector(
            ".gallery-section .swiper-slide-active"
          );
          if (activeSlide) {
            const activeImg = activeSlide.querySelector(
              ".gallery-section .swiper-slide-active img"
            );
            activeImg.style.width = "200vh";
          }
        }, 10);
      },
    },
  });

  setTimeout(() => {
    const activeSlide = document.querySelector(
      ".gallery-section .swiper-slide-active"
    );
    if (activeSlide) {
      const activeImg = activeSlide.querySelector(
        ".gallery-section .swiper-slide-active img"
      );
      activeImg.style.width = "200vh";
    }
  }, 100);
});
