import csv
import json

# Nombre de archivo CSV de entrada y JSON de salida
csv_file = 'resultado_pruebita2.csv'         # Cambia esto por el nombre real de tu archivo CSV
json_file = 'datos.json'       # Nombre del archivo JSON de salida

# Leer el CSV y convertir a lista de diccionarios
with open(csv_file, mode='r', encoding='latin-1') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Escribir la lista en formato JSON
with open(json_file, mode='w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Archivo convertido exitosamente a {json_file}")
