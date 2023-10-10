import os
import importlib

package_dir = os.path.dirname(__file__)
module_files = [
    f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py"
]

for module_name in module_files:
    importlib.import_module(f"{__package__}.{module_name}")

__all__ = module_files