from __future__ import annotations
from typing import List

import model

class GAgent:
    def __init__(self, server: model.GServer) -> None:
        self.server = server
        server.add_agent(self)

    def interact(self, agents: List[GAgent]) -> None:
        pass

    def update(self) -> None:
        pass

    def draw_graphic(self) -> None:
        pass

    def delete(self) -> None:
        self.server.remove_agent(self)