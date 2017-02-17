$(document).ready(function() {
	$("input[type='radio'][data-color-select='true']").change(function(e) {
		$("#" + $(this).data('target')).val($(this).val());
	});

	$(".player").on('click', function(e) {
		$('.detail').hide();
		$(this).find(".detail").show();
	});
});
