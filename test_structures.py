"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will not be used for marking and is here to provide you with
a simple way of testing your data structures. You may edit this file by adding
your own test functionality.
"""

# Import helper libraries
import argparse
import sys
import random

# Import our new structures
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable

def test_pqueue() -> None:
    """
    A simple set of tests for the priority queue.
    This is not marked and is just here for you to test your code.
    """
    print("==== Executing Priority Queue Tests ====")
    my_pq = PriorityQueue()
    my_pq.insert(0, "highest priority item")
    my_pq.insert(10, "priority value 10 item")
    my_pq.insert(1, "highest priority item")
    my_pq.insert(9, "priority value 10 item")
    my_pq.insert(12, "highest priority item")
    my_pq.insert(3, "priority value 10 item")
    print(my_pq)
    my_pq.remove_min()
    print(my_pq)
    my_pq.remove_min()
    print(my_pq)
    my_pq.insert(50, "highest priority item")
    print(my_pq)
    my_pq.remove_min()
    print(my_pq)
    print("==== Executing Priority Queue Tests ====")
    pq1 = PriorityQueue()
    list = DynamicArray()
    list.append(Entry(10, "hi"))
    list.append(Entry(0, "Yo"))
    list.append(Entry(2, "Haha"))
    list.append(Entry(13, "gg"))
    list.append(Entry(11, "hi"))
    list.append(Entry(45, "Yo"))
    list.append(Entry(24, "Haha"))
    list.append(Entry(-12, "gg"))
    list.append(Entry(3, "hi"))
    list.append(Entry(1, "Yo"))
    list.append(Entry(58, "Haha"))
    list.append(Entry(7, "gg"))
    
    list.append(Entry(100, "hi"))
    list.append(Entry(-1, "Yo"))
    list.append(Entry(6, "Haha"))
    list.append(Entry(-4, "gg"))
    list.append(Entry(14, "hi"))
    list.append(Entry(43, "Yo"))
    list.append(Entry(5, "Haha"))
    list.append(Entry(-22, "gg"))
    list.append(Entry(-24, "hi"))
    list.append(Entry(-23, "Yo"))
    list.append(Entry(-50, "Haha"))
    list.append(Entry(1110, "gg"))
    pq1.ip_build(list)
    print(pq1)
    pq1.sort()
    print(pq1)
    for x in range(24):
        pq1.remove_min()
        #print(pq1)
        
    for x in range(1000):
        pq1.insert_fifo(x+3)
    
    for x in range(1000):
        y = pq1.remove_min()
        if ((x+3) != y):
            print(pq1)
            

    """
    This one is up to you - we provided most of the code already :-)
    """


def test_map() -> None:
    """
    A simple set of tests for the associative map.
    This is not marked and is just here for you to test your code.
    """
    # Seed PRNG
    random.seed(1337)
    print("==== Executing Map Tests ====")
    my_map = Map()
    my_map.remove(10)
    # Make some entries    
    e1 = Entry(1, "value_for_key_1")
    e2 = Entry(10, "value_for_key_10")
    e3 = Entry(10, "vvvv")
    my_map.insert(e1)
    print(my_map.insert(e2))
    print(my_map.insert(e3))
    print(my_map.insert(e2))
    print(my_map.insert_kv(True, "Barry rules"))
    print(my_map.insert_kv("Hello", "rules"))
    print(my_map.insert_kv(45, "Barry"))
    print(my_map.insert_kv(-100, "NANANA"))
    print(my_map.insert_kv("Yolo", "Pen"))
    my_map[3] = "value_for_key_3"
    print("Size is " + str(my_map.get_size()))
    #assert my_map.get_size() == 4
    print("insert works")
    my_map.remove(10)
    my_map.remove(3)
    #assert my_map.get_size() == 2
    print(my_map.find(True))
    print(my_map.find(3))
    print(my_map.__getitem__("Yolo"))
    print(my_map.__getitem__("Hello"))
    print(my_map.__getitem__(10))

    """
    OK, simple boring hand written tests don't really find bugs... Just
    use them to detect specific corner cases and/or unit test each individual
    function. Let's do some better testing now. Fuzz against a python dict
    to make sure your data structure works. Make sure you capture all functions
    including any resizing that is done.
    """
    


def test_bloom() -> None:
    """
    Bloom Filter tests. Not marked.
    """
    # Seed PRNG
    random.seed(1337)

    # Some parameters we might like to mess around with
    MAX_KEYS = 200_000
    GEN_MAX = 100_000
    MIN_LEN = 5
    MAX_LEN = 15

    print("==== Executing BFF Tests ====")
    bf = BloomFilter(MAX_KEYS)
    assert bf.is_empty()==True, "Error: is_empty() is not True on an empty BF."

    print("Generating", GEN_MAX, "random strings to insert into the BF...")
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
    random_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(MIN_LEN, MAX_LEN))) for _ in range(GEN_MAX)]
    print("Removing duplicates...")
    random_strings = list(set(random_strings))
    print("Retained", len(random_strings), "elements...")

    # Now add them to the BF
    print ("Adding all strings to the BF now...")
    for string in random_strings:
        bf.insert(string)
    print ("Done!")

    # Now look them all up
    print ("Now looking up every key; the BF must return true for every single one.")
    for string in random_strings:
        assert bf.contains(string) == True, "Bloom Filter did not return True for a key that was inserted."

    # Now generate some new random strings
    print ("Generating new query strings that ARE NOT contained in the BF...")
    query_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(5, 15))) for _ in range(100000)]
    query_strings = list(set(query_strings).difference(random_strings))
    print ("Retained", len(query_strings), "query strings that are NOT in the BF.")

    # Now we'll look for these; we might get false positives, so we can measure
    # this and return the false positive rate
    pos = 0
    for string in query_strings:
        if bf.contains(string):
            pos += 1
    print("Querying for", len(query_strings), "unique strings not in the BF returned a count of", pos, " 'True' - False positive rate = ", pos / len(query_strings))

    """
    You need to now decide if this FP rate is acceptable or not. You could
    also try mixed query sets where some elements are inside, and some not.
    You can always track the fp/tp rate by maintaining a list/map/dict/set of
    elements that you have inserted, and checking against that as you go.
    """


# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description="COMP3506/7505 Assignment Two: Data Structure Tests")

    parser.add_argument("--pq", action="store_true", help="Run Priority Queue tests?")
    parser.add_argument("--map", action="store_true", help="Run Map tests?")
    parser.add_argument("--bloom", action="store_true", help="Run Bloom Filter tests?")
    parser.set_defaults(pq=False, map=False, bloom=False)

    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Test each
    if args.pq:
        test_pqueue()
    if args.map:
        test_map()
    if args.bloom:
        test_bloom()
