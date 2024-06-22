'use strict';

window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)',
    black: 'rgb(0,0,0)',
};

(function(global) {
	var MONTHS = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	var COLORS = [
		'#4dc9f6',
		'#f67019',
		'#f53794',
		'#537bc4',
		'#acc236',
		'#166a8f',
		'#00a950',
		'#58595b',
		'#8549ba'
	];

	var Samples = global.Samples || (global.Samples = {});
	var Color = global.Color;

	Samples.utils = {
		// Adapted from http://indiegamr.com/generate-repeatable-random-numbers-in-js/
		srand: function(seed) {
			this._seed = seed;
		},

		rand: function(min, max) {
			var seed = this._seed;
			min = min === undefined ? 0 : min;
			max = max === undefined ? 1 : max;
			this._seed = (seed * 9301 + 49297) % 233280;
			return min + (this._seed / 233280) * (max - min);
		},

		numbers: function(config) {
			var cfg = config || {};
			var min = cfg.min || 0;
			var max = cfg.max || 1;
			var from = cfg.from || [];
			var count = cfg.count || 8;
			var decimals = cfg.decimals || 8;
			var continuity = cfg.continuity || 1;
			var dfactor = Math.pow(10, decimals) || 0;
			var data = [];
			var i, value;

			for (i = 0; i < count; ++i) {
				value = (from[i] || 0) + this.rand(min, max);
				if (this.rand() <= continuity) {
					data.push(Math.round(dfactor * value) / dfactor);
				} else {
					data.push(null);
				}
			}

			return data;
		},

		labels: function(config) {
			var cfg = config || {};
			var min = cfg.min || 0;
			var max = cfg.max || 100;
			var count = cfg.count || 8;
			var step = (max - min) / count;
			var decimals = cfg.decimals || 8;
			var dfactor = Math.pow(10, decimals) || 0;
			var prefix = cfg.prefix || '';
			var values = [];
			var i;

			for (i = min; i < max; i += step) {
				values.push(prefix + Math.round(dfactor * i) / dfactor);
			}

			return values;
		},

		months: function(config) {
			var cfg = config || {};
			var count = cfg.count || 12;
			var section = cfg.section;
			var values = [];
			var i, value;

			for (i = 0; i < count; ++i) {
				value = MONTHS[Math.ceil(i) % 12];
				values.push(value.substring(0, section));
			}

			return values;
		},

		color: function(index) {
			return COLORS[index % COLORS.length];
		},

		transparentize: function(color, opacity) {
			var alpha = opacity === undefined ? 0.5 : 1 - opacity;
			return Color(color).alpha(alpha).rgbString();
		}
	};

	// DEPRECATED
	window.randomScalingFactor = function() {
		return Math.round(Samples.utils.rand(-100, 100));
	};

	// INITIALIZATION

	Samples.utils.srand(Date.now());

	// Google Analytics
	/* eslint-disable */
	if (document.location.hostname.match(/^(www\.)?chartjs\.org$/)) {
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
		ga('create', 'UA-28909194-3', 'auto');
		ga('send', 'pageview');
	}
	/* eslint-enable */

}(this));

function validato(){
	$(".check-blob").click(function(){
		$(this).toggleClass("checked");
		if ($(this).attr("fwd") == "false"){
			$(this).attr("fwd", "true")
		}
		else{
			$(this).attr("fwd", "false")
		}
    });
    $('[data-toggle="popover"]').popover();
    $("#some").trigger("click");
    $("#file-upload-button").click(function(){
      $("#id_profile_photo").trigger('click');
    });
	$('#id_profile_photo').on('change', handleFileSelect);
    $("#pwd1").on("click", function(e){
        e.preventDefault()
        var p = document.getElementById("id_password1")
        if (p.type == "password"){
            p.type = "text"
        }
        else if (p.type == "text"){
            p.type = "password"
        }
	});
	$("#pwd2").on("click", function(e){
        e.preventDefault()
        var p = document.getElementById("id_password2")
        if (p.type == "password"){
            p.type = "text"
        }
        else if (p.type == "text"){
            p.type = "password"
        }
	});
	$("#pwdy").on("click", function(e){
        e.preventDefault()
        var p = document.getElementById("id_passwordy")
        if (p.type == "password"){
            p.type = "text"
        }
        else if (p.type == "text"){
            p.type = "password"
        }
    });

    $("#pwdo").on("click", function(e){
        e.preventDefault()
        var p = document.getElementById("id_oldpassword")
        if (p.type == "password"){
            p.type = "text"
        }
        else if (p.type == "text"){
            p.type = "password"
        }
    });

    $(".capinames").blur(function(){
        var cap = $(this).siblings(".searchBDir");
        if($(this).val().length == 0){
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("wrong");
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This field is required")
            $(op).css("color", "#FF5A5F")
        }
        else{
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("correct");
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
    });
    $(".capinames").on("input", function(){
        var cap = $(this).siblings(".searchBDir");
        if ($(this).length > 0){
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("correct");
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
    });
    $("#id_email").blur(function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (/(.+)@(.+){2,}\.(.+){2,}/.test(val)){
            if (freeEmails.includes(val.split("@")[1])){
                $(cap).attr("class", "searchBDir");
                $(cap).addClass("wrong");
                $(this).css("border", "2px solid #FF5A5F")
                $("#email_errors").html("A business email is required.")
                $("#email_errors").css("color", "#FF5A5F")
            }
            else{
                $(cap).attr("class", "searchBDir");
                $(cap).addClass("correct");
                $(this).css("border", "2px solid #8CE071")
                $("#email_errors").html("")
            }

        }
        else if (val.length == 0){
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("wrong");
            $(this).css("border", "2px solid #FF5A5F")
            $("#email_errors").html("This is a required field")
            $("#email_errors").css("color", "#FF5A5F")
        }
        else{
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("wrong");
            $(this).css("border", "2px solid #FF5A5F")
            $("#email_errors").html("Please enter a valid email address.")
            $("#email_errors").css("color", "#FF5A5F")
        }
    });
    $("#id_email").on("input", function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (/(.+)@(.+){2,}\.(.+){2,}/.test(val)){
            if (freeEmails.includes(val.split("@")[1])){
                $(cap).attr("class", "searchBDir");
                $(cap).addClass("wrong");
                $(this).css("border", "2px solid #FF5A5F")
                $("#email_errors").html("A business email is required.")
                $("#email_errors").css("color", "#FF5A5F")
            }
            else{
                $(cap).attr("class", "searchBDir");
                $(cap).addClass("correct");
                $(this).css("border", "2px solid #8CE071")
                var op = $(this).parents(".form-group")[0]
                op = $(op).children("p")[0]
                $(op).html("")
            }
        }
	});
	$("#id_emaily").on("blur", function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (! /(.+)@(.+){2,}\.(.+){2,}/.test(val)){
            $(cap).attr("class", "searchBDir");
            $(cap).addClass("wrong");
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("Please enter a valid email address.")
            $(op).css("color", "#FF5A5F")
		}
		if (val.length == 0){
			$(cap).attr("class", "searchBDir");
            $(cap).addClass("wrong");
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This is a required field")
            $(op).css("color", "#FF5A5F")
		}
	});
	$("#id_emaily").on("input", function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (/(.+)@(.+){2,}\.(.+){2,}/.test(val) && val.length > 0){
            $(cap).attr("class", "searchBDir");
            $(this).css("border", "1px solid rgba(56, 56, 56, 0.5)")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
			$(op).html("")
		}
	});
	$("#id_passwordy").on("input", function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (val.length > 0){
            $(this).css("border", "1px solid rgba(56, 56, 56, 0.5)")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
			$(op).html("")
		}
	});
	$("#id_passwordy").blur(function(){
        var val = $(this).val()
        if (val.length == 0){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This is a required field")
            $(op).css("color", "#FF5A5F")
        }
    });
    $("#id_oldpassword").on("input", function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        if (val.length > 0){
            $(this).css("border", "1px solid rgba(56, 56, 56, 0.5)")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
			$(op).html("")
		}
	});
	$("#id_oldpassword").blur(function(){
        var val = $(this).val()
        if (val.length == 0){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This is a required field")
            $(op).css("color", "#FF5A5F")
        }
    });
    $("#id_password1").blur(function(){
        var val = $(this).val()
        if (val.length == 0){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This is a required field")
            $(op).css("color", "#FF5A5F")
        }
        else if (val.length < 8){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("8 or more characters are required.")
            $(op).css("color", "#FF5A5F")
        }
        else{
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
    });
    $("#id_password1").on("input", function(){
        var val = $(this).val()
        if (val.length >= 8){
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
    });
    $("#id_password2").on("input", function(){
        var val = $(this).val()
        var val1 = $("#id_password1").val()
        if (val.length > 0 && val == val1){
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
    });
    $("#id_password2").blur(function(){
        var cap = $(this).siblings(".searchBDir");
        var val = $(this).val()
        var val1 = $("#id_password1").val()
        if (val.length == 0){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("This is a required field")
            $(op).css("color", "#FF5A5F")
        }
        else if (val != val1){
            $(this).css("border", "2px solid #FF5A5F")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("Passwords do not match.")
            $(op).css("color", "#FF5A5F")
        }
        else{
            $(this).css("border", "2px solid #8CE071")
            var op = $(this).parents(".form-group")[0]
            op = $(op).children("p")[0]
            $(op).html("")
        }
	});
	var timer;
	$("#signup_form input").on("input", function(){
		clearTimeout(timer);
		var ms = 200;
		timer = setTimeout(function() {
			if(signupValidate()){
				$("#disabled").addClass("enableCont");
			}
			else{
				$("#disabled").removeClass("enableCont");
			}
		}, ms);
	})
	$("#agreement").click(function(){
		if(signupValidate()){
			$("#disabled").addClass("enableCont");
		}
		else{
			$("#disabled").removeClass("enableCont")
		}
	});

	var kimer;
	$("#login_form input").on("input", function(){
		clearTimeout(kimer);
		var ms = 200;
		kimer = setTimeout(function() {
			if(loginValidate()){
				$("#disabledl").addClass("enableCont");
			}
			else{
				$("#disabledl").removeClass("enableCont");
			}
		}, ms);
	});
}

function Validate(oInput) {
    var _validFileExtensions = [".jpg", ".jpeg", ".bmp", ".webp", ".png"];
    if (oInput.type == "file") {
        var sFileName = oInput.value;
        if (sFileName.length > 0) {
            var blnValid = false;
            for (var j = 0; j < _validFileExtensions.length; j++) {
                var sCurExtension = _validFileExtensions[j];
                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                    blnValid = true;
                    break;
                }
            }
            if (!blnValid) {
                var k = $("#profile-picture")
                k.attr("data-original-title", "Loading Error")
                k.attr("data-content", "Invalid file extension. Allowed extensions are: " + _validFileExtensions.join(", "))
                $("#profile-picture").popover("show")
                return false;
            }
        }
    }
    if (oInput.files.length > 0) {
        for (var i = 0; i <= oInput.files.length - 1; i++) {
            var fsize = oInput.files.item(i).size;
            var file = Math.round((fsize / 1024));
            if (file >= 4096) {
                var k = $("#profile-picture")
                k.attr("data-original-title", "Loading Error")
                k.attr("data-content", "File size should not exceed 2 MB. Please try agian with a smaller size.")
                $("#profile-picture").popover("show")
                return false;
            }
        }
    }
    $("#profile-picture").popover("hide")
    return true;
}

function signupValidate(){
	var val = $("#id_password1").val()
	var valemail = $("#id_email").val()
	if ($("#id_first_name").val().length > 0
		&& $("#id_last_name").val().length > 0
		&& /(.+)@(.+){2,}\.(.+){2,}/.test(valemail)
		&& valemail.length > 0
		&& val.length >=8
		&& !freeEmails.includes(valemail.split("@")[1])
		&& $("#id_password2").val() == val
		&& $("#agreement").attr("fwd") == "true"
		&& Validate(document.getElementById("id_profile_photo"))){
			return true;

		}
	else{
		return false;
	}
}

function loginValidate(){
	var valemail = $("#id_emaily").val()
	if (/(.+)@(.+){2,}\.(.+){2,}/.test(valemail)
	&& valemail.length > 0
	&& $("#id_passwordy").val().length > 0){
		return true
	}
	else{
		return false
	}
}

function dropys(){
	$("#profile-disp").click(function(e){
        e.stopPropagation()
        $("#profile-menu").css("display", "block")
    });
    $(document).on("click", function(event){
        var n = $("#profile-menu").css("display");
        if (n == "block"){
            $("#profile-menu").css("display", "none")
        }
    });
    $(".dropdown").click(function(e){
        e.stopPropagation()
        $(this).find(".dropdown-content").css("display", "block");
    });
    $(document).on("click", function(event){
        var n = $(".dropdown-content").css("display");
        if (n == "block"){
            $(".dropdown-content").css("display", "none")
        }
    });
    $(".dropdown").hover(function(){
        $(this).find(".dropdown-content").css("display", "block");
    },function(){
        $(this).find(".dropdown-content").css("display", "none");
    });
}

function passValidate(){
    var p1 = $("#id_password1").val();
    var p2 = $("#id_password2").val();
    if (p2 != "" && p1 != "" && p2 == p1 && $("#id_oldpassword").val() != ""){
        return true
    }
    return false
}

function checkSome(){
    $('#disabled').on('click', function(event){
        if (signupValidate()){
            create_post();
        }
        });
    $('#disabledl').on('click', function(event){
    if (loginValidate()){
        login_post();
    }
    });
}

function openSome(){
    try{
        $("#signup_form")[0].reset();
        $("#login_form")[0].reset();
    }
    catch(e){
    }
    $("#gotoin").click(function(){
        $("#SignupModal").modal("hide");
        $("#LoginModal").modal("show");
    });
    $("#gotoup").click(function(){
        $("#LoginModal").modal("hide");
        $("#SignupModal").modal("show");
    });
}

function logmeout(){
    $("#logmeout").click(function(){
        $("#logout").submit();
    });
}

function logmeout(){
    $("#logmeout").click(function(){
        $("#logout").submit();
    });
}

function mobileSignup(){
    $("#hidden-login").click(function(){
        $("#LoginModal").modal("show");
    });
    $("#hidden-signup").click(function(){
        $("#SignupModal").modal("show");
    });
}
