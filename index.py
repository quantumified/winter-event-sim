import random

def simulate_board_with_currency(trials):
    total_boxes_opened = 0
    total_bells_spent = 0

    for _ in range(trials):
        boxes_opened = 0
        bells_spent = 0

        while True:  # Continue until the key is found
            # Step 1: 50% chance there is a key on this board
            has_key = random.random() < 0.5
            key_position = random.randint(0, 13) if has_key else None

            # Step 2: Randomly place the shuffle
            shuffle_position = random.randint(0, 13)

            # Step 3: Randomly assign a bell reward (2/3 chance of one box containing bells)
            bell_reward_position = random.randint(0, 13) if random.random() < (2/3) else None

            # Step 4: Randomly choose a box that will reveal two other boxes
            reveal_box_index = random.randint(0, 13)
            revealed_boxes = []

            while len(revealed_boxes) < 2:
                idx = random.randint(0, 13)
                if idx != reveal_box_index and idx not in revealed_boxes:
                    revealed_boxes.append(idx)

            # Handle box opening logic - keep track of all boxes opened
            boxes_opened += 1  # Open the reveal box first

            # Check revealed boxes
            if key_position in revealed_boxes:
                # We found the key in the revealed boxes
                boxes_opened += 1  # Open the box with the key
                break  # Stop when the key is found
            elif shuffle_position in revealed_boxes:
                # If shuffle is hit, we move to a new board but keep searching
                # Reset the counts for boxes opened and bells spent
                boxes_opened = 0
                bells_spent = 0
                continue  # Restart the while loop for a new board
            else:
                # None of the revealed boxes have the key or shuffle
                boxes_opened += 2  # Open the revealed boxes

                # Open the remaining boxes to search for the key
                for i in range(14):
                    if i not in revealed_boxes and i != reveal_box_index:
                        boxes_opened += 1
                        if i == key_position:
                            break  # Stop when we find the key

        # Track the total number of boxes opened and bells spent for this trial
        total_boxes_opened += boxes_opened

        # Now calculate the bells spent for this trial:
        # Step 1: Open the reveal box (cost 10 bells, gives back 3 bells, net -7 bells)
        bells_spent += 10  # Cost of opening the reveal box
        bells_spent -= 3   # You get 3 bells back from the reveal box (net -7 bells)

        # Step 2: Process the two revealed boxes if opened (each costs 10 bells)
        bells_spent += 10 * 2  # 10 bells for each of the two revealed boxes

        # Step 3: Check if any revealed boxes contain a bell reward (gain 14 bells)
        if bell_reward_position in revealed_boxes:
            bells_spent -= 14  # Gain 14 bells from the bell reward box

        # Step 4: Process remaining boxes (each costs 10 bells)
        for i in range(14):
            if i not in revealed_boxes and i != reveal_box_index:
                bells_spent += 10  # 10 bells to open each box

                # If the current box is the bell reward box, adjust the bell count
                if i == bell_reward_position:
                    bells_spent -= 14  # Gain 14 bells from the bell reward

                if i == key_position:
                    break  # Stop spending once the key is found

        total_bells_spent += bells_spent  # Track the total bells spent across all boards

    # Return the average number of boxes opened and bells spent per key
    average_boxes_opened = total_boxes_opened / trials
    average_bells_spent = total_bells_spent / trials
    return average_boxes_opened, average_bells_spent

# Simulate over a large number of trials
trials = 10000
average_boxes_opened, average_bells_spent = simulate_board_with_currency(trials)
print(f"Average number of boxes opened to find a key: {average_boxes_opened:.2f}")
print(f"Average number of bells spent to find a key: {average_bells_spent:.2f}")
