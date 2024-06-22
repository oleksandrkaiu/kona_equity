function setGlide(panel){
    var p = $(panel).find(".glide").attr("id")
    var glide = new Glide('#' + p, {
    type: 'carousel',
    perView: itemize(),
    });
    glide.mount()
    $(panel).find(".left-glide").click(function(){
        glide.go("<")
    });
    $(panel).find(".right-glide").click(function(){
        glide.go(">");
    });
}

function itemize(){
    var p;
    var width = $(document).width();
    if (width >= 1270){p=3}
    else if (width >= 661 && width <= 768){p=2}
    else if (width >= 992 && width <= 1270){p=2}
    else{p=1}
    console.log(p)
    return p;
}