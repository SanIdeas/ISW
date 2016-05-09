var monthNames = ["Ene.", "Feb.", "Mar.", "Abr.", "May", "Jun.", "Jul.", "Ago.", "Sep.", "Oct.", "No.v", "Dec."];
(function($){
	//Resetea el input de archivo
	$.fn.resetInput = function(){
		this.wrap('<form>').closest('form').get(0).reset();
		this.unwrap();
	};
})(jQuery);

//Para formatear Bytes a diferentes unidades.
//http://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript
function formatSizeUnits(bytes){
        if      (bytes>=1000000000) {bytes=(bytes/1000000000).toFixed(2)+' GB';}
        else if (bytes>=1000000)    {bytes=(bytes/1000000).toFixed(2)+' MB';}
        else if (bytes>=1000)       {bytes=(bytes/1000).toFixed(2)+' KB';}
        else if (bytes>1)           {bytes=bytes+' bytes';}
        else if (bytes==1)          {bytes=bytes+' byte';}
        else                        {bytes='0 byte';}
        return bytes;
}


/*Metodos para eliminar elementos*/
Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}



function convertDataURIToBinary(dataURI) {
	var BASE64_MARKER = ';base64,';
	var base64Index = dataURI.indexOf(BASE64_MARKER) + BASE64_MARKER.length;
	var base64 = dataURI.substring(base64Index);
	var raw = window.atob(base64);
	var rawLength = raw.length;
	var array = new Uint8Array(new ArrayBuffer(rawLength));

	for(var i = 0; i < rawLength; i++) {
	array[i] = raw.charCodeAt(i);
	}
	return array;
}

function replaceValues(object){
	console.log(object);
	if(object['Author'].length > 0){
		var input = $('#author');

		input.val(object['Author']);
		input.prop('readOnly', true);
		input.addClass('read-only');
	}
	else{
		input.val('');
		input.prop('readOnly', false);
		input.removeClass('read-only');
	}
	if(object['Title'].length > 0){
		var input = $('#title');

		input.val(object['Title']);
		input.prop('readOnly', true);
		input.addClass('read-only');
	}
	else{
		input.val('');
		input.prop('readOnly', false);
		input.removeClass('read-only');
	}
	if(object['CreationDate'].length > 0){
		var input = $('#date');
		var year = object["CreationDate"].substr(2, 4);
		var month = object["CreationDate"].substr(6, 2);
		var day = object["CreationDate"].substr(8, 2);
		var date = year + '-' + month + '-' + day;

		input.val(date);
		input.prop('readOnly', true);
		input.addClass('read-only');
	}
	else{
		input.val('');
		input.prop('readOnly', false);
		input.removeClass('read-only');
	}
}

function getMeta(index, filename, file){
	var reader  = new FileReader();
				
	reader.addEventListener("load", function () {
		PDFJS.getDocument(convertDataURIToBinary(reader.result)).then(function (pdfDoc_) {
		    pdfDoc = pdfDoc_;   
		    pdfDoc.getMetadata().then(function(stuff) {
		        //console.log(stuff); // Metadata object here
		        return addDocument(index, filename, stuff['info']);
		    }).catch(function(err) {
		       console.log('Error getting meta data');
		       console.log(err);
		    });

		   // Render the first page or whatever here
		   // More code . . . 
		}).catch(function(err) {
		    console.log('Error getting PDF from ' + url);
		    console.log(err);
		});
	}, false);

	reader.readAsDataURL(file);
}

function methodSwitcher(method){
	if(method == 'local'){
		$('.upload-body[upload-method="local"]').css('display', 'block');
		$('.upload-body[upload-method="drive"]').css('display', 'none');
	}
	else{
		$('.upload-body[upload-method="local"]').css('display', 'none');
		$('.upload-body[upload-method="drive"]').css('display', 'block');
	}
}

function addDocument(index, filename, object){
	var code = ['<div class="document-frame" doc-index="$index">',
					'<div class="frame-header" doc-index="$index">',
						'<h5 class="frame-title">$filename</h5>',
						'<button class="close-btn"><i class="fa fa-times" aria-hidden="true"></i></button>',
						'<select class="type-select" name="type" doc-index="$index" required>',
							'<option value="" disabled selected>Selecciona privacidad</option>',
							'<option value="0">Publico</option>',
							'<option value="1">Privado</option>',
						'</select>',
						'<div class="clear"></div>',
					'</div>',
					'<ul class="frame-data">',
						'<li><strong>Titulo:</strong> <input type="text" value="$title" placeholder="Ej: Tesis de microbiologia"></li>',
						'<li><strong>Autor:</strong> <input type="text" value="$author" placeholder="Ej: Hernán Herreros"></li>',
						'<li><strong>Año:</strong> <input type="text" value="$year" placeholder="Ej: 2016"></li>',
						'<li><strong>Colaboradores:</strong> <input type="text"></li>',
						'<li><strong>Area:</strong> <input type="text"></li>',
					'</ul>',
				'</div>'].join('').replace(/\$index/g, index).replace(/\$filename/g, filename).replace(/\$title/g, object['Title'] ? object['Title']:'').replace(/\$author/g, object['Author'] ? object['Author']:'').replace(/\$year/g, (object['CreationDate'] ? object['CreationDate']:'').substr(2, 4));
	$('.upload-body[upload-method="local"]').append(code);

	$('.type-select').change(function(){
				if($(this).val() == "0")
					$('.frame-header[doc-index="' + $(this).attr('doc-index') + '"]').addClass('public-type').removeClass('private-type');
				else
					$('.frame-header[doc-index="' + $(this).attr('doc-index') + '"]').addClass('private-type').removeClass('public-type');
			});

}

function filesHandler(){
	var new_files = document.getElementById('mult-files').files;
	var files_names = [];
	for(var i = 0; i < files.length; i++){
		files_names.push(files[i].name);
	}

	for (var i = 0; i < new_files.length; i++){
		if (files_names.indexOf(new_files[i].name) < 0){
			files.push(new_files[i]);
			getMeta(files.length, new_files[i].name, new_files[i]);
			console.log(files.length);
		}
	}
}


//http://stackoverflow.com/questions/4068373/center-a-popup-window-on-screen
function PopupCenter(url, title, w, h, autoSearch) {
    // Fixes dual-screen position                         Most browsers      Firefox
    var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
    var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;
    
    var left = (window.top.outerWidth -  w )/2 +dualScreenLeft;
    var top = window.top.outerHeight / 2 + window.top.screenY - ( h / 2) + dualScreenTop;
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

    // Puts focus on the newWindow
    if (window.focus) {
        newWindow.focus();
    }

    if (autoSearch){
    	var timer = setInterval(function(){
    		if(newWindow.closed){
    			clearInterval(timer);
    			initial_drive_request(link_analizer_link.replace('999', encodeURIComponent($('#drive-link').val())));
    		}
    	}, 500);
    }


}


function initial_drive_request(link){
	if (link == '/drive/analizer//'){
		alternator('#error-message', 'Debes añadir un enlace de Google Drive a la solicitud');
		/*if(!$('.folder-wrapper').hasClass('hidden'))$('.folder-wrapper').addClass('hidden');
		if($('#error-message').hasClass('hidden'))$('#error-message').removeClass('hidden');
		$('#error-message').text('Debes añadir un enlace de Google Drive a la solicitud');*/
	}
	else{
		$('#spinner-wrapper').removeClass('hidden');
		xhr = new XMLHttpRequest;
		xhr.open('GET', link, true);
		xhr.onload =function(){
			response = JSON.parse(xhr.responseText);
			console.log(response);
			if (xhr.readyState == 4 && xhr.status == 200 && !response['error']) {
				if (response['type'] == 'Folder')
					create_drive_table(response);
				else if(response['type'] == 'PDF Document')
					create_drive_document(response);
			}
			else if ((response['error'])){
				$('#spinner-wrapper').removeClass('hidden');
				alternator('#error-message', JSON.parse(xhr.responseText)['message']);
				if  (JSON.parse(xhr.responseText)['code'] == 'gglir')
					PopupCenter(get_credentials_link, 'Iniciar sesion en Google Drive', 650, 700, true);
				/*if(!$('.folder-wrapper').hasClass('hidden'))$('.folder-wrapper').addClass('hidden');
				if($('#error-message').hasClass('hidden'))$('#error-message').removeClass('hidden');
				$('#error-message').text(JSON.parse(xhr.responseText)['message']);*/
			}
			$('#spinner-wrapper').addClass('hidden');
		};
		xhr.onprogress = function(e) {
		    if (e.lengthComputable) {
		        console.log(e.total);
		        console.log(e.loaded);
		    }
		};
		xhr.onloadstart = function(e) {
		    console.log(0);
		};
		xhr.onloadend = function(e) {
		    console.log(e.loaded);
		};
		xhr.send();
	}
}


function create_drive_table(response){
	$('.folder-row').remove();
	var files = response['files'];
	if (files.length > 0){
		var code = ['<tr class="folder-row">',
						'<td><input class="checkbox" type="checkbox" name="id" value="$id"></td>',
						'<td>$filename</td>',
						'<td>$owner</td>',
						'<td>$date</td>',
						'<td>$fileSize</td>',
					'</tr>',]
		$('#drive-title').text(response['folder_name']);
		var body = $('#folder-body');

		for(var i = 0; i < files.length; i++){			
			body.append(code.join('').replace(/\$filename/g, files[i]['title']).replace(/\$owner/g, files[i]['ownerNames']).replace(/\$date/g, format_date(files[i]['modifiedDate'])).replace(/\$fileSize/g, formatSizeUnits(parseInt(files[i]['fileSize']))).replace(/\$id/g, files[i]['id']));
		}

		$('.main-checkbox').click(function(){
			console.log(this.checked);
			if (this.checked){
				$('.checkbox').prop('checked', true);
			}
			else{
				$('.checkbox').prop('checked', false);
			}
		});

		$('.checkbox').click(function(){
			$('.main-checkbox').prop('indeterminate', true);
		});

		alternator('#folder-table', null);
		/*$('.folder-wrapper').removeClass('hidden');
		if(!$('#error-mesage').hasClass('hidden'))$('#error-message').addClass('hidden');*/
	}
	else{
		alternator('#error-message', 'No se encontraron archivos compatibles en el enlace')
		/*if(!$('.folder-wrapper').hasClass('hidden'))$('.folder-wrapper').addClass('hidden');
		if($('#error-message').hasClass('hidden'))$('#error-message').removeClass('hidden');
		$('#error-message').text('No se encontraron archivos compatibles en el enlace');*/
	}
}

function create_drive_document(response){
	var file = response['file'];
	$('#drive-title').text(file['title']);
	$('#document-owner').text(file['ownerNames']);
	$('#document-email').text(file['owners'][0]['emailAddress']);
	$('#document-modifiedDate').text(format_date(file['modifiedDate']));
	$('#document-size').text(formatSizeUnits(parseInt(file['fileSize'])));
	$('#information-section').attr('document-id', file['id']);
	$('#document-thumbnail').attr('src', file['thumbnailLink']);
	console.log(file['thumbnailLink']);
	alternator('#information-section', null);
}

//Alterna entre los diferentes tipos de respuesta. Estos son: Carpetas, archivos individuales y mensajes de error.
function alternator(id, message){
	var options = ['#information-section', '#error-message', '#folder-table'];
	if (id == options[1]){
		if(!$('.folder-wrapper').hasClass('hidden'))$('.folder-wrapper').addClass('hidden');
		if($('#error-message').hasClass('hidden'))$('#error-message').removeClass('hidden');
		$('#error-message').text(message);
	}
	else{
		if(id == options[0])state='single';
		else if(id == options[2])state='multi';
		if($('.folder-wrapper').hasClass('hidden'))$('.folder-wrapper').removeClass('hidden');
		if($(id).hasClass('hidden'))$(id).removeClass('hidden');
		for(var i = 0; i < options.length; i++){
			if(id != options[i])
				if(!$(options[i]).hasClass('hidden'))$(options[i]).addClass('hidden');			
		}
	}
}

function download_drive_request(){
	xhr = new XMLHttpRequest;
	xhr.onload =function(){
		response = JSON.parse(xhr.responseText);
		if (xhr.readyState == 4 && xhr.status == 200 && !response['error']) {
			console.log(response)
		}
		else if ((response['error'])){
		}
			
	};

	if(state == 'single'){	
		url = download_drive_link.replace('999', $('#information-section').attr('document-id'));
		xhr.open('GET', url, true);
		xhr.send();
	}
	else if(state == 'multi'){
		var ids = [];
		$('.checkbox:checked').each(function(){ids.push($(this).val())});
		var url = download_drive_link.replace('999', ids.join('+'));
		xhr.open('GET', url, true);
		xhr.send();
	}
}

//Le da formato a la fecha proporcionada por Google Drive.
function format_date(date){
	var date = new Date(date);
	var day = date.getDate();
	var month = monthNames[date.getMonth()];
	var year = date.getFullYear();
	return formated_date = day + ' ' + month + ' ' + year;
}
