import csv

# Función para convertir la duración a segundos (formato mm:ss:zz)
def convert_duration_to_seconds(duration):
    # Dividir la duración por los dos puntos ":"
    parts = duration.split(":")
    
    # Asegurarnos de que el formato es correcto (xx:yy:zz)
    if len(parts) == 3:
        m, s, _ = map(int, parts)  # Tomamos minutos y segundos, y desechamos los milisegundos
        total_seconds = (m * 60) + s  # Convertimos los minutos a segundos y sumamos los segundos
    else:
        return 0  # Si el formato no es correcto, devolvemos 0 segundos
    
    return total_seconds

# Leer el archivo CSV, procesar la última columna y guardar el resultado
def process_csv(input_file, output_file):
    # Cambiar a 'latin1' para manejar caracteres especiales
    with open(input_file, 'r', newline='', encoding='latin1') as infile:
        # Especificamos el delimitador como punto y coma ';'
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = reader.fieldnames
        
        # Imprimir los encabezados para ver si hay algo raro
        print(f"Encabezados del archivo CSV: {fieldnames}")
        
        # Comprobar que hay al menos una columna
        if len(fieldnames) == 0:
            print("No hay columnas en el archivo CSV.")
            return
        
        # Procesar la última columna
        last_column = fieldnames[-1]  # Tomar la última columna
        
        with open(output_file, 'w', newline='', encoding='latin1') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            
            # Escribir los encabezados en el archivo de salida
            writer.writeheader()
            
            for row in reader:
                # Obtener el valor de la última columna y convertirlo a segundos
                row[last_column] = convert_duration_to_seconds(row[last_column])
                
                # Escribir la fila procesada
                writer.writerow(row)
            
    print(f"Archivo procesado y guardado como '{output_file}'.")

# Llamada a la función con los archivos de entrada y salida
input_file = 'C:/Users/Alexv/Downloads/pruebita2.csv'  # Ruta del archivo CSV de entrada
output_file = 'resultado_pruebita2.csv'  # Nombre del archivo CSV de salida

process_csv(input_file, output_file)
