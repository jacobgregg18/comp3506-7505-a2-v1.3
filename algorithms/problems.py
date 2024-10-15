"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

 Each problem will be assessed on three sets of tests:

1. "It works":
       Basic inputs and outputs, including the ones peovided as examples, with generous time and memory restrictions.
       Large inputs will not be tested here.
       The most straightforward approach will likely fit into these restrictions.

2. "Exhaustive":
       Extensive testing on a wide range of inputs and outputs with tight time and memory restrictions.
       These tests won't accept brute force solutions, you'll have to apply some algorithms and optimisations.

 3. "Welcome to COMP3506":
       Extensive testing with the tightest possible time and memory restrictions
       leaving no room for redundant operations.
       Every possible corner case will be assessed here as well.

There will be hidden tests in each category that will be published only after the assignment deadline.

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry, Compound, Offer, TreeNode
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList, DLLNode
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
import math


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    Task 3.1: Maybe Maybe Maybe

    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.

    Limitations:
        "It works":
            @database@ contains up to 1000 elements;
            @query@ contains up to 1000 elements.

        "Exhaustive":
            @database@ contains up to 100'000 elements;
            @query@ contains up to 100'000 elements.

        "Welcome to COMP3506":
            @database@ contains up to 1'000'000 elements;
            @query@ contains up to 500'000 elements.

    Each test will run over three false positive rates. These rates are:
        fp_rate = 10%
        fp_rate = 5%
        fp_rate = 1%.

    You must pass each test in the given time limit and be under the given
    fp_rate to get the associated mark for that test.
    """
    bloom = BloomFilter(len(database))
    for x in database:
        bloom.insert(x)

    answer = []

    for x in query:
        if bloom.contains(x) is True:
            answer.append(x)

    # DO THE THING

    return answer


def dora(graph: Graph, start: int, symbol_sequence: str,
         ) -> tuple[BitVector, list[Entry]]:
    """
    Task 3.2: Dora and the Chin Bicken

    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G.

    Return a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector should be read from index 0 upwards (so, the first symbol is
    encoded from index 0). You also need to return your codebook as a
    Python list of unique Entries. The Entry key should correspond to the
    symbol, and the value should be a string. More information below.

    Limitations:
        "It works":
            @graph@ has up to 1000 vertices and up to 1000 edges.
            the alphabet consists of up to 26 characters.
            @symbol_sequence@ has up to 1000 characters.

        "Exhaustive":
            @graph@ has up to 100'000 vertices and up to 100'000 edges.
            the alphabet consists of up to 1000 characters.
            @symbol_sequence@ has up to 100'000 characters.

        "Welcome to COMP3506":
            @graph@ has up to 1'000'000 vertices and up to 1'000'000 edges.
            the alphabet consists of up to 300'000 characters.
            @symbol_sequence@ has up to 1'000'000 characters.

    """
    coded_sequence = BitVector()
    queue = PriorityQueue()

    """
    list of Entry objects, each entry has key=symbol, value=str. The str
    value is just an ASCII representation of the bits used to encode the
    given key. For example: x = Entry("c", "1101")
    """
    codebook = []
    symbol = []
    frequency = []

    # DO THE THING
    node = graph.get_node(start)
    symbolMap = Map()
    visit = 0
    pathMap = Map()
    pathMap.insert_kv(start, node.get_data())
    queue = PriorityQueue()
    queue.insert_fifo(start)

    while queue.get_size() > 0:
        currentNode = queue.remove_min()
        nodes = graph.get_neighbours(currentNode)

        # Node is reachable from the start
        index = symbolMap.find(graph.get_node(currentNode).get_data())
        if index is None:
            # Node not in the map yet
            symbolMap.insert_kv(graph.get_node(currentNode).get_data(), visit)
            visit += 1
            symbol.append(graph.get_node(currentNode).get_data())
            frequency.append(1)
        else:
            # Node is in map
            frequency[index] += 1

        for y in nodes:
            # Not the target, enqueue and add to visited order if not repeated
            if pathMap.find(y.get_id()) is None:
                queue.insert_fifo(y.get_id())
                pathMap.insert_kv(y.get_id(), y.get_data())

    # Huffman time
    for x in range(len(frequency)):
        node = TreeNode(symbol[x], frequency[x], None, None)
        queue.insert(frequency[x], node)
        # print("Symbol: " + str(symbol[x]) + " Frequency: " + str(frequency[x]))

    while queue.get_size() > 1:
        left = queue.remove_min()
        right = queue.remove_min()
        node = TreeNode(None, left.get_freq() + right.get_freq(), left, right)
        queue.insert(node.get_freq(), node)

    tree = queue.remove_min()
    codeMap = Map()
    stack = DoublyLinkedList()
    stack.insert_to_front((tree, ''))

    while stack.get_size() > 0:
        node = stack.remove_from_front()
        left = node[0].get_left()
        right = node[0].get_right()

        if right.get_data() is None:
            stack.insert_to_front((right, node[1] + '1'))
        else:
            codeMap.insert_kv(right.get_data(), node[1] + '1')
            codebook.append(Entry(right.get_data(), node[1] + '1'))
            # print(node.get_value() + '1')

        if left.get_data() is None:
            stack.insert_to_front((left, node[1] + '0'))
        else:
            codeMap.insert_kv(left.get_data(), node[1] + '0')
            codebook.append(Entry(left.get_data(), node[1] + '0'))
            # print(node.get_value() + '0')

    for x in symbol_sequence:
        huffman = codeMap.find(x)
        for y in huffman:
            # print(y)
            coded_sequence.append(int(y))

    return (coded_sequence, codebook)


def chain_reaction(compounds: list[Compound]) -> int:
    """
    Task 3.3: Chain Reaction

    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Return the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.

    Limitations:
        "It works":
            @compounds@ has up to 10 elements

        "Exhaustive":
            @compounds@ has up to 50 elements

        "Welcome to COMP3506":
            @compounds@ has up to 100 elements

    """
    maximal_compound = -1

    # DO THE THING
    size = len(compounds)
    reactions = DynamicArray()
    list = [0] * (size * size)
    reactions.build_from_list(list)

    # First iteration adds reactions based on occurance from main reaction
    for x in range(size):
        base = compounds[x].get_coordinates()
        base_radius = compounds[x].get_radius()
        for y in range(size):
            compare = compounds[y].get_coordinates()
            x_diff = base[0] - compare[0]
            y_diff = base[1] - compare[1]
            if (math.pow(x_diff, 2) + math.pow(y_diff, 2)) <= math.pow(base_radius, 2):
                # The comparison is inside the chain reaction
                reactions[(x * size) + y] = 1

    # Second iteration adds the chain reactions
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if reactions[x * size + z] == 1:
                    # Reaction occurs, cycle through reactions and add to X
                    if reactions[y * size + x] == 1:
                        reactions[y * size + z] = 1

    # Third iteration sums the total reactions
    max_size = -1
    sum = 0
    for x in range(size):
        for y in range(size):
            sum += reactions[x * size + y]
        if sum > max_size:
            max_size = sum
            maximal_compound = compounds[x].get_compound_id()
            # print(str(maximal_compound) + " " + str(max_size))
        if sum == max_size:
            if compounds[x].get_compound_id() < maximal_compound:
                maximal_compound = compounds[x].get_compound_id()
        sum = 0

    return maximal_compound


def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    Task 3.4: Labyrinth

    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.

    Return the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier.
    You are guaranteed that all offer ids are distinct.

    Limitations:
        "It works":
            @offers@ contains up to 1000 items.
            0 <= n <= 1000
            0 <= m <= 1000
            0 <= k <= 1000

        "Exhaustive":
            @offers@ contains up to 100'000 items.
            0 <= n <= 10^6
            0 <= m <= 10^6
            0 <= k <= 10^6

        "Welcome to COMP3506":
            @offers@ contains up to 5'000'000 items.
            0 <= n <= 10^42
            0 <= m <= 10^42
            0 <= k <= 10^42

    """
    best_offer_id = -1
    best_offer_cost = float('inf')

    # DO THE THING

    for x in offers:
        if x.get_num_edges() > (x.get_num_nodes() * (x.get_num_nodes() - 1) / 2):
            # Not a sigmple graph (has over maximum edges)
            continue
        if x.get_num_edges() < x.get_num_nodes() - 1:
            # Not a connected graph (Less edges then nodes)
            continue
        if x.get_k() == 1:
            if x.get_num_edges() < (x.get_num_nodes() * (x.get_num_nodes() - 1) / 2):
                # Not all nodes connected via single edge
                continue
        if x.get_k() < 1 or x.get_num_nodes() < 1 or x.get_num_edges() < 0:
            # Not valid inputs
            continue
        if x.get_cost() < best_offer_cost:
            best_offer_cost = x.get_cost()
            best_offer_id = x.get_offer_id()
            continue
        if x.get_cost() == best_offer_cost:
            if x.get_offer_id() < best_offer_id:
                best_offer_cost = x.get_cost()
                best_offer_id = x.get_offer_id()

    return (best_offer_id, best_offer_cost)
