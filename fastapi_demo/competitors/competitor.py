from pydantic import BaseModel
from uuid import uuid4
from ipaddress import IPv4Address


class RegistrationModel(BaseModel):
    name: str
    open_port: int
    ip_addr: IPv4Address
    team_description: str


class CompetitorModel(BaseModel):
    name: str
    open_port: int
    ip_addr: str                    # To make serialization work out of the box
    team_description: str
    points: int
    challenge_level: int


class Competitor:

    def __init__(self, name: str, open_port: int, ip_addr: IPv4Address):
        self._name = name
        self._open_port = open_port
        self._ip_addr = ip_addr
        self._challenge_level = 1
        self._token = uuid4()  # generate a random UUID

    @classmethod
    def from_model(cls, registration: RegistrationModel, ip_addr: IPv4Address):
        return cls(registration.name, registration.open_port, ip_addr)

    def next_challenge(self):
        return {"to_ip": self._ip_addr,
                "to_port": self._open_port,
                "level": self._challenge_level,
                "token": self._token,
                "challenge": "1+1"}

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, o: object) -> bool:
        return (isinstance(o, Competitor)) and o._name == self._name


