# =============================================================
# Proyecto Integrador - Etapa 1
# Sección 1.5: Higienización y Transformación de Datos
# Dataset: Sample - Superstore Sales Dataset
# Herramienta: Python con Pandas
# =============================================================

import pandas as pd

# -------------------------------------------------------------
# 1. CARGA DEL DATASET
# -------------------------------------------------------------
df = pd.read_csv('Sample - Superstore.csv', encoding='latin-1')

print("=" * 55)
print("REPORTE DE HIGIENIZACIÓN - SUPERSTORE DATASET")
print("=" * 55)

print(f"\n[1] DIMENSIONES ORIGINALES")
print(f"    Registros : {df.shape[0]}")
print(f"    Columnas  : {df.shape[1]}")

# -------------------------------------------------------------
# 2. VALORES NULOS
# -------------------------------------------------------------
print(f"\n[2] VALORES NULOS POR COLUMNA")
nulos = df.isnull().sum()
if nulos.sum() == 0:
    print("    No se encontraron valores nulos. ✅")
else:
    print(nulos[nulos > 0])

# -------------------------------------------------------------
# 3. REGISTROS DUPLICADOS
# -------------------------------------------------------------
print(f"\n[3] REGISTROS DUPLICADOS")
duplicados = df.duplicated(subset='Row ID').sum()
if duplicados == 0:
    print("    No se encontraron duplicados en Row ID. ✅")
else:
    print(f"    Se encontraron {duplicados} duplicados. Se eliminarán.")
    df = df.drop_duplicates(subset='Row ID')

# -------------------------------------------------------------
# 4. ESTANDARIZACIÓN DE FECHAS (MM/DD/YYYY → YYYY-MM-DD)
# -------------------------------------------------------------
print(f"\n[4] ESTANDARIZACIÓN DE FECHAS")
print(f"    Formato original  : {df['Order Date'].iloc[0]}")
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  format='%m/%d/%Y')
print(f"    Formato convertido: {df['Order Date'].iloc[0].date()}")
print("    Columnas Order Date y Ship Date convertidas. ✅")

# -------------------------------------------------------------
# 5. CORRECCIÓN DE POSTAL CODE (número → texto)
# -------------------------------------------------------------
print(f"\n[5] CORRECCIÓN DE TIPO - POSTAL CODE")
print(f"    Tipo original : {df['Postal Code'].dtype}")
df['Postal Code'] = df['Postal Code'].astype(str).str.zfill(5)
print(f"    Tipo nuevo    : {df['Postal Code'].dtype} (string, 5 dígitos) ✅")

# -------------------------------------------------------------
# 6. DERIVACIÓN DE NUEVAS VARIABLES
# -------------------------------------------------------------
print(f"\n[6] NUEVAS VARIABLES DERIVADAS")
df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days
print(f"    Days_to_Ship creado. Promedio: {df['Days_to_Ship'].mean():.1f} días ✅")
df['Profit_Margin_Pct'] = (df['Profit'] / df['Sales'] * 100).round(2)
print(f"    Profit_Margin_Pct creado. Promedio: {df['Profit_Margin_Pct'].mean():.2f}% ✅")
df['Order_Year']  = df['Order Date'].dt.year
df['Order_Month'] = df['Order Date'].dt.month
print(f"    Order_Year y Order_Month creados. ✅")
df['High_Discount'] = df['Discount'] >= 0.5
cantidad_high = df['High_Discount'].sum()
print(f"    High_Discount creado. Registros con descuento >= 50%: {cantidad_high} ✅")

# -------------------------------------------------------------
# 7. RESUMEN ESTADÍSTICO
# -------------------------------------------------------------
print(f"\n[7] RESUMEN ESTADÍSTICO DE VARIABLES CLAVE")
resumen = df[['Sales', 'Quantity', 'Discount', 'Profit',
              'Days_to_Ship', 'Profit_Margin_Pct']].describe().round(2)
print(resumen.to_string())

# -------------------------------------------------------------
# 8. ANÁLISIS DE KPIs
# -------------------------------------------------------------
print(f"\n[8] VISTA PREVIA DE KPIs")

print("\n  KPI 1 - Ganancia total por categoría:")
kpi1 = df.groupby('Category')['Profit'].sum().round(2).sort_values(ascending=False)
for cat, val in kpi1.items():
    print(f"    {cat}: ${val:,.2f}")

print("\n  KPI 2 - Ventas totales por región:")
kpi2 = df.groupby('Region')['Sales'].sum().round(2).sort_values(ascending=False)
for reg, val in kpi2.items():
    cumple = "✅" if val >= 500000 else "❌ (no alcanza meta)"
    print(f"    {reg}: ${val:,.2f} {cumple}")

print("\n  KPI 3 - Impacto del descuento alto en ganancia promedio:")
kpi3 = df.groupby('High_Discount')['Profit'].mean().round(2)
print(f"    Descuento < 50% : ${kpi3[False]:,.2f}")
print(f"    Descuento >= 50%: ${kpi3[True]:,.2f}")

print("\n  KPI 4 - Ticket promedio por segmento:")
kpi4 = df.groupby('Segment')['Sales'].mean().round(2).sort_values(ascending=False)
for seg, val in kpi4.items():
    print(f"    {seg}: ${val:,.2f}")

print("\n  KPI 5 - Días promedio de envío por Ship Mode:")
kpi5 = df.groupby('Ship Mode')['Days_to_Ship'].mean().round(1).sort_values()
for modo, dias in kpi5.items():
    print(f"    {modo}: {dias} días")

# -------------------------------------------------------------
# 9. EXPORTAR DATASET LIMPIO
# -------------------------------------------------------------
df.to_csv('Superstore_Limpio.csv', index=False, encoding='utf-8')
print(f"\n[9] DATASET LIMPIO EXPORTADO como Superstore_Limpio.csv ✅")
print(f"    Registros: {df.shape[0]} | Columnas: {df.shape[1]}")
print("\n✅ Proceso de higienización completado exitosamente.")
print("=" * 55)
