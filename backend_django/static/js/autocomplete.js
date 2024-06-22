function autocomplete(inp) {
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
            url: Url,
            data: {
                'search': val
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                arr = data.list;
                if (!val) { return false; }
                currentFocus = -1;
                var getauth = document.getElementById("auth");
                var paidPremium = document.getElementById("paid-premium");
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
                a.setAttribute("class", "autocomplete-items");
                inp.parentNode.appendChild(a);
                b = document.createElement("a");
                b.setAttribute("href", newUrl + 'name=' + val);
                b.innerHTML = `<div><img src='/static/web_photos/bcase.svg'> Company names containing ${val}</div>`;
                b.addEventListener("click", function(e) {
                    closeAllLists();
                });
                a.appendChild(b);

                b = document.createElement("a");
                b.setAttribute("href", newUrl + 'desc=' + val);
                if (getauth == 0) {
                    b.innerHTML = `<div class="d-flex align-items-center justify-content-between"><span style='display:block'><img src='/static/web_photos/gps.svg'> Pages containing ${val}</span><a style='display:block;color:#ff7b5a;' href='/pricing'><img style='object-fit:contain;' src='/static/web_photos/pre-icon.png'>Try Premium</a></div>`;
                } else {
                    if (paidPremium === null) {
                        b.innerHTML = `<div class="d-flex align-items-center justify-content-between"><span style='display:block'><img src='/static/web_photos/gps.svg'> Pages containing ${val}</span><a style='display:block;color:#ff7b5a;' href='/pricing'><img style='object-fit:contain;' src='/static/web_photos/pre-icon.png'>Try Premium</a></div>`;
                    } else {
                        if (paidPremium.value == 1) {
                            b.innerHTML = `<div><img src='/static/web_photos/gps.svg'> Pages containing ${val}</div>`;
                        } else {
                            b.innerHTML = `<div class="d-flex align-items-center justify-content-between"><span style='display:block'><img src='/static/web_photos/gps.svg'> Pages containing ${val}</span><a style='display:block;color:#ff7b5a;' href='/pricing'><img style='object-fit:contain;' src='/static/web_photos/pre-icon.png'>Try Premium</a></div>`;
                        }
                    }
                }
                b.addEventListener("click", function(e) {
                    closeAllLists();
                });
                a.appendChild(b);
                if (getauth != 0) {
                    if (paidPremium !== null) {
                        if (paidPremium.value == 1) {
                            for (i = 0; i < arr.length; i++) {
                                var firstIndex = arr[i].toLowerCase().indexOf(val);
                                var textLength = val.length;
                                var highlightedText = arr[i].substring(0, firstIndex) + "<strong>" + arr[i].substring(firstIndex, firstIndex + textLength + 1) + "</strong>" + arr[i].substring(firstIndex + textLength + 1);
                                b = document.createElement("a");
                                b.setAttribute("href", newUrl + 'categories=' + arr[i]);
                                b.innerHTML = "<div><img src='/static/web_photos/menu.svg'>" + highlightedText + "</div>";
                                b.addEventListener("click", function(e) {
                                    closeAllLists();
                                });
                                a.appendChild(b);
                            }
                        }
                    }
                }
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