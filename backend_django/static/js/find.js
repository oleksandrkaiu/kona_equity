function highlight(inp){
    var attr = inp.attr("data-show")
    if (attr != ""){
        inp.html(attr)
        inp.addClass("btnclr")
    }

}

function clear(inp, val){
    inp.html("Select " + val)
    inp.attr("data-show", "")
    inp.attr("data-back", "")
    inp.removeClass("btnclr")
}

function openNav() {
document.getElementById("myNav").style.height = "100%";
element = document.getElementsByTagName("body")[0];
element.classList.add("noscroll");
}

function closeNav() {
document.getElementById("myNav").style.height = "0%";
element = document.getElementsByTagName("body")[0];
element.classList.remove("noscroll");
}

abbreviate_number = function(num) {
    if (num === null) { return null; } // terminate early
    if (num === 0) { return '0'; } // terminate early
    fixed = 0
    var b = (num).toPrecision(2).split("e"), // get power
        k = b.length === 1 ? 0 : Math.floor(Math.min(b[1].slice(1), 14) / 3), // floor at decimals, ceiling at trillions
        c = k < 1 ? num.toFixed(0 + fixed) : (num / Math.pow(10, k * 3) ).toFixed(1 + fixed), // divide by power
        d = c < 0 ? c : Math.abs(c), // enforce -0 is 0
        e = d + " " + ['', 'K', 'M', 'B', 'T'][k]; // append power
    return e;
    }
function returnSlug(){
    var source = document.location.href
    if (source.includes("?")){
        var args = source.split("?")
        source = args[0].split("/find")[1]
        args = args[1]
    }
    else{
        var args = ""
        source = source.split("/find")[1]
    }
    source = source.split("/").join("")
    if (source.includes("--")){
        var ind = source.split("--")
        var st = ind[1]
        var ind = ind[0]
    }
    else{
        var ind = ""
        var st = ""
    }
    return [ind, st, args]
}

function removeSlug(key){
    var ind = returnSlug()
    var st = ind[1]
    var args = ind[2]
    ind = ind[0]
    if (key == "industry"){
        return "/find/" + "--" + st + "?" + args
    }
    else if (key == "state"){
        return "/find/" + ind + "--" + "?" + args
    }
    return document.location.href
}

function insertSlug(key, value){
    var ind = returnSlug()
    var st = ind[1]
    var args = ind[2]
    ind = ind[0]
    if (key == "industry"){
        return "/find/" + value + "--" + st + "?" + args
    }
    else if (key == "state"){
        return "/find/" + ind + "--" + value + "?" + args
    }
    return document.location.href
}


function removeParam(key, sourceURL) {
var rtn = sourceURL.split("?")[0],
    param,
    params_arr = [],
    queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
if (queryString !== "") {
    params_arr = queryString.split("&");
    for (var i = params_arr.length - 1; i >= 0; i -= 1) {
        param = params_arr[i].split("=")[0];
        if (param === key) {
            params_arr.splice(i, 1);
        }
    }
    rtn = rtn + "?" + params_arr.join("&");
}
return rtn;
}

function delog(n, min, max){
    pos = (Math.log(n) - Math.log(min))/(Math.log(max) - Math.log(min))
    return min + pos*(max-min)
}

function logify(n, min, max){
    var diff = max - min
    if (diff > 10000){
        var position = Math.floor(n / max * (diff));
        var minPos = min, maxPos = max;
        var minLog = Math.log(min), maxLog = Math.log(max);
        var scale = (maxLog-minLog) / (maxPos-minPos);
        n = Math.floor(Math.exp(minLog + scale * (position - minPos)))
        }
    return n
}

function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);

    var s = document.location.search
    if (!s.includes("?")){
        return document.location.href.split("?")[0] + "?" + key + "=" + value
    }
    var kvp = s.substr(1).split('&');
    var i=0;

    for(; i<kvp.length; i++){
        if (kvp[i].startsWith(key + '=')) {
            var pair = kvp[i].split('=');
            pair[1] = value;
            kvp[i] = pair.join('=');
            break;
        }
    }

    if(i >= kvp.length){
        kvp[kvp.length] = [key,value].join('=');
    }
    return document.location.href.split("?")[0] + "?" + kvp.join('&');
}
function numberWithCommas(x) {
return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function latch(){
    $(".bg-2").css("height", $("#indicator").offset().top + 100)
}

function searchy(inp, text){
    if (text == ""){
        inp.parent().children(".dropdown-item").each(function(i, obj){
            $(obj).css("display", "inline-block")
        })
    }
    else{
    inp.parent().children(".dropdown-item").each(function(i, obj){
        if (!["sinput", "clearit", "indinput"].includes(obj.id)){
            if (text.length < 3){
                var bool = $(obj).html().toLowerCase().startsWith(text.toLowerCase())
            }
            else{
                var bool = $(obj).html().toLowerCase().includes(text.toLowerCase())
            }
            if (bool){
                $(obj).css("display", "inline-block")
            }
            else{
                $(obj).css("display", "none")
        }}
    })
}

}