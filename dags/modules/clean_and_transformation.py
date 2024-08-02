
def clean_data(df):
    try:
        # Limpia los valores nulos o null
        df_cleaned = df.dropna()
        return df_cleaned
    except Exception as e:
        print(f"Error al limpiar los datos: {e}")
        return None
