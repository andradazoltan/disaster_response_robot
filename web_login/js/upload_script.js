function preview_image(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var output = document.getElementById('output_image');
    output.src = reader.result;
  }
  reader.readAsDataURL(event.target.files[0]);
}

function uploadFile() {
  if (document.getElementById("uploaded-img").files.length != 0) {
    var file = ($("#uploaded-img"))[0].files[0];
    console.log("upload button clicked");

    showBar();
    var form = new FormData();
    form.append('uploaded-img', file);

    var progressBar = document.getElementById("progressBar");
    progressBar.value = 0;

    $.ajax({
      type: 'POST',
      url: "http://38.88.75.83/db/uploadfile.php",
      data: form,
      processData: false,
      contentType: false,
      xhr: function(){
         var xhr = $.ajaxSettings.xhr() ;
         xhr.upload.onprogress = function(data){
            var perc = Math.round((data.loaded / data.total) * 100);
            progressBar.value = perc;
         };
         return xhr;
      },
      success: function (response) {
        console.log(response);
        showResponseSuccess();
      },
      error: function (errorMessage) {
        console.log(errorMessage);
        showResponseFail();
      }
    });
  }
};


//helper functions for css
document.getElementById("uploaded-img").addEventListener('change', function () {
  hideBar();
  hideResponses();
});

function hideBar() {
  var uploadBar = document.getElementById("progressBar");
  uploadBar.style.display = "none";
}

function showBar() {
  var uploadBar = document.getElementById("progressBar");
  uploadBar.style.display = "inline-block";
}

function hideResponses() {
  var response = document.getElementById("uploadResponseSuccess");
  response.style.display = "none";
  response = document.getElementById("uploadResponseFail");
  response.style.display = "none";
}

function showResponseSuccess() {
  var response = document.getElementById("uploadResponseSuccess");
  response.style.display = "inline-block";
}

function showResponseFail() {
  var response = document.getElementById("uploadResponseFail");
  response.style.display = "inline-block";
}

