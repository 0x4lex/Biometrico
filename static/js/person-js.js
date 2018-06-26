$(function () {


  var loadForm = function () {
    $("#fileupload").click();
  };

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
      $("#modal-progress").modal("show");
    },
    stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
      $("#modal-progress").modal("hide");
    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
      
      if (data.result.is_valid) {
          $("#button-enabled #face_count").html(data.result.html_person_button);
          swal.resetDefaults();
          swal('Listo!',
            'Foto agregado correctamente!',
            'success');
      }else{
        swal('Ooops!',
            'No se pudo validar el archivo!',
            'error');
      }
    }

  });

  var loadFormFingerprint = function(){
    swal({
      title: 'buscando dispositivo',
      text: '',
      timer: 5000,
      onOpen: function () {
        swal.showLoading()
      }
    }).then(
      function () {},
      function (dismiss) {
        if (dismiss === 'timer') {
          swal.resetDefaults();
          swal('Ooops!',
            'no se pudo detectar ningún dispositivo!',
            'error');
          
        }
      }
    )
  };

  var loadFormIris = function(){
    swal({
      title: 'buscando dispositivo',
      text: '',
      timer: 5000,
      onOpen: function () {
        swal.showLoading()
      }
    }).then(
      function () {},
      function (dismiss) {
        if (dismiss === 'timer') {
          swal.resetDefaults();
          swal('Ooops!',
            'no se pudo detectar ningún dispositivo!',
            'error');
          
        }
      }
    )
  };

  var loadFormUpdate = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-person").modal("show");             
      },
      success: function (data) {
        $("#modal-person .modal-content").html("");
        $("#modal-person .modal-content").html(data.html_form);
      },
       error: function(){
        $("#modal-person .modal-content").html("");
      }
    });
  };

  var saveFormUpdate = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#box-body-detail").html(data.html_person_detail);
          $("#modal-person").modal("hide");
          swal('Listo!',
            'Datos actualizado correctamente!',
            'success');
        }
        else {
          $("#modal-person .modal-content").html(data.html_person_detail);
          swal('Ooops!',
            'No se pudo actualizar!',
            'error');
        }
      }
    });
    return false;
  };


  $("#content-detail").on("click", ".js-upload-photo", loadForm);
  $("#content-detail").on("click", ".js-upload-fingerprint", loadFormFingerprint);
  $("#content-detail").on("click", ".js-upload-iris", loadFormIris);

  $("#content-detail").on("click", ".js-update-person", loadFormUpdate);
  $("#modal-person").on("submit", ".js-person-update-form", saveFormUpdate);
});


