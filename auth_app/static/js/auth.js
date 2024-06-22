// --------------- 3rd party idp information --------------- //
// var base_url = "http://localhost:8000/";
// var base_url = "https://konaequity2.pythonanywhere.com/";
var base_url = "https://www.konaequity.com/";

var google_client_id = "654052632789-04mk6slmqqhg5cnfcmabi7fg8443du3m.apps.googleusercontent.com";
var google_signup_url = "https://accounts.google.com/o/oauth2/v2/auth?client_id=" +
						google_client_id +
						"&response_type=code&scope=openid email profile" +
						"&redirect_uri=" + base_url + "signup/register_google_user" +
						"&state=1";
var google_login_url = "https://accounts.google.com/o/oauth2/v2/auth?client_id=" +
						google_client_id +
						"&response_type=code&scope=openid email profile" +
						"&redirect_uri=" + base_url + "login_google_user" +
						"&state=1";


function onclick_signup_bygoogle() {
    window.location.href=google_signup_url;
}
function onclick_login_bygoogle(){
	window.location.href=google_login_url;
}
function onclick_login() {
    window.location.href = '/login';
}
function onclick_signup() {
    window.location.href = '/signup/cold-join';
}
function validate_email(n) {
	var res = false;
	if (n.length < 1){
		return res;
	}
	if (/(.+)@(.+){2,}\.(.+){2,}/.test(n) && !freeEmails.includes(n.split("@")[1]) && "" == !n.split("@")[1]) {
		res = true;
	}
	return res;
}