function simulateKeyFindingRuns(runs) {
    const BOARD_SIZE = 14;
    let totalMoves = 0;

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

        return board;
    }

    // Function to play a run until a key is found
    function playRun(board) {
        let moves = 0;

        while (true) {
            // Open a random box
            let boxIndex = getRandomInt(BOARD_SIZE);

            if (board[boxIndex] === 'key') {
                // Key found, end the run
                moves++;
                return moves;
            } else if (board[boxIndex] === 'shuffle') {
                // Shuffle found, reset board and continue
                board = generateBoard();
                moves++;
            } else if (board[boxIndex] === 'uncover') {
                // Uncover two other boxes
                let uncovered = 0;
                while (uncovered < 2) {
                    let randomIndex = getRandomInt(BOARD_SIZE);
                    if (randomIndex !== boxIndex && board[randomIndex] !== null) {
                        uncovered++;
                        if (board[randomIndex] === 'key') {
                            // Key found through uncover, end the run
                            moves++;
                            return moves;
                        } else if (board[randomIndex] === 'shuffle') {
                            // Shuffle found through uncover, reset board and continue
                            board = generateBoard();
                            moves++;
                            break;
                        }
                    }
                }
                moves++;
            } else {
                // Empty box opened
                moves++;
            }
        }
    }

    // Simulate multiple runs to find the average number of moves
    for (let i = 0; i < runs; i++) {
        let board = generateBoard();
        totalMoves += playRun(board);
    }

    return totalMoves / runs;
}

// Simulate 1000 runs and print the average number of moves to find a key
console.log(simulateKeyFindingRuns(1000000));
