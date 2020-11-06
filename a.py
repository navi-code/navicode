# Hello world this is a comment
var i = "Hello"
# And this is another # one

 def change_player_xposition(self, x):
    """
    Update player's x coordinate
    Params
    ======
    x (int)
        : Add to player's current x coordinate the value x (either positive or negative)
    """

    # If agent can move
    if not self.cannot_move:
        # Update current x coordinate by adding new x
        self.playerX += x

        # If x coordinate goes out of bounds of the pygame screen then adjust it
        if self.playerX <= 0:
            self.playerX = 0
        elif self.playerX >= (SCREEN_WIDTH - self.PLAYER_WIDTH):
            self.playerX = SCREEN_WIDTH - self.PLAYER_WIDTH

        # Reduce energy by 2 for movement
        self.energy -= 2