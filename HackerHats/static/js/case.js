"use strict";

window.onload = function() {
	$('#response-form input').change(function() {
		$.ajax({
			url : '/responses/submit',
			type : 'post',
			data : $('#response-form').serialize(),
			success : function() {
				 window.location.href = $('a#next-button').attr('href');
			},
			error : function() {
				alert("Failed to send data to server.");
			},
		});
	});
}