$(document).ready(function(){
	$('button#login').click(function() {
		login();
	});
	$('button#register').click(function() {
		window.location.href='/dms/devregisterview'
	});
	$('button#facebook').click(function() {
		window.location.href="https://www.facebook.com/dialog/oauth?client_id=239733542752050&redirect_uri=http://"+window.location.hostname+"/dms/fblogin&scope=email,read_stream";
	});
	$('button').button().css('width','130px').css('height','30px');
});

function login(){
	email=$('input#email').attr('value');
	pw=$('input#pw').attr('value');
	if ( email == '' ){
		alert('email == NULL');
	}else if ( pw == '' ){
		alert('pw == NULL');
	}else{
		$.getJSON('/dms/devlogin', {email:email, password:pw}, function(json){
			if (json.error==0){
				window.location.href="/dms/devmainmenuview";
			}else{
				alert(json.error);
			}
		});
	}
}