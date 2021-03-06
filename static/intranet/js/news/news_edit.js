$(document).ready(function() {
	$('input.text, input.date').each(function() {
		$(this).attr('original', $(this).val())
	});
	$('input.text, input.date').on('input', function(){
		 checkFields();
	});
	$('.image').on('load', function(){
		 checkFields();
	});
	$('input[type="submit"].editor-link').click(function(e){
		e.preventDefault();
		// Si el formulario no tiene cambios
		if($('input[type="submit"].news').attr('disabled')){
			window.location.href = live_editor_url.replace('888', id);
		}
		else{
			$('.news form').attr('redirect-to', 'live-editor')
			$('input[type="submit"].news').click();
		}
	});
});

function checkFields() {
	var changed = false;
	$('input.text, input.date').each(function() {
		if($(this).val() != $(this).attr('original')) {
			changed = true;
		}
	});
	$('.image').each(function(){
		if($(this).attr('new')){
			changed = true;
		}
	});
	var formElement = $('.news form')[0];
	var formStatus = formElement.checkValidity();
	if(!formStatus){
		changed = false;
	}
	if(changed)
		$('input[type="submit"].news').attr('disabled', false);
	else
		$('input[type="submit"].news').attr('disabled', true);
}