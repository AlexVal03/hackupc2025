import pandas as pd
import csv
import os
import sys
import datetime
import argparse

def extraer_canciones_unicas(archivo_csv, columna_titulo='titulo'):
    """
    Extrae una lista de canciones únicas de un archivo CSV.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV
        columna_titulo (str): Nombre de la columna que contiene los títulos
    
    Returns:
        list: Lista de títulos únicos de canciones
    """
    # Lista de codificaciones a probar
    encodings = ['latin1', 'utf-8', 'cp1252', 'iso-8859-1', 'utf-16']
    
    # Lista de separadores a probar
    separators = [',', ';', '\t', '|']
    
    print(f"Intentando leer el archivo: {archivo_csv}")
    
    # Probar diferentes combinaciones de codificación y separador
    for encoding in encodings:
        print(f"Probando codificación: {encoding}")
        
        try:
            # Intentar detectar el separador
            with open(archivo_csv, 'r', encoding=encoding) as f:
                content = f.read(1024)
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(content)
                    separador_detectado = dialect.delimiter
                    print(f"  Detectado separador: '{separador_detectado}'")
                    
                    # Intentar primero con el separador detectado
                    try:
                        df = pd.read_csv(archivo_csv, sep=separador_detectado, encoding=encoding, on_bad_lines='skip')
                        if not df.empty:
                            print(f"  ¡Éxito! Archivo leído con separador: '{separador_detectado}' y codificación: {encoding}")
                            print(f"  Columnas encontradas: {', '.join(df.columns)}")
                            break
                    except Exception as e:
                        print(f"  Error con separador detectado: {str(e)}")
                except:
                    print("  No se pudo detectar el formato automáticamente. Probando separadores conocidos...")
                
                # Probar con separadores conocidos
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
                    # Si ningún separador funcionó con esta codificación
                    continue
                
                # Si llegamos aquí, encontramos una combinación que funciona
                break
        except Exception as e:
            print(f"  Error con codificación {encoding}: {str(e)}")
            continue
    else:
        # Si ninguna combinación funcionó
        print("No se pudo leer el archivo con ninguna codificación o separador.")
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
    
    # Mantener el orden original pero eliminar duplicados
    titulos_unicos = []
    titulos_vistos = set()
    
    for titulo in titulos:
        if titulo not in titulos_vistos:
            titulos_unicos.append(titulo)
            titulos_vistos.add(titulo)
    
    print(f"Canciones únicas encontradas: {len(titulos_unicos)}")
    
    return titulos_unicos

if __name__ == "__main__":
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Extractor de canciones únicas de un CSV')
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
    canciones_unicas = extraer_canciones_unicas(archivo, nombre_columna)
    
    # Mostrar resultados
    if canciones_unicas:
        # Mostrar en consola (limitado a 20 para no saturar)
        print("\nCanciones únicas encontradas:")
        print("-" * 60)
        
        for i, titulo in enumerate(canciones_unicas[:20], 1):
            print(f"{i}. {titulo}")
        
        if len(canciones_unicas) > 20:
            print(f"... y {len(canciones_unicas) - 20} más (total: {len(canciones_unicas)})")
        
        # Determinar el archivo de salida
        if args.output:
            archivo_salida = args.output
        else:
            # Generar nombre para archivo de salida
            base_name = os.path.splitext(os.path.basename(archivo))[0]
            fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"{base_name}_canciones_unicas_{fecha_hora}.csv"
        
        # Determinar si guardar
        guardar = args.auto_save
        if not guardar:
            respuesta = input(f"\n¿Quieres guardar las canciones únicas en '{archivo_salida}'? (s/n): ").strip().lower()
            guardar = respuesta.startswith('s')
        
        if guardar:
            # Crear DataFrame y guardar como CSV
            df_resultado = pd.DataFrame(canciones_unicas, columns=['Titulo_Cancion'])
            df_resultado.to_csv(archivo_salida, index=False, encoding='utf-8')
            print(f"Canciones únicas guardadas en: {archivo_salida}")
    else:
        print("No se pudieron extraer las canciones. Revisa los errores anteriores.")