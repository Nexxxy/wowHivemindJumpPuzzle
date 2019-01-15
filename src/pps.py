'''
Created on 08.01.2019

@author: ernstm
Version 1.3
'''


import networkx as nx
import threading
import copy
import gc
#import resource, sys
#resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
#sys.setrecursionlimit(10**6)

import sys
sys.setrecursionlimit(999999)



def get_empty_field () :
    return {"A5" : plattform}

def set_val_from_field (dic, loc, val):
    dic[loc] = val

def get_val_from_field (dic, loc) :
    if loc in dic :
        return dic[loc]
    else :
        return None

def del_val_from_field (dic, loc):
    del dic[loc]

def get_player_loc(dic, player):
    return dic[player];

def set_player_loc(dic, player, newLoc):
    dic[player] = newLoc
    return

def del_player_loc(dic, player):
    if player in dic :
        del (dic[player])
    return

def is_player_on_loc(dic, loc) :
    for key in dic.keys() :
        if dic[key] == loc:
            return key;
    return None

def get_target_node(curLoc, dir) :
    targetNotes = nx.neighbors(path_db, curLoc)
    for note in targetNotes :
        if (path_db[curLoc][note]["label"] == dir) :
            return note;
    return None;

def get_dir_from_path(fromLoc, toLoc) :
    if (not (toLoc in nx.neighbors(path_db,fromLoc))) and toLoc != "S" :
        print ("Move error : ", fromLoc, " -> " , toLoc)
    
    if (toLoc == "S") :
        return "drop from " + fromLoc
    else : 
        return path_db[fromLoc][toLoc]["label"]
    
def is_path_connected(fromLoc, toLoc, dir) :
    if (not (toLoc in nx.neighbors(path_db,fromLoc))) :
        return False  
    else : 
        if path_db[fromLoc][toLoc]["label"] == dir :
            return True
        else :
            return False

def get_available_paths_from_player(field, pLocs, player) :
    availablePathes = []
    playerLoc = pLocs[player]
    for testLoc in nx.neighbors(path_db, playerLoc) :
        if testLoc in field.keys() :
            if (not (testLoc in pLocs.values())) :
                availablePathes.append(testLoc) 
    if (pLocs[player] != "S") and ("S" in pLocs.keys()) :
        if (enableDropping) :        
            availablePathes.append("S")
    return sorted(availablePathes)



def printField(field, pLocs) :
    lineLetter = ["A", "B", "C" , "D", "E" , "F" , "G" , "H"];

    print ("\n------------------------------------------------------------------------------------------------")
    for col in range(1,10) :
        print ("\t" + str(col), end="");

    for line in reversed(range(len(lineLetter))) :
        print ("")
        for col in range(1,11) :
            if col == 1 :
                print ("   " + lineLetter[line], end="")
            if col == 10 :
                print ("   " + lineLetter[line], end="")
                continue

            node = lineLetter[line] + str(col)
            p = is_player_on_loc(pLocs, node)
            if (p != None) :
                print ("\t" + p, end = "")
            elif node in field.keys() :
                print ("\t" + plattform, end= "")
            else :
                print ("\t-", end="")
    print("")
    for col in range(1,10) :
        print ("\t" + str(col), end="");
    print ("\n------------------------------------------------------------------------------------------------")

    return

def get_initial_player_loc_array() :
    return {p1 : "S" , p2 : "S" , p3 : "S" , p4 : "S" , p5 : "S"};

def generate_DB_pathes ():
    g = nx.DiGraph()
    lineLetter = ["A", "B", "C" , "D", "E" , "F" , "G" , "H", "I", "J"];
    g.add_node("S")

    for line in range(len(lineLetter)) :
        print ("\n")
        for col in range(1,10) :
            node = lineLetter[line] + str(col)
            print (node + " ", end="")
            g.add_node(node)
            if line != 0 :
                g.add_edge(node, lineLetter[line-1] + str(col), label="path_B")
                g.add_edge(lineLetter[line-1] + str(col), node, label="path_F")
            else :  # line == 0
                g.add_edge("S", node, label="path_F")
            if col != 1 :
                g.add_edge(node, lineLetter[line] + str(col-1), label="path_L")
                g.add_edge(lineLetter[line] + str(col-1), node, label="path_R")
    nx.write_gexf(g,"path.gexf")
    return

def generate_empty_node_graph (filename):
    g = nx.DiGraph()
    lineLetter = ["A", "B", "C" , "D", "E" , "F" , "G" , "H"];
    g.add_node("S")

    for line in range(len(lineLetter)) :
        print ("\n")
        for col in range(1,10) :
            node = lineLetter[line] + str(col)
            print (node + " ", end="")
            g.add_node(node)
        nx.write_gexf(g,filename)
    return

def merge_pathNodes_with_field(possiblePathNodes, field):
    mergedList = []
    possiblePathNodes = list(possiblePathNodes)
    for loc in field.keys() :
        if field[loc] == plattform :
            if loc in possiblePathNodes :
                mergedList.append(loc)
                
    
    return mergedList

# returns True if something spawns
def execute_spawns(field, loc) :
    if loc == "S" :
        return False
    spawnList = nx.neighbors(spawn_db, loc)
    retVal = False
    for spawn in spawnList :
        retVal = True
        field[spawn] = plattform
        #print ("spawn : " , spawn)
    return retVal

def execute_despawns(field, pLocs, loc) :
    removeList = nx.neighbors(remove_db, loc)
    retVal = False
    for removeItem in removeList :
        retVal = True
        if (not is_player_on_loc(pLocs, removeItem)) :
            if (removeItem in field) :
                del field[removeItem]
            #print ("remove : " , removeItem)
        #else :
            #print ("cant remove because of playerpos : " , removeItem)
    return retVal

def execute_drop(field, pLocs, player):
    
    if ["S", "S" , "S" , "S" ] == list(sorted(pLocs.keys())) :
        return False
        
    for item in field.keys() :
        del field[item]       
    
    field["A5"] = plattform       
    
    pLocs[player] = "S"
    
    for p in players :
        if pLocs[p] == "S" :
            pass
        else :
            field[pLocs[p]] = plattform
            execute_spawns(field, pLocs[p])

    
    return True




def move_player (field, pLocs, player, dir, dirExtraNumber = -1):
    # returns retVal and retVal2
    # retVal = False means you cant do the step or there are more differten posibilites
    #          False + retVal2 = amount of posibilities that are possible
    # retVal = True -> we did take the step
    #          if there is a retVal2 then we did a step to a new unknown plattform !
    #---------------------------------------------------------------------------------
    # first check for available pathes
    retVal = False
    newLoc = None
    playernode = pLocs[player]

    possiblePathNodes = nx.neighbors(path_db, playernode)
    availablePathes = merge_pathNodes_with_field(possiblePathNodes, field)
#
#     print("available pathes for p" , player , " : " , end="")
#     for i in sorted(availablePathes) :
#         print (i + " ", end = "")
#     print ("")


    if playernode == start and dir == forward :
        if len(availablePathes) == 1 :
            newLoc = availablePathes[0]
            if (get_val_from_field(field, newLoc) != plattform) :
                #print("cant move ", dir, "because of : " , get_val_from_field(field, newLoc), " on field" , newLoc)
                newLoc = None
            if (is_player_on_loc(pLocs, newLoc)) :
                #print("cant move ", dir, "because of Player :" , is_player_on_loc(pLocs, newLoc) , " on field" , newLoc)
                newLoc = None
        else :
            if (dirExtraNumber == -1) :
                #print ("error diff start") # TODO
                return False, len(availablePathes)
            else :
                if (dirExtraNumber >= len(availablePathes)) :
                    print ("Out of Bounds exception")
                    exit();
                else :
                    newLoc = availablePathes[dirExtraNumber]
                    if (get_val_from_field(field, newLoc) != plattform) :
                        print("cant move ", dir, "because of : " , get_val_from_field(field, newLoc), " on field" , newLoc)
                        newLoc = None
                    if (is_player_on_loc(pLocs, newLoc)) :
                        print("cant move ", dir, "because of Player :" , is_player_on_loc(pLocs, newLoc) , " on field" , newLoc)
                        newLoc = None

    else :
        targetNode = get_target_node(playernode, dir)
        if (targetNode != None) :
            if (get_val_from_field(field, targetNode) == plattform and not is_player_on_loc(pLocs, targetNode)) :
                newLoc = targetNode
            else :
                pass
                #print("cant move ", dir, "because of : " , get_val_from_field(field, targetNode), " on field" , targetNode)

    if (newLoc != None) :
        #print (player, "taking path: " + newLoc)
        retVal = True
        set_player_loc(pLocs, player, newLoc)
        b = execute_despawns(field, pLocs, newLoc)
        a = execute_spawns(field, newLoc)

        for p in playerList :
            execute_spawns(field, pLocs[p])

        if (a == False and b == False) :
            print ("got no information about", newLoc)
            return retVal, newLoc
    return retVal, None;


def move_player_to(field,pLocs,player,targetLoc) :
    # returns False, None if your path isnt available
    # returns True, False if the path was taken but we dont have a new field
    # returns True, True if the path was taken and we got a new field !
    retVal = False
    #test for that specific path
    playerLoc = pLocs[player]
    if (not (targetLoc in nx.neighbors(path_db, playerLoc))) :
        return False, None
    #now check for available platform
    if (field[targetLoc] != plattform) :
        return False, None
    #now check for players there
    for p in playerList :
        if p == player :
            continue
        if pLocs[p] == targetLoc :
            return False, None
        
    if targetLoc != "S" :
        #print (player, "taking path: " + targetLoc)
        set_player_loc(pLocs, player, targetLoc)
        
        b = execute_despawns(field, pLocs, targetLoc)
        a = execute_spawns(field, targetLoc)
    
        #spawn locked platforms again
        for p in playerList :
            execute_spawns(field, pLocs[p])
    
        if (a == False and b == False and ForcedDestination == None) :
            print ("got no information about", targetLoc)
            return True, True
        elif (ForcedDestination != None and ForcedDestination == targetLoc) :
            #print ("found path to", targetLoc)
            return True, True
        else :
            pass
    else : # targetLoc == "S" 
        if (not execute_drop(field, pLocs, player)) :
            return False, None    
    
    return True, False

def hashDics(field,pLocs) :
    sortedField = sorted(list(field.keys()))
    sortedPlayer = sorted(list(pLocs.values()))    
    retVal = ""
    for i in sortedField :
        retVal += i
    retVal += "-"
    for i in sortedPlayer :
        retVal += i
    return retVal

# parent = Nodehash from which your coming
# dir = direction to get here from $parent
def do_recursive_bruteforce(parent, player, dir, field, pLocs, brute_graph, depth = 0) :
    # part 1 : we got no parent !
    if (depth > 110) :
        return None
    if (parent == None) :
        node = hashDics(field, pLocs)
        brute_graph.add_node(node)
        resultList = []
        for p in playerList :
            if (p != p1) :
                continue
            d = forward
            result = do_recursive_bruteforce(node, p, d, field.copy(), pLocs.copy(), brute_graph, depth +1)
            if result != None :
                resultList.extend(result)
        return resultList

    # part 2 : ok we got a parentnode lets test if that move is valid
    if (type(dir) is list) :
        #print ("alternativ start: ",  dir[0], dir[1])
        result, result2 = move_player(field, pLocs, player, dir[0], dir[1])
    else :
        result, result2 = move_player(field, pLocs, player, dir)
    if (result == False) :
        if result2 == None :
            return None;
        # ok we are at the start and got 2 ways Forward !
        resultList = []
        playernode = pLocs[player]
        availablePathes = sorted(merge_pathNodes_with_field(nx.neighbors(path_db, playernode), field))
        index = 0
        for targetNode in availablePathes :
            targetDir = path_db[playernode][targetNode]["label"]
            if (targetDir == forward) :
                result = do_recursive_bruteforce(parent, player, [dir,index], field.copy(), pLocs.copy(), brute_graph, depth +1)
                if result != None :
                    resultList.extend(result)
            index = index + 1
        if len(resultList) > 0 :
            return resultList
        else :
            return None
    else :  # we did a step !
        cont = True
        node = hashDics(field, pLocs)
        if node in brute_graph :
            cont = False
        else :
            brute_graph.add_node(node)
        if (type(dir) is list) :
            brute_graph.add_edge(node, parent, label =  str(player) + " -> " + str(dir[0]) + " to " + pLocs[player], weigth = depth)
        else :
            brute_graph.add_edge(node, parent, label =  str(player) + " > " + str(dir) + " to " + pLocs[player], weigth = depth)
        if result2 != None :        # we did a step to a new plattform ! exit !
            print (">> Found a new plattform : " , result2, node)
            result = []
            result.append(node)
            printField(field, pLocs)
            #########################
            #starthash = hashDics(get_empty_field(), get_initial_player_loc_array())
            #print ("\n\n-------- Path to: ", node)
            #pathway = reversed(getPathTo(brute_graph, node, starthash))
            #for step in pathway :
            #    print (step)
            #print ("-------")
            #exit();
            #########################
            return result;
        else :                      # we did a step but there wasnt anything new
            if (cont == False) :    # dont continue if we were already here
                return None
            # calc next step
            resultList = []
            for p in playerList :
                #if p == p5 :
                    #continue
                playernode = pLocs[p]
                availablePathes = sorted(merge_pathNodes_with_field(nx.neighbors(path_db, playernode), field))
                for targetNode in availablePathes :
                    targetDir = path_db[playernode][targetNode]["label"]
                    result = do_recursive_bruteforce(node, p, targetDir, field.copy(), pLocs.copy(), brute_graph, depth +1)
                    if result != None :
                        resultList.extend(result)
            if len(resultList) > 0 :
                return resultList
            else :
                return None
    print ("something went wrong")
    exit()
    return

def isToDoListEmpty(toDoList):
    emptyToDoList = {p1 : [] , p2 : [], p3 : [], p4 : [], p5 : []}
    return toDoList == emptyToDoList

def getNewEmptyToDoList () :
    return {p1 : [] , p2 : [], p3 : [], p4 : [], p5 : []}
                

def do_nonrecursive_bruteforce(brute_graph, depthsearchMAX) :
    pLocs = get_initial_player_loc_array()
    field = get_empty_field()    
    toDoList = getNewEmptyToDoList()
    bruteTree = {}
    depth = 0
    newPlattforms = []    
    itcounter = 0

    # ok first generate rootNode !
    rootNode = hashDics(field, pLocs)
    bruteTree[rootNode] = {parentEntry : None, fieldEntry : field, pLocsEntry : pLocs, depthEntry : depth, toDoListEntry : toDoList}
    field = copy.deepcopy(field)
    pLocs = copy.deepcopy(pLocs) 
    move_player_to(field, pLocs, p1, "A5")
    curNode = hashDics(field, pLocs)    
    bruteTree[curNode] = {parentEntry : rootNode, fieldEntry : field, pLocsEntry : pLocs, depthEntry : depth}    
    # add the graph edge
    brute_graph.add_node(rootNode, depthEntry = 0)
    brute_graph.add_node(curNode, depthEntry = 1)
    brute_graph.add_edge(curNode, rootNode, label =  str(p1) + " > " + str(forward) + " to " + pLocs[p1], weigth = depth)
    depth = depth + 1
    # ok throw in first child !
    while (curNode != rootNode) :  
        itcounter += 1
        if (itcounter % 200000 == 0) :
            #print("garbagec",itcounter)
            #sys.stdout.flush()            
            gc.collect()             
        #step 1 : test for toDoList
        if toDoListEntry in bruteTree[curNode] :
            toDoList = bruteTree[curNode][toDoListEntry]
        else : # generate toDoList
            toDoList = getNewEmptyToDoList()
            for p in playerList :
                toDoList[p] = get_available_paths_from_player(field, pLocs, p)
            #printField(field, pLocs)
            #print ("avail Pathes: ", toDoList)                
            #save it
            bruteTree[curNode][toDoListEntry] = toDoList
        #step 2 : savecall : we have a toDoList
        if isToDoListEmpty(toDoList) :
            #we dont have anything to do -> jump to parent and delete our node
            delNode = curNode
            curNode = bruteTree[curNode][parentEntry]
            depth = depth - 1
            # delete delNode
            del bruteTree[delNode][parentEntry]
            del bruteTree[delNode][fieldEntry]
            del bruteTree[delNode][pLocsEntry]
            del bruteTree[delNode][depthEntry]
            del bruteTree[delNode][toDoListEntry]            
            del bruteTree[delNode]
            del delNode            
            continue
        # ok, we got something to do ! lets move to the first thing in our List
        #step 3 : load field and pLocs
        field = None
        pLocs = None
        field = copy.deepcopy(bruteTree[curNode][fieldEntry])
        pLocs = copy.deepcopy(bruteTree[curNode][pLocsEntry])
        #step 4 : try to move there
        for p in playerList :
            # check if p can do anything
            if len(toDoList[p]) == 0 :
                continue   
            dir = get_dir_from_path(pLocs[p], toDoList[p][0])   
            weMoved, weFoundSomething = move_player_to(field, pLocs, p, toDoList[p][0])                 # ok lets to first available thing
            #delete this move from current plan
            del toDoList[p][0]
            #reset alreadyVisited Var            
            alreadyVisited = False
            if (weMoved) :                
                newNode = hashDics(field, pLocs)
                #print(p, " moved from", bruteTree[curNode][pLocsEntry][p], " to " , toDoList[p][0], "hash: ", newNode)
                #printField(field, pLocs)
                if (newNode in brute_graph) :
                    #print (brute_graph.node[newNode])
                    if (depth >= brute_graph.node[newNode][depthEntry]) :
                        alreadyVisited = True                        
                    else :
                        # ok we have to recalculate this whole tree .. cause we dropped that data :(
                        #print ("depth failed cur:",depth,"vs",brute_graph.node[newNode][depthEntry])
                        # update note !
                        brute_graph.node[newNode][depthEntry] = depth
                        pass                                                                                        
                else :
                    # since we cant calculate the next node dont add it !
                    if (depth >= depthsearchMAX) :
                        # but if we dont find a new location .. it doesnt matter !
                        if not weFoundSomething :                            
                            break
                    # add the new new into our discoverylist                                                                
                    brute_graph.add_node(newNode, depthEntry = depth)           
                # add a edge between newNode and its new parent      
                if (curNode in nx.neighbors(brute_graph, newNode)) :
                    #print ("bin hier", brute_graph[newNode][curNode])
                    # update edge
                    brute_graph[newNode][curNode]["weigth"] = depth
                else :                              
                    brute_graph.add_edge(newNode, curNode, label =  str(p) + " > " + str(dir) + " to " + pLocs[p], weigth = depth)
                # check if we found a new plattform !
                if (weFoundSomething) :
                    print ("\r", len(newPlattforms), end="")
                    sys.stdout.flush()
                    
                    newLoc = "NP:" +pLocs[p]  
                    if (not(newLoc in brute_graph)) :                  
                        brute_graph.add_node(newLoc)
                    brute_graph.add_edge(newLoc, newNode, label =  "--" , weigth = depth + 1)
                    newPlattforms.append({"newLoc" : newLoc, "last-node" : newNode, fieldEntry : field, pLocsEntry : pLocs, depthEntry : depth})   
                    alreadyVisited = True   
                
                
                if (alreadyVisited) :
                    break
                if (depth >= depthsearchMAX) :
                    break               
                #print ("-", depth)                
                bruteTree[newNode] = {parentEntry : curNode, fieldEntry : field, pLocsEntry : pLocs, depthEntry : depth}               
                
                #jump deeper into the tree
                depth = depth+1
                curNode = newNode
                break         
            # if weMoved
            else :
                pass
            print("this shouldnt happen!")
            exit()
        # for p in playerList
        continue
    print ("")
    print ("Iterations : ", itcounter)    
    print ("solutions:",len(newPlattforms))
    return newPlattforms  
                              
                

def getPathTo_v2(brute_graph, sourceNode, sinkNode) :
    pathlist = list(nx.shortest_path(brute_graph, sourceNode, sinkNode, None))
    path = []    
    for index in range(len(pathlist)-1) :
        path.append(brute_graph[pathlist[index]][pathlist[index+1]]["label"])
    return path, len(pathlist), pathlist[1]
        


def getPathTo(brute_graph, sourceNode, sinkNode) :
    path = []
    curnode = sourceNode
    while(curnode != sinkNode) :
        availablepathes = nx.neighbors(brute_graph, curnode)
        min = 99999999999
        bestNode = ""
        for nextNode in availablepathes :
            weight = brute_graph[curnode][nextNode][0]["weigth"]
            if weight < min :
                min = weight
                bestNode = nextNode
        path.append(brute_graph[curnode][bestNode][0]["label"])
        curnode = bestNode
    return path


#generate_DB_pathes();
#generate_empty_node_graph("spawn.gexf")
#generate_empty_node_graph("remove.gexf")


def main() :   

    # print("Moving : ", move_player(field, pLocs, p1, forward));
    # printField(field, pLocs)
    # print("Moving p2: ", move_player(field, pLocs, p2, forward));           ## error
    # print("Moving p2: ", move_player(field, pLocs, p2, forward,1));         ## fixed
    # print("Moving p1: ", move_player(field, pLocs, p1, forward));           ## geht
    # print("Moving p2: ", move_player(field, pLocs, p2, forward));           ## geht
    # printField(field, pLocs)

    field = get_empty_field()
    pLocs = get_initial_player_loc_array()

    #brute_graph = nx.MultiDiGraph()
    brute_graph = nx.DiGraph()
    starthash = hashDics(field, pLocs)
    retlist = []       
    
    #retList = do_recursive_bruteforce(None, None, None, field, pLocs, brute_graph)
    if (ForcedDepth == None ) :
    ###################################################################################################################################################
        retlist = do_nonrecursive_bruteforce(brute_graph, 100)
    else :
        retlist = do_nonrecursive_bruteforce(brute_graph, ForcedDepth)
    
    if (len(retlist) == 0) :
        print ("No solutions ..")
        #nx.write_gexf(brute_graph,"result.gexf")
    else :   
    
        #nx.write_gexf(brute_graph,"result.gexf")
    
        # search for min depth node
        mindepth = 9999999
        bestTargetIndex = 0
        for index in range(len(retlist)) :
            if retlist[index][depthEntry] < mindepth :
                mindepth = retlist[index][depthEntry]
                bestTargetIndex = index
        
        print ("best solution depth:", retlist[bestTargetIndex][depthEntry])
        
        
                        
        ######## reform output    
        playerNames = {p1 : "Gelb" , p2 : "Blau" , p3 : "Orange" , p4 : "Lila", p5 : "Gruen"}      
        pLocs = get_initial_player_loc_array()
        lastplayer = ""      
        
        #print (retlist)
        
        pathway, depth, bestSolutionNode = getPathTo_v2(brute_graph, retlist[bestTargetIndex]["newLoc"], starthash)
        pathway = reversed(pathway)
        print ("\n\n-------- Path to : ", retlist[bestTargetIndex]["newLoc"], " , len =", depth-2)
        counter = 0        
        for step in pathway :
            #print (step)
            if (len(step) == len("1 > path_F to A5")) :
                dir = step[4:10]
                targetLoc = step[14:]
                found_a_step = False                
                for p in playerList :
                    if is_path_connected(pLocs[p], targetLoc, dir) :                        
                        pLocs[p] = targetLoc
                        found_a_step = True
                        if lastplayer != p :
                            lastplayer = p
                            print ("")
                        counter += 1
                        print (counter, " : " , playerNames[p] , "->", dir[5] , "to" , targetLoc) # , "\t pLocs:", pLocs)
                        break;
                if (found_a_step) :
                    pass
                else :
                    print("this should not happen !")
            elif (step == "--") :
                print ("-FIN-")                
            else :
                print ("irgendwer muss droppen : " + step)
        print ("-------")
        #search for right field
        
        for solution in retlist :
            if solution["last-node"] == bestSolutionNode :
                field = solution[fieldEntry]
                pLocs = solution[pLocsEntry] 
                        
        printField(field, pLocs)
        #printField(retlist[bestTargetIndex][fieldEntry], retlist[bestTargetIndex][pLocsEntry])

    #print (hashDics(field, pLocs))


# recurse in greedy thread

p1 = "1"
p2 = "2"
p3 = "3"
p4 = "4"
p5 = "5"
player = "1"
plattform = "0"
start = "S"
forward = "path_F"
backward = "path_B"
left = "path_L"
right = "path_R"
toDoListEntry = "toDoList"
fieldEntry = "field"
depthEntry = "depthEntry"
pLocsEntry = "pLocs"
parentEntry = "parent"

############################################################################## Options
enableDropping = False

ForcedDestination = None
ForcedDepth = None
if (len(sys.argv) == 1) :
    pass
else :
    if len(sys.argv) >= 2 : 
        ForcedDestination = sys.argv[1].upper()
    if len(sys.argv) >= 3 :
        ForcedDepth = int(sys.argv[2])
        

print ("ForcedDestination : ", ForcedDestination)

playerList = [p1,p2,p3,p4,p5]
dirList = [forward, left, right, backward]


path_db = nx.read_gexf("path.gexf")
spawn_db = nx.read_gexf("spawn.gexf")
remove_db = nx.read_gexf("remove.gexf")

sys.setrecursionlimit(9999999)
threading.stack_size(0xF000000)
t = threading.Thread(target=main())
t.start()
t.join()














