function ukraine() {

    $('#ru').css('background-color', 'white')
    $('#uk').css('background-color', '#ddd')
    $('#title').text('Назва Акції');
    $('#date').text('Дата публікації');
    $('#description').text('Опис');
    $('#id_title').attr('placeholder', 'Назва акції');
    $('#id_description').attr('placeholder', 'Опис')
}

function russian() {
    $('#ru').css('background-color', '#ddd')
    $('#uk').css('background-color', 'white')
    $('#title').text('Название Акции');
    $('#date').text('Дата публикации');
    $('#description').text('Описание')
    $('#id_title').attr('placeholder', 'Название акции');
    $('#id_description').attr('placeholder', 'Описание')
}