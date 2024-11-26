import arcade
import random

# Constants

# Screen Title and Size
screen_width = 1024
screen_height = 768
screen_title = "Solitaire"

# Card Setup
card_scale = 0.6

# How big are the cards?
card_width = 140 * card_scale
card_height = 190 * card_scale

# Mat creation
mat_percent_oversize = 1.25
mat_height = int(card_height * mat_percent_oversize)
mat_width = int(card_width * mat_percent_oversize)

# Space between the gap of mats
vertical_margin_percent = 0.10
horizontal_margin_percent = 0.10

# Y axis of the bottom row
bottom_y = mat_height / 2 + mat_height * vertical_margin_percent

# The x of where to start putting things on the left
start_x = mat_width / 2 + mat_width * horizontal_margin_percent

# The Y of the top row (4 piles)
top_y = screen_height - mat_height / 2 - mat_height * vertical_margin_percent

# The Y of the middle row (7 piles)
middle_y = top_y - mat_height - mat_height * vertical_margin_percent

# How far apart each pile goes
x_spacing = mat_height + mat_width * horizontal_margin_percent

# If we fan out cards stacked on each other, how far apart to fan them?
card_vertical_offset = card_height * card_scale * 0.3

# Face down image
face_down_image = "/Users/bpicard/Desktop/CodingProjects/Solitaire/arcade-development/arcade/resources/assets/images/cards/cardBack_red2.png"

# Constants that represent "what pile is what" for the game
pile_count = 13
bottom_face_down_pile = 0
bottom_face_up_pile = 1
play_pile_1 = 2
play_pile_2 = 3
play_pile_3 = 4
play_pile_4 = 5
play_pile_5 = 6
play_pile_6 = 7
play_pile_7 = 8
top_pile_1 = 9
top_pile_2 = 10
top_pile_3 = 11
top_pile_4 = 12

# Card constants
card_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
card_suits = ['Clubs', 'Hearts', 'Spades', 'Diamonds']

# Card value mapping for comparison
card_value_map = {value: index for index, value in enumerate(card_values)}

# Class Section
class Card(arcade.Sprite):
    def __init__(self, suit, value, scale=1):

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"/Users/bpicard/Desktop/CodingProjects/Solitaire/arcade-development/arcade/resources/assets/images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(face_down_image, scale, hit_box_algorithm="None")
    
    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(face_down_image)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up

class Solitarie(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.AMAZON)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(mat_width, mat_height, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = start_x, bottom_y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(mat_width, mat_height, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = start_x + x_spacing, bottom_y
        self.pile_mat_list.append(pile)

        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(mat_width, mat_height, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = start_x + i * x_spacing, middle_y
            self.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(mat_width, mat_height, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = start_x + i * x_spacing, top_y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in card_suits:
            for card_value in card_values:
                card = Card(card_suit, card_value, card_scale)
                card.position = start_x, bottom_y
                self.card_list.append(card)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(pile_count)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[bottom_face_down_pile].append(card)

        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(play_pile_1, play_pile_7 + 1):
            # Deal proper number of cards for that pile
            for j in range(pile_no - play_pile_1 + 1):
                # Pop the card off the deck we are dealing from
                card = self.piles[bottom_face_down_pile].pop()
                # Put in the proper pile
                self.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                card.position = self.pile_mat_list[pile_no].position
                # Put on top in draw order
                self.pull_to_top(card)

        # Flip up the top cards
        for i in range(play_pile_1, play_pile_7 + 1):
            self.piles[i][-1].face_up()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)

            ''' Should I do one card instead of three? Yes''' 
            # Are we clicking on the bottom deck, to flip one card?
            if pile_index == bottom_face_down_pile:
                # Flip three cards
                for i in range(1):
                    # If we ran out of cards, stop
                    if len(self.piles[bottom_face_down_pile]) == 0:
                        break
                    # Get top card
                    card = self.piles[bottom_face_down_pile][-1]
                    # Flip face up
                    card.face_up()
                    # Move card position to bottom-right face up pile
                    card.position = self.pile_mat_list[bottom_face_up_pile].position
                    # Remove card from face down pile
                    self.piles[bottom_face_down_pile].remove(card)
                    # Move card to face up list
                    self.piles[bottom_face_up_pile].append(card)
                    # Put on top draw-order wise
                    self.pull_to_top(card)

            elif primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too.
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)

        else:

            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == bottom_face_down_pile and len(self.piles[bottom_face_down_pile]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.piles[bottom_face_up_pile].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[bottom_face_up_pile].remove(card)
                        self.piles[bottom_face_down_pile].append(card)
                        card.position = self.pile_mat_list[bottom_face_down_pile].position

    def foundation_rules(self, card, pile_index):
        # Get the top pile
        pile = self.piles[pile_index]

        if not pile:
            # If the pile is empty, we can place the card if it's an Ace
            return card_values == 'A'
        else:
            # If the pile is not empty, check if the card is the next in sequence
            top_card = pile[-1]
            # Check if the suits match and if the card is the next in sequence
            return (card_suits == top_card.suit and
                    card_value_map[card.value] == card_value_map[top_card.value] + 1)
        
    def tableau_rules(self, card, pile_index):
        pile = self.piles[pile_index]

        if not pile:
            return card.value
        else:
            top_card = pile[-1]
            return (card.suit != top_card.suit and
                    card_value_map[card.value] == card_value_map[top_card.value] +1)

    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a middle play pile?
            elif play_pile_1 <= pile_index <= play_pile_7:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - card_vertical_offset * (i + 1)
                else:
                    # Are there no cards in the middle play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - card_vertical_offset * i

                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False

            # Release on top play pile? And only one card held?
            elif top_pile_1 <= pile_index <= top_pile_4 and len(self.held_cards) == 1:
                if self.foundation_rules(self.held_cards[0], pile_index):
                    # Move position of card to pile
                    self.held_cards[0].position = pile.position
                    # Move card to card list
                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, pile_index)
                    reset_position = False

        if reset_position:
            # Wherever we were dropped, it wasn't valid. Reset each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

def main():
    """ Main function """
    window = Solitarie()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()