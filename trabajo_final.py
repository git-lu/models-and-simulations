from random import random
from random import seed
import numpy as np
import matplotlib.pyplot as pltb
from collections import deque
seed(123)

class Banco():
    def __init__(
        self, 
        n_filas,
        n_cajas,
        lambda_cajas = [3,4],
        asignacion_filas = None,
        lambda_clientes = 6
        ):
        self.lambda_clientes = lambda_clientes
        self.n_cajas = n_cajas
        self.n_filas = n_filas
        self.lambda_cajas = lambda_cajas
        # Tiempo transcurrido
        self.t = 0
        # Clientes siendo atendidos en cada caja
        self.cajas_clientes = [0]*n_cajas
        # Cantidad de clientes actualmente en el banco
        self.clientes_actuales = 0
        # Clientes en cada fila
        self.filas = [deque()]*n_filas
        # Cantidad de clientes atendidos en cada caja
        self.atenciones_cajas = [0]*n_cajas
        # Cantidad de arribos de clientes
        self.n_arribos = 0
        # Tiempos de llegadas y egresos de los clientes
        self.clientes_llegadas = []
        self.clientes_salidas = []
        # Eventos del banco
        # Arribo proximo cliente
        self.llegada_prox_cliente = 0
        # Liberación de cajas
        self.liberacion_cajas = [np.infty]*n_cajas
        # Si #filas != #cajas, debemos asignar
        # a cada caja una fila.
        # En la posición i-esima del arreglo está la
        # fila en la cual los clientes se forman para la
        # caja i.
        self.asignacion_filas = asignacion_filas
        self.clientes_tiempo_promedio_atencion = []
        # Variables para comparar rendimiento
        self.clientes_esperando_t = []
        self.clientes_atendidos_t = []

    def exponencial(self,lamda):
        u = random()
        return -np.log(u)/lamda
    
    def servicio_caja(self,caja):
        lamda = self.lambda_cajas[caja]
        return self.exponencial(lamda)

    def simular_cliente(self):
        """
        Los clientes llegan al banco de acuerdo
        a un proceso de Poisson homogeneo con tasa
        lambda. 
        Este algoritmo devuelve el tiempo
        de llegada de un cliente pasados 
        s minutos
        """
        lamda = self.lambda_clientes
        self.llegada_prox_cliente = self.t + self.exponencial(lamda) 
        return self

    def guardar_estado_colas(self):
        # Guarda el estado de las colas en el momento actual
        clientes_en_colas = self.clientes_actuales - self.n_cajas
        self.clientes_esperando_t.append(clientes_en_colas)
        clientes_atendidos = sum(self.atenciones_cajas)
        self.clientes_atendidos_t.append(clientes_atendidos)
        return self


    def resetear_simulacion(self):
        # Tiempo transcurrido
        self.t = 0
        # Clientes siendo atendidos en cada caja
        self.cajas_clientes = [0]*self.n_cajas
        # Cantidad de clientes actualmente en el banco
        self.clientes_actuales = 0
        # Clientes en cada fila
        self.filas = [deque()]*self.n_filas
        # Cantidad de clientes atendidos en cada caja
        self.atenciones_cajas = [0]*self.n_cajas
        # Cantidad de arribos y salidas del banco
        self.n_arribos = 0
        self.n_salidas = 0
        # Tiempos de llegadas y egresos de los clientes
        self.clientes_llegadas = []
        self.clientes_salidas = []
        # Eventos del banco
        # Arribo proximo cliente
        self.llegada_prox_cliente = 0
        # Liberación de cajas
        self.liberacion_cajas = [np.infty]*self.n_cajas
        self.clientes_tiempo_promedio_atencion = []
        self.clientes_esperando_t = []
        self.clientes_atendidos_t = []
        self.SEED = 123
        return self

    def caja_finalizar_atencion(self,caja):
        """
        Cuando una caja finaliza de atender a un cliente
        actualizamos las siguientes variables
        """
        # Registramos a cual cliente estaba atendiendo la caja
        n_cliente = self.cajas_clientes[caja]
        # Actualizamos el tiempo de la simulación al tiempo
        # de liberacion de la caja
        self.t = self.liberacion_cajas[caja]
        # Contamos la atención de la caja
        self.atenciones_cajas[caja] += 1
        # Anotamos el horario de salida del cliente
        self.clientes_salidas[n_cliente] = self.t
        # Hay un cliente menos en el sistema
        self.clientes_actuales -= 1
        # La caja no está atendiendo a nadie
        self.cajas_clientes[caja] = 0
        # Reinicializamos el tiempo de atención
        self.liberacion_cajas[caja] = np.infty
        return self

    def caja_atender_siguiente(self,caja):
        fila_caja = self.asignacion_filas[caja]
        t = self.t
        # Si quedan clientes por atender, lo atendemos
        if len(self.filas[fila_caja]) > 0:
            # Elegimos al primer cliente de la fila
            n_cliente = self.filas[fila_caja].popleft()
            # Indicamos que estamos atendiendo a ese cliente
            self.cajas_clientes[caja] = n_cliente
            # Actualizamos el tiempo de finalización
            self.liberacion_cajas[caja] = t + self.servicio_caja(caja)
        return self

    def arribo_cliente(self):
        """
        El evento de llegada del proximo cliente
        es lo primero que ocurre
        """
        # Nos posicionamos en el tiempo en el cual
        # llega el cliente
        llegada_cliente = self.llegada_prox_cliente
        self.t = llegada_cliente
        # Contamos el arribo
        self.n_arribos += 1
        # Registramos el horario de llegada
        self.clientes_llegadas[self.n_arribos] = llegada_cliente
        # Atendemos al cliente recién llegado
        self.arribo_cliente_atencion()
        # Registramos que hay un nuevo cliente
        # en el banco
        self.clientes_actuales += 1
        # Registramos cuando va a suceder la próxima llegada
        self.simular_cliente()
        return self

    def arribo_cliente_atencion(self):
        """
        Cuando arriba un nuevo cliente, debemos
        ver si podemos atenderlo inmediatamente
        o bien debemos encolarlo
        """
        # Identificamos al cliente por su número de
        # llegada
        n_cliente = self.n_arribos
        # Si todas las cajas están ocupadas
        # encolamos al cliente
        if self.clientes_actuales >= self.n_cajas:
            self.encolar_cliente()
        # Sino, hay alguna caja en donde podemos atender
        # al nuevo cliente.
        else:
            # Sabemos que hay una caja libre, luego
            # elegimos la que tiene el menor numero
            # de cliente, que debería ser 0
            # y comenzamos a atender al cliente en esa 
            # caja
            caja_libre = np.argmin(self.cajas_clientes)
            # Nos aseguramos que efectivamente esa caja esté libre
            assert(self.cajas_clientes[caja_libre] == 0)
            # Marcamos que ahora hay un cliente en esa caja
            self.cajas_clientes[caja_libre] = n_cliente
            # Calculamos el tiempo finalizacion de atención de esa caja 
            self.liberacion_cajas[caja_libre] = self.t + self.servicio_caja(caja_libre)

        return self

    def encolar_cliente(self):
        """
        El cliente se encola en la fila
        mas corta
        """
        n_cliente = self.n_arribos
        # Calculamos el largo de las filas
        largos_filas = [len(fila) for fila in self.filas]
        # Elegimos la que menos personas tiene
        fila_mas_corta = np.argmin(largos_filas)
        # Agregamos al cliente al final de la fila más corta
        self.filas[fila_mas_corta].append(n_cliente)
        
        return self

    def simulacion(self,N_ARRIBOS,SEED=123):
        # Reseteamos las variables de la simulación
        self.resetear_simulacion()
        seed(SEED)
        # Inicializamos los arreglos de llegadas y salidas
        self.clientes_llegadas = [0]*(N_ARRIBOS+1)
        self.clientes_salidas = [0]*(N_ARRIBOS+1)
        # Simulamos el arribo del primer cliente
        self.simular_cliente()
    
        while sum(self.atenciones_cajas) < N_ARRIBOS:
            # Avanzamos en la simulación según cual
            # evento ocurre primero:

            # Si el proximo cliente llega antes que se
            # libere alguna caja
            if self.llegada_prox_cliente <= min(self.liberacion_cajas):
                # Si aun no llegamos al limite de clientes
                if self.n_arribos < N_ARRIBOS:
                    # Llega el cliente
                    self.arribo_cliente()
                    self.guardar_estado_colas()
                else:
                    # Sino, no deberían llegar más clientes
                    self.llegada_prox_cliente = np.infty
            # Si alguna caja se libera primero
            else:
                # Buscamos la caja que se libera antes
                caja = np.argmin(self.liberacion_cajas)
                # Terminamos la atención del cliente que estaba
                # siendo atendido
                self.caja_finalizar_atencion(caja)
                # Atendemos al siguiente de esa caja
                self.caja_atender_siguiente(caja)
        return self


    def tiempos_de_atencion(self):
        self.clientes_tiempo_promedio_atencion = np.array(self.clientes_salidas)\
             - np.array(self.clientes_llegadas)
        return self.clientes_tiempo_promedio_atencion