$("#id_title_uk").css('display', 'none');
$("#id_description_uk").css('display', 'none');

function ukraine() {

    $('#ru').css('background-color', 'white')
    $('#uk').css('background-color', '#ddd')
    $('#title_promotions').text('Назва Акції');
    $('#title_news').text('Назва Новини');
    $('#description').text('Опис');
    $("#id_title").css('display', 'none');
    $("#id_description").css('display', 'none');
    $("#id_title_uk").css('display', 'block');
    $("#id_description_uk").css('display', 'block');

}

function russian() {
    $('#ru').css('background-color', '#ddd')
    $('#uk').css('background-color', 'white')
    $('#title_promotions').text('Название Акции');
    $('#title_news').text('Название Новости');
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