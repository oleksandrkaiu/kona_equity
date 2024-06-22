import Swiper from "swiper";

function init() {
  for (let sliderEl of document.querySelectorAll(".company-meta__slider")) {
    let swiper = null;
    let init = false;

    function initSwiper() {
      const isPhone = window.matchMedia("(max-width: 767px)");

      if (isPhone.matches) {
        if (!init) {
          swiper = new Swiper(sliderEl, {
            slidesPerView: "auto",
            spaceBetween: 16,
          });
          init = true;
        }
      } else if (swiper !== null) {
        swiper.destroy(true, true);
        init = false;
      }
    }

    window.addEventListener("resize", initSwiper);
    initSwiper();
  }
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
