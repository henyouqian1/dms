$(document).ready(function(){
	tryLogin();
});

function tryLogin(){
	$.getJSON('/dms/trylogin', function(json){
		if (json.login){
			window.location.href="/dms/mainmenuview";
		}else{
			loadLoginView();
		}
	});
}

function loadLoginView(){
	window.location.href="/dms/loginview";
}