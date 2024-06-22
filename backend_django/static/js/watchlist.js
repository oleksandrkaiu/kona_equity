var loadingDiv = '<div id="load" class="row data-def mx-auto"><div style="color: #ffffff" class="la-ball-scale-pulse la-3x mx-auto my-auto"><div></div><div></div></div></div>'
var emptyDiv = '<div class="row mx-auto data-def">\
<div class="col-lg-6 col-md-8 col-sm-12 col-12 mx-auto my-auto">\
  <div class="upb" style="text-align: center; color: white; padding: 1.5% 5%;">\
    Feels a little empty in here...\
  </div>\
  <div class="lowb" style="text-align: center; color: white; padding: 1.5% 10%; padding-bottom: 3%;">\
    Stay up to date by adding some companies to this watchlist.\
  </div>\
  <a href="/find/" style="padding-top:3%;">\
    <div class="text-center mx-auto w-100">\
        <div class="wjuio lowb mx-auto my-auto itnk" style="position: relative; left: 0; bottom: 0;">Find Companies</div>\
    </div>\
  </a>\
</div>'


var reference = {
    "0": "nearby",
    "1": "saved",
    "2": "visited",
    "3": "study"
}

function peekify(){
    return $(document).width() * 0.25
}

function adjust(){
    if ($(document).width() < 768){
        $("#menu-select").css("display", "none")
        $("#intro").css("display", "block")
      }
      else{
        $("#menu-select").css("display", "block")
        $("#intro").css("display", "none")
      }
}