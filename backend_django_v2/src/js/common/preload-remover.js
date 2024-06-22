function init() {
  const allPreloads = document.querySelectorAll(".preload");
  for (let preload of allPreloads) {
    preload.classList.remove("preload");
  }
}

if (["complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("load", init);
}
