$(function () {

  var loadForm = function () {
    $("#fileupload").click();
  };

  var loadPersons = function (data) {
          $("#content-detail #photo_scream").html("");
          $("#content-detail #photo_scream").html(data.result.html_person_scream);
          $("#content-detail #person_list").html("");
          $("#content-detail #person_list").html(data.result.html_person_list);
          
          var img = $("#content-detail img#scream.img-responsive")[0]; // Get my img elem
          
          img.onload = function() {
              catImageWidth = img.naturalWidth;
              catImageHeight = img.naturalHeight;
              var c=document.getElementById("myCanvas");
              $(c).prop('width', catImageWidth);
              $(c).prop('height', catImageHeight);

              var c=document.getElementById("myCanvas");
              var ctx=c.getContext("2d");

              ctx.drawImage(img,10,10);  
              var canvas = document.getElementById('myCanvas');
              var context = canvas.getContext('2d');
              
              for (var i in data.result.rectangles) {
                  console.log(data.result.rectangles[i].rectangle_x)
                  context.beginPath();
                  context.rect(data.result.rectangles[i].rectangle_x, data.result.rectangles[i].rectangle_y, data.result.rectangles[i].rectangle_w, data.result.rectangles[i].rectangle_h);
                  context.lineWidth = 3;
                  context.strokeStyle = 'blue';
                  context.stroke();
              }
              
          }
                

               
                  
              
         
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

     
      console.log(data.result)
      if (data.result.is_valid) {
          loadPersons(data);
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

  

  $("#content-detail").on("click", ".js-upload-photo", loadForm);
  $("#content-detail").on("click", ".js-upload-fingerprint", loadFormFingerprint);
  $("#content-detail").on("click", ".js-upload-iris", loadFormIris);
  
   
  

});


