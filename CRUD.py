from tkinter import *
from tkinter import messagebox
import sqlite3 as sq3
import matplotlib.pyplot as plt

#No me funciono la creación de entorno virtual en el disco externo
'''pip install virtualenv
#CREAR CARPETA --> virtualenv venv
#ACTIVAR --> venv\Scripts\activate
#DESACTIVAR --> deactivate
REQUERIMIENTOS --> pip freeze > requirements.txt
 '''



'''
******************************
PARTE FUNCIONAL
******************************
'''
# Menu-BBDD/ Conectar y Salir de la BBDD
def conectarBBDD():
  global conexion
  global micursor
  conexion=sq3.connect('miBase.db') 
  micursor=conexion.cursor()
  messagebox.showinfo("ESTADO", "¡Conectado a la Base de Datos!")

def listar():
  class Table():
    def __init__(self, otra_ventana):
      nombre_column=['Legajo', 'Apellido', 'Nombre', 'Promedio', 'Email', 'Escuela', 'Localidad', 'Provincia']
      for i in range(cantidad_columnas):
        self.e=Entry(frameppal)
        self.e.config(bg=color_letra, fg= color_blanco)
        self.e.grid(row=0, column=i)
        self.e.insert(END, nombre_column[i])
        
      for fila in range(cantidad_filas):
        for columna in range(cantidad_columnas):
          self.e=Entry(frameppal)
          self.e.grid(row=fila+1, column=columna)
          self.e.insert(END, resultado[fila][columna])
          self.e.config(state='readonly')
      
  
  #Interfaz de la ventana emergente
  otra_ventana=Tk()
  otra_ventana.title('Listado de Alumnos')
  frameppal=Frame(otra_ventana)
  frameppal.pack(fill='both')
  framecerrar=Frame(otra_ventana)
  framecerrar.config(bg=color_fondo)
  framecerrar.pack(fill='both')
  boton_cerrar=Button(framecerrar, text='CERRAR', command=otra_ventana.destroy)
  boton_cerrar.config(bg=color_fondo, fg=color_letra)
  boton_cerrar.pack(fill='both')
  
  #obtner los datos
  conexion=sq3.connect('miBase.db') 
  micursor=conexion.cursor()
  query1='''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id LIMIT 30'''
  micursor.execute(query1)
  resultado=micursor.fetchall()
  cantidad_filas=len(resultado) #cantidad de filas
  cantidad_columnas=len(resultado[0]) #cantidad de columnas
  
  tabla=Table(frameppal)
  conexion.close()
  
  otra_ventana.mainloop()


def salirBBDD():
  resp=messagebox.askquestion("CONFIRMAR", "¿Desea salir de la Base de Datos?")
  if resp == 'yes':
    conexion.close()
    ventana.destroy()
    
#Limpiar
def limpiarPantalla():
  legajo.set("")
  apellido.set("")
  nombre.set("")
  email.set("")
  calificacion.set("")
  escuela.set("Selecione")
  localidad.set("")
  provincia.set("")
  legajo_input.config(state='normal')
  

#GRAFICAS
#por escuelas con función para contar
def alumnos_en_escuelas():
  query_buscar='''SELECT COUNT(alumnos.legajo) AS "total", escuelas.nombre FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id GROUP BY escuelas.nombre ORDER BY total DESC'''
  micursor.execute(query_buscar)
  resultado=micursor.fetchall()
  cuenta=[]
  escuela=[]
  for indice in resultado:
    cuenta.append(indice[0])
    escuela.append(indice[1])
  
  plt.bar(escuelas,cuenta)
  plt.xticks(rotation=90)
  plt.show()

#por notas
def alumnos_notas():
  query_buscar='''SELECT COUNT(alumnos.legajo) AS "total", nota FROM alumnos GROUP BY nota ORDER BY total DESC'''
  micursor.execute(query_buscar)
  resultado=micursor.fetchall()
  cuenta=[]
  nota=[]
  for indice in resultado:
    cuenta.append(indice[0])
    nota.append(indice[1])
  
  plt.bar(nota,cuenta)
  plt.show()


#MENU ACERCA DE...
def mostrar_licencia():
  msg= '''Sistema CRUD en Python
    Copyright (C) 2023 - xxxxx xxxx
    Email: and.bergna@gmail.com\n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
  messagebox.showinfo('LICENCIA', msg)

def mostrar_acerca_de():
  messagebox.showinfo("ACERCA DE...", "Creado por Bergna Andrea C.\npara Codo a Codo 4.0-Big Data I\nJunio 2023\nEmail: and.bergna@gmail.com")

  
#FUNCIONES CRUD
#CREAR
def crear():
  id_escuela= int(buscar_escuela(True)[0])
  datos= id_escuela, legajo.get(), apellido.get(), nombre.get(), calificacion.get(), email.get()
  micursor.execute("INSERT INTO alumnos (id_escuela, legajo, apellido, nombre, nota, email) VALUES (?,?,?,?,?,?)", datos)
  conexion.commit()
  messagebox.showinfo('ESTADO', 'Registro agregado')
  
#BUSCAR
def buscar_legajo():
  query_buscar= '''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela=escuelas._id WHERE legajo='''
  micursor.execute(query_buscar + legajo.get())
  resultado=micursor.fetchall()
  if resultado == []:
    messagebox.showerror('¡ERROR!', 'El número de legajo existe')
    legajo.set("")
  else:
    for campo in resultado:
      legajo.set(campo[0])
      apellido.set(campo[1])
      nombre.set(campo[2])
      calificacion.set(campo[3])
      email.set(campo[4])
      escuela.set(campo[5])
      localidad.set(campo[6])
      provincia.set(campo[7])
      legajo_input.config(state='disabled') #Desabilita el campo/ inhabilitado


#ACTUALIZAR
def actualilzar():
  id_escuela= int(buscar_escuela(True)[0])
  datos= id_escuela, apellido.get(), nombre.get(), calificacion.get(), email.get()
  micursor.execute("UPDATE alumnos SET id_escuela=?, apellido=?, nombre=?, nota=?, email=? WHERE legajo=" + legajo.get(), datos)
  conexion.commit()
  messagebox.showinfo('ESTADO', 'Se han actualizado los datos')
  limpiarPantalla()


#BORRAR
def borrar_datos():
  resp=messagebox.askquestion('BORRAR', '¿Desea eliminar el registro?')
  if resp == 'yes':
    micursor.execute('DELETE FROM alumnos WHERE legajo='  + legajo.get())
    conexion.commit()
    messagebox.showinfo('ESTADO', 'Registro eliminado')
    limpiarPantalla()


#Función Varias
def buscar_escuela(actualiza): 
  conexion=sq3.connect('miBase.db')
  micursor=conexion.cursor()
  if actualiza:
    micursor.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre=?', (escuela.get(),)) #Elemento fantasma
    
  else: #llena la lista del desplegable
    micursor.execute('SELECT nombre FROM escuelas')
  
  #lista de tuplas
  resultado= micursor.fetchall()
  retorno=[]
  for elemento in resultado:
    if actualiza:
      localidad.set(elemento[1])
      provincia.set(elemento[2])
    esc= elemento[0]
    retorno.append(esc)
  conexion.close()
  return retorno




'''
******************************
INTERFAZ GRAFICA
******************************
'''

#Colores
color_fondo='pink'
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
bbddmenu.add_command(label='Conectar a la BBDD', command=conectarBBDD)
bbddmenu.add_command(label='Listado de alumnos', command=listar)
bbddmenu.add_command(label='Salir', command=salirBBDD)

#Menú de gráficas
graficamenu=Menu(barramenu, tearoff=0)
graficamenu.add_command(label='Alumnos por escuela', command=alumnos_en_escuelas)
graficamenu.add_command(label='Calificaciones', command=alumnos_notas)

#Menú limpiar
limpiaventana=Menu(barramenu, tearoff=0)
limpiaventana.add_command(label='Limpiar', command=limpiarPantalla)

#Menú de descripción
info=Menu(barramenu,tearoff=0)
info.add_command(label='Licencia', command=mostrar_licencia)
info.add_command(label='Acerca de...', command=mostrar_acerca_de)

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

#Campo desplegable
escuelas=buscar_escuela(False)
escuela.set("Seleccione")
escuela_opcion=OptionMenu(framecampos, escuela, *escuelas)
escuela_opcion.grid(row=5, column=1, padx=10, pady=10, ipadx=50, sticky='w')

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
  
boton_crear= Button(framebotones, text='Crear', command=crear)
config_bottons(boton_crear,0)
boton_buscar= Button(framebotones, text='Buscar', command=buscar_legajo)
config_bottons(boton_buscar,1)
boton_actualizar= Button(framebotones, text='Actualizar', command=actualilzar)
config_bottons(boton_actualizar,2)
boton_borrar= Button(framebotones, text='Borrar', command=borrar_datos)
config_bottons(boton_borrar,3)

#Frame al pie de página
framecopy=Frame(ventana)
framecopy.config(bg=color_letra)
framecopy.pack(fill='both')
copylabel=Label(framecopy,text='(2023) por Bergna Andrea C., para CaC/Big Data I')
copylabel.config(bg=color_letra, fg=color_blanco)
copylabel.grid(row=0, column=0, padx=10, ipadx=12)

ventana.mainloop()