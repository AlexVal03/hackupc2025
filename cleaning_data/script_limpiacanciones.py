import pandas as pd
import csv
import os
import sys
import datetime
import argparse

def eliminar_filas_con_interrogantes(archivo_csv):
    """
    Lee un archivo CSV y elimina todas las filas que contienen signos de interrogación.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV
        
    Returns:
        DataFrame: DataFrame sin las filas que contienen interrogantes
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
                            print(f"  Filas originales: {len(df)}")
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
                            print(f"  Filas originales: {len(df)}")
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
        return None
    
    # Filtrar las filas que contienen interrogantes
    filas_antes = len(df)
    
    # Convertir todos los valores a string para poder buscar interrogantes
    df_str = df.astype(str)
    
    # Filtrar filas que contienen '?' en cualquier columna
    df_filtrado = df[~df_str.apply(lambda row: row.str.contains('\?', regex=True).any(), axis=1)]
    
    filas_despues = len(df_filtrado)
    filas_eliminadas = filas_antes - filas_despues
    
    print(f"Filas originales: {filas_antes}")
    print(f"Filas eliminadas con interrogantes: {filas_eliminadas}")
    print(f"Filas restantes: {filas_despues}")
    
    return df_filtrado, encoding, separador_detectado

if __name__ == "__main__":
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Elimina filas con interrogantes de un CSV')
    parser.add_argument('archivo', nargs='?', help='Ruta al archivo CSV')
    parser.add_argument('-o', '--output', help='Nombre del archivo de salida')
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
    
    # Ejecutar la función
    print("\nProcesando archivo...")
    resultado = eliminar_filas_con_interrogantes(archivo)
    
    if resultado:
        df_filtrado, encoding, separador = resultado
        
        # Determinar el archivo de salida
        if args.output:
            archivo_salida = args.output
        else:
            # Generar nombre para archivo de salida
            base_name = os.path.splitext(os.path.basename(archivo))[0]
            fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"{base_name}_sin_interrogantes_{fecha_hora}.csv"
        
        # Determinar si guardar
        guardar = args.auto_save
        if not guardar:
            respuesta = input(f"\n¿Quieres guardar el archivo filtrado en '{archivo_salida}'? (s/n): ").strip().lower()
            guardar = respuesta.startswith('s')
        
        if guardar:
            # Guardar como CSV manteniendo el mismo formato del original
            df_filtrado.to_csv(archivo_salida, index=False, encoding=encoding, sep=separador)
            print(f"Archivo filtrado guardado en: {archivo_salida}")
    else:
        print("No se pudo procesar el archivo. Revisa los errores anteriores.")