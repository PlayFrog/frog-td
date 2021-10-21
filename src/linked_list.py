from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class Node:
    item: Any
    next: Optional['Node'] = None
