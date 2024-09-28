import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from time import time

def seleccionar_archivo(mensaje):
    showinfo("Selección de archivo", mensaje)
    return filedialog.askopenfilename()

def procesar_linea(linea):
    return {
        'CUIT': linea[0:11],
        'DENOMINACION': linea[11:41].strip(),
        'IMP GANANCIAS': linea[41:43],
        'IMP IVA': linea[43:45],
        'MONOTRIBUTO': linea[45:47],
        'INTEGRANTE SOC': linea[47],
        'EMPLEADOR': linea[48],
        'ACTIVIDAD': linea[50:52]
    }

def main():
    root = tk.Tk()
    root.withdraw()

    start = time()

    # Seleccionar y leer el archivo Excel con CUITs
    excel_file = seleccionar_archivo("Seleccione el archivo Excel con la lista de CUITs")
    df_excel = pd.read_excel(excel_file, dtype={'CUIT': str})
    df_excel['CUIT'] = df_excel['CUIT'].str.replace(r'[\.-]', '', regex=True).str.zfill(11)
    cuits_a_buscar = set(df_excel['CUIT'])

    # Seleccionar el archivo de texto del padrón
    txt_file = seleccionar_archivo("Seleccione el archivo de texto del padrón AFIP")

    # Procesar el archivo de texto
    registros_encontrados = []
    cuits_encontrados = set()
    try:
        with open(txt_file, 'r', encoding='ISO-8859-1') as file:  # Cambiar a ISO-8859-1
            for linea in file:
                registro = procesar_linea(linea)
                if registro['CUIT'] in cuits_a_buscar:
                    registros_encontrados.append(registro)
                    cuits_encontrados.add(registro['CUIT'])
    except UnicodeDecodeError:
        showinfo("Error", "No se pudo leer el archivo con la codificación especificada. Intenta con otra codificación.")

    # Crear DataFrame con los registros encontrados
    df_encontrados = pd.DataFrame(registros_encontrados)

    # Filtrar CUITs no encontrados
    df_no_encontrados = df_excel[~df_excel['CUIT'].isin(cuits_encontrados)]

    # Seleccionar dónde guardar el archivo de reporte
    output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                               initialfile="Reporte_AFIP_Padron.xlsx")

    # Ordenar el reporte según coincidentes / no coincidentes
    with pd.ExcelWriter(output_file) as writer:
        df_encontrados.to_excel(writer, sheet_name='Encontrados', index=False)
        df_no_encontrados.to_excel(writer, sheet_name='No Encontrados', index=False)

    end = time()
    showinfo("Proceso completado", 
             f"El proceso ha finalizado en {round(end - start, 2)} segundos.")

if __name__ == "__main__":
    main()
