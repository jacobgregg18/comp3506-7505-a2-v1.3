"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable

def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
    ) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()
    reversedPath = DynamicArray()
    

    # ALGO GOES HERE
    duplicate = False
    queue = PriorityQueue()
    queue.insert_fifo(origin)
    visited_order.append(origin)
    pathMap = Map()
    goal_reached = 0
    
    while queue.get_size() > 0:
        nodes = graph.get_neighbours(origin)
        for y in nodes:
            if y.get_id() == goal:
                #Target reached, append then break
                visited_order.append(y.get_id())
                pathMap.insert_kv(y.get_id(), origin)
                goal_reached = 1
                break
            
            #Not the target, enqueue and add to visited order if not repeated
            for x in range(visited_order.get_size()):
                if visited_order.get_at(x) == y.get_id():
                    #Duplicate node, do not revist
                    duplicate = True
        
            if duplicate is False:
                #Enqueue only if firt time visited
                queue.insert_fifo(y.get_id())
                pathMap.insert_kv(y.get_id(), origin)
                visited_order.append(y.get_id())
                duplicate = False
      
        origin = queue.remove_min()

    #Create the path by travesing the map of nodes visited, if goal was reached
    if goal_reached == 1:
        while goal != origin:
            reversedPath.append(goal)
            goal = pathMap.find(goal)
        
        #Add the origin at the end  
        reversedPath.append(origin)
        
        for x in range(reversedPath.get_size()):
            path.append(reversedPath.get_at(reversedPath.get_size() - x - 1))
    
    # Return the path and the visited nodes list
    return (path, visited_order)

def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """
    valid_locations = DynamicArray() # This holds your answers

    # ALGO GOES HERE

    # Return the DynamicArray containing Entry types
    return valid_locations


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
    ) -> tuple[DynamicArray, DynamicArray]: 
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE

    # Return the path and the visited nodes list
    return (path, visited_order)




