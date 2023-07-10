
function display_result(arg, response)
{
  var resultDiv = document.getElementById("result-"+arg);
  // elimino eventuale risultato precedente
  while (resultDiv.firstChild) {
    resultDiv.removeChild(resultDiv.firstChild);
  }
  // è un'immagine
  if(response === "ok")
  {
      var img = document.createElement("img");
      img.className = "img-fluid mb-3";
      // reload dell'immagine
      img.src = "static/teoria/files/"+arg+".jpg" + "?" + new Date().getTime();
      resultDiv.appendChild(img);
  }
  // è testuale
  else
  {
      var pre = document.createElement("pre");
      pre.className = "text-danger";
      // reload dell'immagine
      pre.textContent = response;
      resultDiv.appendChild(pre);
  }
}

function prepara_ajax_fdt_in(arg)
{
  $("#"+arg+"-form").submit(function(e) 
  {
      // avoid to execute the actual submit of the form.
      e.preventDefault(); 
  
      var form = $(this);
      var fdt = $("#fdt-"+arg+"").val();
      
      $.ajax({
          type: 'POST',
          url: "/ajax/"+arg,
          data: { 
              'fdt': fdt
          },
          success: function(response) {
            console.log(response);  
            display_result(arg, response);
          },
          error: function(error) {
            console.log(error);  
            display_result(arg, "");
          }
        });
  });
}
  
argomenti = ["bode", "laplace", "nyquist", "rlocus", "step", "stability", "observability", "reachability"];
argomenti.forEach(element => {
  prepara_ajax_fdt_in(element);
});