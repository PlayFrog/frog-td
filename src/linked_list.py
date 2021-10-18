from typing import TypeVar

T = TypeVar("T")


class Node:
    def __init__(self, item: T):
        self.item = item
        self.next = None
