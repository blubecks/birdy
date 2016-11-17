/**
 * Created by beccaris on 11/11/2016.
 */
$(document).ready(function(){
    $("#myForm :input[name^='ipv']").prop('disabled', true);
    $('#checkbox_ipv4').change(function() {
        // this will contain a reference to the checkbox
        if (this.checked) {
            $("#myForm :input[name^='ipv4']").prop('disabled', false);
        } else {
            $("#myForm :input[name^='ipv4']").prop('disabled', true);
        }
    });
    $('#checkbox_ipv6').change(function() {
        // this will contain a reference to the checkbox
        if (this.checked) {
            $("#myForm :input[name^='ipv6']").prop('disabled', false);
        } else {
            $("#myForm :input[name^='ipv6']").prop('disabled', true);
        }
    });
    $.validate();
    $('#myForm').submit(function(e) {
        e.preventDefault();
        var inputs = $("#myForm :input[name^='ipv']:enabled");
        var values = {};
        inputs.each(function() {
            if (this.name!=""){
                if($(this).val().trim().length != 0){
                    var res = this.name.split('_');
                    if(values[res[0]] === undefined){
                        if($('#checkbox_'+res[0]+':checked').length>0){
                            values[res[0]] = {};
                        }
                    }
                    values[res[0]][res[1]] = $(this).val();
                }
            }
        });
        values['secret'] = $("#myForm :input[name='secret']").val();
        var posting = $.ajax({
            type: "POST",
            url: '/api/configure/session',
            data: JSON.stringify(values),
            headers: {'Content-Type': 'application/json'}
        });
        posting.done(function(data) {
            if (data.status == 'error'){
                if( typeof data.message === 'string' ) {
                    data.message = [ data.message ];
                }
                data.message.forEach(function (error) {
                    toastr.warning(error);
                });
            }else{
                toastr.success(data.message)
                setTimeout(function () {
                    location.reload();
                },2000)
            }
        });
        posting.fail(function(err) {
            toastr.error("Server Error, please check")
        });
        return false;
    });
});

