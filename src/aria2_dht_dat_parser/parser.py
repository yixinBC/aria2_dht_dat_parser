import os
from socket import inet_ntop, AF_INET, AF_INET6


def parse(path: str) -> dict:
    """
    [WARNING] This function is not tested on IPv6 addresses.
    Parses an Aria2 DHT file and returns a dictionary containing its contents.

    Args:
        path (str): The path to the Aria2 DHT file.

    Returns:
        dict: A json-liked dictionary containing the parsed contents of the Aria2 DHT file.
        It's structure is as follows:
        {
            "format_id": 2,
            "version": 3,
            "file_saved_time": 1620000000,
            "local_node_id": "x"*20,
            "num_node": 100,
            "nodes": [
                {
                    "ip": "127.0.0.1",
                    "port": 6881,
                    "id": "x"*20
                }, ...(in total 100 nodes)
            ]
        }

    Raises:
        ValueError: If the file has an invalid magic header.
        FileNotFoundError: If the file does not exist.
        AssertionError: If the file has an invalid format id or version.
        AssertionError: If the file has an invalid node length.
    """
    result = {}
    if os.path.isfile(path):
        with open(path, "rb") as f:
            magic_header = f.read(2)
            if magic_header != b"\xA1\xA2":
                raise ValueError("Invalid magic header")
            result["format_id"] = int.from_bytes(f.read(1), "big")
            assert result["format_id"] == 2
            f.read(3)  # reserved bytes (3 bytes)
            result["version"] = int.from_bytes(f.read(2), "big")
            assert result["version"] == 3
            result["file_saved_time"] = int.from_bytes(f.read(8), "big")
            f.read(8)  # reserved bytes (8 bytes)
            result["local_node_id"] = f.read(20).hex()
            f.read(4)  # reserved bytes (4 bytes)
            result["num_node"] = int.from_bytes(f.read(4), "big")
            f.read(4)  # reserved bytes (4 bytes)
            result["nodes"] = []
            for _ in range(result["num_node"]):
                PLEN = int.from_bytes(f.read(1), "big")
                assert PLEN == 6 or PLEN == 18
                f.read(7)  # reserved bytes (7 bytes)
                if PLEN == 6:
                    node_ip = inet_ntop(AF_INET, f.read(4))
                    node_port = int.from_bytes(f.read(2), "big")
                else:
                    node_ip = inet_ntop(AF_INET6, f.read(16))  # IPv6 not tested
                    node_port = int.from_bytes(f.read(2), "big")
                f.read(24 - PLEN)  # reserved bytes (24-PLEN bytes)
                node_id = f.read(20).hex()
                f.read(4)  # reserved bytes (4 bytes)
                result["nodes"].append(
                    {"ip": node_ip, "port": node_port, "id": node_id}
                )
        return result
    else:
        raise FileNotFoundError(f"File not found: {path}")
