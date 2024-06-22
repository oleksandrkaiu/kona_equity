function automain(inp) {
  var timer;
  var currentFocus;
  var arr;
  inp.addEventListener("input", function(e) {
    clearTimeout(timer);
    var ms = 300;
    timer = setTimeout(function() {
        search(inp);
    }, ms);

  });
  inp.addEventListener("focus", function(e) {
    if (inp.value != ""){
        search(inp);
    }
  });
  inp.addEventListener("keydown", function(e) {
    var x = document.getElementsByClassName("search-item")
      if (e.keyCode == 40) {
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) {
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) {
        e.preventDefault();
        if (currentFocus > -1) {
          if (x) x[currentFocus].click();
        }
      }
  });
  function search(inp){
    var a, b, i, val = inp.value;
    closeAllLists();
    $.ajax({
        url: Url,
        data: {
        'search': val
        },
        dataType: 'json',
        success: function (data) {
            arr = data.list;
            if (!val) { return false;}
            currentFocus = -1;
            a = document.createElement("div")
            a.setAttribute("class", "s-cont")
            inp.parentNode.parentNode.appendChild(a);
            for (i = 0; i < arr.length; i++) {
                b = document.createElement("a");
                b.setAttribute("href", '/find/--/?categories=' + arr[i]);
                b.setAttribute("class", "search-item");
                b.innerHTML = "<div><img src='/static/web_photos/menu.svg'>" + "<strong>" + arr[i].substr(0, val.length) + "</strong>" + arr[i].substr(val.length) + "</div>";
                b.addEventListener("click", function(e) {
                    closeAllLists();
                });
                a.appendChild(b)
            }
        }
    });
  }
  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("main-active");
  }
  function removeActive(x) {
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("main-active");
    }
  }
  function closeAllLists() {
      $(".search-item").remove();
  }
  document.addEventListener("click", function (e) {
      if (document.activeElement != inp){
      closeAllLists(e.target);
      }
  });
}