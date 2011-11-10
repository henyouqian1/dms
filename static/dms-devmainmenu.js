$(document).ready(function(){
	$('button#logout').click(function() {
		logout();
	});
	$('button#award').click(function() {
		awardView();
	});
	$('button').button().css('width','130px').css('height','30px');
});

function logout(){
	$.getJSON('/dms/devlogout', function(json){
		window.location.href=json.url;
	});
}

function awardView(){
	window.location.href='/dms/devawardview';
}

