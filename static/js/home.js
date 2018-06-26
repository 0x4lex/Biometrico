$(function () {

  var loadFormUpdate = function () {
    $("#search_box").val("");
    $("#modal-person").modal("show");
  };

  var saveFormUpdate = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log(data);
        if (data.redirect) {
          window.location.href = data.redirect;
          }
        else {
          $("#modal-person .modal-content").html(data.html_person_detail);
          swal('ID INCORRECTO!',
            'no se pudo encontrar el id!',
            'error');
        }
      }
    });
    return false;
  };
  $("#content-button").on("click", ".js-search-person", loadFormUpdate);
  $("#modal-person").on("submit", ".js-person-search-form", saveFormUpdate);
});
