################################### Primer función: Carga los archivos con extensiones .csv y .xlsx  ###################################################
def cargar_dataset (archivo):  #Definimos la función
    import pandas as pd   #Importamos las librerias necesarias para la función
    import os
    extension = os.path.splitext(archivo)[1].lower()  #Extraemos la extensión del archivo que nos entreguen

    #Filtramos de acuerdo a la extensión
    if extension == '.csv': 
        return pd.read_csv(archivo)   

    elif extension == '.xlsx':
        return pd.read_excel(archivo)
    
    else:
        raise ValueError(f'Este formato no está soportado para esta función: {extension}')
    
################################## Segunda función: Sustituye los valores nulos ###########################################################################
def vn_completo(dataframe):
    import pandas as pd
    #Vamos a separar columnas cuantitativas del data frame
    col_cuan = dataframe.select_dtypes(include=['float64', 'int64', 'float', 'int'])
    #Ahora separamos las columnas con datos cualitativas
    col_cual = dataframe.select_dtypes(include=['object', 'datetime', 'category'])
    #Separamos las variables cuantitativas en pares e impares mediante la posición de sus indices y con saltos de dos en dos (lo unico que cambias es desde donde inicia)
    cuantitativas_pares = col_cuan.iloc[ : ,0::2]
    cuantitativas_impares = col_cuan.iloc[ : ,1::2]
    #Aplicamos la sustitució correspondiente de acuerdo al método que corresponda
    cualitativas = col_cual.fillna('Este_es_un_valor_nulo')  #Por un str específico
    cuantitativas_impares_limpias = cuantitativas_impares.fillna(99)
    cuantitativas_pares_limpias = cuantitativas_pares.fillna(round(col_cuan.mean(), 1))  
    #Ahora unimos las cuantitativas y las cualitativas
    dt_f = pd.concat([cuantitativas_impares_limpias, cualitativas], axis=1)
    dt_f2 = pd.concat([dt_f, cuantitativas_pares_limpias], axis=1)
    return(dt_f2)

################################## Tercer función: Identifica los valores nulos ####################################################################################
def val_nu(dataframe): #Tomamos como parámetro el Data Frame que se analizara
    valo_nu_col = dataframe.isnull().sum()  #Y solo hacemos la suma de nulos detectados en el DataFrame
    valo_nu_tot = dataframe.isnull().sum().sum()

    return('Valores nulos por columna:',valo_nu_col,
           "Valores nulos en total:", valo_nu_tot)   #Y los imprimimos

################################## Cuarta función: Valores atípicos de las columnas numéricas ####################################################################################
def val_ati(dataframe):
    col_cuan = dataframe.select_dtypes(include=['float64', 'int64', 'float', 'int'])
    y = col_cuan


    per25 = y.quantile(0.25) #Q1
    per75 = y.quantile(0.75) #Q1

    iqr_p = per75 - per25

    Limite_Superior_P = per75 + 1.5*iqr_p
    Limite_Inferior_P = per25 - 1.5*iqr_p

    data3_p = col_cuan[(y<=Limite_Superior_P) & (y>=Limite_Inferior_P)]
    data4_p = data3_p.copy()
    data4_p = data4_p.fillna(round(data3_p.mean(),1))
    return(data4_p)
