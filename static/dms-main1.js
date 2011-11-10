$(document).ready(function(){
	$('button#games').click(function() {
		requestGameList();
	});
	$('button#tournaments').click(function() {
		requestTournaments();
	});
	$('button#matchs').click(function() {
		requestMatchs();
	});
	$('button#facebook').click(function() {
		window.location.href="https://www.facebook.com/dialog/oauth?client_id=239733542752050&redirect_uri=http://localhost:8001/dms/auth/fbauth&scope=email,read_stream";
	});
	
	$('button').button();
});

function buildTable(th, trs){
	$('div#d').empty();
	$('div#d').append("<table id=d></table>");
	var str='<tr class=head>';
	$(th).each(function(){
		str+='<th>'+this+'</th>'
	});
	str+='</tr>';
	$("table#d").append(str);
	$(trs).each(function(i){
		var str='<tr class=data>';
		$(this).each(function(){
			str+='<td>'+this+'</td>'
		});
		str+='</tr>';
		$("table#d").append(str);
	});
}
	
//matchs
function requestMatchs(){
	$.getJSON('lsMatchs', function(d) {
		g_td = d;
		buildTable(d.th, d.trs);
	});
}

