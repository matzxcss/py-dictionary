class Dictionary:
    class _Node:
        def __init__(self, key: str, hash_value: int, value: str) -> None:
            self.key = key
            self.hash = hash_value
            self.value = value

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity
        self.load_factor = 0.75

    def _hash_index(self, key: str) -> tuple[int, int]:
        key_hash = hash(key)
        index = key_hash % self.capacity
        return index, key_hash

    def _find_slot(self, key: str, key_hash: int) -> int:
        index = key_hash % self.capacity
        start_index = index
        while self.hash_table[index] is not None:
            if (
                self.hash_table[index].key == key
                and self.hash_table[index].hash == key_hash
            ):
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return index

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                index = node.hash % self.capacity
                while self.hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                self.hash_table[index] = node

    def __setitem__(self, key: str, value: str) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if self.hash_table[index] is not None:
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = self._Node(key, key_hash, value)
            self.length += 1
            if self.length / self.capacity >= self.load_factor:
                self._resize()

    def __getitem__(self, key: str) -> str:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if self.hash_table[index] is not None:
            return self.hash_table[index].value
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: str) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if self.hash_table[index] is None:
            raise KeyError(key)
        self.hash_table[index] = None
        self.length -= 1

    def __iter__(self) -> str:
        for node in self.hash_table:
            if node is not None:
                yield node.key
