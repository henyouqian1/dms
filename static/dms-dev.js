$(document).ready(function(){
	$.getJSON('/dms/devislogin', function(json){
		if (json.login==1){
			gDeveloperId=json.developerid;
			gDeveloperEmail=json.developeremail;
			openMainMenuView();
		}else if (json.login==0){
			openLoginView();
		}
	});
});

function openLoginView(){
	if (typeof(gHTMLLoginView)=='undefined'){
		$.getJSON('/dms/devloginview', function(json){
			gHTMLLoginView = json.view;
			buildLoginView();
		});
	}else{
		buildLoginView();
	}
}

function buildLoginView(){
	var body=$('body');
	body.empty();
	body.append(gHTMLLoginView);
	
	$('button#login').click(function() {
		login();
	});
	$('button#register').click(function() {
		openRegisterView();
	});
	
	$('button').button();
}

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
				gDeveloperId=json.developerid;
				gDeveloperEmail=json.developeremail;
				openMainMenuView();
			}else{
				alert(json.error);
			}
		});
	}
}

function logout(){
	$.getJSON('/dms/devlogout', function(json){
		if (json.error==0){
			window.location.href='/dms/devview'
			delete gDeveloperId;
			delete gDeveloperEmail;
		}else{
			alert('logout failed');
		}
	});
}

function openRegisterView(){
	if (typeof(gHTMLRegisterView)=='undefined'){
		$.getJSON('/dms/devregisterview', function(json){
			gHTMLRegisterView = json.view;
			buildRegisterView();
		});
	}else{
		buildRegisterView();
	}
}

function buildRegisterView(){
	var body=$('body');
	body.empty();
	body.append(gHTMLRegisterView);
	
	$('button#register').click(function() {
		register();
	});
	$('button#cancel').click(function() {
		openLoginView();
	});
	
	$('button').button();
}

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
		$.getJSON('/dms/devregister', {email:email, password:pw1}, function(json){
			if (json.error==0){
				gDeveloperId=json.developerid;
				gDeveloperEmail=json.developeremail;
				openMainMenuView();
			}else{
				alert(json.error);
			}
		});
	}
}

function openMainMenuView(){
	if (typeof(gHTMLMainManuView)=='undefined'){
		$.getJSON('/dms/devmainmenuview', function(json){
			gHTMLMainManuView = json.view;
			buildMainMenuView();
		});
	}else{
		buildMainMenuView();
	}
}

function buildMainMenuView(){
	var body=$('body');
	body.empty();
	body.append(gHTMLMainManuView);
	var str="developer_id="+gDeveloperId+" developer_email="+gDeveloperEmail;
	$('p#userinfo').html(str);
	$('button#logout').click(function() {
		logout();
	});
	$('button#award').click(function() {
		openAwardView();
	});
	$('button').button();
}

function openAwardView(){
	if (typeof(gAwardPageIdx)=='undefined'){
		gAwardPageIdx=0;
		gAwardsPerPage=20;
	}
	if (typeof(gHTMLAwardView)=='undefined'){
		$.getJSON('/dms/devawardview', function(json){
			gHTMLAwardView = json.view;
			buildAwardView();
			gHTMLAddAwardView = json.addview;
			gHTMLEditAwardView = json.editview;
		});
	}else{
		buildAwardView();
	}
}

function buildAwardView(){
	var body=$('body');
	body.empty();
	body.append(gHTMLAwardView);
	
	$('button#back').click(function() {
		openMainMenuView();
	});
	$('button#add').click(function() {
		openAddAwardView();
	});
	
	getAwardPage(gAwardPageIdx, gAwardsPerPage)
	$('button').button();
}

function getAwardPage(page, num){
	$.getJSON('/dms/devgetawards', {page:gAwardPageIdx, num:gAwardsPerPage}, function(json){
		if (json.error==0){
			$('tr.datarow').remove();
			var str='';
			$(json.data).each(function(i){
				var obj = $(this)[0];
				str+='<tr class=datarow>';
				str+='<td><button class=edit idx='+obj.idx+'>edit</button></td>';
				str+='<td class=name>'+obj.name+'</td>';
				str+='<td class=desc>'+obj.desc+'</td>';
				str+='<td class=img>'+obj.img+'</td>';
				str+='</tr>';
			});
			$('table#d').append(str);
		}else{
			alert(json.error);
		}
		$('button').button();
		$('button.edit').click(function(){
			tds = $(this).parent().siblings('td');
			//console.info(tds.filter('.name'));
			openEditAwardView($(this).attr('idx'), tds.filter('.name').text(), tds.filter('.desc').text(), tds.filter('.img').text());
		});
	});
}

function openAddAwardView(){
	var body=$('body');
	body.empty();
	body.append(gHTMLAddAwardView);
	
	$('button#back').click(function() {
		openAwardView();
	});
	$('button#add').click(function() {
		addAward();
	});
	
	$('button').button();
};

function addAward(){
	name=$('input#name').attr('value');
	desc=$('input#desc').attr('value');
	img=$('input#img').attr('value');
	if ( name == '' ){
		alert('name == NULL');
	}else if ( desc == '' ){
		alert('description == NULL');
	}else if ( img == '' ){
		alert('image == NULL');
	}else{
		$.getJSON('/dms/devaddaward', {name:name, desc:desc, img:img}, function(json){
			if (json.error==0){
				openAwardView();
			}else{
				alert(json.error);
			}
		});
	}
}

function openEditAwardView(idx, name, desc, img){
	var body=$('body');
	body.empty();
	body.append(gHTMLEditAwardView);
	
	$('button#back').click(function() {
		openAwardView();
	});
	$('button#add').click(function() {
		editAward();
	});
	$('input#name').attr('value', name);
	$('input#desc').attr('value', desc);
	$('input#img').attr('value', img);
	gEditAwardIdx=idx;
	
	$('button#delete').click(function(){
		deleteAward();
	});
	
	$('button').button();
};

function editAward(){
	name=$('input#name').attr('value');
	desc=$('input#desc').attr('value');
	img=$('input#img').attr('value');
	if ( name == '' ){
		alert('name == NULL');
	}else if ( desc == '' ){
		alert('description == NULL');
	}else if ( img == '' ){
		alert('image == NULL');
	}else{
		$.getJSON('/dms/deveditaward', {id:gEditAwardIdx, name:name, desc:desc, img:img}, function(json){
			if (json.error==0){
				openAwardView();
			}else{
				alert(json.error);
			}
		});
	}
}

function deleteAward(){
	var $dialog = $('<div class=ui-dialog></div>')
		.html('This game will be permanently deleted and cannot be recovered. Are you sure?!')
		.dialog({
			title: 'Delete award',
			modal: true,
			buttons: {
				"Confirm": function() {
					$.getJSON('/dms/devdeleteaward', {id:gEditAwardIdx}, function(json){
						if (json.error==0){
							openAwardView();
						}else{
							alert(json.error);
						}
					});
					$( this ).dialog("close");
				},
				Cancel: function() {
					$( this ).dialog("close");
				}
			},
			close: function(ev, ui) { $(this).dialog('destroy').remove(); } 
		});
}