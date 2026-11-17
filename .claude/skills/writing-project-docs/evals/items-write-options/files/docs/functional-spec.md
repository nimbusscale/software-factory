# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Player.** A person playing a game.
- **Tile.** A square piece with an edge on each side, which a player lays on the board.
- **Hand.** The tiles a player holds and hasn't laid yet.
- **Space.** A square on the board that a tile can be laid in.

## F-SEC-2. Laying tiles

**FR-1.** When a player lays a tile from their hand, the app shall lay it only in a space where
each of its edges matches the edge of every tile next to it.

**FR-2.** While a player has a tile from their hand picked, the app shall highlight each space where
FR-1 lets them lay it.

**FR-3.** When a player lays a tile, the app shall show it to every player in the game, without
them refreshing.
