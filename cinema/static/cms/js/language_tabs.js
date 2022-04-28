$(".uk").css('display', 'none')
var indexes = []
$('.contacts_container').each(function () {
    indexes.push(this.id)
})


function russian(event) {
    const index = event.target.value;
    $("#ru-" + index).removeAttr().css('background-color', '#ddd');
    $('#uk-' + index).css('background-color', 'white');
    $('#title-' + index).text('Название кинотеатра');
    $('#address-' + index).text('Адресc');
    $("#id_" + index + "-title_uk").css('display', 'none')
    $("#id_" + index + "-address_uk").css('display', 'none')
    $("#id_" + index + "-title").css('display', 'block')
    $("#id_" + index + "-address").css('display', 'block')


}

function ukraine(event) {
    const index = event.target.value;
    $('#ru-' + index).css('background-color', 'white');
    $('#uk-' + index).css('background-color', '#ddd');
    $('#title-' + index).text('Назва кінотеатру');
    $('#address-' + index).text('Адреса');
    $("#id_" + index + "-title_uk").css('display', 'block')
    $("#id_" + index + "-address_uk").css('display', 'block')
    $("#id_" + index + "-title").css('display', 'none')
    $("#id_" + index + "-address").css('display', 'none')

}

$('form').submit(function () {
    for (i in indexes) {
        console.log(indexes[i])
        if ($("#id_" + indexes[i] + "-title_uk").val().length < 1 || $("#id_" + indexes[i] + "-address_uk").val().length < 1) {
            $(".callout").css('display', 'block');
            $('body,html').animate({scrollTop: 0}, 400);
            setTimeout(function () {
                $(".callout").css('display', 'none');
            }, 4000)
            return false;
        }
    }
})




