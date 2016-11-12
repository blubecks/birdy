/**
 * Created by beccaris on 11/11/2016.
 */
$().ready(function(){
    $.validate();
    $('#myForm').submit(function() {
        var inputs = $('#myForm :input');
        var values = {};
        inputs.each(function() {
            if (this.name!=""){
                values[this.name] = $(this).val();
            }
        });
        return false;

    });
});

