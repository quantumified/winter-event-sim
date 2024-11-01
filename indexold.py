import random

def simulate_board_with_currency(trials):
    total_boxes_opened = 0
    total_bells_spent = 0

    for _ in range(trials):
        boxes_opened = 0
        bells_spent = 0

        while True:
            # Step 1: 50% chance there is a key
            has_key = random.random() < 0.5
            key_position = random.randint(0, 13) if has_key else None

            # Step 2: Randomly place the shuffle
            shuffle_position = random.randint(0, 13)

            # Step 3: Randomly assign a bell reward (2/3 chance)
            bell_reward_position = random.randint(0, 13) if random.random() < (2/3) else None

            # Step 4: Randomly choose a box that will reveal two other boxes
            reveal_box_index = random.randint(0, 13)
            revealed_boxes = []

            while len(revealed_boxes) < 2:
                idx = random.randint(0, 13)
                if idx != reveal_box_index and idx not in revealed_boxes:
                    revealed_boxes.append(idx)

            # Handle box opening logic - IDENTICAL to your original logic
            boxes_opened += 1  # The reveal box counts as opened

            if key_position in revealed_boxes:
                # We found the key in the revealed boxes
                boxes_opened += 1  # Open the box with the key
                break
            elif shuffle_position in revealed_boxes:
                # Shuffle hit, restart with a new board
                continue  # Go to the next board
            else:
                # None of the revealed boxes have the key or shuffle
                boxes_opened += 2  # Open the revealed boxes and continue searching

                # Open the rest of the boxes if we haven't found the key yet
                for i in range(14):
                    if i not in revealed_boxes and i != reveal_box_index:
                        boxes_opened += 1
                        if i == key_position:
                            break  # Stop when we find the key
            break  # End this trial if we don't hit shuffle

        total_boxes_opened += boxes_opened

        # Now, calculate the bells spent based on the number of boxes opened
        # (Currency logic starts after we determine how many boxes were opened)

        # Step 1: Open the reveal box (net -7 bells)
        bells_spent += 10  # Opening the reveal box costs 10 bells
        bells_spent -= 3   # You get 3 bells back (net -7 bells)

        # Step 2: Process the two revealed boxes if opened
        bells_spent += 10 * 2  # 10 bells for each of the two revealed boxes

        # Step 3: Check if any revealed boxes contain a bell reward (gain 14 bells)
        if bell_reward_position in revealed_boxes:
            bells_spent -= 14  # Gain 14 bells from the bell reward box

        # Step 4: Process remaining boxes
        for i in range(14):
            if i not in revealed_boxes and i != reveal_box_index:
                bells_spent += 10  # 10 bells to open each box

                # If the current box is the bell reward box, adjust the bell count
                if i == bell_reward_position:
                    bells_spent -= 14  # Gain 14 bells from the bell reward

                if i == key_position:
                    break  # Stop processing once the key is found

        total_bells_spent += bells_spent

    # Return the average number of boxes opened and bells spent per key
    average_boxes_opened = total_boxes_opened / trials
    average_bells_spent = total_bells_spent / trials
    return average_boxes_opened, average_bells_spent

# Simulate over a large number of trials
trials = 1000000
average_boxes_opened, average_bells_spent = simulate_board_with_currency(trials)
print(f"Average number of boxes opened to find a key: {average_boxes_opened:.2f}")
