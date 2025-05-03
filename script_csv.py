import csv

# Nombre del archivo de entrada
input_file = 'C:/Users/Alexv/Downloads/pruebita2.csv' # Cambia esto por el nombre de tu archivo CSV de entrada
output_file = 'prueba_salida2.csv'  # Cambia esto por el nombre del archivo de salida

# Abrir el archivo CSV de entrada para lectura
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    # Crear un lector CSV
    reader = csv.reader(infile)

    # Abrir el archivo de salida para escritura
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)

        # Leer cada fila del archivo CSV
        for row in reader:
            # Para cada columna de la fila, si contiene comas entre comillas, lo dejamos intacto
            new_row = []
            for col in row:
                # Si la columna tiene comillas dobles, procesar correctamente
                if '"' in col:
                    # Remover las comillas dobles si es necesario
                    col = col.replace('""', '"')  # Reemplazar comillas dobles dobles por una sola
                new_row.append(col)
            
            # Escribir la fila procesada en el archivo de salida
            writer.writerow(new_row)

print(f"Archivo procesado y guardado como {output_file}")
