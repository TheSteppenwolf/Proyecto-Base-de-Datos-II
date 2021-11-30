# Proyecto-Base-de-Datos-II

## Autor:
- Sebastián Felipe Tamayo Proaño

## Descripción

Este es el proyecto final de la materia de base de datos II, consiste en una integración con una base de datos en MongoDB con python realizando un CRUD para la manipulación de los datos.

El proyecto consiste en una simulación de control de ventas de una empresa a nivel nacional, en esta, se pueden observar las ventas de algún producto en cierta región, provincia y ciudad, así como cuando se vendio y cuanto dinero genero; a parte de ello, el programa permite al usuario realizar busquedas eficientes de cualquier producto, región, provincia y ciudad, además, permite visualizar la información por diversos tipos de orden como por mayor pvp, menor pvp, mayor cantidad vendida, menor cantidad vendida, mayor total generado y menor total generado. Por otra parte, el programa permite visualizar algún documento en una nueva pestaña en la cual se puede editar o eliminar el propio documento. Finalmente, el programa permite la creación de nuevos documentos.

## Lenguage de programación utilizado
- Python

## Principales paquetes utilizados
- Tkinter
- Pymongo

## Base de datos utilizada:
- MongoDB

## Modelo utilizado para la colección
- _id : Se refiere al identificador del documento
- producto : Se refiere al producto en venta
- pvp : Se refiere al precio de vente del producto
- region : Se refiere a la región donde ocurrieron las ventas
- provincia : Se refiere a la provincia donde ocurrieron las ventas
- ciudad : Se refiere a la ciudad donde ocurrieron las ventas
- cantidad_vendido : Se refiere a la cantidad de productos vendidos
- total_generado : Se refiere a la cantidad de dinero generado por las ventas. (pvp * cantidad_vendido)

## Fecha de realización
- 30/11/2021
