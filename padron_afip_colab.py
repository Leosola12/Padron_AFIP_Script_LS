import pandas as pd
from google.colab import files
from time import time

# --- Función para interpretar cada línea del padrón ---
def procesar_linea(linea):
    return {
        'CUIT': linea[0:11],
        'DENOMINACION': linea[11:41].strip(),
        'IMP GANANCIAS': linea[41:43].strip(),
        'IMP IVA': linea[43:45].strip(),
        'MONOTRIBUTO': linea[45:47].strip(),
        'INTEGRANTE SOC': linea[47].strip(),
        'EMPLEADOR': linea[48].strip(),
        'ACTIVIDAD': linea[50:52].strip()
    }

def main():
    start = time()

    # === 1. Subir archivos ===
    print("📂 Subí el archivo Excel con la lista de CUITs:")
    uploaded_excel = files.upload()
    excel_filename = list(uploaded_excel.keys())[0]

    print("\n📄 Ahora subí el archivo de texto del padrón AFIP (.txt):")
    uploaded_txt = files.upload()
    txt_filename = list(uploaded_txt.keys())[0]

    # === 2. Leer Excel con CUITs ===
    df_excel = pd.read_excel(excel_filename, dtype={'CUIT': str})
    df_excel['CUIT'] = df_excel['CUIT'].str.replace(r'[\.-]', '', regex=True).str.zfill(11)
    cuits_a_buscar = set(df_excel['CUIT'])

    # === 3. Leer padrón TXT ===
    registros_encontrados = []
    cuits_encontrados = set()
    with open(txt_filename, 'r', encoding='ISO-8859-1') as file:
        for linea in file:
            registro = procesar_linea(linea)
            if registro['CUIT'] in cuits_a_buscar:
                registros_encontrados.append(registro)
                cuits_encontrados.add(registro['CUIT'])

    df_encontrados = pd.DataFrame(registros_encontrados)
    df_no_encontrados = df_excel[~df_excel['CUIT'].isin(cuits_encontrados)]

    # === 4. Mapas de códigos AFIP ===
    map_gan = {
        'NI':'No Inscripto','AC':'Activo','EX':'Exento','NC':'No corresponde',
        'NA':'No alcanzado','XN':'Exento no alcanzado','AN':'Activo no alcanzado'
    }
    map_iva = {
        'NI':'No Inscripto','AC':'Activo','EX':'Exento',
        'NA':'No alcanzado','XN':'Exento no alcanzado','AN':'Activo no alcanzado'
    }
    map_mono = {
        'BT':'Trabajador promovido','AP':'Actividad primaria','AC':'Asociado a cooperativa',
        'AL':'Monotributo social locación','AV':'Monotributo social ventas',
        'AT':'Trabajador promovido','NI':'No inscripto'
    }
    map_soc = {'N':'No activo','S':'Activo'}
    map_emp = {'N':'No empleador','S':'Empleador activo'}
    map_act = {
        '00':'No es monotributista','01':'Comercial','02':'Profesional','03':'Servicios/Oficio',
        '04':'Industrial','05':'Agropecuaria','06':'Otros','07':'Eventual',
        '08':'Prest. de Servicio o Locación','09':'Otras actividades','10':'Ventas','11':'Agricultura Familia'
    }

    # === 5. Agregar descripciones legibles ===
    if not df_encontrados.empty:
        df_encontrados['GANANCIAS_DESC'] = df_encontrados['IMP GANANCIAS'].map(map_gan)
        df_encontrados['IVA_DESC'] = df_encontrados['IMP IVA'].map(map_iva)
        df_encontrados['MONOTRIBUTO_DESC'] = df_encontrados['MONOTRIBUTO'].map(map_mono)
        df_encontrados['INTEGRANTE_DESC'] = df_encontrados['INTEGRANTE SOC'].map(map_soc)
        df_encontrados['EMPLEADOR_DESC'] = df_encontrados['EMPLEADOR'].map(map_emp)
        df_encontrados['ACTIVIDAD_DESC'] = df_encontrados['ACTIVIDAD'].map(map_act)

    # === 6. Crear hoja Resumen ===
    total_cuits = len(df_excel)
    total_encontrados = len(df_encontrados)
    total_no_encontrados = len(df_no_encontrados)
    porcentaje = round((total_encontrados / total_cuits) * 100, 2)

    resumen = pd.DataFrame({
        'Métrica': [
            'Total CUITs buscados',
            'Total encontrados',
            'Total no encontrados',
            'Porcentaje de coincidencia (%)'
        ],
        'Valor': [
            total_cuits,
            total_encontrados,
            total_no_encontrados,
            porcentaje
        ]
    })

    # === 7. Guardar Excel final ===
    output_file = "Reporte_AFIP_Padron.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        df_encontrados.to_excel(writer, sheet_name='Encontrados', index=False)
        df_no_encontrados.to_excel(writer, sheet_name='No Encontrados', index=False)
        resumen.to_excel(writer, sheet_name='Resumen', index=False)

    end = time()
    print(f"\n✅ Proceso completado en {round(end - start, 2)} segundos.")
    print("📊 Archivo generado:", output_file)

    files.download(output_file)

main()
