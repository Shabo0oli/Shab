//Allows bootstrap carousels to display 3 items per page rather than just one
$('.carousel.carousel-multi .item').each(function () {
	var next = $(this).next();
	if (!next.length) {
		next = $(this).siblings(':first');
	}
	next.children(':first-child').clone().attr("aria-hidden", "true").appendTo($(this));

	if (next.next().length > 0) {
		next.next().children(':first-child').clone().attr("aria-hidden", "true").appendTo($(this));
	}
	else {
		$(this).siblings(':first').children(':first-child').clone().appendTo($(this));
	}
});


$('#form-comment').on('submit',function (e) {
    e.preventDefault();
    $.ajax({
        url: '/comment/',
        cache: false,
        type: 'POST',
        data : $('#form-comment').serialize(),
        success: function(json_obj) {
        alert(json_obj.message);
        document.getElementById("form-comment").reset();
    }
    });
});