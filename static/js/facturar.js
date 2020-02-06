
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
        agregarproducto.valorstatico = parseInt( agregarproducto.valorstatico,10) + cantidadproducto*nuevoprecioproducto;
        console.log(agregarproducto.valorstatico);
        document.getElementById('valortotal').innerHTML="$"+agregarproducto.valorstatico;
    }
}
