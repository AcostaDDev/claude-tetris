# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Vanilla JavaScript Tetris — HTML5 Canvas + CSS, no dependencies, no build step, no tests.
Three files do everything: [index.html](index.html) (DOM + two canvases), [style.css](style.css)
(dark arcade theme), [game.js](game.js) (all game logic). README.md is in Spanish and documents
mechanics and tunable constants in detail.

## Running

Open [index.html](index.html) directly in a browser, or serve statically:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

There is nothing to lint or test. `game.js` runs under `'use strict'` as a classic script
(not a module) — it relies on top-level function/`let` declarations being globally visible.

## Architecture (game.js)

State lives in module-level `let` bindings (`board`, `current`, `next`, `score`, `level`,
`dropInterval`, `animId`, …). `init()` resets all of it and is also the restart handler.

- **Board**: `ROWS × COLS` array; each cell is `0` or a color index `1–7`. That same index is
  the piece `type`, indexes into `COLORS`, and is the fill value stored in `PIECES` shape
  matrices — the three are deliberately kept in sync.
- **Pieces**: square matrices in `PIECES[1..7]`. `rotateCW` builds a rotated copy;
  `tryRotate` applies it with wall kicks `[0, -1, 1, -2, 2]` (first non-colliding offset wins).
- **`collide(shape, x, y)`** is the single source of truth for legality — used by movement,
  rotation, `ghostY`, soft/hard drop, and spawn (a collision on spawn ends the game).
- **Game loop** (`loop`): `requestAnimationFrame` + `dropAccum` accumulator; a step drops one
  row or calls `lockPiece()` (merge → clearLines → spawn).
- **`clearLines`** splices full rows and `unshift`s empty ones, then recomputes
  `level = floor(lines / 10) + 1` and `dropInterval = max(100, 1000 - (level-1)*90)`.
- **Rendering**: `draw()` clears and repaints grid → locked board → ghost (alpha 0.2) →
  current piece every frame; `drawNext()` only repaints on `spawn()`.
- **Pause/over**: both share the `#overlay` element; `togglePause` cancels/restarts the RAF
  loop and re-seeds `lastTime` to avoid a large `dt` spike on resume.

## Changing board dimensions

`COLS`, `ROWS`, `BLOCK` in `game.js` must match the `#board` canvas `width`/`height` in
[index.html](index.html) (`width = COLS*BLOCK`, `height = ROWS*BLOCK`). The `NEXT` preview
assumes a 4×4 area at 30px in `drawNext()`.
