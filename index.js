function simulateKeyFindingRunsWithCurrency(runs) {
    const BOARD_SIZE = 14;
    let totalMoves = 0;
    let totalCurrencySpent = 0;

    // Helper function to get a random integer in the range [0, max)
    function getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }

    // Function to generate a new board
    function generateBoard() {
        let board = Array(BOARD_SIZE).fill(null);

        // Decide if there's a key (50% chance)
        let hasKey = Math.random() < 0.5;
        if (hasKey) {
            board[getRandomInt(BOARD_SIZE)] = 'key';
        }

        // Place a shuffle in a random box
        let shuffleIndex;
        do {
            shuffleIndex = getRandomInt(BOARD_SIZE);
        } while (board[shuffleIndex] === 'key');
        board[shuffleIndex] = 'shuffle';

        // Place the uncover in a random box
        let uncoverIndex;
        do {
            uncoverIndex = getRandomInt(BOARD_SIZE);
        } while (board[uncoverIndex] === 'key' || board[uncoverIndex] === 'shuffle');
        board[uncoverIndex] = 'uncover';

        // Decide if there's a special box (2/3 chance) that gives currency
        if (Math.random() < (2 / 3)) {
            let specialBoxIndex;
            do {
                specialBoxIndex = getRandomInt(BOARD_SIZE);
            } while (board[specialBoxIndex] === 'key' || board[specialBoxIndex] === 'shuffle' || board[specialBoxIndex] === 'uncover');
            board[specialBoxIndex] = 'special';
        }

        return board;
    }

    // Function to play a run until a key is found, tracking moves and currency
    function playRunWithCurrency(board) {
        let moves = 0;
        let currencySpent = 0;

        while (true) {
            // Open a random box
            let boxIndex = getRandomInt(BOARD_SIZE);
            let box = board[boxIndex];

            if (box === 'key') {
                // Key found, end the run
                moves++;
                currencySpent -= 10; // Deduct 10 for opening the box
                return { moves, currencySpent };
            } else if (box === 'shuffle') {
                // Shuffle found, reset board and continue, no currency spent
                board = generateBoard();
                moves++;
            } else if (box === 'uncover') {
                // Uncover two other boxes, deduct 7 currency
                let uncovered = 0;
                while (uncovered < 2) {
                    let randomIndex = getRandomInt(BOARD_SIZE);
                    if (randomIndex !== boxIndex && board[randomIndex] !== null) {
                        uncovered++;
                        if (board[randomIndex] === 'key') {
                            // Key found through uncover, end the run
                            moves++;
                            currencySpent -= 7; // Deduct 7 for uncovering
                            return { moves, currencySpent };
                        } else if (board[randomIndex] === 'shuffle') {
                            // Shuffle found through uncover, reset board and continue
                            board = generateBoard();
                            moves++;
                            break;
                        }
                    }
                }
                moves++;
                currencySpent -= 7; // Deduct 7 for uncovering
            } else if (box === 'special') {
                // Special box, gain +4 currency
                currencySpent += 4; // Gain 4 currency
                moves++;
            } else {
                // Regular box, deduct 10 currency
                moves++;
                currencySpent -= 10; // Deduct 10 for opening the box
            }
        }
    }

    // Simulate multiple runs to find the average number of moves and currency spent
    for (let i = 0; i < runs; i++) {
        let board = generateBoard();
        let { moves, currencySpent } = playRunWithCurrency(board);
        totalMoves += moves;
        totalCurrencySpent += currencySpent;
    }

    // Return average moves and currency spent per key
    return {
        averageMoves: totalMoves / runs,
        averageCurrencySpent: totalCurrencySpent / runs
    };
}

// Simulate 1000000 runs and print the average number of moves and currency spent to find a key
let result = simulateKeyFindingRunsWithCurrency(1000000);
console.log(`Average Moves: ${result.averageMoves}`);
console.log(`Average Currency Spent: ${result.averageCurrencySpent}`);
