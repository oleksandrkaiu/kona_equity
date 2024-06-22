/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
navToggle = document.getElementById('nav-toggle'),
navClose = document.getElementById('nav-close')


/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}


/*===== Filter accordion ===*/
var acc = document.getElementsByClassName("accordion")

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
      /* Toggle between adding and removing the "active" class,
      to highlight the button that controls the panel */
      this.classList.toggle("active");
  
      /* Toggle between hiding and showing the active panel */
      let panel = document.getElementById("filter-content")
    //   if (panel.style.display === "block") {
    //     panel.style.display = "none";
    //   } else {
    //     panel.style.display = "block";
    //   }
      if (panel.classList.contains("accordion-open")) {
        panel.removeAttribute('style')
        panel.classList.remove("accordion-open");
      } else {
        panel.style.height = panel.scrollHeight + 'px'
        panel.classList.add("accordion-open");
      }
    
    });
  }



/*============== Autocomplete script =================*/
// function main(){

//     var elem = document.getElementById("searchy2");
//     elem.addEventListener("keypress", function (e){
//         if (e.keyCode == 13){
//             e.preventDefault();
//             var elem = document.getElementById("searchy2");
//             if (elem.value != ""){
//                 var href = removeParam("page", insertParam("search", elem.value))
//                 window.location.href = href
//             }
//         }
//     });

//     var elem = document.getElementById("searchhy");
//     elem.addEventListener("keypress", function (e){
//         if (e.keyCode == 13){
//             e.preventDefault();
//             var elem = document.getElementById("searchhy");
//             if (elem.value != ""){
//                 var href = removeParam("page", insertParam("search", elem.value))
//                 window.location.href = href
//             }
//         }
//     });

//     var elems = document.getElementsByClassName("pg-link")
//     for (var i = 0; i < elems.length; i++){
//         href = elems[i].getAttribute("href")
//         href = elems[i].setAttribute("href", insertParam("page", href))
//     }

//     $(".dropdown").click(function(e){
//         e.stopPropagation()
//         $(this).find(".dropdown-content").css("display", "block");
//     });

//     $(document).on("click", function(event){
//         var n = $(".dropdown-content").css("display");
//         if (n == "block"){
//             $(".dropdown-content").css("display", "none")
//         }
//     });
//     $(".dropdown").hover(function(){
//         $(this).find(".dropdown-content").css("display", "block");
//     },function(){
//         $(this).find(".dropdown-content").css("display", "none");
//     });

//     $("#searchy2").val("");
//     $("#searchhy").val("");

//     $("#sinput").focus(function(e){
//         $("#droppys").addClass("mich");
//     });

//     $("#sinput").blur(function(){
//         $("#droppys").removeClass("mich");
//     });

//     $("#sinput").on("input focus", function(){
//         var text = $(this).val()
//         searchy2($(this), text)
//     });

//     $("#indinput").focus(function(e){
//         $("#droppyi").addClass("mich");
//     });

//     $("#indinput").blur(function(){
//         $("#droppyi").removeClass("mich");
//     });

//     $("#indinput").on("input focus", function(){
//         var text = $(this).val()
//         searchy2($(this), text)
//     });

//     highlight($('#droppys'));
//     highlight($('#droppyi'));
//     $("#clrbtn").click(function(){
//         window.location.href = "/find/"
//     });
//     $(".dropdown-item").click(function(){
//         var attr = $(this).attr("data-value")
//         var show = $(this).html()
//         var p = $(this).parent().parent().children("button")[0]
//         if (attr == "nulli"){
//             clear($(p), "Industry")
//         }
//         else if (attr == "nulls"){
//             clear($(p), "State")
//         }
//         else{
//             $(p).attr("data-show", show)
//             $(p).attr("data-back", attr)
//             highlight($(p))
//         }
//     });

//     var inp = document.getElementById("searchy2")
//     autocomplete(inp);
//     Url = "{% url 'ajax_autocomplete' %}"

//     dropys();
//     logmeout();
//     openSome();
//     validato();
//     checkSome();
//     favCheck();
//     popitUp();
//     mobileSignup();

//     var ar_min = 100000;
//     var ar_max = 52000000000;
//     var em_min = 1;
//     var em_max = 75000;
//     var g_min = 0;
//     var g_max = 8;

//     var se = new URL(window.location.href).searchParams
//     var arn = delog(Number(se.get("arn")), ar_min, ar_max)
//     if (!arn){arn = ar_min}
//     var arx = delog(Number(se.get("arx")), ar_min, ar_max)
//     if (!arx){arx = ar_max}
//     var empn = delog(Number(se.get("empn")), em_min, em_max)
//     if (!empn){empn = em_min}
//     var empx = delog(Number(se.get("empx")), em_min, em_max)
//     if (!empx){empx = em_max}
//     var gn = Number(se.get("gn"))
//     if (!gn){gn=g_min}
//     var gx = parseInt(se.get("gx"))
//     if (!gx){gx=g_max}


//     $("#filterUp").click(function(){
//         $("#searchy2").val($("#searchhy").val())
//         $("#slidyBoi").slideUp(400, function() {
//             $("#showBoi2").fadeIn();
//         });
//     });
//     $("#droppyi").blur(function(){
//         $('this').dropdown('hide');
//     })
//     $("#droppys").blur(function(){
//         $('this').dropdown('hide');
//     })
//     $("#dropdowni").on('hidden.bs.dropdown', function () {
//             $(this).find("button").blur();
//     });
//     $("#dropdowns").on('hidden.bs.dropdown', function () {
//             $(this).find("button").blur();
//     });
//     $("#filterDown2").click(function(){
//         $("#searchhy").val($("#searchy2").val())
//         $("#showBoi2").fadeOut(200, function() {
//             $("#slidyBoi").slideDown(400, function() {
//                 $(".droppy+.dropdown-menu").css('width', $(".droppy").outerWidth());
//             });
//         });
//     });
//     $("#revenue-slider").ionRangeSlider({
//         type: "double",
//         skin: "round",
//         prettify: function (n) {
//             return abbreviate_number(logify(n, ar_min, ar_max));
//         },
//         grid: true,
//         min: ar_min,
//         max: ar_max,
//         from: parseInt(arn),
//         to: parseInt(arx),
//         hide_min_max: true,
//         prefix: ""
//     });

//     $("#employee-slider").ionRangeSlider({
//         type: "double",
//         skin: "round",
//         prettify: function (n) {
//             return abbreviate_number(logify(n, em_min, em_max));
//         },
//         grid: true,
//         min: em_min,
//         max: em_max,
//         from: parseInt(empn),
//         to: parseInt(empx),
//         hide_min_max: true,
//         prefix: ""
//     });

//     $("#g-slider").ionRangeSlider({
//         type: "double",
//         skin: "round",
//         prettify: function (n) {
//             return abbreviate_number(n);
//         },
//         grid: true,
//         min: g_min,
//         max: g_max,
//         from: gn,
//         to: gx,
//         hide_min_max: true,
//         step: 1,
//         values: [0, 1, 2, 3, 4, 5, 6, 7, 8],
//         prefix: ""
//     });

//     var btnn = $("#filter-btn")
//     btnn.on("click", function(){
//         buffer = []
//         removal = []
//         var ids = ["#revenue-slider", "#employee-slider", "#g-slider"];
//         var keys = ["ar", "emp", "g"];
//         for (var i = 0; i < ids.length; i++){
//             var inp = $(ids[i]);
//             var data = inp.data('ionRangeSlider').result;
//             if (data.from != data.min){
//                 buffer.push({
//                     "key": keys[i] + "n",
//                     "value": logify(data.from, data.min, data.max)
//                 })
//             }
//             else{
//                 removal.push(keys[i] + "n")
//             }
//             if (data.to != data.max){
//                 buffer.push({
//                     "key": keys[i] + "x",
//                     "value": logify(data.to, data.min, data.max)
//                 })
//             }
//             else{
//                 removal.push(keys[i] + "x")
//             }
//         }
//         var curl = "{{request.get_full_path}}".split("amp;").join("")
//         for (var i = 0; i < removal.length; i++){
//             curl = removeParam(removal[i], curl)
//         }
//         for(var i = 0; i < buffer.length; i++){
//             curl = removeParam(buffer[i].key, curl)
//             if (curl.includes("?")){
//             curl = curl + "&" + buffer[i].key + "=" + buffer[i].value
//             }
//             else{
//             curl = curl + "?" + buffer[i].key + "=" + buffer[i].value
//             }
//         }
//         curl = removeParam("search", curl)
//         if (curl.includes("?")){
//             var args = curl.split("?")[1]
//         }
//         else{
//             var args = ""
//         }
//         var ni = $("#droppyi").attr("data-back")
//         var ns = $("#droppys").attr("data-back")
//         var mk = "/"
//         if (ni != ""){
//             mk += ni
//         }
//         mk += "--"
//         if (ns != ""){
//             mk += ns
//         }
//         ind = $("#searchhy").val()
//         if (args == ""){
//             if(ind == ""){
//                 curl = "/find" + mk
//             }
//             else{
//                 curl = "/find" + mk + "?"
//                 curl += "search=" + ind
//             }
//         }
//         else{
//             if (ind == ""){
//                 curl = "/find" + mk + "?" + args
//             }
//             else{
//                 curl = "/find" + mk + "?" + args
//                 curl += "&search=" + ind
//             }

//         }
//         window.location.href = removeParam("page", curl)

//     })
//     latch();
//     $(window).resize(function(){
//         latch();
//     })

//     var elems = document.getElementsByClassName("fix_urls");
//     for (var i = 0; i < elems.length; i++){
//         var ident = elems[i].getAttribute("data-identifier");
//         var href = elems[i].getAttribute("data-value");
//         elems[i].setAttribute("href", removeParam("page", insertParam(ident, encodeURIComponent(href))));
//     }

//     var elems = document.getElementsByClassName("fix_slug");
//     for (var i = 0; i < elems.length; i++){
//         var ident = elems[i].getAttribute("data-identifier");
//         var href = elems[i].getAttribute("data-value");
//         href = href.split("_").join(" ");
//         href = href.split(" ").join("-");
//         href = href.split("/").join("__");
//         if (ident != "state"){
//             href = href.toLowerCase();
//         }
//         elems[i].setAttribute("href", removeParam("page", insertSlug(ident, encodeURIComponent(href))));
//     }

//     var elems = document.getElementsByClassName("fix_underscore");
//     for (var i = 0; i < elems.length; i++){
//         var text = elems[i].innerHTML;
//         text = text.trim().split("_").join(" ").toLowerCase()
//         elems[i].innerHTML = text;
//     }

//     var elems = document.getElementsByClassName("fix_address");
//     for (var i = 0; i < elems.length; i++){
//         var text = elems[i].innerHTML;
//         text = text.trim()
//         if(text.startsWith(",")){text = text.substring(1);}
//         elems[i].innerHTML = text.replace(/\s+,/ ,',');
//     }

//     var elems = document.getElementsByClassName("on-click");
//     for (var i = 0; i < elems.length; i++){
//         elems[i].addEventListener("click", function(){
//             var attr = this.getAttribute("data-identifier");
//             if (attr == "industry" || attr == "state"){
//                 attr = removeParam("page", removeSlug(attr))
//                 window.location.href = attr
//             }
//             else{
//                 attr = removeParam("page", removeParam(attr, document.location.href));
//                 window.location.href = attr;
//             }
//         });
//     }
// }
// if (window.addEventListener) {
//       window.addEventListener('load', main);
//    } else if (window.attachEvent) {
//       window.attachEvent('onload', main);
//    } else {
//       window.onload = main;
//    }
