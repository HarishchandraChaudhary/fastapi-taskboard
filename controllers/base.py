from punq import Container
from fastapi import Depends
from typing import Annotated

# Placeholder for DI - will be overridden in main.py
def get_container() -> Container:
    raise NotImplementedError("Container dependency not initialized.")

ContainerDep = Annotated[Container, Depends(get_container)]