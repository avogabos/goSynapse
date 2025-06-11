from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Any
import json
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

@dataclass
class InitData:
    tick: int
    text: str
    abstick: int
    hash: str
    task: str

@dataclass
class NodeData:
    iden: str
    tags: dict[str, str]
    props: dict[str, Any]
    tagprops: dict[str, str]
    nodedata: dict[str, str]
    path: dict[str, str]

@dataclass
class Node:
    key: str
    data: List[List[str]]
    info: NodeData

@dataclass
class FiniData:
    tock: int
    abstock: int
    took: int
    count: int


@dataclass
class PrintData:
    mesg: str


def parse_json_stream(raw: bytes) -> Tuple[List[InitData], List[Node], List[FiniData], List[PrintData]]:
    """Parse a stream of JSON messages produced by Synapse.

    Args:
        raw: Raw bytes from the server.

    Returns:
        A tuple of lists: (init messages, nodes, fini messages, print messages).
    """
    reader = BytesIO(raw)
    decoder = json.JSONDecoder()
    buffer = ""

    init_items: List[InitData] = []
    nodes: List[Node] = []
    fini_items: List[FiniData] = []
    print_items: List[PrintData] = []

    for line in reader.readlines():
        decoded = line.decode()
        buffer += decoded
        buffer = buffer.strip()
        if not buffer:
            continue
        try:
            data, index = decoder.raw_decode(buffer)
            buffer = buffer[index:].lstrip()
        except json.JSONDecodeError:
            logger.debug("Failed to decode JSON line: %s", decoded.strip())
            continue

        if not isinstance(data, list) or not data:
            logger.debug("Unexpected storm message: %s", data)
            continue
        key = data[0]
        payload = data[1]
        if key == "init":
            init_items.append(InitData(**payload))
        elif key == "node":
            node_pairs = []
            if isinstance(payload[0], list):
                for pair in payload[0]:
                    node_pairs.append([str(x) for x in pair])
            info = NodeData(**payload[1])
            nodes.append(Node(key="node", data=node_pairs, info=info))
        elif key == "print":
            print_items.append(PrintData(**payload))
        elif key == "fini":
            fini_items.append(FiniData(**payload))
    return init_items, nodes, fini_items, print_items
