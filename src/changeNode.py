'''
Created on 09.01.2019

@author: ernstm
'''

import networkx as nx
spawn_db_filename = "spawn.gexf"
remove_db_filename = "remove.gexf"



def print_spawns(node) :
    spawns = nx.neighbors(spawn_db, node)
    for spawn in spawns :
        print("spawn : " + spawn)
    return

def print_removes(node) :
    removes = nx.neighbors(remove_db, node)
    for remove in removes :
        print("remove : " + remove)
    return

def exists_node(node):
    return (node in path_db.nodes());

def execute_cmd(sourceNode, cmd) :
    if (len(cmd) < 3) :
        return
    target = cmd[1:];
    target = target.upper()
    if (not exists_node(target)) : 
        print ("cant find target node : ", target)
        return
              
    if (cmd[0] == "#" ) :
        if target in nx.neighbors(spawn_db, sourceNode) :            
            spawn_db.remove_edge(source,target)
        if target in nx.neighbors(remove_db, source) :
            remove_db.remove_edge(source,target)
        print ("delete  : ", target)
    elif (cmd[0] == "+" ) :
        spawn_db.add_edge(sourceNode, target, label="+")
        print ("spawn   : ", target)            
    elif (cmd[0] == "-" ) :
        remove_db.add_edge(sourceNode, target, label="-")
        print ("despawn : ", target)
    else :
        print ("bad command")
    return
    

def edit_node(node):  
    sourceNode = node
    print("current info : ")
    print_spawns(node);
    print_removes(node);   
    
    print("---\n+a7 = new spawn a7, -a7 = new despawn a7, #a7 = remove everthing about a7, d = delete note info, s = saveToFile, enter = exit")
    while (True) :
        cmd = input ("cmd >> ")
        if (len(cmd) == 0) :
            print ("no cmd given -> exit")
            break;    
        if (len(cmd) == 1 and cmd[0] == "s") :            
            print ("savingFiles -> exit")
            nx.write_gexf(spawn_db,spawn_db_filename)
            nx.write_gexf(remove_db,remove_db_filename)
            break;  
        if (len(cmd) == 1 and cmd[0] == "d") :
            spawns = nx.neighbors(spawn_db, node)
            for spawn in list(spawns) :
                spawn_db.remove_edge(node, spawn)            
            removes = nx.neighbors(remove_db, node)                
            for removeNode in list(removes) :
                remove_db.remove_edge(node, removeNode)            
            print("info deleted")
            continue
    
        while (len(cmd) > 0) : 
            execute_cmd(sourceNode, cmd[0:3])
            cmd = cmd[4:]         
                 
    return;


################################### MAIN ###################################################

path_db = nx.read_gexf("path.gexf")


while (True) :
    spawn_db = nx.read_gexf(spawn_db_filename)
    remove_db = nx.read_gexf(remove_db_filename)      
    
    print ("######################################")
    node = input ("Enter node : ")
    if (len(node) > 3 ) :
        if node == "patchdbs" :
            print ("patching spawn db")
            index = 0
            for edgepath in spawn_db.edges() :
                spawn_db[edgepath[0]][edgepath[1]]["id"] = index        
                index += 1
            index = 0
            for edgepath in spawn_db.edges() :
                spawn_db[edgepath[0]][edgepath[1]]["id"] = index        
                index += 1
            nx.write_gexf(spawn_db,spawn_db_filename)
            nx.write_gexf(remove_db,remove_db_filename)
            continue;
        
    node = node.upper()
    if exists_node(node) :
        edit_node(node)
    else :
        print ("exiting, didnt find your node")
        exit();
    



