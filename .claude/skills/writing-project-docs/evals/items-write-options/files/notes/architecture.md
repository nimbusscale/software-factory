# Tile game: architecture notes

Notes on how to build the tile game. What the game does is in docs/functional-spec.md. Nothing is
built yet.

The code has three parts.

1. **Engine.** All game rules and game state live here. It has no network code, no DOM, and no
   React. Given a game state and an action, it either rejects the action or returns the new state.
2. **Server.** Runs the engine and holds the one true copy of each game's state. It receives
   actions from players, checks them with the engine, and sends each player the updated state.
3. **Client.** The React app in each player's browser. It shows the game and sends the player's
   actions to the server. It holds no rules logic of its own beyond what it needs to show options,
   such as highlighting where a tile fits.

The engine is shared code. The server uses it to run the game. The client may use it to show legal
moves, but the server always has the final say.

Every action is checked by the engine on the server. A modified client can't make an illegal move.
