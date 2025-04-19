from dataclasses import dataclass

@dataclass
class Configuration:
    debug: bool = True
    host: str = '0.0.0.0'
    port: int = 5001

def read_config():
    return Configuration()