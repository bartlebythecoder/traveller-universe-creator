def create_route_xml(seed_number,db_name, settlement_mod):
    
    # Create an xboat route table and extract for traveller map
    
    import sqlite3
    import pandas as pd
    import numpy as np
    import networkx as nx
    import warnings
    
    
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
        
    
    
    ######################################################################
    
    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning) 
    warnings.simplefilter(action='ignore', category=FutureWarning)
    print('processing...')
    
    
    cube_direction_vectors = [
        (+1, 0, -1), 
        (+1, -1, 0), 
        (0, -1, +1), 
        (-1, 0, +1),
        (-1, +1, 0),
        (0, +1, -1)
    ]
    
    

    
    
    conn = sqlite3.connect(db_name)
    sql3_select = """   SELECT s.location, s.ix
                        FROM system_stats s 
                        LEFT JOIN traveller_stats t 
                        ON t.location = s.location
                        WHERE t.main_world = 1"""
    
    try:
        df = pd.read_sql_query(sql3_select,conn,index_col='location')
    
    
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
    l_important = list(df_imp.index)
    
    
    d_distance = df.to_dict('index')
    
    
    
    conn.commit()
    conn.close()            
    ########################################################################
    
    
    G = nx.Graph()
    
    elist = []
    
    for loc in l_location:
        for loc2 in l_location:
            if loc < loc2:
                if d_distance[loc][loc2] <= 4:
                    elist.append([loc,loc2])
    
    
    G.add_edges_from(elist)
    
    
    path_list = []
    used_list = []
    #max_list = 8
    
    min_list_max = 4
    max_list_max = 20
    if settlement_mod == 1: 
        max_list_max = 5  # reduces route connections in diminishing sectors
    
    for max_list in range(min_list_max,max_list_max):
        for loc in l_important:
            for loc2 in l_important:
                one_chain = []
                if loc < loc2 and d_distance[loc][loc2] <= max_list:
                    if max_list <= 6 or (loc not in used_list):
                        used_list.append(loc)
                        one_chain = nx.shortest_path(G,source=loc,target=loc2)
                        for x,dest in enumerate(one_chain):
                            if x < (len(one_chain)-1):
                                path_list.append([dest,one_chain[x+1]])
    
    
    route_text = ''
    
    for each in path_list:
        
        route_text +=    """    <Route Start='""" + each[0] + \
                        """' End='""" + each[1] +  """'  />""" + '\n'  
                        
        
    important_text = ''
    
    for each in l_important:
                            
        important_text += """    <Label Hex='""" + each + \
                          """' Color="red">Ix+</Label>""" + '\n' 
    
    
    
    
        
    file_name = db_name + '_routes.txt'
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
            
    f.close()
    print('Routes complete')

