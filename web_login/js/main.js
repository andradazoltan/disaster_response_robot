
function test() {
    $.ajax({
        type: 'POST',
        url: 'http://38.88.75.83/db/login1.php',
        data: {'username': "fafa", 'password': "fewfaafwfwaaw"},
        success: function(data) {
            console.log("sucessfully logged in!");
            location.href = "http://38.88.75.83/Login/signup.html"
        },
        error: function(data) {
            console.log("error logging in!");
        },
    });
}

(function ($) {
    "use strict";

     /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-form .input100')

    $('.validate-form').on('submit',function(){
        var username = $("input[name=username]").val();
        var pw = $("input[name=pass]").val();

        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        if (check) {
            $.ajax({
                type: 'POST',
                url: 'http://38.88.75.83/db/login1.php',
                data: {'username': username, 'password': pw},
                success: function(data) {
                    console.log("sucessfully logged in!");
                    console.log(data);
                    if (data == "{\"success\"}") {
                        location.href = "http://38.88.75.83/Login/home.html";
                    } else if (data == "{\"no such user\"}"){
                    } 
                },
                error: function(data) {
                    console.log("error logging in!");
                },
            });
        }

       

        return check;
    });

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }   
    

})(jQuery);