$("#id_description_uk").css('display', 'none');

function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $('#description').text('Описание');
    $("#id_description_uk").css('display', 'none');
    $("#id_description").css('display', 'block');
}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $('#description').text('Опис');
    $("#id_description_uk").css('display', 'block');
    $("#id_description").css('display', 'none');
}

$('form').submit(function () {
    if ($("#id_description_uk").val().length < 1) {
        $(".callout").css('display', 'block');
        $('body,html').animate({scrollTop: 0}, 400);
        setTimeout(function () {
            $(".callout").css('display', 'none');
        }, 4000)
        return false;
    }
})