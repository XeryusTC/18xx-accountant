$(document).ready(function() {
	$("input[type='radio'][data-color-select='true']").change(function(e) {
		$("#" + $(this).data('target')).val($(this).val());
	});
});
