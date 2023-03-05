from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Array, Manager
from multiprocessing import Semaphore
from random import randint

"""
Practica 1, PRPA 22/23
Sinhue Garcia Gil
"""


N_productores = 20
assert N_productores < 48 #Depende del ordenador
Min_produccion = 4
Max_produccion = 20
Min_buffer = 2
Max_buffer = 10

def prod(common,tid,cap,limit,sem_empty,sem_nonempty):
    valor=0
    ind=0 # Lugar donde produce el productor
    
    for _ in range(limit):
        valor += randint(0,100) #genara un entero siempre de forma creciente
        #print(f'{tid} : Ha obtenido valor')
        sem_empty.acquire()
        #print(f'{tid} : va a anadir valor {valor}')
        common[ind]=valor
        #print(f'{tid} : anade elemento {ind}')
        sem_nonempty.release()
        ind=(ind+1)%cap
        
    sem_empty.acquire() #Ya ha producido todo lo necesario, por lo que incluye un -1 para indicarlo
    common[ind]= -1
    #print(f'{tid} : anade elemento -1')
    sem_nonempty.release()
    #print(f'{tid} join and added on {i}')

def merge(common_list,res, indices, cap, sem_empty, sem_nonempty):
    cond=True # Hay procesos sin acabar
    ind=0 # marcará el tid que tiene el valor minimo cuando todos hayan producido
    
    for j in range(N_productores): #Primero comprobamos que todos productores han producido
        sem_nonempty[j].acquire()
    
    while cond:
        minimo=-1 #Reiniciamos el minimo
        for j in range(N_productores): #Miramos cual es el mínimo
            a=common_list[j][indices[j]]
            if  a>=0 and (minimo<0 or a<minimo): # comprueba si hay nuevo minimo y guarda el indice
                    minimo=a
                    ind=j
        if minimo==-1:
            cond=False #no había ningún número positivo, por lo que todos procesos habían acabado
        else: #consumimos el minimo
            sem_empty[ind].release()
            #print(f'merge añade de {ind} el valor {minimo}')
            indices[ind]=(indices[ind]+1)%cap[ind]
            res.append((minimo,f"prod:{ind}"))
            sem_nonempty[ind].acquire() #comprobamos que tiene elementos para consumir, el resto ya ha producido

            
    
def main():
    print("\nNumero de productores:", N_productores)
    print("Minimo de produccion:",Min_produccion)
    print("Maximo de produccion:",Max_produccion)
    print("Minimo buffer permitido:",Min_buffer)
    print("Maximo buffer permitido:",Max_buffer)
    
    lp = []
    capacidades = Array ('i',[0]*N_productores)
    producciones = Array ('i',[0]*N_productores)
    for i in range(N_productores):
        capacidades[i]=randint(Min_buffer,Max_buffer)
        producciones[i]=randint(Min_produccion,Max_produccion)
    common = [Array('i',[0]*(capacidades[i])) for i in range(N_productores)]
    semaforos_empty=[Semaphore(capacidades[i]) for i in range(N_productores)]
    semaforos_nonempty=[Semaphore(0) for _ in range(N_productores)]
    indices = Array ('i',[0]*N_productores)
    manager=Manager()
    res=manager.list()

    print("\nPropiedades de los productores:")
    
    for i in range(N_productores): print(f"productor {i}: buffer {capacidades[i]}, produce {producciones[i]}")
    
    for tid in range(N_productores):
        lp.append(Process(target=prod, args=(common[tid],tid,capacidades[tid], producciones[tid],
                                             semaforos_empty[tid], semaforos_nonempty[tid])))
    lp.append(Process(target=merge, args=(common, res, indices,capacidades,semaforos_empty,
                                          semaforos_nonempty)))
    for p in lp:
        p.start()
    for p in lp:
        p.join()

    print("\nTiene que producir:",sum(producciones),'\n')
    print(res)
    print("\nLongitud del resultado:",len(res))
    print ("\nFIN")


if __name__ == "__main__":
    main()
