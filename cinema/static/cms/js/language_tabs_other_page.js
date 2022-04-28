$("#id_title_uk").css('display', 'none');
$("#id_description_uk").css('display', 'none');


function ukraine() {

    $('#ru').css('background-color', 'white')
    $('#uk').css('background-color', '#ddd')
    $('#title').text('Назва');
    $('#description').text('Опис')
    $("#id_title_uk").css('display', 'block');
    $("#id_description_uk").css('display', 'block');
    $("#id_title").css('display', 'none');
    $("#id_description").css('display', 'none');

}

function russian() {
    $('#ru').css('background-color', '#ddd')
    $('#uk').css('background-color', 'white')
    $('#title').text('Название');
    $('#description').text('Описание')
    $("#id_title_uk").css('display', 'none');
    $("#id_description_uk").css('display', 'none');
    $("#id_title").css('display', 'block');
    $("#id_description").css('display', 'block');

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