# Imports
import pandas as pd
import matplotlib.pyplot as plt
from clean_data import clean_data
import os

#Parses the data and makes list of lists based on unique values for the Districts columns
def ocurrence_frequency(df:pd.DataFrame,categorylevel:str,geoscope:str,datasetisclean = False):
    
    if datasetisclean == False:
        ocorrencias = clean_data(ocorrencias)
    
    geoscopef = geoscope
    geo_list = []
    abreviation_dict = {'Assistência e Prevenção a actividades humanas' : 1, 'Comprometimento total ou parcial de segurança, serviços ou estruturas': 2,
                        'Incêndios Urbanos ou em Área Urbanizável':3, 'Incêndios em Equipamento e Produtos':4}

    for row1 in df[geoscopef].unique():
        cat_list = []
        i = 0
        #Parses the Districts columns to count ocurrences
        for row2 in df[geoscopef]:
            if row1 == row2:
                category = df[categorylevel].iloc[i]
                #Abbreviates some categories for better visualization graphs
                if category in abreviation_dict:
                    value = abreviation_dict[category]
                    if value == 1:
                        category = "Assist e Prev a actv humanas"
                    elif value == 2:
                        category = "Comp total ou parcial de seg"
                    elif value == 3:
                        category = "Incêndios urbanos"
                    elif value == 4:
                        category = "Incêndio em equipm"
                #Verifies if category is in list and adds to occurrence count if it does, adds category to list if it doesn't
                if category in cat_list:
                    cat_list.index(category)
                    cat_list[cat_list.index(category)+1] = cat_list[cat_list.index(category)+1] + 1
                else:
                    cat_list.append(category)
                    cat_list.append(1)
            i = i + 1
        geo_list.append(cat_list)
        

    # Transform the elements in each sublist into tuples of two
    list_of_tuples = [[(lst[2*i], lst[2*i+1]) for i in range(round(len(lst)/2-1))] for lst in geo_list]

    #Define a counter and makes relation between Ocurrences and Districts for visualization of data
    j = 0
    for row1 in df[geoscopef].unique():
        list_of_tuples[j] = sorted(list_of_tuples[j], key = lambda x: (x[0]))
    # Separate the x and y values into two lists
        x_values = [x[0] for x in list_of_tuples[j]]
        y_values = [x[1] for x in list_of_tuples[j]]
    # Plot the data
        plt.bar(x_values, y_values)
        plt.title("Breakdown of ocurrences for" + " " + str(row1))
        plt.xlabel("Ocurrence type")
        plt.xticks(fontsize=8,rotation=45,ha='right')
        plt.ylabel("Number of ocurrences")
        plt.tight_layout()
        plt.savefig(os.path.join('.','images',f'{row1}_ocurrences.png'))
        plt.clf()
        plt.cla()
        j = j+1
        
    return list_of_tuples