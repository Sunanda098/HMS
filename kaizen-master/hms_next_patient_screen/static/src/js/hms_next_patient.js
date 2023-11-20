$(document).ready(function(){
    var cookie_var = $(".cookie").text()
    $( ".cookie" ).each(function( index ) {
	  if($( this ).text() != '0'){
	  	if(!$.cookie($( this ).text())){
	  		$.cookie($( this ).text(), 1);
	  		if($.cookie($( this ).text()) == 1)
	  			$( ".media[data-id="+ $( this ).text() +"]").css("background-color", "red");
	  	}
	  	else{
	  		$.cookie($( this ).text(), 2);
	  	}
	  }
	});
    console.log(cookie_var, ">>>>>>>>>>>>>>>>>>>>>>", $.cookie());
});