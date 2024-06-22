function initClose() {
  for (let button of document.querySelectorAll(".js-popup-close")) {
    button.addEventListener("click", function () {
      const popup = button.closest(".popup");
      if (!popup) return;
      popup.classList.remove("popup--active");
    });
  }
}

function init() {
  initClose();
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
