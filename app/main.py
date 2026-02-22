from typing import Any, Hashable, Iterator


class Dictionary:
    _TOMBSTONE = object()

    class _Node:
        def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
            self.key = key
            self.hash = hash_value
            self.value = value

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity
        self.load_factor = 0.75

    def _find_slot(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self.capacity
        first_tombstone = None

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if isinstance(node, self._Node):
                if node.hash == key_hash and node.key == key:
                    return index
            elif node is self._TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index

            index = (index + 1) % self.capacity
        return first_tombstone if first_tombstone is not None else index

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if isinstance(node, self._Node):
                index = node.hash % self.capacity
                while self.hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                self.hash_table[index] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if isinstance(self.hash_table[index], self._Node):
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = self._Node(key, key_hash, value)
            self.length += 1
            if self.length / self.capacity >= self.load_factor:
                self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if isinstance(self.hash_table[index], self._Node):
            return self.hash_table[index].value
        else:
            raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if not isinstance(self.hash_table[index], self._Node):
            raise KeyError(f"Key not found: {key}")
        self.hash_table[index] = self._TOMBSTONE
        self.length -= 1

    def __iter__(self) -> Iterator[Hashable]:
        for node in self.hash_table:
            if isinstance(node, self._Node):
                yield node.key
