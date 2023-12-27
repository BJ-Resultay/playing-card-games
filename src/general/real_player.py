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

    def input(self, actions: list[str]) -> str:
        """function takes player input

        Args:
            actions (list[str]): available actions

        Returns:
            str: closest action
        """
        actions.sort()
        for action in actions:
            print(f'* {action}')
        raw_input = input('> ')
        self.logger.info('Raw input %s', raw_input)

        # if action starts with input
        filtered_actions = [action for action in actions if action.startswith(raw_input)]
        if filtered_actions:
            return filtered_actions[0]

        # else if action contains input
        filtered_actions = [action for action in actions if raw_input in action]
        if filtered_actions:
            return filtered_actions[0]

        # else use minimum levenshtein distance
        # https://maxbachmann.github.io/Levenshtein
        levenshtein_distances = [distance(raw_input, action) for action in actions]
        print(levenshtein_distances)
        minimum_position = levenshtein_distances.index(min(levenshtein_distances))
        return actions[minimum_position]
