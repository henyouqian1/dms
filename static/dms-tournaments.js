//tournaments
function requestTournaments(){
	$.getJSON('lsTournaments', function(d) {
		g_td = d;
		buildTable(d.th, d.trs);
		$('tr.head').prepend('<th><button class=addGame>Add</button></td></th>');
		$('tr.data').each(function(i){
			var tr = $(this);
			tr.prepend('<td><button class=editGame tabindex='+i+'>Edit</button></td>')
		});
		$('tr.head').children().eq(1).hide();
		$('tr.data').children().eq(1).hide();
		$('button.addGame').click(function(){
			buildTournamentPage();
			$('table#d').remove();
		});
		$('button.editGame').click(function(){
			buildTournamentPage();
			$('table#d').remove();
		});
		$('button').button();
	});
}

function buildTournamentPage(){
	var str='	<table class=form>\
			<caption>Tournaments</caption>\
				<tr>\
					<th>Title:</th>\
					<td><input id=title type=text /></td>\
				</tr>\
				<tr>\
					<th>Description:</th>\
					<td><textarea id=description cols=30 rows=20 /></td>\
				</tr>\
			</table>';
	$('div#d').append(str);
}