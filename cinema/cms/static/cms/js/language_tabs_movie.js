$("#id_title_uk").css('display', 'none');
$("#id_description_uk").css('display', 'none');


function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $("#id_title_uk").css('display', 'none');
    $("#id_title").css('display', 'block');
    $("#id_description_uk").css('display', 'none');
    $("#id_description").css('display', 'block');
    $('#title').text('Название фильма');
    $('#description').text('Описание');
}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $("#id_title").css('display', 'none');
    $("#id_title_uk").css('display', 'block');
    $("#id_description_uk").css('display', 'block');
    $("#id_description").css('display', 'none');
    $('#title').text('Назва фильму');
    $('#description').text('Опис');

}

$('form').submit(function () {
    if ($("#id_title_uk").val().length < 1 || $("#id_description_uk").val().length < 1) {
        $(".callout").css('display', 'block');
        $('body,html').animate({scrollTop: 0}, 400);
        setTimeout(function () {
            $(".callout").css('display', 'none');
        }, 4000)
        return false;
    }
})
