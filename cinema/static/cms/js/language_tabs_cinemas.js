$("#id_title_uk").css('display', 'none');
$("#id_description_uk").css('display', 'none');
$("#id_conditions_uk").css('display', 'none');

function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $('#title').text('Название кинотеатра');
    $('#description').text('Описание');
    $('#conditions').text('Условия');
    $("#id_title_uk").css('display', 'none');
    $("#id_description_uk").css('display', 'none');
    $("#id_conditions_uk").css('display', 'none');
    $("#id_title").css('display', 'block');
    $("#id_description").css('display', 'block');
    $("#id_conditions").css('display', 'block');
}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $('#title').text('Назва кінотеатру');
    $('#description').text('Опис');
    $('#conditions').text('Умови');
    $("#id_title_uk").css('display', 'block');
    $("#id_description_uk").css('display', 'block');
    $("#id_conditions_uk").css('display', 'block');
    $("#id_title").css('display', 'none');
    $("#id_description").css('display', 'none');
    $("#id_conditions").css('display', 'none');
}

$('form').submit(function () {
    if ($("#id_title_uk").val().length < 1 || $("#id_description_uk").val().length < 1 ||
        $("#id_conditions_uk").val().length < 1) {
        $(".callout").css('display', 'block');
        $('body,html').animate({scrollTop: 0}, 400);
        setTimeout(function () {
            $(".callout").css('display', 'none');
        }, 4000)
        return false;
    }
})

