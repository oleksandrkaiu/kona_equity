function initMenuButton() {
  const buttons = document.querySelectorAll(".header__menu-button");
  for (let button of buttons) {
    button.addEventListener("click", function () {
      const body = document.querySelector("body");
      if (!body) return;
      const header = this.closest(".header");
      if (!header) return;
      const isOpen = this.classList.contains("menu-button--active");

      if (isOpen) {
        this.classList.remove("menu-button--active");
        header.classList.remove("header--opened");
        body.classList.remove("overflow-hidden");
      } else {
        this.classList.add("menu-button--active");
        header.classList.add("header--opened");
        body.classList.add("overflow-hidden");
      }
    });
  }

  window.addEventListener("resize", function () {
    for (let el of document.querySelectorAll(".header--opened")) {
      el.classList.remove("header--opened");

      const menuButton = el.querySelector(".header__menu-button");
      if (menuButton) menuButton.classList.remove("menu-button--active");
    }
  });
}

function init() {
  initMenuButton();
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
