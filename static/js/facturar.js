lineasDeVentaProducto=[];
lineasDeVentaServicio=[];
function agregarproducto(){
    /* VARIABLE STATICA */
    
    /* Obtenemos el producto */
    var nombreproducto = document.getElementById("select-producto").value;
    /* Si el producto no esta seleccionado no dejamos pasar */
    if (nombreproducto=='Seleccione el producto'){
        alert('Seleccione un producto primero');
    }
    else{
        /* Si se selecciono un producto obtenemos los demas datos */
        var cantidadproducto = document.getElementById('cantidadproducto').value;
        var nuevoprecioproducto = document.getElementById('nuevoprecioproducto').value;
        console.log(nombreproducto);
        console.log(cantidadproducto);
        console.log(nuevoprecioproducto);
        /* CREACION DE ELEMENTOS DOM */
        /* Creacion de Row */
        var row = document.createElement("div");
        row.className="row lineaproducto";
        row.id=nombreproducto;
        document.getElementById("factura").appendChild(row);
        /* Creacion de Cols */
        /* Nombre producto */
        var producto = document.createElement("div");
        producto.className="col-6";
        producto.innerHTML=nombreproducto;
        document.getElementById(nombreproducto).appendChild(producto);
        /* Cantidad */
        var cantidad = document.createElement("div");
        cantidad.className="col-3";
        cantidad.innerHTML=cantidadproducto;
        document.getElementById(nombreproducto).appendChild(cantidad);
        /* precio final */
        var pfinal = document.createElement("div");
        pfinal.className="col-3";
        pfinal.innerHTML='$'+cantidadproducto*nuevoprecioproducto;
        document.getElementById(nombreproducto).appendChild(pfinal);
        agregarproducto.valorstatico = agregarproducto.valorstatico + cantidadproducto*nuevoprecioproducto;
        console.log(agregarproducto.valorstatico);
        var lineaprod = {
            producto:nombreproducto,
            cantidad:cantidadproducto,
            descuento:"null",
            nuevoprecio:nuevoprecioproducto,
            subtotal:pfinal
        };
        lineasDeVentaProducto.push(lineaprod);
        document.getElementById('valortotal').innerHTML="$"+agregarproducto.valorstatico;
        console.log(lineasDeVentaProducto);
    }
}

function agregarservicio(){
    /* VARIABLE STATICA */
    
    /* Obtenemos el producto */
    var nombreservicio = document.getElementById("select-servicio").value;
    /* Si el producto no esta seleccionado no dejamos pasar */
    if (nombreservicio=='Seleccione el servicio'){
        alert('Seleccione un producto primero');
    }
    else{
        /* Si se selecciono un producto obtenemos los demas datos */
        var colaborador = document.getElementById('select-colaborador').value;
        if(colaborador=='Seleccione el colaborador'){
            alert('Seleccione un colaborador primero');
        }else{
        var nuevoprecioservicio = document.getElementById('nuevoprecioservicio').value;
        var descripcion = document.getElementById('descripcion').value;
        console.log(nombreservicio);
        console.log(nuevoprecioservicio);
        console.log(colaborador);
        console.log(descripcion);
        /* CREACION DE ELEMENTOS DOM */
        /* Creacion de Row */
        var row = document.createElement("div");
        row.className="row lineaservicio";
        row.id=nombreservicio;
        document.getElementById("factura").appendChild(row);
        /* Creacion de Cols */
        /* Nombre producto */
        var servicio = document.createElement("div");
        servicio.className="col-6";
        servicio.innerHTML=nombreservicio;
        document.getElementById(nombreservicio).appendChild(servicio);
        /* Cantidad */
        var cantidad = document.createElement("div");
        cantidad.className="col-3";
        cantidad.innerHTML=1;
        document.getElementById(nombreservicio).appendChild(cantidad);
        /* precio final */
        var sfinal = document.createElement("div");
        sfinal.className="col-3";
        sfinal.innerHTML='$'+1*nuevoprecioservicio;
        document.getElementById(nombreservicio).appendChild(sfinal);
        //agregarservicio.valorstatico = agregarproducto.valorstatico + 1*nuevoprecioservicio;
        agregarproducto.valorstatico = agregarproducto.valorstatico + parseInt(nuevoprecioservicio,10);
        console.log(agregarproducto.valorstatico);
        var lineaservicio = {
            servicio:nombreservicio,
            colaboradorador:colaborador,
            descuento:"null",
            descripcion:descripcion,
            subtotal:1*nuevoprecioservicio
        };
        lineasDeVentaServicio.push(lineaservicio);
        document.getElementById('valortotal').innerHTML="$"+agregarproducto.valorstatico;
        console.log(lineasDeVentaServicio);
        
    }
    }
}
agregarproducto.valorstatico=0;

function finalizarVenta(){
    /* var lineasProducto = JSON.stringify(lineasDeVentaProducto)
    var lineasServicio = JSON.stringify(lineasDeVentaServicio)
    var parmetros = "lineasProducto=" + encodeURI(lineasProducto) + "lineasServicio=" + encodeURI(lineasServicio)
 */
}
function finalizarlineas() {
   var clientename=  document.getElementById('name-cliente').value;
   console.log(clientename);
   var valordiv =  document.getElementById('valortotal').value;
   console.log(valordiv);
    var xhttp;
    //var preparedst = "saludar/"+lineasDeVentaServicio[0].servicio+"/"+lineasDeVentaServicio[0].colaboradorador;
    var preparedst2 = "crearventa/"+clientename+"/0/"+agregarproducto.valorstatico;
    if (window.XMLHttpRequest) {
      // code for modern browsers
      xhttp = new XMLHttpRequest();
      } else {
      // code for IE6, IE5
      xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        this.responseText;
       console.log("lol");
        console.log(lineasDeVentaServicio.length);
        /* Loop para general lineas de servicio */
        if(lineasDeVentaServicio.length>0){
        for (i = 0; i <lineasDeVentaServicio.length; i++) {
            console.log("iteration");
                var xhttp;
                var preparedst = "linea_servicio/"+this.responseText+"/"+lineasDeVentaServicio[i].servicio+"/"+lineasDeVentaServicio[i].colaboradorador+"/"+lineasDeVentaServicio[i].subtotal+"/"+lineasDeVentaServicio[i].descripcion;
                if (window.XMLHttpRequest) {
                  // code for modern browsers
                  xhttp = new XMLHttpRequest();
                  } else {
                  // code for IE6, IE5
                  xhttp = new ActiveXObject("Microsoft.XMLHTTP");
                }
                xhttp.onreadystatechange = function() {
                  if (this.readyState == 4 && this.status == 200) {
                    
                  }
                };
                xhttp.open("GET",preparedst , true);
                xhttp.send(); 
              
          }  
        }
        else{
            console.log("empty service");
        }
          /* fin loop lineas de servicio*/
          if (lineasDeVentaProducto.length>0){
          /* Loop para general lineas de producto */
        for (i = 0; i <lineasDeVentaProducto.length; i++) {
            console.log("iteration");
                var xhttp;
                var preparedst = "linea_servicio/"+this.responseText+"/"+lineasDeVentaServicio[i].servicio+"/"+lineasDeVentaServicio[i].colaboradorador+"/"+lineasDeVentaServicio[i].subtotal+"/"+lineasDeVentaServicio[i].descripcion;
                if (window.XMLHttpRequest) {
                  // code for modern browsers
                  xhttp = new XMLHttpRequest();
                  } else {
                  // code for IE6, IE5
                  xhttp = new ActiveXObject("Microsoft.XMLHTTP");
                }
                xhttp.onreadystatechange = function() {
                  if (this.readyState == 4 && this.status == 200) {
                    
                  }
                };
                xhttp.open("GET",preparedst , true);
                xhttp.send(); 
              
          }  
        }
        else{
            console.log('empty products');
        }
          /* fin loop lineas de servicio*/
      }
    };
    xhttp.open("GET", preparedst2, true);
    xhttp.send();
  
}