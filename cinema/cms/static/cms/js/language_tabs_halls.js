function russian() {
    $("#ru").removeAttr().css('background-color', '#ddd');
    $('#uk').css('background-color', 'white');
    $('#title').text('Номер зала');
    $("#id_number").attr('placeholder', 'Номер зала');
    $('#description').text('Описание');
    $("#id_description").attr('placeholder', 'Описание');

}

function ukraine() {
    $('#ru').css('background-color', 'white');
    $('#uk').css('background-color', '#ddd');
    $('#title').text('Номер залу');
    $("#id_number").attr('placeholder', 'Номер залу');
    $('#description').text('Опис');
    $("#id_description").attr('placeholder', 'Опис');


}

