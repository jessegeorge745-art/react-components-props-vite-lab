# models/person.py
# Base class that User inherits from.
# Provides shared name/email attributes with property validation.


class Person:
    """
    Base class representing a generic person.
    Shared by User via inheritance.
    """

    def __init__(self, name: str, email: str):
        # Initialise to empty so setters can safely assign
        self._name = ""
        self._email = ""
        self.name = name    # validated through setter
        self.email = email  # validated through setter

    # ------------------------------------------------------------------ #
    # Properties with validation (encapsulation)
    # ------------------------------------------------------------------ #

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value or "@" not in value:
            raise ValueError(f"Invalid email address: '{value}'.")
        self._email = value.strip()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, email={self._email!r})"