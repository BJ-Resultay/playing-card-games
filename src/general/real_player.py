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
    def __init__(self, **kwargs) -> None:
        if 'name' not in kwargs:
            kwargs['name'] = input('Enter name: ')
        super().__init__(**kwargs)
        self.logger = LOGGER

    def __input(self) -> str:
        """function takes player input

        Returns:
            str: raw_input
        """
        raw_input = None
        while not raw_input:
            raw_input = input('> ')
        self.logger.debug('Raw input "%s"', raw_input)
        return raw_input

    def user_choice(self, prompt: str, choices: list[str]) -> str:
        """function interprets input into closest choice

        Args:
            prompt (str): question for user
            choices (list[str]): valid choices

        Returns:
            str: closest choice of valid choices
        """
        if not choices:
            raise ValueError("No choices given")
        choices.sort()
        self.__user_choice_print_prompt(prompt, choices)
        choice = None
        while choice is None:
            try:
                choice = self.__user_choice_clean_input(choices)
            except ValueError:
                self.__user_choice_print_prompt(prompt, choices)
        return choice

    def __user_choice_print_prompt(self, prompt: str, choices: list[str]) -> None:
        """function prints prompt for user choice

        Args:
            prompt (str): question for user
            choices (list[str]): valid choices
        """
        print(prompt)
        for choice in choices:
            print(f'* {choice}')

    def __user_choice_clean_input(self, choices: list[str]) -> str:
        """function cleans choice input

        Args:
            choices (list[str]): valid choices

        Returns:
            str: intelligent choice
        """
        raw_input = self.__input()

        # if choice is exact
        if raw_input in choices:
            self.logger.info('Clean input "%s"', raw_input)
            return raw_input

        # if choice starts with input
        filtered_choices = [choice for choice in choices if choice.startswith(raw_input)]
        if filtered_choices:
            if len(filtered_choices) > 1:
                print('Multiple choices available:')
                for choice in filtered_choices:
                    print(f'* {choice}')
                raise ValueError
            self.logger.info('Clean input "%s"', filtered_choices[0])
            return filtered_choices[0]

        # else show minimum levenshtein distance
        # https://maxbachmann.github.io/Levenshtein
        levenshtein_distances = [distance(raw_input, choice) for choice in choices]
        min_levenshtein_distance = min(levenshtein_distances)
        indices = [
            index
            for index, value
            in enumerate(levenshtein_distances)
            if value == min_levenshtein_distance
        ]
        print('Did you mean?')
        for index in indices:
            print(f'* {choices[index]}')
        raise ValueError

    def user_chips(self) -> None:
        """function takes player bet"""
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
