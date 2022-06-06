from cmath import sin
import copy
import pprint
import math
import numpy as np
from pandas import array

#set the random seed to 123
np.random.seed(1234)

################################################
# DATOS DE ENTRADA PARA REALIZAR LA SIMULACIÓN #
################################################

# defininir los datos de entrada
Matriz_A = [[0, 0, 1],
            [0, 1, 0],
            [1, 0, 0]]

# Errores q admite = 1
Matriz_G = [[1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1]]

n_columnas_G = len(Matriz_G[0])
n_filas_G = len(Matriz_G)

Matriz_H = [[1, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1], ]
n_filas_H = len(Matriz_H)
n_columnas_H = len(Matriz_H[0])
mgh = np.array(Matriz_H)

profundidad_intercalado = 5

# Mensaje de entrada
mensaje = "Lana"
# Definición de alfabeto
alf = "aábcdeé AÁBCDEÉfghiíjklmnFGHIÍJKLMNoópqrstuúvwxyzOÓPQRSTUÚVWXYZ.,;¿?¡!"
# la longitud binaria de este alfabeto es 7
longitud_minima_binaria = math.ceil(math.log(len(alf), 2))
print("Alfabeto: ", alf)
print("longitud del alfabeto:", len(alf))
print("longitud minima binaria:", longitud_minima_binaria)

# Codificación de la fuente
diccionario_decodificacion = dict()
posicion = 0
for palabra in alf:
    diccionario_decodificacion[palabra] = bin(
        posicion)[2:].zfill(longitud_minima_binaria)
    posicion += 1

#print("diccionario de decodificación:", diccionario_decodificacion)

mensaje_codificado_fuente = ""
for letra in mensaje:
    mensaje_codificado_fuente += diccionario_decodificacion[letra]

print("Longitud del mensaje codificado fuente:", len(mensaje_codificado_fuente))
print("Numero de caracteres del mensaje original:",
      len(mensaje_codificado_fuente)/longitud_minima_binaria)
print("Mensaje codificado fuente:", mensaje_codificado_fuente)    


# Creamos el string que contendrá el mensaje codificado linealmente
mensaje_codificado_fuente_dividido = [mensaje_codificado_fuente[i:i+n_filas_G]
                                      for i in range(0, len(mensaje_codificado_fuente), n_filas_G)]
mensaje_codificado_lineal = ""
for chunk in mensaje_codificado_fuente_dividido:
    if(len(chunk) == n_filas_G):
        #print("chunk:", chunk)
        # create an array with chunk
        chunk_array = np.array(list(chunk))
        # convert chunk_array to int
        chunk_array = chunk_array.astype(int)
        # multiply chunk_array by matriz_G
        mga = np.array(Matriz_G)
        chunk_array_multiplicado = np.dot(chunk_array, mga)
        # get the module 2 of chunk_array_multiplicado
        chunk_array_multiplicado = np.mod(chunk_array_multiplicado, 2)
        # add to mensaje_codificado_lineal all the elements of chunk_array_multiplicado as strings
        for i in range(0, len(chunk_array_multiplicado)):
            mensaje_codificado_lineal += str(chunk_array_multiplicado[i])
    else:
        # Cola
        print("Longitud de la cola:", len(chunk))
        mensaje_codificado_lineal += chunk

print("Longitud del mensaje codificado lineal:", len(mensaje_codificado_lineal))
print("La profundidad del intercalado es: " + str(profundidad_intercalado))

print("El mensaje codificado lineal que vamos a mandar es:")
for i in range(0, len(mensaje_codificado_lineal)):
    if(i % longitud_minima_binaria == 0 and i != 0):
        print(" ", end="")
    print(mensaje_codificado_lineal[i], end="")
print()


# Transmisión de lista por ráfagas
# Creamos un array de bloques de transmisión rxn simbolos

array_intercalado = []
array_intercalado = [mensaje_codificado_lineal[i:i+longitud_minima_binaria]
                     for i in range(0, len(mensaje_codificado_lineal), longitud_minima_binaria)]
# complete the last line of array_intercalado with "*" if it is not complete
if(len(array_intercalado[len(array_intercalado)-1]) < longitud_minima_binaria):
    for i in range(len(array_intercalado[len(array_intercalado)-1]), longitud_minima_binaria):
        array_intercalado[len(array_intercalado)-1] += "*"

# add len(array_intercalado) % profundidad_intercalado  rows of "*" to array_intercalado
for i in range(0, profundidad_intercalado - (len(array_intercalado) % profundidad_intercalado)):
    array_intercalado.append("*"*longitud_minima_binaria)

# add a line of "-" to array_intercalado between each profundidad_intercalado rows
puntos_de_corte = []
for i in range(0, len(array_intercalado)):
    if(i % (profundidad_intercalado) == 0):
        puntos_de_corte.append(i)

array_strings_bloques_transmision = []
for i in range(0, len(puntos_de_corte)):
    if(i == len(puntos_de_corte)-1):
        array_strings_bloques_transmision.append(
            array_intercalado[puntos_de_corte[i]:len(array_intercalado)])
    else:
        array_strings_bloques_transmision.append(
            array_intercalado[puntos_de_corte[i]:puntos_de_corte[i+1]])

abt = []
for i in range(0, len(array_strings_bloques_transmision)):
    bloque = []
    for j in range(len(array_strings_bloques_transmision[i])):
        linea_bloque = []
        for k in range(0, len(array_strings_bloques_transmision[i][j])):
            linea_bloque.append(array_strings_bloques_transmision[i][j][k])
        bloque.append(linea_bloque)
    abt.append(bloque)
print("Array de bloques de transmisión:")
pprint.pprint(abt)

# Como lo vamos a transmitir:
print("Mensaje que transmitiremos por el canal: ")
for i in range(0, len(abt)):
    for column in zip(*abt[i]):
        for element in column:
            print(element, end="")
print()

# extra
hay_cola = (abt[-1][-1][-1] == "*")

# TODO: introducir ruido random

prob_error = 1/20
ha_habido_error = False

capacidad_correctora = 1
max_long_rafaga = profundidad_intercalado * capacidad_correctora
num_errores = 0


for i in range(0, len(abt)):
    for k in range(0, len(abt[i][j])):
        for j in range(0, len(abt[i])):
            if(np.random.random() < prob_error):
                prob_error = 1
                ha_habido_error = True
                if(num_errores < max_long_rafaga):
                    if(abt[i][j][k] != "*"):
                        abt[i][j][k] = str(np.random.randint(0, 2))
                        #abt[i][j][k] = "x"
                    num_errores += 1
    num_errores = 0
    prob_error = 1/20

print("Mensaje tras introducir error: ")
for i in range(0, len(abt)):
    for column in zip(*abt[i]):
        for element in column:
            print(element, end="")
print()
#print("¿Ha habido algún error al transmitir el mensaje? " + str(ha_habido_error))

# Deshacemos las rafagas

mensaje_codificado_y_enviado = []
for i in range(0, len(abt)):
    for j in range(0, len(abt[i])):
        for k in range(0, len(abt[i][j])):
            if(abt[i][j][k] != "*"):
                mensaje_codificado_y_enviado.append(abt[i][j][k])
print("Deshacemos las ráfagas y obtenemos este mensaje:")
for i in mensaje_codificado_y_enviado:
    print(i, end="")
print()
#print(mensaje_codificado_y_enviado)

# Corregir ruido
print("Recibimos mensaje y corregimos ruido: ")

# GENERAMOS TABLERO DE ERRORES PATRON
array_patron = []
for i in range(0, 2**n_columnas_H):
    array_patron.append(bin(i)[2:].zfill(n_columnas_H))
# print("Array de patrones:")
# #print(array_patron)
# for i in array_patron:
#     print(f"{array_patron.index(i)}:{i}")

# for each string in array_patron convert it to a column matrix
errores_patron = dict()
for i in range(0, len(array_patron)):
    error_matrix = np.array(list(array_patron[i]), dtype=int).T
    sindrome_error = np.dot(mgh, error_matrix)
    sindrome_error = np.mod(sindrome_error, 2)
    # get a string of the sindrome error
    sindrome_error_string = ""
    for j in range(0, len(sindrome_error)):
        sindrome_error_string += str(sindrome_error[j])
    # add to errores_patron array_patron[1] as key and the sindrome_error_string as value
    # check if errores_patron has the key
    if(sindrome_error_string not in errores_patron):
        errores_patron[sindrome_error_string] = (array_patron[i])
    else:
        # count the number of 1s in errores_patron[sindrome_error_string]
        count_patron = 0
        for j in range(0, len(errores_patron[sindrome_error_string])):
            if(errores_patron[sindrome_error_string][j] == "1"):
                count_patron += 1
        # count the number of 1s in array_patron[i]
        count_candidato = 0
        for j in range(0, len(array_patron[i])):
            if(array_patron[i][j] == "1"):
                count_candidato += 1
        # if count_patron > count_candidato, replace the value of errores_patron[sindrome_error_string] with array_patron[i]
        if(count_patron > count_candidato):
            errores_patron[sindrome_error_string] = (array_patron[i])


print("Tablero de errores patron incompleto con sus síndromes:")
#print(errores_patron)
for i in errores_patron:
    print(f"{errores_patron.get(i)}:{i}")

mensaje_corregido = []


for i in range(0, len(mensaje_codificado_y_enviado), n_columnas_H):
    # divide mensaje_codificado_y_enviado in chunks of n_columnas_H
    chunk = mensaje_codificado_y_enviado[i:i+n_columnas_H]
    # make a string with the elements of chunk
    chunk_string = ""
    for j in range(0, len(chunk)):
        chunk_string += chunk[j]
    # make a column matrix of the chunk
    chunk_matrix_col = np.array([chunk]).T
    # make chunk_matrix_col a int matrix
    chunk_matrix_col = chunk_matrix_col.astype(int)
    # if chunk_matrix_col has not n_columnas_H rows, do nothing
    if(chunk_matrix_col.shape[0] != n_columnas_H):
        for i in range(0, len(chunk)):
            mensaje_corregido.append(chunk[i])

    else:
        # multiply chunk_matrix_col by mgh
        sindrome_palabra = np.dot(mgh, chunk_matrix_col)
        # get chunk_matrix_col_multiplicado in module 2
        sindrome_palabra = np.mod(sindrome_palabra, 2)
        # if chunk_matrix_col_multiplicado is all 0, add chunk to mensaje_corregido
        # sum all elements of sinrom_palabra
        suma_sindrome_palabra = 0
        for i in range(0, len(sindrome_palabra)):
            suma_sindrome_palabra += sindrome_palabra[i]
        if(suma_sindrome_palabra == 0):
            for i in range(0, len(chunk)):
                mensaje_corregido.append(chunk[i])
        else:
            # Error aquí
            # get a string of the sindrome_palabra
            sindrome_palabra_string = ""
            for j in range(0, len(sindrome_palabra)):
                for i in range(0, len(sindrome_palabra[j])):
                    sindrome_palabra_string += str(sindrome_palabra[j][i])
            # check if errores_patron has the key
            if(sindrome_palabra_string in errores_patron):
                error_patron = errores_patron[sindrome_palabra_string]
                # substract error_patron to mensaje_corregido
                palabra_corregida = ""
                # for each position in chunk_string, subtract the value of error_patron at the same position
                for i in range(0, len(chunk_string)):
                    value_chunk = int(chunk_string[i])
                    value_error_patron = int(error_patron[i])
                    value_position = np.mod(
                        value_chunk - value_error_patron, 2)
                    palabra_corregida += str(value_position)
                # add palabra_corregida to mensaje_corregido
                for i in range(0, len(palabra_corregida)):
                    mensaje_corregido.append(palabra_corregida[i])

print("Mensaje corregido: ")
for i in mensaje_corregido:
    print(i, end="")
print()

# Decodificación lineal
print("Comenzamos la decodifición lineal")

# COMENZAMOS PASO 3 - DECODIFICACION LINEAL (SIN RUIDO)
# Dividimos en trozos iguales que el numero de columnas de G
mensaje_codificado_lineal_dividido = []
palabra_codificada_lineal = []
columna = 0
contador = 0
for i in range(0, len(mensaje_corregido)):
    palabra_codificada_lineal.append(mensaje_corregido[i])
    contador += 1
    if(contador == n_columnas_G):
        contador = 0
        mensaje_codificado_lineal_dividido.append(palabra_codificada_lineal)
        palabra_codificada_lineal = []
mensaje_codificado_lineal_dividido.append(palabra_codificada_lineal)


# Ahora tenemos en mensaje_codificado_dividido cada fila con 6 bits
print(f"Dividimos el mensaje en trozos de longitud {n_columnas_G}")
pprint.pprint(mensaje_codificado_lineal_dividido)
# print(len(mensaje_codificado))

# Ahora sacamos los n_filas_G primeros bits (porque G es de la forma ID|A)
mensaje_codificado_binario = []
contador = 0
for fila in mensaje_codificado_lineal_dividido:
    if(len(fila) < n_columnas_G):
        for i in fila:
            mensaje_codificado_binario.append(i)
    else:
        for i in range(0, n_filas_G):
            mensaje_codificado_binario.append(fila[i])
print(
    f"Como G es de forma estándar, sacamos los {n_filas_G} primeros bits de cada trozo")
#print(mensaje_codificado_binario)
for i in mensaje_codificado_binario:
    print(i, end="")
print()

# Ahora sacamos el diccionario para decodificar segund alf
diccionario_decodificacion = dict()
posicion = 0
for palabra in alf:
    diccionario_decodificacion[palabra] = '{0:07b}'.format(posicion)
    posicion += 1

# print("Usaremos el siguiente diccionario de decodificación:")
# pprint.pprint(diccionario_decodificacion)

mensaje_codificado_binario_dividido = []
palabra_codificada_binario = []
columna = 0
contador = 0
for i in range(0, len(mensaje_codificado_binario)):
    palabra_codificada_binario.append(mensaje_codificado_binario[i])
    contador += 1
    if(contador == longitud_minima_binaria):
        contador = 0
        mensaje_codificado_binario_dividido.append(palabra_codificada_binario)
        palabra_codificada_binario = []

# pprint.pprint(mensaje_codificado_binario_dividido)

diccionario_invertido = {v: k for k, v in diccionario_decodificacion.items()}
# AHORA POR CADA POSICION SACAR NUMERO
palabra_en_binario = str()
mensaje_final = str()
contador = 0
# pprint.pprint(mensaje_codificado_binario_dividido)
for fila in mensaje_codificado_binario_dividido:
    for numero in fila:
        palabra_en_binario += str(numero)
    mensaje_final += str(diccionario_invertido[palabra_en_binario])

    palabra_en_binario = str()

print("Tras decodificar la fuente, el mensaje final es: ", mensaje_final)
