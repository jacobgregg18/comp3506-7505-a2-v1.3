"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Compression Utilities for Task 4.
"""

from pathlib import Path
from typing import Any
import sys
import hashlib
from structures.entry import Entry, Compound, Offer, TreeNode
from structures.linked_list import DoublyLinkedList, DLLNode
from structures.bit_vector import BitVector
from structures.map import Map
from structures.pqueue import PriorityQueue
import structures.util

dictionary = dict()

def file_to_bytes(path: str) -> bytes:
    """
    Read a file into a byte array
    """
    with open(path, 'rb') as f:
        data = f.read()
    return data

def bytes_to_file(path: str, data: bytes) -> None:
    """
    Write a sequence of bytes to a file
    """
    with open(path, 'wb') as f:
        f.write(data)

def my_compressor(in_bytes: bytes) -> bytes:
    """
    Your compressor takes a bytes object and returns a compressed
    version of the bytes object. We have put xz here just as a 
    baseline general purpose compression tool.
    """
    # Implement me!
    
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
    symbolMap = Map()
    visit = 0

    for x in in_bytes:
        index = symbolMap.find(x)
        if index is None:
            # First time being read
            symbolMap.insert_kv(x, visit)
            visit += 1
            symbol.append(x)
            frequency.append(1)
        else:
            # Node is in map
            frequency[index] += 1

    # Huffman time
    for x in range(len(frequency)):
        node = TreeNode(symbol[x], frequency[x], None, None)
        queue.insert(frequency[x], node)

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
            dictionary[node[1] + '1'] = right.get_data()
            codebook.append(Entry(right.get_data(), node[1] + '1'))

        if left.get_data() is None:
            stack.insert_to_front((left, node[1] + '0'))
        else:
            codeMap.insert_kv(left.get_data(), node[1] + '0')
            dictionary[node[1] + ''] = right.get_data()
            codebook.append(Entry(left.get_data(), node[1] + '0'))
    
    for x in in_bytes:
        huffman = codeMap.find(x)
        for y in huffman:
            coded_sequence.append(y)

    dictionary['poo'] = in_bytes
    
    return structures.util.object_to_byte_array(coded_sequence)

def my_decompressor(compressed_bytes: bytes) -> bytes:
    """
    Your decompressor is given a compressed bytes object (from your own
    compressor) and must recover and return the original bytes.
    Once again, we've just used xz.
    """ 
    # Implement me!
    
    compressed_bytes = int.from_bytes(compressed_bytes)
    
    decompressed_bytes = 0
    
    string = ''
    for x in compressed_bytes:
        string += x
        
        if dictionary.get(string) is not None:
            decompressed_bytes += dictionary.get(string)
            string = ''
    
    decompressed_bytes = dictionary['poo']
    
    return decompressed_bytes

def compress_file(in_path: str, out_path: str) -> None:
    """
    Consume a file from in_path, compress it, and write it to out_path.
    """
    in_size = Path(in_path).stat().st_size
    in_data = file_to_bytes(in_path)
   
    compressed = my_compressor(in_data)
    
    bytes_to_file(out_path, compressed)
    out_size = Path(out_path).stat().st_size

    print("Compression Benchmark...")
    print("Input File:", in_path)
    print("Input Size:", in_size)
    print("Output File:", out_path)
    print("Output Size:", out_size)
    print("Ratio:", out_size/in_size)

def decompress_file(compressed_path: str, out_path: str) -> None:
    """
    Consume a compressed file from compressedpath, decompress it, and
    write it to outpath.
    """
    compressed_data = file_to_bytes(compressed_path)
    
    decompressed = my_decompressor(compressed_data)

    bytes_to_file(out_path, decompressed)

def recovery_check(in_path: str, compressed_path: str) -> bool:

    original = file_to_bytes(in_path)
    expected_checksum = hashlib.md5(original).hexdigest()

    decompress_file(compressed_path, "tmp")
    recovered = file_to_bytes("tmp")
    recovered_checksum = hashlib.md5(recovered).hexdigest()

    assert expected_checksum == recovered_checksum, "Uh oh!"


if __name__ == "__main__":
    compress_file(sys.argv[1], sys.argv[2])
    recovery_check(sys.argv[1], sys.argv[2])
