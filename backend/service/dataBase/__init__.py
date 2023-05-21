# __init__.py

from .InventoryDatabase import Access
from .TrafficDatabase import Traffic

# Initialization code
print("Initializing dataBase package...")

# Define the public interface of the package
__all__ = ['Access', 'Traffic']
