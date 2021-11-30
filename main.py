'''

Realizado por: Sebastián Felipe Tamayo Proaño
Matería: Base de datos II
Descripción:

    Este proyecto consiste en desarrollar una interfaz gráfica para la presentación de una base de datos instanciada en mongoDB.
    El aplicativo debe permitir la visualización de la tabla así como editar, añadir y eliminar datos de la base de datos.
    La base de datos tendrá una tabla donde permitirá el ingreso de datos estadísticos de las ventas de una empresa sobre algún producto.

'''

'''

    *** Área de conexión con nuestra base de datos en MongoDB ***

'''

from pymongo import  MongoClient

# Hacemos la conexión con mongoDB
client = MongoClient("localhost")
# Trabajaremos con la base de datos del proyecto
db = client["Empresa_BD"]
# Llamamos a nuestra colección
ventas = db["VENTAS"]

'''

    *** Área de desarrollo ***

'''

# --- Desarrollo para todas las ventanas ---

def evaluar_ventana(event):
    '''
        Permite evaluar si la ventana selccionada es la de detalles para establecer valores iniciales
    '''
    # Seleccionamos la ventana actual
    ventana = event.widget.select()
    # Seleccionamos el título de la ventana
    titulo = event.widget.tab(ventana, "text")    
    # Evaluamos que no sea la ventana de detalles
    if not titulo == "Detalles":
        # Eliminamos la información
        eliminar_detalles()
        # Habilitamos el botón de editar
        enable_editar_btn()
    if titulo == "Inicio":
        # Vaciamos la tabla
        vaciar_tabla()
        # Actualizamos la tabla
        llenar_tabla()
    if titulo == "Nuevo":
        # Generamos valores por defecto (id)
        establecer_nuevo()

def calcular_total(*args):
    '''
        Calcula el total generado por las ventas dado el pvp y la cantidad vendida
    '''    
    # Para la ventana detalles
    if pvp.get() and cantidad_vendido.get():        
        detalles_total_txt["state"] = "normal"
        total_generado.set((float(pvp.get())*float(cantidad_vendido.get())))     
        detalles_total_txt["state"] = "disabled"
    # Para la ventana nuevo
    if nuevo_pvp.get() and nuevo_cantidad_vendido.get():
        nuevo_total_txt["state"] = "normal"
        nuevo_total_generado.set((float(nuevo_pvp.get())*float(nuevo_cantidad_vendido.get()))) 
        nuevo_total_txt["state"] = "disabled"

# --- Desarrollo de la ventana inicio ---

def buscar():
    ''' 
        Permite la búsqueda de un documento
    '''
    # Vacia los datos de la tabla
    vaciar_tabla()
    # Consigue el valor buscado
    busqueda = busqueda_txt.get()
    filtro_temp = filtro.get()
    # Si existe un valor buscar por categoria seleccionada
    if busqueda:
        if filtro_temp == "Por producto":
            llenar_tabla_busqueda(busqueda, 1)
        elif filtro_temp == "Por región":
            llenar_tabla_busqueda(busqueda, 2)
        elif filtro_temp == "Por provincia":
            llenar_tabla_busqueda(busqueda, 3)
        elif filtro_temp == "Por ciudad":
            llenar_tabla_busqueda(busqueda, 4)
    # Si no existe llenar la tabla con todos los valores
    else:        
        llenar_tabla()

def ordenar_busqueda(ventas_temp):
    '''
        Ordena el registro dado un filtro de orden
    '''
    orden_temp = orden.get()    
    # Si no hay filtro de orden, ordena por el ID   
    if(orden_temp == "Sin filtro de orden"):
        orden_id(ventas_temp)
    # Ordena desde el mayor pvp por producto
    elif(orden_temp == "Mayor precio por producto"):
        orden_pvp_mayor(ventas_temp)
    # Ordena desde el menor pvp por producto
    elif(orden_temp == "Menor precio por producto"):
        orden_pvp_menor(ventas_temp)
    # Ordena desde la mmayor cantidad vendida
    elif(orden_temp == "Mayor cantidad vendida"):
        orden_cantidad_mayor(ventas_temp)
    # Ordena desde la menor cantidad vendida
    elif(orden_temp == "Menor cantidad vendida"):
        orden_cantidad_menor(ventas_temp)
    # Ordena desde el mayor total generado
    elif(orden_temp == "Mayor total generado"):
        orden_total_mayor(ventas_temp)
    # Ordena desde el menor total generado
    elif(orden_temp == "Menor total generado"):
        orden_total_menor(ventas_temp)

def llenar_tabla_busqueda(busqueda, filtro):
    '''
        Llena la tabla en base a la búsqueda realizada
    '''
    ventas_temp = []
    busqueda = busqueda.lower()
    # Búsqueda por producto
    if filtro == 1:
        for venta in ventas.find({}):
            if busqueda in venta["producto"].lower():
                ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))
    # Búsqueda por región
    elif filtro == 2:
        for venta in ventas.find({}):
            if busqueda in venta["region"].lower():
                ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))
    # Búsqueda por provincia
    elif filtro == 3:
        for venta in ventas.find({}):
            if busqueda in venta["provincia"].lower():
                ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))
    # Búsqueda por ciudad
    elif filtro == 4:
        for venta in ventas.find({}):
            if busqueda in venta["ciudad"].lower():
                ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))    
    # Muestra de los resultados en la tabla
    llenar_tabla(ventas_temp, 1)    
    # Si no encuentra registros tras la búsqueda
    if ventas_temp == []:
        messagebox.showwarning("Búsqueda no encontrada", "No se encontraron registros!")
        llenar_tabla()
        

def llenar_tabla(ventas_temp = [], nuevo = 0):
    '''
        Llena la tabla con todos los datos de nuestra colección
    '''
    # Si se debe llenar la tabla con todos los productos
    if nuevo == 0:
        ventas_temp = []
        for venta in ventas.find({}):
            ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))
    # Si se debe llenar la tabla dada una lista de productos buscada
    # Si un orden es entregado ordena la lista antes de llenar la tabla
    ordenar_busqueda(ventas_temp)
    for venta in ventas_temp:
        productos_tbl.insert("", END, values=venta)

def vaciar_tabla():
    '''
        Borra todos los datos de la tabla
    '''
    productos_tbl.delete(*productos_tbl.get_children())   

def set_filtros():
    '''
        Atribuimos valores al combobox de filtros y configuraciones iniciales
    '''
    # Establecemos valores para el combobox
    busqueda_cmb["values"] = (
                            "Por producto",
                            "Por región",
                            "Por provincia",
                            "Por ciudad"
                            )
    # Cambiamos el estado para que no sea editado
    busqueda_cmb["state"] = "readonly"
    # Establecemos una selección por defecto
    busqueda_cmb.current(0)

def set_orden():
    '''
        Atribuimos valores al combobox de orden de resultados y configuraciones iniciales
    '''
    # Establecemos valores para el combobox
    busqueda_orden_cmb["values"] = (
        "Sin filtro de orden",
        "Mayor precio por producto",
        "Menor precio por producto",
        "Mayor cantidad vendida",
        "Menor cantidad vendida",
        "Mayor total generado",
        "Menor total generado"
    )
    # Cambiamos el estado para que no sea editado
    busqueda_orden_cmb["state"] = "readonly"
    # Establecemos una selección por defecto
    busqueda_orden_cmb.current(0)

# --- Desarrollo de la ventana detalles ---

def item_seleccionado(event):
    '''
        Permite visualizar los datos de un valor seleccionado de la tabla
    '''
    # Selecionamos el valor seleccionado   
    record = []
    for selected_item in productos_tbl.selection():
        item = productos_tbl.item(selected_item)
        record = item['values']
    # Seleccionamos la ventana de detalles
    controlador.select(detalles)
    # Presentamos los datos de la venta 
    set_detalles(record)

def set_detalles(ventas_temp):
    '''
        Establece la ventana de detalles con valores dada una lista
    '''    
    # Permitimos la edición de las entradas de texto
    set_entry_enable()
    # Ingresamos los datos
    detalles_id_txt.insert(0, ventas_temp[0])
    detalles_producto_txt.insert(0,ventas_temp[1])
    detalles_pvp_txt.insert(0,ventas_temp[2])
    detalles_region_txt.insert(0,ventas_temp[3])
    detalles_provincia_txt.insert(0,ventas_temp[4])
    detalles_ciudad_txt.insert(0,ventas_temp[5])    
    detalles_cantidad_txt.insert(0,ventas_temp[6])
    detalles_total_txt.insert(0,ventas_temp[7])
    # Colocamos las entradas de texto para que no puedan ser editados
    set_entry_disable()

def eliminar_detalles():
    '''
        Elimina todos los datos existentes o no en la ventana de detalles
    '''    
    # Permitimos la edición de las entradas de texto
    set_entry_enable()
    # Eliminamos los datos
    detalles_id_txt.delete(0,END)    
    detalles_producto_txt.delete(0, END)
    detalles_region_txt.delete(0, END)
    detalles_provincia_txt.delete(0, END)
    detalles_ciudad_txt.delete(0, END)
    detalles_pvp_txt.delete(0, END)
    detalles_cantidad_txt.delete(0, END)
    detalles_total_txt.delete(0, END)  
    # Colocamos las entradas de texto para que no puedan ser editados
    set_entry_disable()

def set_entry_disable():
    '''
        Coloca a las entradas de texto como readonly
    '''  
    detalles_id_txt["state"] = "disabled"
    detalles_producto_txt["state"] = "disabled"
    detalles_region_txt["state"] = "disabled"
    detalles_provincia_txt["state"] = "disabled"
    detalles_ciudad_txt["state"] = "disabled"
    detalles_pvp_txt["state"] = "disabled"
    detalles_cantidad_txt["state"] = "disabled"
    detalles_total_txt["state"] = "disabled"

def set_entry_enable():
    '''
        Coloca a las entradas de texto como editables para añadir información
    '''
    detalles_id_txt["state"] = "normal"    
    detalles_producto_txt["state"] = "normal"    
    detalles_pvp_txt["state"] = "normal"    
    detalles_region_txt["state"] = "normal"    
    detalles_provincia_txt["state"] = "normal"    
    detalles_ciudad_txt["state"] = "normal"      
    detalles_cantidad_txt["state"] = "normal"    
    detalles_total_txt["state"] = "normal"    

def ver_todo():
    '''
        Permite la visualización de la ventana inicio desde la ventana detalles
    '''
    eliminar_detalles()
    controlador.select(inicio)

def parar_vista():
    '''
        Deja de ver algun registro seleccionado en detalles
    '''
    eliminar_detalles()

def editar():
    '''
        Permite la edición del registro visualizado en detalles
    '''
    # Habilitamos las entradas de texto
    set_entry_enable()
    # Menos la del id dado que no cambia
    detalles_id_txt["state"] = "disabled"
    # Igualmente el total ya que se calcula automaticamente
    detalles_total_txt["state"] = "disabled"
    # Habilitamos el boton de guardado
    enable_guardar_btn()

def guardar():
    '''
        Permite guardar la información del registro visualizado en detalles tras un edición
        y crear un nuevo documento en la colección de nuestra base de datos.
    '''      
    # Creamos el item a buscar dado el id
    item = {"_id" : int(id.get())}

    # Creamos el new_item con el formato para actualizar un registro
    new_item = {
        "$set" : {
            "producto" : producto.get(),
            "pvp" : float(pvp.get()),
            "region" : region.get(),
            "provincia" : provincia.get(),
            "ciudad" : ciudad.get(),
            "cantidad_vendido" : int(cantidad_vendido.get()),
            "total_generado" : float(total_generado.get())
        }
    }

    # Actualiza el registro
    ventas.update_one(item, new_item)

    # Mostramos un mensaje de que el registro fue actualizado
    messagebox.showinfo("Registro actualizado", f"Su registro con id {id.get()} ha sido actualizado con exito!")

    # Establecemos los valores iniciales
    eliminar_detalles()
    set_entry_disable()
    enable_editar_btn()

def eliminar():
    '''
        Elimina el registro visualizado en detalles
    '''
    # Advierte al usuario que se eliminará el registro
    advertencia = messagebox.askokcancel("Advertencia","Eliminaras este registro!\n¿Deseas continuar?")
    # Si acepta eliminar
    if advertencia:
        # Creamos el documento a eliminar
        doc = { "_id" : int(id.get()) }
        # Eliminamos el documento
        ventas.delete_one(doc)

        # Avisamos al usuario de la eliminación
        messagebox.showinfo("Registro eliminado", "Se ha eliminado el registro exitosamente!")
        # Reestablecemos los valores iniciales
        eliminar_detalles()
        set_entry_disable()        

def enable_editar_btn():
    '''
        Crea el boton editar y de ser necesario elimina el boton guardar
    '''
    if guardar_btn.winfo_exists:
        guardar_btn.grid_forget()
    editar_btn.grid(row=10, column=0, padx=5, pady=(60,10))

def enable_guardar_btn():
    '''
        Crea el boton guardar y de ser necesario elimina el boton editar
    '''
    if editar_btn.winfo_exists:
        editar_btn.grid_forget()
    guardar_btn.grid(row=10, column=0, padx=5, pady=(60,10))

# --- Desarrollo de la ventana nuevo ---

def establecer_nuevo():
    '''
        Establece el indice a usarse para la creación de un nuevo registro,
        además, vacía todos los datos de la ventana
    '''
    vaciar_nuevo()
    establecer_id()

def vaciar_nuevo():
    '''
        Vacia todos los datos de la ventana nuevo
    '''
    nuevo_id_txt["state"] = "normal"
    nuevo_id_txt.delete(0, END)
    nuevo_id_txt["state"] = "disabled"
    nuevo_producto_txt.delete(0, END)
    nuevo_region_txt.delete(0, END)
    nuevo_provincia_txt.delete(0, END)
    nuevo_ciudad_txt.delete(0, END)
    nuevo_pvp_txt.delete(0, END)
    nuevo_cantidad_txt.delete(0, END)
    nuevo_total_txt["state"] = "normal"
    nuevo_total_txt.delete(0, END)
    nuevo_total_txt["state"] = "disabled"

def establecer_id():
    '''
        Establece el id a utilizarse por el nuevo registro por crearse
    '''
    ventas_temp = []
    for venta in ventas.find({}):
        ventas_temp.append((venta["_id"], venta["producto"], venta["pvp"], venta["region"], venta["provincia"], venta["ciudad"], venta["cantidad_vendido"], venta["total_generado"]))
    orden_id(ventas_temp)
    nuevo_id_txt["state"] = "normal"
    nuevo_id.set(ventas_temp[-1][0]+1)
    nuevo_id_txt["state"] = "disabled"

def crear():
    '''
        Crea un nuevo registro y lo ingresa a nuestra colección de nuestra base de datos
    '''
    # Creamos nuestro documento
    doc = {
        "_id" : int(nuevo_id.get()),
        "producto" : nuevo_producto.get(),
        "pvp" : float(nuevo_pvp.get()),
        "region" : nuevo_region.get(),
        "provincia" : nuevo_provincia.get(),
        "ciudad" : nuevo_ciudad.get(),
        "cantidad_vendido" : int(nuevo_cantidad_vendido.get()),
        "total_generado" : float(nuevo_total_generado.get())
    }
    # Ingresamos el documento a nuestra colección
    ventas.insert_one(doc)
    # Notificamos al usuario de la creación del documento
    messagebox.showinfo("Registro creado","Su registro ha sido creado exitosamente!")
    # Reestaablecemos la ventana
    establecer_nuevo()

# --- Desarrollo general ---

def orden_id(ventas_temp):
    '''
        Ordena los documentos en base al ID de menor a mayor por inserción
    '''    
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los IDs de los documentos
        while j >= 0 and key[0] < ventas_temp[j][0]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j + 1] = key

def orden_pvp_mayor(ventas_temp):
    '''
        Ordena los documentos en base al pvp de mayor a menor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[2] > ventas_temp[j][2]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

def orden_pvp_menor(ventas_temp):
    '''
        Ordena los documentos en base al pvp de menor a mayor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[2] < ventas_temp[j][2]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

def orden_cantidad_mayor(ventas_temp):
    '''
        Ordena los documentos en base a la cantidad vendida de mayor a menor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[6] > ventas_temp[j][6]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

def orden_cantidad_menor(ventas_temp):
    '''
        Ordena los documentos en base a la cantidad vendida de menor a mayor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[6] < ventas_temp[j][6]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

def orden_total_mayor(ventas_temp):
    '''
        Ordena los documentos en base al total generado de mayor a menor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[7] > ventas_temp[j][7]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

def orden_total_menor(ventas_temp):
    '''
        Ordena los documentos en base base al total generado de menor a mayor por inserción
    '''
    for step in range(1, len(ventas_temp)):
        key = ventas_temp[step]
        j = step - 1
        # Comparamos unicamente los pvp de los documentos
        while j >= 0 and key[7] < ventas_temp[j][7]:
            ventas_temp[j+1] = ventas_temp[j]
            j = j - 1
        ventas_temp[j+1] = key

'''

    *** Área de implementación del GUI ***

'''

# Librerias requeridas
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox

''' --- Establecemos la ventana principal --- '''

window = Tk()
window.title("Estadistica de ventas") # El nombre de la aplicación
window.resizable(False, False)

''' --- Variables requeridas --- '''

# Ventana inicio
filtro = StringVar()
orden = StringVar()

# Ventana detalles
id = StringVar()
producto = StringVar()
pvp = StringVar()
region = StringVar()
provincia = StringVar()
ciudad = StringVar()
cantidad_vendido = StringVar()
total_generado = StringVar()
# Establecemos un evento si pvp o cantidad_vendido es modificado
pvp.trace("w", calcular_total)
cantidad_vendido.trace("w", calcular_total)

# Ventana nuevo
nuevo_id = StringVar()
nuevo_producto = StringVar()
nuevo_pvp = StringVar()
nuevo_region = StringVar()
nuevo_provincia = StringVar()
nuevo_ciudad = StringVar()
nuevo_cantidad_vendido = StringVar()
nuevo_total_generado = StringVar()
# Establecemos un evento si pvp o cantidad_vendido es modificado
nuevo_pvp.trace("w", calcular_total)
nuevo_cantidad_vendido.trace("w", calcular_total)

''' --- Diseño del aplicativo --- '''

# --- Deiseño de subventanas ---
# Creación de un controlador de subventanas
controlador = ttk.Notebook(window)
# Ventana de inicio donde se mostrarán todos los registros
inicio = ttk.Frame(controlador)
# Ventana de detalles de registros
detalles = ttk.Frame(controlador)
# Ventana de creación de nuevos registros
nuevo = ttk.Frame(controlador)

# --- Diseño de la ventana de inicio ---
# Creación de un título
titulo_inicio = Label(inicio, text="Estadística de Ventas")

# Menú de búsqueda
busqueda_lb = Label(inicio, text="Búsca: ")
busqueda_txt = Entry(inicio, width="20")
busqueda_filtro_lb = Label(inicio, text="Filtro de búsqueda: ")
busqueda_cmb = ttk.Combobox(inicio, width="12", textvariable=filtro)
busqueda_orden_lb = Label(inicio, text="Orden de resultado: ")
busqueda_orden_cmb = ttk.Combobox(inicio, width="25", textvariable=orden)
busqueda_btn = Button(inicio, text="Buscar", command=buscar)

# Tabla con los datos de la base de datos
# Declaración de la tabla
productos_tbl = ttk.Treeview(inicio, height=20)

# Definición de las columnas
productos_tbl["columns"] = (
    "id",
    "producto",
    "pvp",
    "region",
    "provincia",
    "ciudad",
    "cantidad_vendido",
    "total_generado"
)

# Formateamos la tabla
productos_tbl.column("#0", width=0, stretch=NO)
productos_tbl.column("id", anchor=CENTER, width=50)
productos_tbl.column("producto", anchor=CENTER, width=120)
productos_tbl.column("pvp", anchor=CENTER, width=120)
productos_tbl.column("region", anchor=CENTER, width=80)
productos_tbl.column("provincia", anchor=CENTER, width=80)
productos_tbl.column("ciudad", anchor=CENTER, width=80)
productos_tbl.column("cantidad_vendido", anchor=CENTER, width=120)
productos_tbl.column("total_generado", anchor=CENTER, width=120)

# Establecemos los títulos de las columnas
productos_tbl.heading("#0", text="", anchor=CENTER)
productos_tbl.heading("id", text="ID", anchor=CENTER)
productos_tbl.heading("producto", text="Producto", anchor=CENTER)
productos_tbl.heading("pvp", text="Precio por producto", anchor=CENTER)
productos_tbl.heading("region", text="Región", anchor=CENTER)
productos_tbl.heading("provincia", text="Provincia", anchor=CENTER)
productos_tbl.heading("ciudad", text="Ciudad", anchor=CENTER)
productos_tbl.heading("cantidad_vendido", text="Cantidad vendido", anchor=CENTER)
productos_tbl.heading("total_generado", text="Total generado", anchor=CENTER)

# Llenamos los datos de la tabla con los datos de la collección
llenar_tabla()

# --- Diseño de la ventana de detalles ---

titulo_detalles = Label(detalles, text="Detalles de la Venta")
detalles_id_lb = Label(detalles, text="ID de la venta: ")
detalles_id_txt = Entry(detalles, width=30, state="disabled", textvariable=id)
detalles_producto_lb = Label(detalles, text="Nombre del producto: ")
detalles_producto_txt = Entry(detalles, width=30, state="disabled", textvariable=producto)
detalles_region_lb = Label(detalles, text="Región de las ventas: ")
detalles_region_txt = Entry(detalles, width=30, state="disabled", textvariable=region)
detalles_provincia_lb = Label(detalles, text="Provincia de las ventas: ")
detalles_provincia_txt = Entry(detalles, width=30, state="disabled", textvariable=provincia)
detalles_ciudad_lb = Label(detalles, text="Ciudad de las ventas: ")
detalles_ciudad_txt = Entry(detalles, width=30, state="disabled", textvariable=ciudad)
detalles_pvp_lb = Label(detalles, text="Precio por producto del producto: ")
detalles_pvp_txt = Entry(detalles, width=30, state="disabled", textvariable=pvp)
detalles_cantidad_lb = Label(detalles, text="Cantidad de productos vendidos: ")
detalles_cantidad_txt = Entry(detalles, width=30, state="disabled", textvariable=cantidad_vendido)
detalles_total_lb = Label(detalles, text="Total generado por las ventas: ")
detalles_total_txt = Entry(detalles, width=30, state="disabled", textvariable=total_generado)
# Este boton desaparecera al hacerlo clic y aparecera al hacer clic en el btoton guardar
editar_btn = Button(detalles, text="Editar registro", command=editar)
# Este boton aparecera al momento de dar clic en el boton editar y desaparecera al hacer clic en el mismo
guardar_btn = Button(detalles, text="Guardar registro", command=guardar) 
eliminar_btn = Button(detalles, text="Eliminar registro", command=eliminar)
detalles_pararvista_btn = Button(detalles, text="Dejar de ver el registro", command=parar_vista)
detalles_vertodo_btn = Button(detalles, text="Ver todos los registros", command=ver_todo)

# --- Diseño de la ventana nuevo ---

titulo_nuevo = Label(nuevo, text="Crea un Nuevo Registro de Venta")
nuevo_id_lb = Label(nuevo, text="ID de la venta: ")
nuevo_id_txt = Entry(nuevo, width=30, state="disabled", textvariable=nuevo_id)
nuevo_producto_lb = Label(nuevo, text="Nombre del producto: ")
nuevo_producto_txt = Entry(nuevo, width=30, textvariable=nuevo_producto)
nuevo_region_lb = Label(nuevo, text="Región de las ventas: ")
nuevo_region_txt = Entry(nuevo, width=30, textvariable=nuevo_region)
nuevo_provincia_lb = Label(nuevo, text="Provincia de las ventas: ")
nuevo_provincia_txt = Entry(nuevo, width=30, textvariable=nuevo_provincia)
nuevo_ciudad_lb = Label(nuevo, text="Ciudad de las ventas: ")
nuevo_ciudad_txt = Entry(nuevo, width=30, textvariable=nuevo_ciudad)
nuevo_pvp_lb = Label(nuevo, text="Precio por producto del producto: ")
nuevo_pvp_txt = Entry(nuevo, width=30, textvariable=nuevo_pvp)
nuevo_cantidad_lb = Label(nuevo, text="Cantidad de productos vendidos: ")
nuevo_cantidad_txt = Entry(nuevo, width=30, textvariable=nuevo_cantidad_vendido)
nuevo_total_lb = Label(nuevo, text="Total generado por las ventas: ")
nuevo_total_txt = Entry(nuevo, width=30, state="disabled", textvariable=nuevo_total_generado)
crear_btn = Button(nuevo, text="Crear nuevo registro de venta", command=crear)
vaciar_btn = Button(nuevo, text="Vaciar formulario", command=establecer_nuevo)
nuevo_vertodo_btn = Button(nuevo, text="Ver todos los registros", command=ver_todo)

''' --- Establecimiento de los diseños en el aplicativo --- '''

# --- Establecimiento de la ventana de inicio
titulo_inicio.grid(row=0, column=0, padx=5, pady=15, columnspan=7, sticky=W)
busqueda_lb.grid(row=1, column=0, padx=5, pady=5)
busqueda_txt.grid(row=1, column=1, padx=5, pady=5)
busqueda_filtro_lb.grid(row=1, column=2, padx=5, pady=5)
busqueda_cmb.grid(row=1, column=3, padx=5, pady=5)
busqueda_orden_lb.grid(row=1, column=4, padx=5, pady=5)
busqueda_orden_cmb.grid(row=1, column=5, padx=5, pady=5)
busqueda_btn.grid(row=1, column=6, padx=5, pady=5)
productos_tbl.grid(row=2, column=0, padx=10, pady=10, columnspan=7)

# --- Establecimiento de la ventana de detalles
titulo_detalles.grid(row=0, column=0, padx=5, pady=15, columnspan=7, sticky=W)
detalles_id_lb.grid(row=1, column=0, padx=5, pady=10, sticky=W)
detalles_id_txt.grid(row=1, column=1, padx=5, pady=10)
detalles_producto_lb.grid(row=2, column=0, padx=5, pady=10, sticky=W)
detalles_producto_txt.grid(row=2, column=1, padx=5, pady=10)
detalles_region_lb.grid(row=3, column=0, padx=5, pady=10, sticky=W)
detalles_region_txt.grid(row=3, column=1, padx=5, pady=10)
detalles_provincia_lb.grid(row=4, column=0, padx=5, pady=10, sticky=W)
detalles_provincia_txt.grid(row=4, column=1, padx=5, pady=10)
detalles_ciudad_lb.grid(row=5, column=0, padx=5, pady=10, sticky=W)
detalles_ciudad_txt.grid(row=5, column=1, padx=5, pady=10)
detalles_pvp_lb.grid(row=6, column=0, padx=5, pady=10, sticky=W)
detalles_pvp_txt.grid(row=6, column=1, padx=5, pady=10)
detalles_cantidad_lb.grid(row=7, column=0, padx=5, pady=10, sticky=W)
detalles_cantidad_txt.grid(row=7, column=1, padx=5, pady=10)
detalles_total_lb.grid(row=8, column=0, padx=5, pady=10, sticky=W)
detalles_total_txt.grid(row=8, column=1, padx=5, pady=10)
editar_btn.grid(row=10, column=0, padx=5, pady=(60,10))
eliminar_btn.grid(row=10, column=1, padx=5, pady=(60,10), sticky=W)
detalles_pararvista_btn.grid(row=10, column=2, padx=20, pady=(60,10), sticky=W)
detalles_vertodo_btn.grid(row=10, column=3, padx=20, pady=(60,10), sticky=E)

# --- Establecimiento de la ventana nuevo
titulo_nuevo.grid(row=0, column=0, padx=5, pady=15, columnspan=7, sticky=W)
nuevo_id_lb.grid(row=1, column=0, padx=5, pady=10, sticky=W)
nuevo_id_txt.grid(row=1, column=1, padx=5, pady=10)
nuevo_producto_lb.grid(row=2, column=0, padx=5, pady=10, sticky=W)
nuevo_producto_txt.grid(row=2, column=1, padx=5, pady=10)
nuevo_region_lb.grid(row=3, column=0, padx=5, pady=10, sticky=W)
nuevo_region_txt.grid(row=3, column=1, padx=5, pady=10)
nuevo_provincia_lb.grid(row=4, column=0, padx=5, pady=10, sticky=W)
nuevo_provincia_txt.grid(row=4, column=1, padx=5, pady=10)
nuevo_ciudad_lb.grid(row=5, column=0, padx=5, pady=10, sticky=W)
nuevo_ciudad_txt.grid(row=5, column=1, padx=5, pady=10)
nuevo_pvp_lb.grid(row=6, column=0, padx=5, pady=10, sticky=W)
nuevo_pvp_txt.grid(row=6, column=1, padx=5, pady=10)
nuevo_cantidad_lb.grid(row=7, column=0, padx=5, pady=10, sticky=W)
nuevo_cantidad_txt.grid(row=7, column=1, padx=5, pady=10)
nuevo_total_lb.grid(row=8, column=0, padx=5, pady=10, sticky=W)
nuevo_total_txt.grid(row=8, column=1, padx=5, pady=10)
crear_btn.grid(row=9, column=0, padx=20, pady=(60,10), sticky=W)
vaciar_btn.grid(row=9, column=1, padx=20, pady=(60,10))
nuevo_vertodo_btn.grid(row=9, column=2, padx=20, pady=(60,10))

# --- Establecimiento de subventanas ---
# Agregamos las subventanas al controlador
controlador.add(inicio, text="Inicio")
controlador.add(detalles, text="Detalles")
controlador.add(nuevo, text="Nuevo")
# Permitimos su visibilidad en la aplicación
controlador.pack(expand=1, fill="both")

# Llamamos a funciones establecedoras
set_filtros() # Establece los filtros
set_orden() # Establece los ordenes
# Genera un evento cuando un item es seleccionado de la tabla
productos_tbl.bind('<Double-1>', item_seleccionado) 
# Permite evaluar alguna situación cuando se cambie de ventanas
controlador.bind("<<NotebookTabChanged>>", evaluar_ventana)

# Permite la ejecución del ambiente gráfico de la aplicaciónç
window.mainloop()