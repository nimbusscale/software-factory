# River tile game: architecture notes

Notes on how to build the river tile game. What the game does is in docs/functional-spec.md.
Nothing is built yet.

## Parts

The code is in TypeScript, so the server and the client can share the engine. In two languages,
every rule would be written twice.

The code has three parts.

1. **Engine.** All game rules and game state live here. It has no network or screen code, so the
   server and the client can both run it, and its rules can be tested on their own.
2. **Server.** Runs games and talks to the players' clients.
3. **Client.** Runs in each player's browser. It shows the game and sends the player's moves.

## The board

A tile's sides are numbered 0 to 5 clockwise, starting with the top side as it lies on the board.
A tile's side n faces side (n + 3) mod 6 of the tile next to it across that side, so two rivers
join where they reach a pair of facing sides.
