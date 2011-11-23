$(document).ready(function(){
	$.getJSON('/dms/userislogin', function(json){
		if (json.login==1){
			openMainMenuView();
			gUserId=json.userid;
			gUserEmail=json.useremail;
		}else if (json.login==0){
			openLoginView();
		}
	});
});

function openLoginView(){
	if (typeof(gHTMLLoginView)=='undefined'){
		$.getJSON('/dms/userloginview', function(json){
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
	$('button#facebook').click(function() {
		//window.location.href="https://www.facebook.com/dialog/oauth?client_id=239733542752050&redirect_uri=http://"+window.location.hostname+"/dms/userfblogin&scope=email,read_stream";
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
		$.getJSON('/dms/userlogin', {email:email, password:pw}, function(json){
			if (json.error==0){
				gUserId=json.userid;
				gUserEmail=json.useremail;
				openMainMenuView();
			}else{
				alert(json.error);
			}
		});
	}
}

function logout(){
	$.getJSON('/dms/userlogout', function(json){
		if (json.error==0){
			window.location.href='/dms/userview';
			delete gUserId;
			delete gUserEmail;
		}else{
			alert('logout failed');
		}
	});
}

function openRegisterView(){
	if (typeof(gHTMLRegisterView)=='undefined'){
		$.getJSON('/dms/userregisterview', function(json){
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
		$.getJSON('/dms/userregister', {email:email, password:pw1}, function(json){
			if (json.error==0){
				gUserId=json.userid;
				gUserEmail=json.useremail;
				openMainMenuView();
			}else{
				alert(json.error);
			}
		});
	}
}

function openMainMenuView(){
	if (typeof(gHTMLMainManuView)=='undefined'){
		$.getJSON('/dms/usermainmenuview', function(json){
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
	var str="user_id="+gUserId+" user_email="+gUserEmail;
	$('p#userinfo').html(str);
	$('button#logout').click(function() {
		logout();
	});
	$('button').button();
}









