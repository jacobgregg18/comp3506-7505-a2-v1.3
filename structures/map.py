"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self.size = 0
        self.collisions = 0
        self._arr = [None] * 769
        self.capacity = 769
        self._primes = [769, 1543, 6151, 49157, 786433, 3145739, 12582917]
        self._primesize = 0 

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        prehash = entry.get_hash()
        hash = prehash % self._primes[self._primesize]

        if self._arr[hash] is not None:
            # Elements have been added before
            retValue = self._arr[hash].find_and_update_entry(entry)
            # print("Repeat")
            if retValue is None:
                # Specific key is not in chain yet, add it
                self._arr[hash].insert_to_back(entry)
                self.collisions += 1
                self.size += 1
        else:
            # No element in this hash, create list
            list = DoublyLinkedList()
            list.insert_to_front(entry)
            self._arr[hash] = list
            retValue = None
            self.size += 1

        # Check collisions and size to determine if resize required
        if (self.collisions > self.capacity * 0.25) or (self.size > self.capacity * 0.8):
            # Resize needs to happen
            self.resize_map()

        return retValue

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        # hint: entry = Entry(key, value)
        entry = Entry(key, value)
        return self.insert(entry)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, value)
        self.insert(entry)
        return

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        if key is None:
            return None

        entry = Entry(key, 0)
        prehash = entry.get_hash()
        hash = prehash % self._primes[self._primesize]

        if self._arr[hash] is not None:
            # Data is inside the hash index
            value = self._arr[hash].find_and_remove_element(key)
            if value is not False:
                # Element was in list and removed
                self.size -= 1
                if self._arr[hash].get_size() != 0:
                    # There was a collision in linked list
                    self.collisions -= 1
        return

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, 0)
        prehash = entry.get_hash()
        hash = prehash % self._primes[self._primesize]

        if self._arr[hash] is not None:
            # Element hash has value
            entry = self._arr[hash].find_and_return_entry(key)
            if entry is not None:
                return entry.get_value()
            return None
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return True
        return False

    def resize_map(self) -> None:
        oldSize = self._primes[self._primesize]
        self._primesize += 1
        newSize = self._primes[self._primesize]
        newArr = [None] * newSize
        self.capacity = newSize
        self.collisions = 0

        for x in range(oldSize):
            if self._arr[x] is not None:
                listsize = self._arr[x].get_size()
                for y in range(listsize):
                    entry = self._arr[x].remove_from_front()
                    new_ix = entry.get_hash() % newSize
                    if newArr[new_ix] is not None:
                        # Elements have been added before
                        retValue = newArr[new_ix].find_and_update_entry(entry)
                        if retValue is None:
                            # Specific key is not in chain yet, add it
                            newArr[new_ix].insert_to_back(entry)
                            self.collisions += 1
                    else:
                        # No element in this hash, create list
                        list = DoublyLinkedList()
                        list.insert_to_front(entry)
                        newArr[new_ix] = list

        # New array contains all hashed functions
        self._arr = newArr
        return
