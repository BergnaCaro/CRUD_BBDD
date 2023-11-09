from tkinter import *

#Colores
color_fondo='lawn green'
color_letra='black'
color_framebotone='plum1'
color_fondo_boton='maroon1'
color_blanco='snow'

#Crear la ventana con su titulo y la posibilidad de cerrar cuando uno quiera
# con mainloop cerrar la ventana
ventana=Tk()
ventana.title('ejemplo de interfaz gráfica')

#Barra de menu (hay que ubicarlo y configurarlo)
#La ventana tiene menus
barramenu= Menu(ventana)
ventana.config(menu=barramenu)

#Bontones del Menú en cascada y campos
#Menu de conexión y lista y salir
bbddmenu=Menu(barramenu, tearoff=0)
bbddmenu.add_command(label='Conectar a la BBDD')
bbddmenu.add_command(label='Listado de alumnos')
bbddmenu.add_command(label='Salir')

#Menú de gráficas
graficamenu=Menu(barramenu, tearoff=0)
graficamenu.add_command(label='Alumnos por escuela')
graficamenu.add_command(label='Calificaciones')

#Menú limpiar
limpiaventana=Menu(barramenu, tearoff=0)
limpiaventana.add_command(label='Limpiar')

#Menú de descripción
info=Menu(barramenu,tearoff=0)
info.add_command(label='Licencia')
info.add_command(label='Acerca de...')

barramenu.add_cascade(label='BBDD', menu=bbddmenu)
barramenu.add_cascade(label='Gráficas', menu=graficamenu)
barramenu.add_cascade(label='Limpiar', menu=limpiaventana)
barramenu.add_cascade(label='Acerca de...', menu=info)

#FRAMECAMPOS --> con formulario
framecampos=Frame(ventana)
framecampos.config(bg=color_fondo)
framecampos.pack(fill='both')

#Labels
#Se puede cofigurar todos los elementos en funciones
def config_label(mi_label,fila):
    espaciado_label={'column': 0, 'sticky': 'e', 'padx': 10, 'pady': 10}
    color_labels={'bg': color_fondo, 'fg': color_letra}
    mi_label.grid(row=fila, **espaciado_label)
    mi_label.config(**color_labels)
    
#Sistema STICKY que emplea los puntos cardinales
#Por defecto esta alineado a la izquierda
'''  n
  nw   ne
w         e
  sw   se
     s       '''

legajo_label=Label(framecampos, text='N° de Legajo')
config_label(legajo_label,0)
apellido_label=Label(framecampos, text='Apellido')
config_label(apellido_label,1)
nombre_label=Label(framecampos, text='Nombre')
config_label(nombre_label,2)
email_label=Label(framecampos, text='Email')
config_label(email_label,3)
promedio_label=Label(framecampos, text='Promedio')
config_label(promedio_label,4)
escuela_label=Label(framecampos, text='Escuela')
config_label(escuela_label,5)
localidad_label=Label(framecampos, text='Localidad')
config_label(localidad_label,6)
provincia_label=Label(framecampos, text='Provincia')
config_label(provincia_label,7)

#Campos de entrada
#Necesitan variables de control
'''Declarar variables en tkinter tiene una forma diferente:
Enteros --> IntVar()
Flotantes --> DoubleVar()
Strings --> StringVar()
Booleannos --> BooleanVar() '''
legajo=StringVar()
apellido=StringVar()
nombre=StringVar()
email=StringVar()
calificacion=DoubleVar()
escuela=StringVar()
localidad=StringVar()
provincia=StringVar()

#Función para configurar el ingreso de datos en el formulario
def config_input(mi_input,fila):
    espaciado_input={'column': 1, 'padx': 10, 'pady': 10, 'ipadx': 50}
    mi_input.grid(row=fila, **espaciado_input)
    
legajo_input=Entry(framecampos, textvariable=legajo)
config_input(legajo_input,0)
apellido_input=Entry(framecampos, textvariable=apellido)
config_input(apellido_input,1)
nombre_input=Entry(framecampos, textvariable=nombre)
config_input(nombre_input,2)
email_input=Entry(framecampos, textvariable=email)
config_input(email_input,3)
promedio_input=Entry(framecampos, textvariable=calificacion)
config_input(promedio_input,4)

escuela_input=Entry(framecampos, textvariable=escuela)
config_input(escuela_input,5)

# con .config(state='readonly') --> dejamos el campo en solo lectura
localidad_input=Entry(framecampos, textvariable=localidad)
config_input(localidad_input,6)
localidad_input.config(state='readonly')
provincia_input=Entry(framecampos, textvariable=provincia)
config_input(provincia_input,7)
provincia_input.config(state='readonly')

#Frame Botones
#Botones con acciones para crear, buscar, editar en la BBDD
#Funciones del CRUD
framebotones=Frame(ventana)
framebotones.config(bg=color_framebotone)
framebotones.pack(fill='both')

def config_bottons(mi_button,columna):
  espacaido_bottons={'row':0, 'padx':5, 'pady':10, 'ipadx':12}
  mi_button.config(bg=color_fondo_boton, fg=color_letra)
  mi_button.grid(column=columna, **espacaido_bottons)
  
boton_crear= Button(framebotones, text='Crear')
config_bottons(boton_crear,0)
boton_buscar= Button(framebotones, text='Buscar')
config_bottons(boton_buscar,1)
boton_actualizar= Button(framebotones, text='Actualizar')
config_bottons(boton_actualizar,2)
boton_borrar= Button(framebotones, text='Borrar')
config_bottons(boton_borrar,3)

#Frame al pie de página
framecopy=Frame(ventana)
framecopy.config(bg=color_letra)
framecopy.pack(fill='both')
copylabel=Label(framecopy,text='(2023) por Bergna Andrea C., para CaC/Big Data I')
copylabel.config(bg=color_letra, fg=color_blanco)
copylabel.grid(row=0, column=0, padx=10, ipadx=12)

ventana.mainloop()
