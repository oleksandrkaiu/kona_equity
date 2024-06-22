function init() {
  for (let section of document.querySelectorAll(".section-head-tooltip")) {
    const openButton = section.querySelector(
      ".section-head-tooltip__open-button"
    );
    const closeButton = section.querySelector(
      ".section-head-tooltip__close-button"
    );
    if (!openButton || !closeButton) return;

    openButton.addEventListener("click", function () {
      section.classList.add("section-head-tooltip--active");
    });

    closeButton.addEventListener("click", function () {
      section.classList.remove("section-head-tooltip--active");
    });
  }
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
