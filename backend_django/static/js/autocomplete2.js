function autocomplete2(inp) {
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
        if (inp.value != "") {
            search(inp);
        }
    });
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
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

    function search(inp) {
        var a, b, i, val = inp.value;
        closeAllLists();
        $.ajax({
            url: "/ajax/industry/autocomplete/",
            data: {
                'search': val
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                arr = data.list;
                if (!val) { return false; }
                currentFocus = -1;
                var urlSearchParams = new URLSearchParams(window.location.search);
                var params = Object.fromEntries(urlSearchParams.entries());
                var newUrl = window.location.href.split('?')[0] + '?';
                for (param in params) {
                    if (!['desc', 'name', 'categories'].includes(param)) {
                        newUrl += param + '=' + params[param] + '&';
                    }
                }
                
                a = document.createElement("DIV");
                a.setAttribute("id", inp.id + "autocomplete-list");
                a.setAttribute("class", "autocomplete-items drop");
                inp.parentNode.appendChild(a);
                var list = document.createElement("ul");
                list.setAttribute("id", inp.id + "industry-drop");
                list.setAttribute("class", "drop-menu");
                list.style["display"] = "block";
                for (i = 0; i < arr.length; i++) {
                    b = document.createElement("li");
                    b.setAttribute("id", arr[i]);
                    b.setAttribute("class", "dropdown-item");
                    b.setAttribute("data-value", arr[i]);
                    b.innerHTML = arr[i];
                    b.addEventListener("click", function(e) {
                        var attr = $(this).attr("data-value")
                        var p = $(this).parent().parent().parent().children("input")[0];
                        p.value = attr;
                        closeAllLists();
                    });
                    list.appendChild(b);
                }
                a.appendChild(list);
            }
        });
    }

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}