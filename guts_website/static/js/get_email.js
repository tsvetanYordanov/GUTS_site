    var isGU = true;
    function no_gu_email() {
      if (isGU) {
        $("#modal-error").slideUp();
        $("#gu_email_wrapper").slideUp();
        $("#other_email_wrapper").slideDown();
        $("#no_gu_link").html("Remembered GU email?");
        isGU = false;
      } else {
        $("#modal-error").slideUp();
        $("#gu_email_wrapper").slideDown();
        $("#other_email_wrapper").slideUp();
        $("#no_gu_link").html("Don't have GU email?");
        isGU = true;
      }
    }
    function valid_fields() {
      fullname = $("#fullname").val();
      var pattern = new RegExp(/^[a-z\s]+$/i);
      if (!pattern.test(fullname)) return "name";
      if (isGU) {
        var emailAddress = $("#gu_email").val();
        var epattern = new RegExp(/^\d{7}[a-z]$/i);
      }
      else {
        var emailAddress = $("#other_email").val();
        var epattern = new RegExp(/^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);
      }
      if (epattern.test(emailAddress)) return ""
      else return "email";
    }
    
    $("#modal-register").click(function() {
      var field_val = valid_fields();
      if ( field_val == "") {
        $.ajax({
          type : "POST",
          url : "/submit",
          data: {
            'isGU': isGU,
            'fullname': $("#fullname").val(),
            'gu_email': $("#gu_email").val(),
            'other_email': $("#other_email").val(),
            'confirm_gu': $("#confirm_gu").is(':checked')
          },
          dataType: 'text',
          success: function(result) {
              if (result == "EMAIL_EXISTS") {
                $("#modal-error").slideDown();
                $("#modal-error").html("<b>Oh snap!</b> This email already exists!")
              } else if (result == "NOT_GU") {
                $("#modal-error").slideDown();
                $("#modal-error").html("<b>Oh snap!</b> You need to confirm that you are GU student!")
              } else if (result == "INVALID_EMAIL" ) {
                $("#modal-error").slideDown();
                $("#modal-error").html("<b>Oh snap!</b> Invalid email address (s)!")
              } else {
                $("#content_wrapper").slideUp();
                $("#modal-result").slideDown();
                $("#modal-register").hide();
                $("#modal-thanks").append(result);
              }
          }
        });
      } else {
         $("#modal-error").slideDown();
         $("#modal-error").html("<b>Oh snap!</b> Invalid " + field_val + "!")
      }
    });
