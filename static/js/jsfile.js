function triggerClick1(){
  document.querySelector('#imglink1').click();
}

function PreviewImage1(){
  var oFReader = new FileReader();
  oFReader.readAsDataURL(document.getElementById("imglink1").files[0]);
  oFReader.onload = function (oFREvent){
  document .getElementById("uploadPreview1").src = oFREvent.target.result;
  };
  };

// alert('Hello World');
