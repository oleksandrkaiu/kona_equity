function init() {
  for (let passwordInputEl of document.querySelectorAll(".password-input")) {
    const button = passwordInputEl.querySelector(
      ".password-input__change-button"
    );
    const input = passwordInputEl.querySelector(".password-input__input");
    if (!button && !input) return;

    button.addEventListener("click", function () {
      const active = passwordInputEl.classList.contains(
        "password-input--active"
      );
      if (active) {
        passwordInputEl.classList.remove("password-input--active");
        input.setAttribute("type", "password");
      } else {
        passwordInputEl.classList.add("password-input--active");
        input.setAttribute("type", "text");
      }
    });
  }
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
