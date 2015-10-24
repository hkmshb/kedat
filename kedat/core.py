"""
Defines the core functions and classes for kedat.
"""



class Storage(dict):
    """Represents a dictionary object whose elements can be accessed and set 
    using the dot object notation. Thus in addition to `foo['bar']`, `foo.bar`
    can equally be used.
    """
    
    def __getattr__(self, key):
        return self.__getitem__(key)
    
    def __getitem__(self, key):
        return dict.get(self, key, None)
    
    def __getstate__(self):
        return dict(self)
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __setstate__(self, value):
        dict.__init__(self, value)
    
    def __repr__(self):
        return "<Storage %s>" % dict.__repr__(self)

