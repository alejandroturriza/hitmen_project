
$(document).ready(function  (){
    $('#description_hitman').prop('required', true)
});

function show_input(val) {
    let description_input = $('#description_hitman');
    if(val === 1){
        description_input.show();
        description_input.prop('required', true)
    }else{
        description_input.hide();
        description_input.prop('required', false)
    }
}
