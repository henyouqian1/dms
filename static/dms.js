function buildTable(th, trs){
	$('div#d').empty();
	$('div#d').append("<table></table>");
	var str='<tr class=head>';
	$(th).each(function(){
		str+='<th>'+this+'</th>'
	});
	str+='</tr>';
	$("#d table").append(str);
	$(trs).each(function(i){
		var str='<tr class=data>';
		$(this).each(function(){
			str+='<td>'+this+'</td>'
		});
		str+='</tr>';
		$("#d table").append(str);
	});
}

function requestAddGame(name, bigIsBetter){
	$.getJSON('addGame', {name:name, bigIsBetter:bigIsBetter}, function(){
		requestGameList();
	});
}

function requestEditGame(id, name, bigIsBetter){
	$.getJSON('editGame', {id:id, name:name, bigIsBetter:bigIsBetter}, function(){
		requestGameList();
	});
}

function requestDelGame(id){
	$.getJSON('delGame', {id:id}, function(){
		requestGameList();
	});
}

function buildAddOrEditGamePage(row){
	var isEdit=row>=0?true:false;
	var t='Add';
	if (isEdit){
		t='Edit';
	}
	var str='<h2>'+t+' Game</h2><div><span>name</span><input id=name class=textfield /><div>';
	str+='<div><span>big_is_better</span><input type=checkbox id=big_is_better /><div>'
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
		bibElem.attr('value', 1);
	}	
	$('button#ok').click(function(){
		var name=nameElem.attr('value');
		var bigIsBetter=1;
		if (isEdit){
			requestEditGame(g_td.trs[row][0], name, bigIsBetter);
		}else{
			requestAddGame(name, bigIsBetter);
		}
	});
	$('button#cancel').click(function(){
		requestGameList();
	});
	if (isEdit){
		$('button#delete').click(function(){
			requestDelGame(g_td.trs[row][0]);
		});
	}
	$('div#d table').remove();
}

function requestGameList(){
	$.getJSON('lsGames', function(d) {
		g_td = d;
		buildTable(d.th, d.trs);
		$('tr.head').append('<th><button class=addGame>Add</button></td></th>');
		$('tr.data').each(function(i){
			var tr = $(this);
			tr.append('<td><button class=editGame tabindex='+i+'>Edit</button></td>')
			tr.children('td').eq(2).html('<input type=checkbox />');
		});
		$('button.addGame').click(function(){
			buildAddOrEditGamePage(-1);
		});
		$('button.editGame').click(function(){
			buildAddOrEditGamePage($(this).attr('tabindex'));
		});
	});
}

$(document).ready(function(){
	$('a#games').click(function() {
		requestGameList();
	});
});