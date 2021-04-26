from abc import ABC, abstractmethod
import networkx as nx

class Source(ABC): 
    def __init__(self, context):
        self.context = context
            
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def shutdown(self):
        pass    
    
class Sink(ABC): 
    def __init__(self, context):
        self.context = context
        
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def process(self):
        pass
    
    @abstractmethod
    def shutdown(self):
        pass 

def process_pipeline(p,context):
    seq = [p.nodes[x]['component'] for x in list(nx.topological_sort(p))]
    sources = [x for x in filter(lambda x: issubclass(type(x),Source),seq)]
    sinks = [x for x in filter(lambda x: issubclass(type(x),Sink),seq)]
    
    # Init
    print("Initializing pipeline")
    print("Sequence:", list(nx.topological_sort(p)))
    for x in seq:    
        x.setup()
    
    # Process
    print("Processing pipeline")
    eof_not_reached = False
    for x in sources:
        eof_not_reached |= x.read()
    
    while eof_not_reached:
        for x in sinks:
            x.process()    
            
        # Read next frame
        eof_not_reached = False
        for x in sources:
            eof_not_reached |= x.read()
    
    # Shutdown    
    print("Shutting down pipeline")
    for x in seq:
        x.shutdown()         