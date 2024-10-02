"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.bit_vector import BitVector
import structures.util
import math


class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._data = BitVector()
        self._bits = int((-max_keys * math.log(0.01)) / (math.log(2) * math.log(2))) + 1
        self._data.allocate(self._bits)
        self._contains = 0
        self._hashes = int((self._bits / max_keys) * math.log(2) + 1)
        if self._hashes > 15:
            self._hashes = 15
        self._primes = [6151, 49157, 786433]
        # More variables here if you need, of course

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        bits = ""
        for i in range(self._data.get_size()):
            bits += str(self._data.get_at(i))
        return bits

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity for full marks: O(1)
        """
        self._contains += 1

        for x in range(self._hashes):
            hash1 = self.hash(key, x + 1)
            self._data.set_at(hash1)

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        for x in range(self._hashes):
            hash = self.hash(key, x + 1)
            if self._data.get_at(hash) == 0:
                # Number not set, number not in set
                return False
        return True

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        if self._contains == 0:
            return True
        return False

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._bits

    def hash(self, value: Any, hash_number: int) -> int:
        bytes = structures.util.object_to_byte_array(value)
        bits = int.from_bytes(bytes, "big")

        hash_type = hash_number % 3
        compression_number = hash_number // 3

        if hash_type == 1:
            return self.hash_one(bits) % self._primes[compression_number]
        elif hash_type == 2:
            return self.hash_two(bits) % self._primes[compression_number]
        else:
            return self.hash_three(bits) % self._primes[compression_number]

    def hash_one(self, value: int) -> int:
        return (3079 * value + 98317) % 50331653

    def hash_two(self, value: int) -> int:
        return (1543 * value + 24593) % 25165843

    def hash_three(self, value: int) -> int:
        return (769 * value + 49157) % 3145739
