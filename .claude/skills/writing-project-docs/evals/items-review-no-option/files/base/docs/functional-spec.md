# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Player.** A person playing a game.
- **Tile.** A six-sided piece, which a player lays on the board. A tile can show a river.
- **Space.** A six-sided place on the board that one tile fills.
- **River.** The water a tile shows. A river runs from the middle of the tile to one or more of
  its sides.

## F-SEC-2. Laying tiles

**FR-1.** When a player lays a tile, the app shall lay it only in an empty space next to a space a
tile already fills.

**FR-2.** When a player lays a tile, the app shall join its river to the river of each tile next to
it where both rivers reach the side the two tiles share.

**FR-3.** When a player lays a tile, the app shall show it to every player in the game, without
them refreshing.
