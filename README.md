# Practica 1: Sinhue Garcia Gil

Practica 1 con parte opcional incluida, cada productor tiene su propio buffer que puede ser variable.

Numero de productores, minimo y maximo de produccion y minimo y maximo de buffer como constantes globales para ser modificados como fuera necesario.

Hay un assert sobre el numero de productores, aunque la cantidad de productores (procesos) que se pueden llevar a cabo a al vez depende del ordenador. El incluido en el codigo es para mi ordenador.

## Correccion

Se ha incluido un Lock para que controle las secciones criticas, en particular las 3 secciones criticas de la correccion. Ya comentamos en una tutoria que no era necesario ya que accedia a distintos elementos de la lista, pero comentaste que era mejor ponerlo.