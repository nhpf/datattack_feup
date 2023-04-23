# Imports
import pandas as pd
import matplotlib.pyplot as plt
from preprocess_data import clean_data
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
                        category = "Assist e prev a act humanas"
                    elif value == 2:
                        category = "Comp total ou parcial de seg"
                    elif value == 3:
                        category = "Incêndios urbanos"
                    elif value == 4:
                        category = "Incêndio em equipmt"
                #Verifies if category is in list and adds to occurrence count if it does, adds category to list if it doesn't
                if category in cat_list:
                    cat_list.index(category)
                    cat_list[cat_list.index(category)+1] = cat_list[cat_list.index(category)+1] + 1
                else:
                    cat_list.append(category)
                    cat_list.append(1)
            i = i + 1
        geo_list.append(cat_list)
        
    print()
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
        plt.savefig(os.path.join('.','images',f'{row1}_ocurrences_{geoscope}_{categorylevel}.png'))
        plt.clf()
        plt.cla()
        j = j+1
        
    return list_of_tuples


def ocurrence_avgmanpowerph(df:pd.DataFrame,datasetisclean = False):
    

    if datasetisclean == False:
        ocorrencias = clean_data(ocorrencias)
        
    category = 'category2'    
    
    avg_list = []
    for row1 in df[category].value_counts().keys():
        i = 0
        total_mth = 0
        for row2 in df[category]:
            if row1 == row2:
                #print(df['hh'].iloc[i])
                #print(df['NumeroOperacionaisTerrestresEnvolvidos'].iloc[i])
                #print(df['NumeroOperacionaisAereosEnvolvidos'].iloc[i])
                total_mth = total_mth + df['hh'].iloc[i]
            else:
                i = i + 1
        avg_list.append(total_mth)
    
    #print(df[category].value_counts())
    #print(df[category].value_counts().keys())
    #print(df[category].value_counts().to_list())
    total_ocurrences = df[category].value_counts().to_list()
    
    
    for i in range(len(avg_list)):
        avg_list[i] = (avg_list[i]/total_ocurrences[i])
    
    print(avg_list,'\n\n\n\n\n\n')
    
    abreviation_dict = {'Assistência e Prevenção a actividades humanas' : 1, 'Comprometimento total ou parcial de segurança, serviços ou estruturas': 2,
                        'Incêndios Urbanos ou em Área Urbanizável':3, 'Incêndios em Equipamento e Produtos':4}
    
    
    # Separate the x and y values into two lists
    str_list = df[category].value_counts().keys().tolist()  
    for elem in str_list:
        if elem in abreviation_dict:
            key = elem
            value = abreviation_dict[key]
            if value == 1:
                elem = "Assist e prev a act humanas"
            elif value == 2:
                elem = "Comp total ou parcial de seg"
            elif value == 3:
                elem = "Incêndios urbanos"
            elif value == 4:
                elem = "Incêndio em equipmt"
    x_values = str_list
    print(x_values)
    y_values = avg_list
    print(y_values)
    # Plot the data
    plt.bar(x_values, y_values)
    plt.title("Average manpower per hour per ocurrence category")
    plt.xlabel("Ocurrence type")
    plt.xticks(fontsize=5,rotation=45,ha='right')
    plt.ylabel("Average manpower * hour")
    plt.tight_layout()
    plt.savefig(os.path.join('.','images',f'avgmanpowerph.png'))
    plt.clf()
    plt.cla()
    
    avg_list = [round(x,2) for x in avg_list]
    res = dict(zip(str_list,avg_list)) 
    return res
    
    
# def concelho_manpower(df:pd.DataFrame,categorylvl:str,geoscope:str,datasetisclean = False):
    
#     if datasetisclean == False:
#         ocorrencias = clean_data(ocorrencias)
    
#         geoscopef = geoscope
#         geo_list = []
#         abreviation_dict = {'Assistência e Prevenção a actividades humanas' : 1, 'Comprometimento total ou parcial de segurança, serviços ou estruturas': 2,
#                         'Incêndios Urbanos ou em Área Urbanizável':3, 'Incêndios em Equipamento e Produtos':4}

#     for row1 in df[geoscopef].unique():
#         cat_list = []
#         i = 0
#         #Parses the Districts columns to count ocurrences
#         for row2 in df[geoscopef]:
#             if row1 == row2:
#                 category = df[categorylvl].iloc[i]
#                 #Abbreviates some categories for better visualization graphs
#                 if category in abreviation_dict:
#                     value = abreviation_dict[category]
#                     if value == 1:
#                         category = "Assist e prev a act humanas"
#                     elif value == 2:
#                         category = "Comp total ou parcial de seg"
#                     elif value == 3:
#                         category = "Incêndios urbanos"
#                     elif value == 4:
#                         category = "Incêndio em equipmt"
#                 #Verifies if category is in list and adds to occurrence count if it does, adds category to list if it doesn't
#                 if category in cat_list:
#                     cat_list.index(category)
#                     cat_list[cat_list.index(category)+1] = cat_list[cat_list.index(category)+1] + 1
#                 else:
#                     cat_list.append(category)
#                     cat_list.append(1)
#             i = i + 1
#         geo_list.append(cat_list)
        
#     print()
#     # Transform the elements in each sublist into tuples of two
#     list_of_tuples = [[(lst[2*i], lst[2*i+1]) for i in range(round(len(lst)/2-1))] for lst in geo_list]

#     #Define a counter and makes relation between Ocurrences and Districts for visualization of data
#     j = 0
#     for row1 in df[geoscopef].unique():
#         list_of_tuples[j] = sorted(list_of_tuples[j], key = lambda x: (x[0]))
#     # Separate the x and y values into two lists
#         x_values = [x[0] for x in list_of_tuples[j]]
#         y_values = [x[1] for x in list_of_tuples[j]]
#     # Plot the data
#         plt.bar(x_values, y_values)
#         plt.title("Breakdown of ocurrences for" + " " + str(row1))
#         plt.xlabel("Ocurrence type")
#         plt.xticks(fontsize=8,rotation=45,ha='right')
#         plt.ylabel("Number of ocurrences")
#         plt.tight_layout()
#         plt.savefig(os.path.join('.','images',f'{row1}_ocurrences_{geoscope}_{categorylevel}.png'))
#         plt.clf()
#         plt.cla()
#         j = j+1