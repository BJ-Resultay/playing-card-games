"""module models actual player"""
# Date:	27 Dec 2023
# Revision History:
#	resultay | 27-12-23 | Initial version

from logging import getLogger
from Levenshtein import distance
from src.general.player import Player

LOGGER = getLogger(__name__)

class RealPlayer(Player):
    """class takes in player input"""
    def __init__(self) -> None:
        name = input('Enter name: ')
        super().__init__(name)
        self.logger = LOGGER

    def multiple_choice(self, prompt: str, choices: list[str]) -> str:
        """function takes player input

        Args:
            prompt (str): question for user
            choices (list[str]): valid choices

        Returns:
            str: closest choice
        """
        print(prompt)
        choices.sort()
        for choice in choices:
            print(f'* {choice}')
        raw_input = ''
        while not raw_input:
            raw_input = input('> ')
        self.logger.info('Raw input %s', raw_input)

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
