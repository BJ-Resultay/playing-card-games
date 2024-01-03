"""module models actual player"""
# Date:	27 Dec 2023
# Revision History:
#	resultay | 27-12-23 | Initial version

from logging import getLogger
from math import inf
from Levenshtein import distance
from src.general.player import (
    InsufficientAmount,
    NotPositive,
    Player,
)

LOGGER = getLogger(__name__)

class RealPlayer(Player):
    """class takes in player input"""
    def __init__(self) -> None:
        name = input('Enter name: ')
        super().__init__(name)
        self.logger = LOGGER

    def __input(self) -> str:
        """function takes player input

        Returns:
            str: raw_input
        """
        raw_input = None
        while not raw_input:
            raw_input = input('> ')
        self.logger.info('Raw input %s', raw_input)
        return raw_input

    def user_choice(self, prompt: str, choices: list[str]) -> str:
        """function interprets input into closest choice

        Args:
            prompt (str): question for user
            choices (list[str]): valid choices

        Returns:
            str: closest choice of valid choices
        """
        print(prompt)
        choices.sort()
        for choice in choices:
            print(f'* {choice}')
        raw_input = self.__input()

        # if choice starts with input
        filtered_choices = [choice for choice in choices if choice.startswith(raw_input)]
        if filtered_choices:
            return filtered_choices[0]

        # else use minimum levenshtein distance
        # https://maxbachmann.github.io/Levenshtein
        levenshtein_distances = [distance(raw_input, choice) for choice in choices]
        print(levenshtein_distances)
        minimum_position = levenshtein_distances.index(min(levenshtein_distances))
        return choices[minimum_position]

    def user_chips(self) -> None:
        """function takes player bet
        """
        prompt = f"""
        Current Balance {self.chips}
        Place bet.
        """
        chips = inf
        clean = None
        while clean is None:
            try:
                chips = self.user_float(prompt)
                self.bet_chips(chips)
                clean = False
            except (InsufficientAmount, NotPositive) as e:
                self.logger.warning(e)
                print(e)

    def user_float(self, prompt: str) -> float:
        """function interprets input as float

        Args:
            prompt (str): question for user

        Returns:
            float: input as float
        """
        print(prompt)
        number = None
        while number is None:
            try:
                number = float(self.__input())
            except ValueError:
                print(prompt)
        return number

    def user_integer(self, prompt: str) -> int:
        """function interprets input as int

        Args:
            prompt (str): question for user

        Returns:
            int: input as integer
        """
        print(prompt)
        number = None
        while number is None:
            try:
                number = int(self.__input())
            except ValueError:
                print(prompt)
        return number
