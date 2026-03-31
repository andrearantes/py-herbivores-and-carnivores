from typing import List, Self
from app.main import Animale, Herbivori, Carnivoro


class Animale:
    alive = List["Animal"] = []

    def __init__(
            self,
            name: str,
            health: int = 100,
            hidden: bool = False
    ) -> None:
        self.health = health
        self.name = name
        self.hidden = hidden
        Animale.alive.append(self)

    def __repr__(self) -> str:
        return (f"{{Name: {self.name},"
                f" Health: {self.health},"
                f" Hidden: {self.hidden}}}")


class Herbivori(Animale):
    def hide(self) -> None:
        self.hidden = not self.hidden


class Carnivoro(Animale):
    @staticmethod
    def bite(self: Self, herbivore: Herbivori) -> str:
        if isinstance(herbivore, Herbivori) and herbivore.hidden is False:
            herbivore.health -= 50
        if herbivore.health <= 0:
            Animale.alive.remove(herbivore)
