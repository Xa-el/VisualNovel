init python:
    from renpy.display.image import Image
    from renpy.display.motion import Transform
    import time
    import random

    target_time = 3.8     # The target time in seconds when the block should be hit, will be changed based on difficulty speed
    block_creation_count = 0
    max_block_creation = 10  # Set the maximum number of block creations here, can be changed for easy medium or hard difficulty

    class RhythmBlock:
        def __init__(self, image_path, x, y, speed, transform_name, zoom):
            self.sprite = Image(image_path)
            self.x = x
            self.y = y
            self.speed = speed
            self.transform_name = transform_name
            self.zoom = zoom
            self.hit = False
            self.start_time = time.time()  # Track the start time when the block is created

        def get_elapsed_time(self):
            # Calculate the elapsed time since the block was created
            return time.time() - self.start_time

        def check_hit_timing(self, target_time):
            """
            Check if the block is hit within a certain time window since its creation.
            """
            if self.hit:
                return "already_hit"

            elapsed_time = self.get_elapsed_time()
            time_difference = abs(elapsed_time - target_time)

            # Determine hit quality based on the time difference
            if time_difference <= 0.3:  # Perfect within 0.3 seconds
                self.hit = True
                return "perfect"
            elif time_difference <= 0.6:  # Good within 0.6 seconds
                self.hit = True
                return "good"
            elif time_difference <= 0.9:  # Bad within 0.9 seconds
                self.hit = True
                return "bad"
            else:
                return "missed"

    class BurgerBlock(RhythmBlock):
        def __init__(self, x, y, speed):
            super().__init__("DDR_images/burger.png", x, y, speed, move_arrow_1, 0.15)

    class FriesBlock(RhythmBlock):
        def __init__(self, x, y, speed):
            super().__init__("DDR_images/Fries.png", x, y, speed, move_arrow_2, 0.15)

    class SodaBlock(RhythmBlock):
        def __init__(self, x, y, speed):
            super().__init__("DDR_images/Soda.png", x, y, speed, move_arrow_3, 0.17)

    class TendiesBlock(RhythmBlock):
        def __init__(self, x, y, speed):
            super().__init__("DDR_images/tendies.png", x, y, speed, move_arrow_4, 0.12)


    active_blocks = []    # Initialize an empty list to hold active blocks
    block_classes = [BurgerBlock, FriesBlock, SodaBlock, TendiesBlock]
    def random_block_order():
        global block_creation_count
        global max_block_creation

        if block_creation_count < max_block_creation:
            chosen_block_class = random.choice(block_classes)
            new_block = chosen_block_class(1100, -50, 5)  # Create a new block with default parameters
            active_blocks.append(new_block)
            block_creation_count += 1

    def log_key_press(block_name, elapsed_time):    # Debugging function to log key press times, will be removed later
        print(f"[DEBUG] Key pressed for {block_name} at {elapsed_time:.2f} seconds after block creation.")

    gameScore = 0
    def handle_block_hit(block_type, target_time):    # Function to register block hits
        global gameScore
        # Find the latest block of the specified type that has not yet been hit
        matching_blocks = [block for block in active_blocks if isinstance(block, block_type) and not block.hit]
        if matching_blocks:
            block = matching_blocks[-1]  # Get the most recent block
            elapsed_time = block.get_elapsed_time()
            log_key_press(block.__class__.__name__, elapsed_time)  # Log the time when the key is pressed
            result = block.check_hit_timing(target_time)

            if result == "perfect":
                renpy.notify("Perfect!")
                gameScore += 10

            elif result == "good":
                renpy.notify("Good!")
                gameScore += 5

            elif result == "bad":
                renpy.notify("Bad!")
                gameScore += 1

            elif result == "missed":
                renpy.notify("Missed!")
                gameScore += 0

            else:
                renpy.notify("Already hit!")
        
        else:
            renpy.notify(f"No {block_type.__name__} blocks to hit!")


    def sprite_manager(image, xpos, ypos, zoom=1.0):
        return Transform(image, xpos=xpos, ypos=ypos, zoom=zoom)

transform move_arrow_1:
    xalign 0.425
    linear 5.0 yalign 1.5
    repeat

transform move_arrow_2:
    xalign 0.515
    linear 5.0 yalign 1.5
    repeat

transform move_arrow_3:
    xalign 0.60
    linear 5.0 yalign 1.5
    repeat

transform move_arrow_4:
    xalign 0.68
    linear 5.0 yalign 1.5
    repeat


screen DDR_instructions:
    frame:
        xsize 800
        ysize 600
        align (0.5, 0.5) # Center the frame in the middle of the screen
        background "#333333" # Dark gray background for the frame
        padding (20, 20)
        vbox:
            spacing 20

            text "Welcome to the DDR-style Rhythm Game!" color "#FFFFFF" size 40
            text "Instructions:" color "#FFFFFF" size 30
            text "1. Watch as blocks fall from the top of the screen." color "#FFFFFF" size 25
            text "2. Press the corresponding arrow keys when the blocks reach the target zone." color "#FFFFFF" size 25
            text "3. Hit the keys with perfect timing to score the most points!" color "#FFFFFF" size 25
            text "4. Try to score as many points as you can within the time limit." color "#FFFFFF" size 25

            text "Good luck and have fun!" color "#FFFFFF" size 30

            textbutton "Start Game" action [Hide('instructions'), Show('DDRgame')] align (0.5, 0.5) # Button to start the game





screen DDRgame:
    frame:
        xsize 1920
        ysize 1000
        background "map_images/Food_bytes#2.jpg"
        add sprite_manager("DDR_images/scaleBackground.png", 90, -5)
        add sprite_manager("DDR_images/straight-line.png", 1100, -50)
        add sprite_manager("DDR_images/straight-line.png", 950, -50)
        add sprite_manager("DDR_images/straight-line.png", 800, -50)
        add sprite_manager("DDR_images/straight-line.png", 650, -50)
        add sprite_manager("DDR_images/straight-line.png", 500, -50)

        # Dynamically add all active blocks with continuous falling effect
        
        for block in active_blocks:
            add block.sprite at block.transform_name zoom block.zoom
            
        # this will be replaced to be displayed at the end of the game    
        text "Score: [gameScore]" xpos 20 ypos 20 color "#FFFFFF" size 40

        add sprite_manager("DDR_images/zone.png", 760, 900, zoom=0.10)
        add sprite_manager("DDR_images/zone.png", 915, 900, zoom=0.10)
        add sprite_manager("DDR_images/zone.png", 1065, 900, zoom=0.10)
        add sprite_manager("DDR_images/zone.png", 1215, 900, zoom=0.10)

        key "K_LEFT" action Function(handle_block_hit, BurgerBlock, target_time)
        key "K_UP" action Function(handle_block_hit, FriesBlock, target_time)
        key "K_DOWN" action Function(handle_block_hit, SodaBlock, target_time)
        key "K_RIGHT" action Function(handle_block_hit, TendiesBlock, target_time)

    timer 2.0 action Function(random_block_order) repeat True    


