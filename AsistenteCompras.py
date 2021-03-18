import os
import msvcrt
import sqlite3
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import sys
found=set()
conexion=sqlite3.connect("product.db")
cursor=conexion.cursor()

#cursor.execute("CREATE TABLE productos (Codigo VARCHAR(10),Nombre VARCHAR(50),Precio REAL,Cantidad INTEGER,Pasillo INTEGER,Categoria VARCHAR(15))")

def ingresoProductos(codigo,producto,precio,cantidad,pasillo,categoria):
    infoprod=[(codigo,producto,precio,cantidad,pasillo,categoria)]
    cursor.executemany("INSERT INTO productos VALUES(?,?,?,?,?,?)",infoprod)
    conexion.commit()
    
    

def menu():
    opcion=4
    while (opcion!=0):
        print("1.Cliente\n2.-Administrador\n3.-Salir\n")
        opcion= int(input("Ingrese una opcion\n"))
        os.system("cls")
        if (opcion==1):
            menu_2(opcion)
        elif(opcion==2):
            password=123
            pw=int(input("Ingrese la contraseña: "))
            os.system("cls")
            while(pw!=password):
                pw=int(input("Ingrese la contraseña correcta"))
                os.system("cls")
            menu_2(opcion)
        elif(opcion==3):
            opcion=0
            os.system("cls")
        else:
            print("Ingrese una opcion correcta")
def menu_2(op):
    if op==1:
        op1=7
        while(op1!=5):
            os.system("cls")
            print("1.-Registrar datos\n2.-Buscar por teclado\n3.-Añadir un producto\n4.-Canasta\n5.-Atras\n")
            op1=int(input("Ingrese una opcion\n"))
            os.system("cls")
            if(op1==1):
                usuario(op1)
            elif(op1==2):
                usuario(op1)
            elif(op1==3):
                usuario(op1)
            elif(op1==4):
                print(found)
                msvcrt.getch()
            elif(op1==5):
                os.system("cls")
                pass
    elif op==2:
        op_admin=6
        while (op_admin!=5):
            print("1.-Ingreso de productos\n2.-Consulta de productos\n3.-Eliminar productos\n4.-Modificar productos\n5.-Atras")
            op_admin=int(input("Ingrese una opcion:\n"))
            os.system("cls")
            if(op_admin==1):
                admin(op_admin)
                os.system("cls")
            if(op_admin==2):
                admin(op_admin)
                msvcrt.getch()
                os.system("cls")
            if(op_admin==3):
                admin(op_admin)
            if(op_admin==4):
                admin(op_admin)
            if(op_admin==5):
                os.system("cls")
                pass

def usuario(op):
    if op==1:
        print("Bienvenido al asistente  de compras\n")
        nombre=str(input("Ingrese su nombre: "))
        apellido=str(input("Ingrese su apellido: "))
        cedula=str(input("Ingrese su cedula: "))
        os.system("cls")
    elif op==2:
        prod=str(input("Ingrese el producto que desea buscar: ")).upper()
        encontrar(prod)
        msvcrt.getch()
        os.system("cls")
    elif op==3:
        print("[INFO] Inicializando camara")
        vs=VideoStream(src=0).start()
        time.sleep(1.0)
        
        while True:
            frame=vs.read()
            frame=imutils.resize(frame,width=400)
            barcodes=pyzbar.decode(frame)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData=str(barcode.data.decode("utf-8"))
                if barcodeData not in found:
                    print("Para el producto "+barcodeData)
                    cantidad=int(input("Ingrese la cantidad"))
                    found.add(barcodeData)
                  
            cv2.imshow("Scanner Codigo de barras",frame)
            key=cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        print("[INFO] limpiando...")
        cv2.destroyAllWindows()
        vs.stop()
        os.system("cls")

        

    elif op==4:
        os.system("cls")


def admin(op):
    if op==1:
        cod=str(input("Ingrese el codigo del producto: "))
        prod=str(input("Ingrese el nombre del producto: ")).upper()
        pre=float(input("Ingrese el precio del producto: "))
        cant=int(input("Ingrese las existencias: "))
        pas=int(input("Ingrese el pasillo en el que se encuentra el producto: "))
        cat=str(input("Ingrese la categoria a la que pertenece el producto: "))
        ingresoProductos(cod,prod,pre,cant,pas,cat)
        os.system("cls")
    elif op==2:
        print("Codigo\tNombre\tPrecio\tExistencias\tPasillo\tCategoria\n")
        cursor.execute("SELECT * FROM productos")
        productos=cursor.fetchall()
        for producto in productos:
            print("{0}\t{1}\t{2}\t\t{3}\t{4}\t{5}".format(producto[0],producto[1],producto[2],producto[3],producto[4],producto[5]))

    elif op==3:
        producto=str(input("Ingrese el codigo del producto que desea eliminar")).upper()
        info=[(producto)]
        cursor.execute("DELETE FROM productos WHERE Codigo=?",(info))
        os.system("cls")
        conexion.commit()
    elif op==4:
        os.system("cls")
        prod=str(input("Ingrese el nombre del producto a modificar: ")).upper()
        cursor.execute("SELECT * FROM productos")
        productos=cursor.fetchall()
        for producto in productos:
            if producto[1]==prod:
                opmod=int(input("Que desea modificar\n1.-Codigo\n2.-Nombre\n3.-Precio\n4.-Existencias\n5.-Pasillo\n6.-Categoria\n7.-Todo\n"))
                if opmod==1:
                    cod=str(input("Ingrese el codigo: "))
                    cursor.execute("UPDATE productos SET Codigo=? WHERE Nombre=?",(cod,prod))
                    conexion.commit()
                elif opmod==2:
                    nom=str(input("Ingrese el nombre: ")).upper()
                    cursor.execute("UPDATE productos SET Nombre=? WHERE Nombre=?",(nom,prod))
                    conexion.commit()
                elif opmod==3:
                    precio=float(input("Ingrese el precio: "))
                    cursor.execute("UPDATE productos SET Precio=? WHERE Nombre=?",(precio,prod))
                    conexion.commit()
                elif opmod==4:
                    exist=int(input("Ingrese las existencias: "))
                    cursor.execute("UPDATE productos SET Cantidad=? WHERE Nombre=?",(exist,prod))
                    conexion.commit()
                elif opmod==5:
                    pas=int(input("Ingrese el pasillo: "))
                    cursor.execute("UPDATE productos SET Pasillo=? WHERE Nombre=?",(pas,prod))
                    conexion.commit()
                elif opmod==6:
                    cat=str(input("Ingrese la categoria: "))
                    cursor.execute("UPDATE productos SET Categoria=? WHERE Nombre=?",(cat,prod))
                    conexion.commit()
                elif opmod==7:
                    cod=str(input("Ingrese el codigo: "))
                    nom=str(input("Ingrese el nombre: ")).upper()
                    precio=float(input("Ingrese el precio: "))
                    exist=int(input("Ingrese las existencias: "))
                    pas=int(input("Ingrese el pasillo: "))
                    cat=str(input("Ingrese la categoria: "))
                    cursor.execute("UPDATE productos SET Codigo=?,Nombre=?,Precio=?,Cantidad=?,Pasillo=?,Categoria=? WHERE Nombre=?",(cod,nom,precio,exist,pas,cat,prod))
                    conexion.commit()
        os.system("cls")



menu()
