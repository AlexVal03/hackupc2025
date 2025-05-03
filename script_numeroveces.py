import pandas as pd
from collections import Counter
import csv

def contar_canciones(archivo_csv, columna_titulo='titulo'):
    """
    Analiza un archivo CSV y cuenta las repeticiones de cada título de canción.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV
        columna_titulo (str): Nombre de la columna que contiene los títulos (por defecto 'titulo')
    
    Returns:
        list: Lista de tuplas con formato (titulo_cancion, contador)
    """
    # Lista de codificaciones a probar
    encodings = ['latin1', 'utf-8', 'cp1252', 'iso-8859-1', 'utf-16']
    
    # Lista de separadores a probar
    separators = [',', ';', '\t', '|']
    
    print(f"Intentando leer el archivo: {archivo_csv}")
    
    # Probar diferentes combinaciones de codificación y separador
    for encoding in encodings:
        print(f"Probando codificación: {encoding}")
        
        # Intentar detectar el separador
        try:
            with open(archivo_csv, 'r', encoding=encoding) as f:
                content = f.read(1024)  # Leer los primeros 1024 bytes para analizar
                dialect = None
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(content)
                    has_header = sniffer.has_header(content)
                    print(f"  Detectado separador: '{dialect.delimiter}'")
                    print(f"  Detectado encabezado: {has_header}")
                    
                    # Intentar con el separador detectado primero
                    try:
                        df = pd.read_csv(archivo_csv, sep=dialect.delimiter, encoding=encoding, on_bad_lines='skip')
                        if not df.empty:
                            print(f"  ¡Éxito! Archivo leído con separador: '{dialect.delimiter}' y codificación: {encoding}")
                            print(f"  Columnas encontradas: {', '.join(df.columns)}")
                            break
                    except Exception as e:
                        print(f"  Error al leer con separador detectado: {str(e)}")
                except:
                    print("  No se pudo detectar automáticamente el formato. Probando separadores...")
                
                # Si no se pudo detectar o leer con el separador detectado, probar con los otros
                for sep in separators:
                    try:
                        df = pd.read_csv(archivo_csv, sep=sep, encoding=encoding, on_bad_lines='skip')
                        if not df.empty:
                            print(f"  ¡Éxito! Archivo leído con separador: '{sep}' y codificación: {encoding}")
                            print(f"  Columnas encontradas: {', '.join(df.columns)}")
                            break
                    except Exception as e:
                        continue
                else:
                    # Si llegamos aquí, ningún separador funcionó con esta codificación
                    continue
                
                # Si llega aquí, es porque encontró una combinación que funciona
                break
        except Exception as e:
            print(f"  Error con codificación {encoding}: {str(e)}")
            continue
    else:
        # Si llega aquí, ninguna combinación funcionó
        print("No se pudo leer el archivo con ninguna combinación de codificación y separador.")
        return []
    
    # Verificar si la columna existe
    if columna_titulo not in df.columns:
        print(f"¡Error! La columna '{columna_titulo}' no existe en el CSV.")
        print(f"Columnas disponibles: {', '.join(df.columns)}")
        return []
        
    # Obtener lista de títulos
    titulos = df[columna_titulo].tolist()
    print(f"Total de canciones encontradas: {len(titulos)}")
    
    # Filtrar valores nulos o vacíos
    titulos = [str(t).strip() for t in titulos if pd.notna(t) and str(t).strip()]
    print(f"Canciones válidas después de filtrar valores vacíos: {len(titulos)}")
    
    # Contar repeticiones
    contador = Counter(titulos)
    
    # Convertir a lista de tuplas (titulo, contador)
    resultado = [(titulo, conteo) for titulo, conteo in contador.items()]
    
    # Ordenar por frecuencia (mayor a menor)
    resultado.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Canciones únicas encontradas: {len(resultado)}")
    return resultado

# Ejemplo de uso
if __name__ == "__main__":
    import sys
    import os
    import datetime
    import argparse
    
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Contador de repeticiones de canciones en un CSV')
    parser.add_argument('archivo', nargs='?', help='Ruta al archivo CSV')
    parser.add_argument('-c', '--columna', help='Nombre de la columna con los títulos')
    parser.add_argument('-o', '--output', help='Guardar resultados en un archivo CSV')
    parser.add_argument('--auto-save', action='store_true', help='Guardar automáticamente sin preguntar')
    args = parser.parse_args()
    
    # Obtener la ruta del archivo
    if args.archivo:
        archivo = args.archivo
    else:
        archivo = input("Introduce la ruta completa del archivo CSV: ")
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        sys.exit(1)
    
    # Mostrar información del archivo
    print(f"\nAnalizando archivo: {archivo}")
    print(f"Tamaño del archivo: {os.path.getsize(archivo)} bytes")
    
    # Obtener el nombre de la columna
    if args.columna:
        nombre_columna = args.columna
    else:
        nombre_columna = input("Introduce el nombre de la columna con los títulos (por defecto 'titulo'): ").strip()
        if not nombre_columna:
            nombre_columna = "titulo"
    
    # Ejecutar la función
    print("\nProcesando archivo...")
    resultado = contar_canciones(archivo, nombre_columna)
    
    # Mostrar resultados
    if resultado:
        # Mostrar en consola
        print("\nResultados de conteo de canciones:")
        print("-" * 60)
        print(f"{'TÍTULO':<40} | {'REPETICIONES'}")
        print("-" * 60)
        
        for titulo, conteo in resultado:
            # Truncar títulos largos
            titulo_mostrado = titulo[:37] + "..." if len(titulo) > 40 else titulo
            print(f"{titulo_mostrado:<40} | {conteo}")
        
        print("\nEstadísticas:")
        print(f"- Total de entradas analizadas: {sum(count for _, count in resultado)}")
        print(f"- Títulos únicos encontrados: {len(resultado)}")
        if resultado:
            print(f"- Título más repetido: {resultado[0][0]} ({resultado[0][1]} veces)")
        
        # Determinar el archivo de salida
        if args.output:
            archivo_salida = args.output
        else:
            # Generar nombre para archivo de salida
            base_name = os.path.splitext(os.path.basename(archivo))[0]
            fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"{base_name}_resultados_{fecha_hora}.csv"
        
        # Determinar si guardar
        guardar = args.auto_save
        if not guardar:
            respuesta = input(f"\n¿Quieres guardar los resultados en '{archivo_salida}'? (s/n): ").strip().lower()
            guardar = respuesta.startswith('s')
        
        if guardar:
            # Crear DataFrame y guardar como CSV
            df_resultado = pd.DataFrame(resultado, columns=['Titulo_Cancion', 'Repeticiones'])
            df_resultado.to_csv(archivo_salida, index=False, encoding='utf-8')
            print(f"Resultados guardados en: {archivo_salida}")
    else:
        print("No se pudieron contar las canciones. Revisa los errores anteriores.")