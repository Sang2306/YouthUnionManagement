$(function(){

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'GET',
            dataType: 'JSON',
            beforeSend: function(){
                $("#modal-user .modal-content").html("");
                $("#modal-user" ).modal('show');
            },
            success: function (data){
                $("#modal-user .modal-content").html(data.html_form);
            }
        });
      };

      var saveForm = function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $("#user-table tbody").html(data.html_user_list);
              $("#modal-user").modal("hide");
            }
            else {
              $("#modal-user .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      };


    $(".js-create-user").click(loadForm);
    $("#modal-user").on("submit", ".js-user-create-form", saveForm);

    $("#user-table").on("click", ".js-delete-user", loadForm);
    $("#modal-user").on("submit", ".js-user-delete-form", saveForm);

    $("#user-table").on("click", ".js-update-user", loadForm);
    $("#modal-user").on("submit", ".js-user-update-form", saveForm);

});