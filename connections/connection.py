import abc

class ConnectionInterface(metaclass=abc.ABCMeta):
    """Interface class for connections."""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'send') and 
                callable(subclass.send) and 
                hasattr(subclass, 'close') and 
                callable(subclass.close) or 
                NotImplemented)

    @abc.abstractmethod
    def open(self):
        """Opens the connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, color):
        """Sends a color.

        Parameters
        ----------
        color : tuple
            Expects a tuple like (r,g,b) with r,g,b ∈ {0,...,255}
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        """Closes the connection."""
        raise NotImplementedError

class InvalidColorError(Exception):
    """Raised when a color is not a tuple of (r,g,b) with r,g,b ∈ {0,..,255}."""
    pass
    