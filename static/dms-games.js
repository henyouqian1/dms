//games
function requestGameList(){
	$.getJSON('lsGames', function(d) {
		g_td = d;
		buildTable(d.th, d.trs);
		$('tr.head').prepend('<th><button class=addGame>Add</button></td></th>');
		$('tr.data').each(function(i){
			var tr = $(this);
			tr.prepend('<td><button class=editGame tabindex='+i+'>Edit</button></td>')
			var str = '<input type=checkbox disabled=disabled value=1 ';
			if (d.trs[i][2]!=0){
				str+='checked=checked ';
			}
			str+='/>';
			tr.children('td').eq(2).html(str);
		});
		$('button.addGame').click(function(){
			buildAddOrEditGamePage(-1);
		});
		$('button.editGame').click(function(){
			buildAddOrEditGamePage($(this).attr('tabindex'));
		});
		$('button').button();
	});
}

function buildAddOrEditGamePage(row){
	var isEdit=row>=0?true:false;
	var t='Add';
	if (isEdit){
		t='Edit';
	}
	var str='	<table class=form>\
				<caption>'+t+' Game</caption>\
					<tr>\
						<th>name:</th>\
						<td><input id=name type=text /></td>\
					</tr>\
					<tr>\
						<th>score_small_better:</th>\
						<td><input type=checkbox id=big_is_better value=1 /></td>\
					</tr>\
				</table>'
	if (isEdit){
		str+='<div><button id=ok>ok</button><button id=delete>delete</button><button id=cancel>cancel</button><div>'
	}else{
		str+='<div><button id=ok>ok</button><button id=cancel>cancel</button><div>'
	}
	$('div#d').append(str);
	var nameElem=$('#name');
	var bibElem=$('#big_is_better');
	if (isEdit){
		nameElem.attr('value', g_td.trs[row][1]);
		if (g_td.trs[row][2]!=0){
			bibElem.attr('checked', 'checked');
		}
	}
	$('button#ok').click(function(){
		var name=nameElem.attr('value');
		var scoreSmallBetter=bibElem.get(0).checked?1:0;
		if (isEdit){
			requestEditGame(g_td.trs[row][0], name, scoreSmallBetter);
		}else{
			requestAddGame(name, scoreSmallBetter);
		}
	});
	$('button#cancel').click(function(){
		requestGameList();
	});
	if (isEdit){
		$('button#delete').click(function(){
			var $dialog = $('<div class=ui-dialog></div>')
				.html('This game will be permanently deleted and cannot be recovered. Are you sure?!')
				.dialog({
					title: 'Delete game',
					modal: true,
					buttons: {
						"Confirm": function() {
							requestDelGame(g_td.trs[row][0]);
							$( this ).dialog("close");
						},
						Cancel: function() {
							$( this ).dialog("close");
						}
					},
					close: function(ev, ui) { $(this).dialog('destroy').remove(); } 
				});
		});
	}
	$('table#d').remove();
	$('button').button();
	
	
}

function requestAddGame(name, scoreSmallBetter){
	$.getJSON('addGame', {name:name, scoreSmallBetter:scoreSmallBetter}, function(){
		requestGameList();
	});
}

function requestEditGame(id, name, scoreSmallBetter){
	$.getJSON('editGame', {id:id, name:name, scoreSmallBetter:scoreSmallBetter}, function(){
		requestGameList();
	});
}

function requestDelGame(id){
	$.getJSON('delGame', {id:id}, function(){
		requestGameList();
	});
}

