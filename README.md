# aria2_dht_dat_parser

parse aria2's dht.dat into human-readable json

## Install

```bash
pip install aria2-dht-dat-parser
```

## Usage

use as a cli tool

```bash
aria2-dht-dat-parser -i dht.dat [-o dht.json]
```

use as a python module

```python
from aria2_dht_dat_parser import parse
result = parse('dht.dat')
```

## Parsed Result Example

```json
{
    "format_id": 2,
    "version": 3,
    "file_saved_time": 1620000000,
    "local_node_id": "xxxxxxxxxxxxxxxxxxxx",
    "num_node": 100,
    "nodes": [
        {
            "ip": "127.0.0.1",
            "port": 6881,
            "id": "xxxxxxxxxxxxxxxxxxxx"
        }, ...
    ]
}
```

## License

MIT
