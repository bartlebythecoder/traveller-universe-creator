# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:30:10 2021

@author: sean
"""

def build_route_xml(seed_number,db_name):

# UNDER CONSTRUCTION

# Create a trader and xboat route table and extract for traveller map

    import sqlite3
    import pandas as pd
    import numpy as np
    import PySimpleGUI as sg
    import os
    import io
    
    def offset_to_cube(location):
        x = int(location[0:2])
        y = int(location[2:4])
        q = x
        r = y - (q + (q&1)) / 2
        s = -q - r
        return(q,r,s)
    
    def cube_to_offset(location):
        x = location[0]
        y = int(location[1] + (x + (x&1)) / 2)
        if x > 9:
            x_string = str(x)
        else:
            x_string = '0' + str(x)
        if y > 9:
            y_string = str(y)
        else:
            y_string = '0' + str(y)
        
        return (x_string+y_string)
        
    
    def cube_direction(direction):
        return cube_direction_vectors[direction]
    
    def cube_add(cube, vec):
        return (cube[0] + vec[0], cube[1] + vec[1], cube[2] + vec[2])
    
    def cube_neighbor(cube, direction):
        return cube_add(cube, cube_direction(direction))
    
    
    def cube_subtract(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
    
    
    def cube_distance(a, b):
        vec = cube_subtract(a, b)
        return (abs(vec[0]) + abs(vec[1]) + abs(vec[2])) / 2
    
    def jump_range(center,j_range):
        results = []
        for q in range(-j_range,j_range+1):
            for r in range(-j_range,j_range+1):
                for s in range(-j_range,j_range+1):
                    if q + r + s == 0:
                        results.append(cube_add(center,[q, r, s]))
        return results
    
    
    def off_distance(o_start,o_end):
        try:
            c_start = offset_to_cube(o_start)
        except:
            print('C_start failed to convert to cube',o_start)
    
    
        try:        
            c_end = offset_to_cube(o_end)
        except:
            print('C_end failed to convert to cube',o_end)
    
    
        return int(cube_distance(c_start,c_end))
        
    
             
            
    def build_j4_chain(l):
        
        chain_list = []
        
        for destination in l_important:
    #        print('comparing',l,destination,d_distance[l][destination])
            cd = d_distance[l][destination]
            if cd > 0 and cd <= 4 and l < destination:
    #            print('Yes')
                chain_list.append([l,destination])
                
    
        return chain_list
    
    
    def build_j8_chain(i,chain_list):
        
       
        for i2 in l_important:
            
    
        
            if 5 <= d_distance[i][i2] <=8:
                temp_intermediate = []
                for a in l_location:
                    if a != i and a!= i2 and d_distance[a][i] <= 4 and d_distance[a][i2] <= 4:
                        temp_intermediate.append(a)
        
                top_import = -10
                t_choice = ''
                
                if len(temp_intermediate) > 0:
                    for t in temp_intermediate:
        
                        if d_distance[t]['ix'] > top_import: 
                            t_choice = t
                            top_import = d_distance[t]['ix'] 
                        
    
                    chain_list[i].append([i,t_choice])               
                    chain_list[i].append([t_choice,i2])
        return chain_list[i]
    
    
    def in_pair(coord,list_of_pairs):

        answer = False
        for each_pair in list_of_pairs:
 
            if coord in each_pair:
                print('true for ',coord)
                answer = True
                    
        return answer
    
    
    
    def clean_chain(master_chain):
    
        new_chain = {}
        rinse_chain = {}
        master_destination_list = []
        rinse_list = []
#        print('Cleaning chain')
        for key in master_chain:
#            print('Trying key:',key)
            if len(master_chain[key]) > 0:
                if key not in master_destination_list:
 #                   print(key,'Not in master destination list - proceeding') 
                    new_chain[key] = master_chain[key]

                    
            
                    for each_pair in master_chain[key]:
  #                      print(each_pair,' pair in ',key)
                      
                        for each_item in each_pair:
 #                           print(each_item,' item in', key,each_pair)
                            if each_item != key and each_item not in master_destination_list:
                                if each_item in master_chain:    
                                    if len(master_chain[each_item]) > 0:
#                                        print(each_item,' has a list greater than 0')
#                                        print(master_chain[each_item])
                                        for each_other in master_chain[each_item]:
#                                            print(each_item,each_other)
                                            try:
                                                new_chain[key].append(each_other)
#                                                print(each_other,' appending to', new_chain[key])
                                            except:
                                                print(each_other,' is not appending to', new_chain[key])
                                            master_destination_list.append(each_item)
#                                            print('Adding ',each_item,' to destination_list')
#                                     else:
# #                                        print(each_item,' location does not have key in master_chain')
#                             else:
#  #                               print(each_item,key,' are the same or in destination list - process skipped')
#                 else:
# #                    print(key,' skipped as it is in master destination list')
#             else:
# #                print(key,' skipped - nothing in key')
            
        print(new_chain)     
        print('Entering final route rinse')

        for key in new_chain:
           
            print('Rinsing key ',key)
            rinse_chain[key] = new_chain[key]
            rinse_list.append(key)
            for key2 in new_chain:
                print(key2,' comparison.  Going into in_pair function')
                if key != key2 :
                    match = False
                    for each_pair in key2:
                        for each_item in each_pair:
                            if in_pair(each_item,rinse_chain[key]):
                                match = True
                            
                    if match:
                        print('Found a match.  Closing out ',key2,'.  Adding to ',key)
                        rinse_chain[key].append(new_chain[key2])
                        rinse_list.append(key2)
                else:
                    print(key,key2,' or failed in_pair')
        else:
            print(key,' in rinse_list and being skipped')
                    
     
    
        return rinse_chain
    
    
    
    
    
    # def build_j8_chain(i,chain_list):
        
       
    #     for i2 in l_important:
            
    
        
    #         if 5 <= d_distance[i][i2] <=8 and i < i2:
    #             temp_intermediate = []
    #             for a in l_location:
    #                 if a != i and a!= i2 and d_distance[a][i] <= 4 and d_distance[a][i2] <= 4:
    #                         temp_intermediate.append(a)
        
    #             top_import = -10
    #             t_choice = ''
                
    #             if len(temp_intermediate) > 0:
    #                 for t in temp_intermediate:
        
    #                     if d_distance[t]['ix'] > top_import: 
    #                         t_choice = t
    #                         top_import = d_distance[t]['ix'] 
                        
    
    #                 chain_list[i].append([t_choice,i2])
    #  #               print('Adding J8 - ',t_choice,i2)
    
    
            
    
    #     return chain_list[i]
    
                    
    def make_path_list(master_chain):
    
        path_list = []
    
        for key in master_chain:
            if len(master_chain[key]) >= 1:
                for pair in master_chain[key]:
                    path_list.append(pair)
    
                                    
                    
        return(path_list)
    
        
    
    
    
    cube_direction_vectors = [
        (+1, 0, -1), 
        (+1, -1, 0), 
        (0, -1, +1), 
        (-1, 0, +1),
        (-1, +1, 0),
        (0, +1, -1)
    ]
    
    
    
    
    # location = input('What is your hex?: ')
    
    # q,r,s = offset_to_cube(location)
    
    # cube = [q,r,s]
    
    # print('cube coordinates are',cube)
    
    # cube_neighbors = []
    # for adj in range(0,6):
    #     adj_neighbor = cube_neighbor(cube,adj)
        
    #     cube_neighbors.append(adj_neighbor)
    
    # print('cube neighbors:',cube_neighbors)
    
    
    # off_neighbors = []
    # for loc in cube_neighbors:
    #     off_neighbors.append(cube_to_offset(loc))
    
    # print('off neighbors:',off_neighbors)
    
    # destination = input('What is your destination?: ')
    
    # a,b,c = offset_to_cube(destination)
    
    # destination_abc = [a,b,c]
    
    # loc_distance = cube_distance(cube,destination_abc)
    
    # print("The distance is ",loc_distance)
    
    # four_hexes = jump_range(cube,4)
    # off_hexes = []
    # for loc in four_hexes:
    #     off_hexes.append(cube_to_offset(loc))
        
    # print('hexes within 4:',off_hexes)
    
    
    
    

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    sql3_select = """   SELECT s.location, s.ix
                        FROM system_stats s 
                        LEFT JOIN traveller_stats t 
                        ON t.location = s.location
                        WHERE t.main_world = 1"""
    
    try:
        df = pd.read_sql_query(sql3_select,conn,index_col='location')
    #        print('df load clearly worked')
    except:
        print('Problem - df failed')
        
    df['ix'] = df['ix'].str.replace('{','')
    df['ix'] = df['ix'].str.replace('}','')
    df['ix'] = df['ix'].astype(int)
    
    df['ix_flag'] = np.where(df['ix'] >= 4,1,0)
    
    #df = df.loc[df['ix_flag'] == 1]
        
    l_location = list(df.index)
    
    for l in l_location:
        df[l] = df.index
        df[l] = df[l].apply(off_distance,args=(l,))    
    
    
    df_imp = df.loc[df['ix_flag'] == 1]
    # df = df.drop(['ix'], axis=1)
    # df = df.drop(['ix_flag'], axis=1)
    
    d_distance = df.to_dict('index')
    
    # df.to_sql('distance_data', conn)
    
    conn.commit()
    conn.close()            
    #######################################################
    
    
    
    
    
    
    
    
    
    
    
    l_important = list(df_imp.index)
    
    master_chain = {}
    destination_list = []
    path_list = []
    
                   
    
    
    for i in l_important:            
        master_chain[i] = build_j4_chain(i)




    try:
        
        key_list = list(master_chain.keys())
        key_list_len = len(key_list)
        print('master chain keys:',key_list)
        print('number of chains:',key_list_len)
        print('master_chain after j4 build: ',master_chain)
        
    except:
        print('Failed at key list and key list len')

    
     
    
    for i in l_important:       
        try:
            if master_chain[i] == []:
                print('Adding to chain',i,master_chain[i])
                master_chain[i] = build_j8_chain(i,master_chain)
                print('master_chain added',master_chain[i])
        except:
            print('Error asking: if master_chain[i] == []:')




    try:
        
        key_list = list(master_chain.keys())
        key_list_len = len(key_list)
        print('master chain keys:',key_list)
        print('number of chains:',key_list_len)
        print('master_chain after j8 build: ',master_chain)
        
    except:
        print('Failed at key list and key list len')





    
    master_chain = clean_chain(master_chain)  
    
    
    
    
    try:
        
        key_list = list(master_chain.keys())
        key_list_len = len(key_list)
        print('master chain keys:',key_list)
        print('number of chains:',key_list_len)
        print('master_chain after clean: ',master_chain)
        
    except:
        print('Failed at key list and key list len')    
    
    
    
    
    
    
    path_list = make_path_list(master_chain)
    

        
    
    route_text = ''
    
    for each in path_list:
        
        route_text +=    """    <Route Start='""" + each[0] + \
                        """' End='""" + each[1] +  """'  />""" + '\n'  
                        
        
    important_text = ''
    
    for each in l_important:
                            
        important_text += """    <Label Hex='""" + each + \
                          """' Color="red">Ix+</Label>""" + '\n' 
    
    
    
    
        
    file_name = db_name + '-routes.txt'
    with open(file_name, 'w') as f:
        f.write('<?xml version="1.0"?>' + '\n' \
                +  '<Sector>' + '\n' \
                +  '<Name>' + db_name + '</Name>' + '\n' \
                +  '<Routes>...' + '\n' \
                +  route_text
                +  '</Routes>' + '\n' \
                +  '<Labels>' + '\n' \
                +  important_text
                +  '</Labels>' + '\n' \
                +  '</Sector>')
            