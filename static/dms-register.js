$(document).ready(function(){
	$('button#register').click(function() {
		register();
	});
	$('button#cancel').click(function() {
		window.location.href="/dms/loginview";
	});
	$('button').button();
	$('button').button().css('width','130px').css('height','30px');
});

function register(){
	email=$('input#email').attr('value');
	pw1=$('input#pw1').attr('value');
	pw2=$('input#pw2').attr('value');
	if ( email == '' ){
		alert('email == NULL');
	}else if ( pw1 != pw2 ){
		alert('pw1 != pw2');
	}else if ( pw1 == '' ){
		alert('pw1 == NULL');
	}else{
		$.getJSON('/dms/register', {email:email, password:pw1}, function(json){
			if (json.error==0){
				window.location.href="/dms/mainmenuview";
			}else{
				alert(json.error);
			}
		});
	}
}