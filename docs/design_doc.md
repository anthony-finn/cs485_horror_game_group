# Engine

## Main Loop

Most games execute their loop once per frame; ours executes its main loop once per text message received from the user. As soon as our server receives a message, the function `handle_request` (open_calls/twillio_webhook.py) is executed and the cycle begins.

To prevent concurrency bugs (Flask *is* multithreaded by default), we implement a locking mechanism. When we receive a message, we check for the presence of a file (players/+00000000.lock). If present, we respond with 'too many messages' and return early. Otherwise, we create the file and begin processing the player's message.

From there, there are a couple possibilities for what happens next.

A.  The message was a command (known word written in CAPS)
    1.  Process the command.
    2.  Send the output to the user.

B.  Else if the user has a save game, we run the game logic, handling the player's message as an action.
    1.  Load the game state from the player's pickle file.
    2.  Call `GameState.run(...)` to run the game logic.
    3.  Send the message to the player.
    4.  Save the updated game state back to the user's pickle file.

C.  Else (if the message is not a known command and there is no save game), we simply send the greeting message ('You've reached [game]; text BEGIN to start a new game').

We finish by deleting the user's lock file.



