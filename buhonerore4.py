# -------------------------------------------
# Bueno profe...Estaba aburrida, quería hacer el personaje del buhonero
# ya sé que no tiene nada que ver con el entorno laboral ni en lo profesional pero me pareció chistoso y por las jajas
# Solo quiero terminar el año haciendo algo chistoso 
# El buhonero del re4 - sistemas de gestión de armas xdddd
# -------------------------------------------

# Importamos sqlite3 para trabajar con la base de datos y Colorama para usar colores (quiero colorcito, si)
import sqlite3
from colorama import Fore, init

# Inicializamos Colorama para que los colores se reinicien automaticamente
init(autoreset=True)

# Nombre del archivo donde se guardara el inventario
BASE_DATOS = "inventario.db"


# Funciones auxiliares para mostrar mensajes con distintos colores
# Muestra titulos en un colorcito celeste
def mostrar_titulo(mensaje):
    print(Fore.CYAN + mensaje)


# Muestra mensajes cuando una operacion se realiza correctamente
def mostrar_exito(mensaje):
    print(Fore.GREEN + mensaje)


# Muestra mensajes de error en rojito >:c
def mostrar_error(mensaje):
    print(Fore.RED + mensaje)


# Muestra advertencias o avisos en amarillo o-o
def mostrar_aviso(mensaje):
    print(Fore.YELLOW + mensaje)

# Abre una conexion con la base de datos SQLite
def conectar():

    """Realiza la conexion con la base de datos."""

    return sqlite3.connect(BASE_DATOS)

# Crea la tabla productos si todavia no existe
def iniciar_inventario():

    conexion = conectar()

    cursor = conexion.cursor()

    # Definimos las columnas que tendra cada producto
    cursor.execute("""

        CREATE TABLE IF NOT EXISTS productos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            descripcion TEXT,

            cantidad INTEGER NOT NULL,

            precio REAL NOT NULL,

            categoria TEXT

        )

    """)

    # Guardamos la creacion de la tabla y cerramos la conexion
    conexion.commit()
    conexion.close()

# Solicita un texto y permite dejarlo vacio si no es obligatorio
def ingresar_texto(mensaje, obligatorio=True, actual=None):

    # Repetimos la pregunta hasta recibir un dato válido
    while True:

        if actual is not None:

            texto = input(f"{mensaje} [{actual}]: ").strip()

            if texto == "":

                return actual

        else:

            texto = input(f"{mensaje}: ").strip()

        if texto == "" and obligatorio:

            mostrar_aviso("¡Forastero! Este dato es necesario.")

        else:

            return texto

# Solicita un numero entero y valida que no sea negativo (validación de numeros pues)
def ingresar_entero(mensaje, actual=None):

    while True:

        if actual is not None:

            texto = input(f"{mensaje} [{actual}]: ").strip()

            if texto == "":

                return actual

        else:

            texto = input(f"{mensaje}: ").strip()

        try:
            # Intentamos convertir el texto ingresado a un numero entero
            numero = int(texto)

            if numero < 0:

                mostrar_error("No se permiten cantidades negativas.")

            else:

                return numero

        except ValueError:

            mostrar_error("Ingresá un numero entero valido.")

# Solicita un precio; acepta coma o punto como separador decimal
def ingresar_precio(mensaje, actual=None):

    while True:

        if actual is not None:

            texto = input(f"{mensaje} [{actual}]: ").strip()

            if texto == "":

                return actual

        else:

            texto = input(f"{mensaje}: ").strip()

        try:

            # Reemplazamos la coma por punto para convertir el precio
            precio = float(texto.replace(",", "."))

            if precio < 0:

                mostrar_error("El precio no puede ser negativo. No existe eso")

            else:

                return precio

        except ValueError:

            mostrar_error("Ingresá un precio valido. >:c")

# Ejecuta sentencias SQL y centraliza el manejo de conexiones y errores
def ejecutar_consulta(sql, parametros=(), consultar=False):

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        # Los parametros se envian por separado para evitar concatenar datos en SQL
        cursor.execute(sql, parametros)

        # Si es una consulta SELECT, devolvemos todos los registros encontrados
        if consultar:

            return cursor.fetchall()

        # Guardamos los cambios y devolvemos la cantidad de filas afectadas
        conexion.commit()
        return cursor.rowcount

    except sqlite3.Error as error:

        mostrar_error(f"Error en la base de datos: {error}")

        return [] if consultar else 0

    finally:

        conexion.close()

# Muestra una lista de productos en formato de tabla
def mostrar_inventario(productos):

    if not productos:

        mostrar_aviso("\nEl inventario esta vacio, Forastero.")

        return

    print(Fore.CYAN + "\n" + "=" * 95)

    print(

        f"{'ID':<5}{'ARTICULO':<22}"

        f"{'STOCK':<10}{'PRECIO':<15}"

        f"{'CATEGORIA':<18}DESCRIPCION"

    )

    print(Fore.CYAN + "-" * 95)

    # Recorremos los productos y mostramos sus datos en columnas
    for producto in productos:

        id_producto, nombre, descripcion, cantidad, precio, categoria = producto

        print(

            f"{id_producto:<5}"

            f"{nombre[:20]:<22}"

            f"{cantidad:<10}"

            f"{precio:<15.2f}"

            f"{(categoria or '')[:16]:<18}"

            f"{descripcion or ''}"

        )

    print(Fore.CYAN + "=" * 95)

    print(Fore.YELLOW + f"Total de articulos: {len(productos)}")

# Busca un producto por su ID y devuelve sus datos si es que existe
def obtener_articulo(id_producto):

    resultado = ejecutar_consulta(

        "SELECT * FROM productos WHERE id = ?",

        (id_producto,),

        consultar=True

    )

    if resultado:

        return resultado[0]

    return None

# Registra un producto nuevo y lo guarda en la base de datos
def registrar_mercancia():

    mostrar_titulo("\n===== NUEVA MERCANCIA =====")

    print(Fore.WHITE + "Veamos que tenemos para ofrecer...")

    nombre = ingresar_texto("Nombre del articulo")

    descripcion = ingresar_texto(

        "Descripcion",

        obligatorio=False

    )

    cantidad = ingresar_entero("Cantidad disponible")

    precio = ingresar_precio("Precio en pesetas")

    categoria = ingresar_texto(

        "Categoria (Armas, Municion, Curacion, Tesoros...)",

        obligatorio=False

    )

    # el INSERT agrega un nuevo registro a la tabla productos
    sql = """

        INSERT INTO productos

        (nombre, descripcion, cantidad, precio, categoria)

        VALUES (?, ?, ?, ?, ?)

    """

    filas = ejecutar_consulta(

        sql,

        (nombre, descripcion, cantidad, precio, categoria)

    )

    if filas > 0:

        mostrar_exito("\n¡Je, je!, Thank you. Mercancia registrada correctamente, Forastero. :)")

# Obtiene todos los productos y los muestra ordenados por ID
def consultar_inventario():

    mostrar_titulo("\n===== INVENTARIO DEL BUHONERO =====")

    productos = ejecutar_consulta(

        "SELECT * FROM productos ORDER BY id",

        consultar=True

    )

    mostrar_inventario(productos)

# Pide un ID y muestra el producto que coincide con ese numero
def buscar_mercancia():

    mostrar_titulo("\n===== BUSQUEDA DE ARTICULOS =====")

    id_producto = ingresar_entero("Ingresá el ID del articulo")

    producto = obtener_articulo(id_producto)

    if producto is None:

        mostrar_error("\nLo siento, Forastero. No tengo ese articulo.")

    else:

        mostrar_exito("\n¡Acá lo tengo! :)")

        mostrar_inventario([producto])

# Permite actualizar los datos de un producto existente
def modificar_mercancia():

    mostrar_titulo("\n===== MODIFICAR MERCANCIA =====")

    id_producto = ingresar_entero("ID del articulo")

    producto = obtener_articulo(id_producto)

    if producto is None:

        mostrar_error("\nNo existe un articulo con ese ID. Forastero.")

        return

    # Guardamos los datos actuales para mostrarlos como valores predeterminados

    _, nombre, descripcion, cantidad, precio, categoria = producto

    print(Fore.WHITE + "\nArticulo seleccionado:")

    mostrar_inventario([producto])

    print("\nIngresá los nuevos datos.")

    print("Presioná ENTER para mantener los valores actuales.\n")

    nuevo_nombre = ingresar_texto("Nombre", actual=nombre)

    nueva_descripcion = ingresar_texto(

        "Descripcion",

        actual=descripcion or ""

    )

    nueva_cantidad = ingresar_entero(

        "Cantidad",

        actual=cantidad

    )

    nuevo_precio = ingresar_precio(

        "Precio",

        actual=precio

    )

    nueva_categoria = ingresar_texto(

        "Categoria",

        actual=categoria or ""

    )

    # UPDATE modifica los datos del producto que tenga el ID indicado
    sql = """

        UPDATE productos

        SET nombre = ?,

            descripcion = ?,

            cantidad = ?,

            precio = ?,

            categoria = ?

        WHERE id = ?

    """

    filas = ejecutar_consulta(

        sql,

        (

            nuevo_nombre,

            nueva_descripcion,

            nueva_cantidad,

            nuevo_precio,

            nueva_categoria,

            id_producto

        )

    )

    if filas > 0:

        mostrar_exito("\n¡Mercancia actualizada correctamente!, Thank you!, forastero. :)")

# Elimina un producto del inventario despues de pedir confirmacion
def retirar_mercancia():

    mostrar_titulo("\n===== RETIRAR ARTICULO =====")

    id_producto = ingresar_entero("ID del articulo")

    producto = obtener_articulo(id_producto)

    if producto is None:

        mostrar_error("\nNo existe un articulo con ese ID, forastero. >:c")

        return

    print(Fore.WHITE + "\nArticulo seleccionado:")

    mostrar_inventario([producto])

    respuesta = input(

        "\n¿Estás seguro de que querés retirar este articulo? (s/n): "

    ).strip().lower()

    # Se elimina el producto si la respuesta es "s"
    if respuesta == "s":

        filas = ejecutar_consulta(

            "DELETE FROM productos WHERE id = ?",

            (id_producto,)

        )

        if filas > 0:

            mostrar_exito("\nArticulo retirado del inventario.")

    else:

        mostrar_aviso("\nOperacion cancelada, Forastero.")

# Genera un reporte de productos cuyo stock es igual o menor al limite
def revisar_existencias():

    mostrar_titulo("\n===== REPORTE DE EXISTENCIAS =====")

    limite = ingresar_entero(

        "Ingresá la cantidad limite de existencias"

    )

    # SELECT filtra los productos que necesitan reposición
    sql = """

        SELECT * FROM productos

        WHERE cantidad <= ?

        ORDER BY cantidad ASC

    """

    productos = ejecutar_consulta(

        sql,

        (limite,),

        consultar=True

    )

    if productos:

        mostrar_aviso("\n¡ATENCION! Estos articulos necesitan reposicion:")

        mostrar_inventario(productos)

    else:

        mostrar_exito("\nTodo en orden, Forastero. No falta mercancia.")

# decoración de mi menu principal (me rendí haciendo un dibujo ASCII del buhonero)
def mostrar_menu():

    print(Fore.CYAN + "\n")
    print(Fore.CYAN + "╔══════════════════════════════════════════╗")
    print(Fore.CYAN + "║                                          ║")
    print(Fore.YELLOW + "║              EL BUHONERO                ║")
    print(Fore.YELLOW + "║          SISTEMA DE MERCANCIA           ║")
    print(Fore.CYAN + "║                                          ║")
    print(Fore.CYAN + "╠══════════════════════════════════════════╣")
    print(Fore.CYAN + "║                                          ║")
    print(Fore.GREEN + "║  1. Registrar mercancia                 ║")
    print(Fore.GREEN + "║  2. Consultar inventario                ║")
    print(Fore.GREEN + "║  3. Buscar articulo                     ║")
    print(Fore.GREEN + "║  4. Modificar mercancia                ║")
    print(Fore.GREEN + "║  5. Retirar articulo                    ║")
    print(Fore.GREEN + "║  6. Revisar existencias bajas          ║")
    print(Fore.CYAN + "║                                          ║")
    print(Fore.YELLOW + "║  0. Cerrar tienda                       ║")
    print(Fore.CYAN + "║                                          ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════╝")

    print(Fore.YELLOW + "\n¿Qué necesitas, Forastero?")


# Funcion principal: inicia la base de datos y controla el menu
def main():

    iniciar_inventario()

    # Relacionamos cada opcion del menu con la funcion que debe ejecutar
    acciones = {

        "1": registrar_mercancia,

        "2": consultar_inventario,

        "3": buscar_mercancia,

        "4": modificar_mercancia,

        "5": retirar_mercancia,

        "6": revisar_existencias

    }

    # Repetimos el menu hasta que el usuario elija cerrar la tienda
    while True:

        mostrar_menu()

        # Leemos la opcion y quitamos espacios sobrantes
        opcion = input("\nSeleccioná una opcion: ").strip()

        if opcion == "0":

            mostrar_exito("\nVuelva cuando quiera, Forastero.")

            print(Fore.MAGENTA + "Je, je, je...")

            break

        # Si la opcion existe, ejecutamos la funcion asociada
        elif opcion in acciones:

            acciones[opcion]()

        else:

            mostrar_error("\nOpcion incorrecta. Intentá de nuevo, forastero.")

# esta condicion permite ejecutar main solo al iniciar este archivo directamente
if __name__ == "__main__":

    main()
