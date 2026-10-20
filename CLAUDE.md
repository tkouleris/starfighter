# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Star Fighter is a small Pygame shmup. Level N spawns N enemies; the player has 3 lives. Requires Python 3.10+ (`menu.py` uses `match`) and `pygame==2.6.0`.

## Commands

```bash
pip install -r requirements.txt   # a local venv/ exists at the repo root
python main.py                    # must be run from the repo root
```

There are no tests, linter or build configuration in this repo.

## Architecture

- **Assets are loaded via relative paths** (`path.join('assets', ...)`) inside class constructors, so the working directory must be the repo root, and `pygame.init()` must run before `Game`/`Menu` are constructed.
- **Control flow is split between `main.py` and `Game`.** `main.py` owns the 60 FPS loop, the event queue (quit/Esc, Space to continue, Y/N on game over), level advancement (when no enemy is `visible`, it sets `game.paused = True` and increments `game.level`), and draws the "Lives/Level" and "Game Over" screens. `Game.handle()` only polls held keys (`pygame.key.get_pressed()`) for movement/shooting, renders, and runs collisions — and does nothing while `paused`.
- **`Game.paused` is the state machine.** Paused + lives > 0 → between rounds (level cleared or a life lost); paused + lives <= 0 → game over. `Game.init_game()` rebuilds the enemy list for the current `level` and un-pauses. Losing a life pauses without changing `level`, so the same level replays.
- **`Menu.handle()` is a separate blocking loop** run once before the main loop; it calls `exit()` directly on Quit.
- **Visibility is the "alive" flag.** `Collision.check(a, b, sound)` compares `hitbox` rects and sets both objects' `visible = False` on hit. The single `Bullet` instance is reused: it can only be fired when not visible. A player hit is detected in `Game.handle()` by checking `player.visible` after the collision check.
- **Player position lives in `Game`** (`spaceship_x`/`spaceship_y`) and is passed into `Player.draw(x, y)` each frame; `Player.x/y` are just mirrors.
- **Enemy movement is strategy functions** in `enemy_animations.py` that mutate the enemy (`x`, `y`, `velocity`, `direction`, `move_index`). `Game.enemy_movement` lists the active ones (`line`, `zig_zag`; `circle` exists but is unused) and is indexed with `random.randint(0, 1)` — update that range when adding patterns. Enemies falling off the bottom are respawned at the top via `Enemy.set_init()`, so every enemy must be shot to clear a level.
- **Score and high scores.** `Game.score` grows by `10 * level` per enemy shot (via the bool returned by `Collision.check`). `HighScores` (`high_scores.py`) keeps the top 10 in `highscores.json` at the repo root (gitignored) and is shared by `main.py` and `Menu`. On game over, `main.py` uses `name_entry` (initials being typed, or `None`) and `score_recorded`; Y/N only respond once `score_recorded` is set.
- **Pause menu.** During active play (`not game.paused`), Esc/P opens `PauseMenu.handle()` (`pause_menu.py`), a blocking loop that draws over a snapshot of the last frame and returns `RESUME`, `MAIN_MENU` or `QUIT`. It's separate from `Game.paused`, which stays reserved for between rounds and game over. Esc still quits on those screens. `MAIN_MENU` re-runs `menu.handle()` and resets lives, level and score.
- Window size is 640×480, but `main.py` and `menu.py` hardcode it in `pygame.display.set_mode` instead of reading `Game.window_width/height`. Sprite sizes (32×32 ship/enemy, 16×32 bullet) are also hardcoded across files.
