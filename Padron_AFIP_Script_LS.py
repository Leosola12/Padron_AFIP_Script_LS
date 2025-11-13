import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from time import time

def seleccionar_archivo(mensaje):
    messagebox.showinfo("Selección de archivo", mensaje)
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
        with open(txt_file, 'r', encoding='ISO-8859-1') as file:
            for linea in file:
                registro = procesar_linea(linea)
                if registro['CUIT'] in cuits_a_buscar:
                    registros_encontrados.append(registro)
                    cuits_encontrados.add(registro['CUIT'])
    except UnicodeDecodeError:
        messagebox.showinfo("Error", "No se pudo leer el archivo con la codificación especificada. Intenta con otra codificación.")
        return

    # Crear DataFrame con los registros encontrados
    df_encontrados = pd.DataFrame(registros_encontrados)

    # Filtrar CUITs no encontrados
    df_no_encontrados = df_excel[~df_excel['CUIT'].isin(cuits_encontrados)]

    # Generar reporte de coincidencias
    resumen = {
        "Total CUITs Excel": [len(df_excel)],
        "Coincidencias encontradas": [len(df_encontrados)],
        "No encontradas": [len(df_no_encontrados)],
        "Porcentaje de coincidencia (%)": [round(len(df_encontrados) / len(df_excel) * 100, 2)]
    }
    df_resumen = pd.DataFrame(resumen)

    # Guardar el archivo Excel final
    output_file = filedialog.asksaveasfilename(
        defaultextension=".xlsx", 
        initialfile="Reporte_AFIP_Padron.xlsx",
        title="Guardar reporte como..."
    )

    with pd.ExcelWriter(output_file) as writer:
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
        df_encontrados.to_excel(writer, sheet_name='Encontrados', index=False)
        df_no_encontrados.to_excel(writer, sheet_name='No Encontrados', index=False)

    end = time()
    messagebox.showinfo("Proceso completado", 
                        f"El proceso ha finalizado en {round(end - start, 2)} segundos.\n"
                        f"Archivo guardado en:\n{output_file}")

if __name__ == "__main__":
    main()
