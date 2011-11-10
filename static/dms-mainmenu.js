$(document).ready(function(){
	$('button#logout').click(function() {
		logout();
	});
	$('button').button().css('width','130px').css('height','30px');
});

function logout(){
	$.getJSON('/dms/logout', function(json){
		window.location.href=json.url;
	});
}