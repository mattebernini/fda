// output della risposta ajax
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

// ajax per i form con un solo ingresso
function prepara_ajax_un_input(arg)
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
            display_result(arg, "Errore durante l'elaborazione, si prega di segnalare l'errore sulla repo di Github (link in fondo alla pagina).");
          }
        });
  });
}
  
// ajax per il form delle matrici
function prepara_ajax_matrix()
{
  $("#matrix-form").submit(function(e) 
  {
      // avoid to execute the actual submit of the form.
      e.preventDefault(); 
  
      var form = $(this);
      var A = $("#A").val();
      var B = $("#B").val();
      var C = $("#C").val();
      var D = $("#D").val();
      
      $.ajax({
          type: 'POST',
          url: "/ajax/"+"matrix",
          data: { 
            'A': A,
            'B': B,
            'C': C,
            'D': D,
          },
          success: function(response) {
            console.log(response);  
            display_result("matrix", response);
          },
          error: function(error) {
            console.log(error);  
            display_result("matrix", "Errore durante l'elaborazione, si prega di segnalare l'errore sulla repo di Github (link in fondo alla pagina).");
          }
        });
  });
}

// chiamata a prepara_ajax_un_input per tutti i form inseriti in lista
argomenti = ["bode", "laplace", "nyquist", "rlocus", "step", "valore_finale", "errore"];
argomenti.forEach(element => {
  prepara_ajax_un_input(element);
});
// chiamata a 
prepara_ajax_matrix();