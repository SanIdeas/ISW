$('.news form').submit(function(e){
	e.preventDefault();
	sendData($(this).attr('action'), $(this).attr('redirect-to'));
});
function sendData(url, redirect_to){
	blockFormAndShowLoading();

	var formElement = $('.news form')[0];
	var formStatus = formElement.checkValidity();
	if(!formStatus){
		showError();
		return
	}
	// Se verifica que se haya adjuntado una miniatura
	if($('#thumbnailPicture').attr('src') == ""){
		showError();
		unlockFormAndHideLoading();
		return;
	}
	// Se almacenan los datos que se enviaran al servidor
	var form = new FormData(formElement);
	if($('#thumbnailPicture').attr('new'))
		form.append('thumbnail', convertDataURIToBinary($('#thumbnailPicture').attr('src')));
	if($('#headerPicture').attr('src') != "" && $('#headerPicture').attr('new')){
		form.append('header', convertDataURIToBinary($('#headerPicture').attr('src')));
	}

	$.ajax({
		url: url,
		method: "POST",
		data: form,
		processData: false,
		contentType: false
	}).done(function(response){
		if(!response['error']){
			if(redirect_to == 'live-editor')
				window.location.href = live_editor_url.replace('888', response['id']);
			if(redirect_to == 'reload')
				location.reload();
			if(redirect_to == 'news-intranet')
				window.location.href = news_url;
		}
		else{

			showError();
			unlockFormAndHideLoading();
		}
	}).error(function(){
		showError();
		unlockFormAndHideLoading();
	});
}

function showError(){
	$.fancybox($('#errorModal').parent('div').html(), {
		closebtn: false,
		autoSize: false,
		width: 400,
		height: 100,
		scrolling: false,
		closeBtn: false,
	});
}

function blockFormAndShowLoading(){
	// Se desactivan los campos y botones
	$('.news form input[type="text"], .news form textarea').attr('readonly', true);
	$('.news form input[type="submit"]').attr('disabled', true);
	busy = true;
	$.fancybox.showLoading();
}

function unlockFormAndHideLoading(){
	// Se desactivan los campos y botones
	$('.news form input, .news form textarea').each(function(){
		if(!($(this).attr('name') == 'mini-description' && $('#headerPicture').attr('src') == ""))
			$(this).attr('readonly', false);
	});
	$('.news form input[type="submit"]').attr('disabled', false);
	busy = false;
	$.fancybox.hideLoading();
}

function convertDataURIToBinary(dataURI) {
	// convert base64 to raw binary data held in a string
    // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
    var byteString = atob(dataURI.split(',')[1]);
    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to an ArrayBuffer
    var ab = new ArrayBuffer(byteString.length);
    var dw = new DataView(ab);
    for(var i = 0; i < byteString.length; i++) {
        dw.setUint8(i, byteString.charCodeAt(i));
    }
    // write the ArrayBuffer to a blob, and you're done
    return new Blob([ab], {type: mimeString});
}