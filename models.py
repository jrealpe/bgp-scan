import db

from sqlalchemy import Column, Integer, String, Float


class BGP(db.Base):
    '''
    1299 174 14522
      216.218.252.167 from 216.218.252.167 (216.218.252.167)
        Origin IGP, metric 48, localpref 70, valid, internal
        Originator: 216.218.252.176, Cluster list: 216.218.252.151
        Last update: Fri Jun  4 21:42:22 2021
    '''

    __tablename__ = 'bgp'

    id = Column(Integer, primary_key=True)
    ip = Column(String, nullable=False)
    network = Column(String, nullable=False)
    next_hop = Column(String, nullable=False)
    metric = Column(String, nullable=False)
    locprof = Column(String, nullable=False)
    path = Column(String, nullable=False)
    cluster_list = Column(String, nullable=True)
    origin = Column(String, nullable=False)
    last_update = Column(String, nullable=False)
  
    def __init__(self, ip, network, next_hop, metric, locprof, path, cluster_list,
                 origin, last_update):
        self.ip = ip
        self.network = network
        self.next_hop = next_hop
        self.metric = metric
        self.locprof = locprof
        self.path = path
        self.cluster_list = cluster_list
        self.origin = origin
        self.last_update = last_update

    def __repr__(self):
        return f'BGP({self.network} -> {self.next_hop} ({self.path}))'

    def __str__(self):
        return f'{self.ip} (self.network)'
