import nomad
import consul
import docker
import socket


class NetworkAgent(object):
    def __init__(self, host:str, port:int):
        # Configure Hashicorp services
        self.nomad = nomad.Nomad(host=host)
        self.consul = consul.Consul(host=host)
        
        # Configure Docker
        self.docker = docker.from_env()
        
        # Set up local UDP socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self._host, self._port = self.socket.getsockname()
        
    @property
    def nomad_members(self) -> list:
        member_list = []
        members = self.nomad.agent.get_members()
        for member in members["Members"]:
            member_list.append(member["Name"])
            
        return member_list
    
    @property
    def address(self) -> tuple:
        return (self._host, self._port)
    
    @property
    def ip_str(self) -> str:
        return f'{self._host}:{self._port}'  
    
    @property
    def health(self):
        return self.nomad.agent.get_health()     
    