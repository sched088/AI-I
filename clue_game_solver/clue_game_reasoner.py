'''clue_game_reasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Ported to Python3 by Andy Exley

Copyright (C) 2008 Dave Musicant
Copyright (C) 2020 Andy Exley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import sat_interface

# Initialize important variables

CASE_FILE = "CF"
POSSIBLE_PLAYERS = ["SC", "MU", "WH", "GR", "PE", "PL"]
POSSIBLE_CARD_LOCATIONS = POSSIBLE_PLAYERS + [CASE_FILE]
SUSPECTS = ["mu", "pl", "gr", "pe", "sc", "wh"]
WEAPONS = ["kn", "ca", "re", "ro", "pi", "wr"]
ROOMS = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
CARDS = SUSPECTS + WEAPONS + ROOMS


##
##
## What player are we? Do we need to differentiate in suggestor code? CardShown is shown for a player besides SC (PL)
## How do we return clauses?
##
## Rules reference: https://howdoyouplayit.com/rules-for-the-clue-boardgame/

class ClueGameReasoner:
    '''This class represents a clue game reasoner, a tool that can be used
    to track the information during a game of clue and deduce information
    about the game. (Hopefully help you win!)
    '''

    def __init__(self, player_order, card_nums=None):
        '''init for a particular clue game.
            player_order is a list of strings of players in the order that they
            are sitting around the table. Note: This may not include all the suspects,
            as there may be fewer than 6 players in any given game.

            card_nums is a list of numbers of cards in players' hands. It is
            possible that different players have different numbers of cards!
        '''
        print("__init__")
        self.players = player_order
        clauses = []

        # Each card is in at least one place (including case file).
        # If you want to change the string representation of the variables,
        #   go ahead!
        for c in CARDS:
            clause = ""
            for p in POSSIBLE_CARD_LOCATIONS:
                clause += c + "_" + p + " "
            clauses.append(clause)

        print("P1" + str(clauses))

        # TO BE IMPLEMENTED AS AN EXERCISE:

        # A card cannot be in two places.
        ''' 
        Places that cards can be: 
                - Case File
                - Player Hands (6 players)
        '''
        for c in CARDS:
            for p in POSSIBLE_CARD_LOCATIONS:
                for p1 in POSSIBLE_CARD_LOCATIONS:
                    if p != p1:
                        clause = "~" + c + "_" + p + " " + "~" + c + "_" + p1 + " "
                        clauses.append(clause)

        print("P2" + str(clauses))

        # At least one card of each category is in the case file.
        '''
        Categories:
            - Rooms
            - Weapons
            - Suspects
        '''
        clause = ""
        for s in SUSPECTS:
            clause += s + "_" + "CF"
        clauses.append(clause)

        clause = ""
        for w in WEAPONS:
            clause += w + "_" + "CF"
        clauses.append(clause)

        clause = ""
        for r in ROOMS:
            clause += r + "_" + "CF"
        clauses.append(clause)

        # No two cards in each category can both be in the case file.

        for s in SUSPECTS:
            for s1 in SUSPECTS:
                if s != s1:
                    clause = "~" + s + "_" + "CF" + " " + "~" + s1 + "_" + "CF" + " "
                    clauses.append(clause)

        for w in WEAPONS:
            for w1 in WEAPONS:
                if w != w1:
                    clause = "~" + w + "_" + "CF" + " " + "~" + w1 + "_" + "CF" + " "
                    clauses.append(clause)

        for r in ROOMS:
            for r1 in ROOMS:
                if r != r1:
                    clause = "~" + r + "_" + "CF" + " " + "~" + r1 + "_" + "CF" + " "
                    clauses.append(clause)

        self.KB = sat_interface.KB(clauses)
        print("P3: " + str(clauses))
        print(type(self.KB))

    def add_hand(self, player_name, hand_cards):  # maybe self.clauses?
        '''Add the information about the given player's hand to the KB'''
        # TO BE IMPLEMENTED AS AN EXERCISE
        clauses = []
        for hc in hand_cards:
            clause = hc + "_" + player_name + " "
            clauses.append(clause)
        print("hand clauses: " + str(clauses))

        # self.KB.add_clause(clauses)
        self.KB.clauses.extend(clauses)

    def suggest(self, suggester, c1, c2, c3, refuter, cardshown=None):
        '''Add information about a given suggestion to the KB'''
        # TO BE IMPLEMENTED AS AN EXERCISE
        # Example play to see variables
        # We go first, we suggest that it was Miss Scarlet,
        # with the Rope in the Lounge. Colonel Mustard refutes us
        # by showing us the Miss Scarlet card.
        # cgr.suggest("SC", "sc", "ro", "lo", "MU", "sc")

        # Need to account for refuting
        # Need to account for hand_cards
        # Need to account for where people are seated

        clauses = []

        if refuter is None:  # No refuter means that it is not in anyone else's hand (can also be written as in CF or player_hand)
            for p in POSSIBLE_PLAYERS:
                if suggester != POSSIBLE_PLAYERS:
                    clause = "~" + c1 + "_" + p + " " + "~" + c2 + "_" + p + " " + "~" + c3 + "_" + p + " "
                    clauses.append(clause)
        else:  # Being refuted: Not in hand until refuter
            suggester_seat = self.players.index(suggester)
            refuter_seat = self.players.index(refuter)
            player = suggester_seat + 1
            while player < refuter_seat:
                p = POSSIBLE_PLAYERS[player]
                clause = "~" + c1 + "_" + p + " " + "~" + c2 + "_" + p + " " + "~" + c3 + "_" + p + " "
                clauses.append(clause)
                player += 1
            # differentiate us getting refuted vs someone else
            if cardshown is None:  # someone else being refuted
                clause = c1 + "_" + refuter + " " + c2 + "_" + refuter + " " + c3 + "_" + refuter + " "
                clauses.append(clause)
            else:
                clause = cardshown + "_" + refuter
                clauses.append(clause)
            clause = "~" + c1 + "_" + CASE_FILE + " " + "~" + c2 + "_" + CASE_FILE + " " + \
                     "~" + c3 + "_" + CASE_FILE + " "
            clauses.append(clause)

        # self.KB.add_clause(clauses)
        print("suggest clauses: " + str(clauses))
        self.KB.clauses.extend(clauses)

    def accuse(self, accuser, c1, c2, c3, iscorrect):
        """Add information about a given accusation to the KB"""
        # TO BE IMPLEMENTED AS AN EXERCISE
        # If correct game over?
        # If incorrect then at least one option is not correct

        clauses = []

        if iscorrect:
            clause = c1 + "_" + CASE_FILE + " " + c2 + "_" + CASE_FILE + " " + c3 + "_" + CASE_FILE + " "
            clauses.append(clause)
        else:
            clause = "~" + c1 + "_" + CASE_FILE + " " + "~" + c2 + "_" + CASE_FILE + " " + \
                     "~" + c3 + "_" + CASE_FILE + " "
            clauses.append(clause)

        # If you are wrong and accuse you cannot win therefore you cannot accuse with cards you have
        clause = "~" + c1 + "_" + accuser + " " + "~" + c2 + "_" + accuser + " " + \
                 "~" + c3 + "_" + accuser + " "
        clauses.append(clause)
        # self.KB.add_clause(clauses)
        self.KB.clauses.extend(clauses)
        # self.KB = sat_interface.KB(clauses)

    def print_notepad(self):
        print("Notepad Clauses: " + str(self.KB.clauses))
        print("Clue Game Notepad:")
        for player in self.players:
            print('\t' + player, end='')
        print('\t' + CASE_FILE)
        for card in CARDS:
            print(card, '\t', end='')
            for player in self.players:
                # if player == "CF":
                print(self.get_test_string(card + "_" + player), '\t', end='')
            print(self.get_test_string(card + "_" + CASE_FILE))

    def get_test_string(self, variable):
        '''test a variable and return 'Y', 'N' or '-'

            'Y' if this positive literal is entailed by the KB
            'N' if its reverse is entailed
            '-' if neither is entailed

            additionally, the entailed literal (if any) will be added to the KB
        '''
        res = self.KB.test_add_variable(variable)
        if res == True:
            return 'Y'
        elif res == False:
            return 'N'
        else:
            return '-'


def play_clue_game1():
    # the game begins! add players to the game
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])
    # cgr.print_notepad()

    # Add information about our hand: We are Miss Scarlet,
    # and we have the cards Mrs White, Library, Study
    cgr.add_hand("SC", ["wh", "li", "st"])
    # cgr.print_notepad()

    # We go first, we suggest that it was Miss Scarlet,
    # with the Rope in the Lounge. Colonel Mustard refutes us
    # by showing us the Miss Scarlet card.
    cgr.suggest("SC", "sc", "ro", "lo", "MU", "sc")
    # cgr.print_notepad()

    # Mustard takes his turn. He suggests that it was Mrs. Peacock,
    # in the Dining Room with the Lead Pipe.
    # Mrs. White and Mr. Green cannot refute, but Mrs. Peacock does.
    cgr.suggest("MU", "pe", "pi", "di", "PE", None)
    # cgr.print_notepad()

    # Mrs. White takes her turn
    cgr.suggest("WH", "mu", "re", "ba", "PE", None)
    cgr.print_notepad()

    # and so on...
    cgr.suggest("GR", "wh", "kn", "ba", "PL", None)
    cgr.suggest("PE", "gr", "ca", "di", "WH", None)
    cgr.suggest("PL", "wh", "wr", "st", "SC", "wh")
    cgr.suggest("SC", "pl", "ro", "co", "MU", "pl")
    cgr.suggest("MU", "pe", "ro", "ba", "WH", None)
    cgr.suggest("WH", "mu", "ca", "st", "GR", None)
    cgr.suggest("GR", "pe", "kn", "di", "PE", None)
    cgr.suggest("PE", "mu", "pi", "di", "PL", None)
    cgr.suggest("PL", "gr", "kn", "co", "WH", None)
    cgr.suggest("SC", "pe", "kn", "lo", "MU", "lo")
    cgr.suggest("MU", "pe", "kn", "di", "WH", None)
    cgr.suggest("WH", "pe", "wr", "ha", "GR", None)
    cgr.suggest("GR", "wh", "pi", "co", "PL", None)
    cgr.suggest("PE", "sc", "pi", "ha", "MU", None)
    cgr.suggest("PL", "pe", "pi", "ba", None, None)
    cgr.suggest("SC", "wh", "pi", "ha", "PE", "ha")

    # aha! we have discovered that the lead pipe is the correct weapon
    # if you print the notepad here, you should see that we know that
    # it is in the case file. But it looks like the jig is up and
    # everyone else has figured this out as well...

    cgr.suggest("WH", "pe", "pi", "ha", "PE", None)
    cgr.suggest("PE", "pe", "pi", "ha", None, None)
    cgr.suggest("SC", "gr", "pi", "st", "WH", "gr")
    cgr.suggest("MU", "pe", "pi", "ba", "PL", None)
    cgr.suggest("WH", "pe", "pi", "st", "SC", "st")
    cgr.suggest("GR", "wh", "pi", "st", "SC", "wh")
    cgr.suggest("PE", "wh", "pi", "st", "SC", "wh")

    # At this point, we are still unsure of whether it happened
    # in the kitchen, or the billiard room. printing our notepad
    # here should reflect that we know all the other information
    cgr.suggest("PL", "pe", "pi", "ki", "GR", None)

    # Aha! Mr. Green must have the Kitchen card in his hand
    print('Before accusation: should show a single solution.')
    cgr.print_notepad()
    print()
    cgr.accuse("SC", "pe", "pi", "bi", True)
    print('After accusation: if consistent, output should remain unchanged.')
    cgr.print_notepad()


def play_clue_game2():
    '''This game recorded by Brooke Taylor and played by Sean Miller,
    George Ashley, Ben Limpich, Melissa Kohl and Andy Exley. Thanks to all!
    '''
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])
    cgr.add_hand("WH", ["kn", "ro", "ki"])

    # all suggestions
    cgr.suggest("MU", "mu", "di", "pi", "PE", None)
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", None)
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", "kn")
    cgr.suggest("WH", "li", "re", "pl", "GR", "re")
    cgr.suggest("PE", "st", "sc", "wr", "MU", None)
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", None)
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", "ro")
    cgr.suggest("MU", "pe", "pi", "ba", "PE", None)
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", None)
    cgr.suggest("PL", "ba", "mu", "wr", "PE", None)
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", "ca")
    cgr.suggest("GR", "sc", "ki", "wr", "PE", None)
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", "ha")
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)
    cgr.suggest("WH", "di", "pe", "wr", None, None)

    cgr.print_notepad()
    # final accusation
    cgr.accuse("WH", "di", "pe", "wr", True)
    # Brooke wins!


def play_clue_game3():
    '''Same as clue game 2, but from ms. peacock's perspective

    Note: It took my computer over 5 minutes to calculate the notepad on this one
    '''
    cgr = ClueGameReasoner(["SC", "MU", "WH", "GR", "PE", "PL"])
    cgr.add_hand("PE", ["sc", "mu", "ba"])
    cgr.suggest("MU", "mu", "di", "pi", "PE", "mu")
    cgr.suggest("WH", "pl", "ca", "ba", "PE", "ba")
    cgr.suggest("GR", "pe", "ba", "ro", "PE", "ba")
    cgr.suggest("PE", "ki", "sc", "re", "WH", "ki")
    cgr.suggest("SC", "wh", "st", "ro", "MU", None)
    cgr.suggest("MU", "lo", "pl", "kn", "WH", None)
    cgr.suggest("WH", "li", "re", "pl", "GR", None)
    cgr.suggest("PE", "st", "sc", "wr", "MU", "st")
    cgr.suggest("PL", "bi", "gr", "wr", "SC", None)
    cgr.suggest("MU", "co", "pe", "ca", "GR", None)
    cgr.suggest("PE", "lo", "mu", "ro", "PL", "lo")
    cgr.suggest("PL", "co", "mu", "wr", "GR", None)
    cgr.suggest("SC", "ha", "ro", "pe", "WH", None)
    cgr.suggest("MU", "pe", "pi", "ba", "PE", "ba")
    cgr.suggest("WH", "sc", "pi", "ha", "PE", "sc")
    cgr.suggest("PE", "pl", "wr", "co", "PL", "pl")
    cgr.suggest("PL", "ba", "mu", "wr", "PE", "ba")
    cgr.suggest("SC", "st", "pi", "pe", "MU", None)
    cgr.suggest("WH", "ca", "st", "gr", "SC", None)
    cgr.suggest("GR", "sc", "ki", "wr", "PE", "sc")
    cgr.suggest("PE", "ki", "mu", "wr", "WH", "ki")
    cgr.suggest("MU", "st", "gr", "wr", "SC", None)
    cgr.suggest("WH", "gr", "ha", "wr", "SC", None)
    cgr.suggest("PE", "pe", "st", "wr", "MU", None)
    cgr.suggest("PL", "ki", "gr", "wr", "SC", None)
    cgr.suggest("SC", "li", "wr", "pe", "PL", None)

    # right before Mrs. White ends the game, I still
    # don't know what room it is in. :(
    cgr.print_notepad()
    cgr.suggest("WH", "di", "pe", "wr", None, None)
    cgr.accuse("WH", "di", "pe", "wr", True)


# Change which game gets called down here if you want to test
# other games
if __name__ == '__main__':
    play_clue_game1()
