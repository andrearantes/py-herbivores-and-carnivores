import os

import pytest
import io

from contextlib import redirect_stdout

from app.main import Animale, Herbivori, Carnivoro


def test_animal_class():
    assert hasattr(Animale, "alive"), (
        f"Animal class should have attribute 'alive'"
    )


def test_animal_constructor():
    lion = Animale("Lion King")
    assert hasattr(lion, "name"), (
        "Animal instance should have attribute 'name'"
    )
    assert hasattr(lion, "health"), (
        "Animal instance should have attribute 'health'"
    )
    assert hasattr(lion, "hidden"), (
        "Animal instance should have attribute 'hidden'"
    )
    assert lion.name == "Lion King", (
        f"'lion.name' should equal to 'Lion King' when "
        f"'lion' created by 'Animal('Lion King')'"
    )
    assert lion.health == 100, (
        f"'lion.health' should equal to 100 when "
        f"'lion' created by 'Animal('Lion King')'"
    )
    assert lion.hidden is False, (
        f"'lion.hidden' should equal to False when "
        f"'lion' created by 'Animal('Lion King')'"
    )
    assert len(Animale.alive) == 1, (
        "Constructor should add created animal to 'Animal.alive'"
    )
    assert Animale.alive[0].name == "Lion King", (
        "Constructor should add created animal to 'Animal.alive'"
    )


@pytest.mark.parametrize(
    "class_,method",
    [
        (Herbivori, "hide"),
        (Carnivoro, "bite"),
    ],
)
def test_only_one_method_should_be_declared_in_each_of_children_classes(
    class_, method
):
    assert Animale in class_.__bases__, (
        f"'{class_.__name__}' should be inherited from 'Animal'"
    )
    assert (
        method in class_.__dict__
    ), f"Method '{method}' should be defined inside class '{class_.__name__}'"
    assert {"__init__", "__str__", "__repr__"}.intersection(class_.__dict__) == set(), (
        f"Magic methods should not be declared in {class_}"
    )


def test_carnivore_bite_not_hidden():
    Animale.alive = []
    lion = Carnivoro("King Lion")
    rabbit = Herbivori("Susan")
    lion.bite(rabbit)
    assert rabbit.health == 50, (
        "If initial health of rabbit equals 100 and rabbit is not hidden "
        "health should equal to 50 after bite."
    )


def test_carnivore_bite_hidden():
    Animale.alive = []
    lion = Carnivoro("King Lion")
    rabbit = Herbivori("Susan")
    rabbit.hide()
    lion.bite(rabbit)
    assert rabbit.health == 100, (
        "Carnivore cannot bite hidden herbivore"
    )


def test_carnivore_bite_to_death():
    Animale.alive = []
    lion = Carnivoro("King Lion")
    pantera = Carnivoro("Bagira")
    rabbit = Herbivori("Susan")
    lion.bite(rabbit)
    pantera.bite(rabbit)
    assert len(Animale.alive) == 2, (
        f"It shouldn't be dead animals in Animals.alive"
    )


def test_carnivore_bite_carnivore():
    lion = Carnivoro("Simba")
    pantera = Carnivoro("Bagire")
    lion.bite(pantera)
    assert pantera.health == 100


def test_herbivore_hide():
    Animale.alive = []
    rabbit = Herbivori("Susan")
    rabbit.hide()
    assert rabbit.hidden is True, (
        "Method 'hide' should change animal attribute 'hidden'"
    )
    rabbit.hide()
    assert rabbit.hidden is False, (
        "Method 'hide' should change animal attribute 'hidden'"
    )


def test_print_animal_alive():
    Animale.alive = []

    lion = Carnivoro("King Lion")
    pantera = Carnivoro("Bagira")
    rabbit = Herbivori("Susan")

    f = io.StringIO()

    with redirect_stdout(f):
        print(Animale.alive)

    out = f.getvalue()
    output = "[{Name: King Lion, Health: 100, Hidden: False}, " \
             "{Name: Bagira, Health: 100, Hidden: False}, " \
             "{Name: Susan, Health: 100, Hidden: False}]\n"
    assert out == output, (
        f"Output should equal to {output} when you print 'Animal.alive' with "
        f"three animals"
    )


def test_when_health_less_than_zero():
    Animale.alive = []
    lion = Carnivoro("King Lion")
    rabbit = Herbivori("Susan", 25)
    lion.bite(rabbit)
    assert len(Animale.alive) == 1, (
        "Herbivore should die if health less than zero"
    )
    assert Animale.alive[0].name == "King Lion"


def test_unnecessary_comment():
    if os.path.exists(os.path.join(os.pardir, "app", "main.py")):
        main_path = os.path.join(os.pardir, "app", "main.py")
    else:
        main_path = os.path.join("app", "main.py")

    with open(main_path, "r") as main:
        main_content = main.read()

        assert (
                "# write your code here" not in main_content
        ), "Remove unnecessary comment"
