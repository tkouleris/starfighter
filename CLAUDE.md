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
- **Visibility is the "alive" flag.** `Collision.check(a, b, sound)` compares `hitbox` rects and sets both objects' `visible = False` on hit. Bullets are created per shot into `Game.bullets` and dropped once invisible (hit or off-screen). A player hit leaves `player.visible = False` (ship hidden, controls disabled) until its explosion finishes; only then does `Game.handle()` take a life and pause.
- **Player position lives in `Game`** (`spaceship_x`/`spaceship_y`) and is passed into `Player.draw(x, y)` each frame; `Player.x/y` are just mirrors. Movement is velocity-based (`Game.move_spaceship`, tuned by `SHIP_SPEED`/`SHIP_RESPONSIVENESS`); velocity resets on `init_game()` and on losing a life.
- **Enemy movement is strategy functions** in `enemy_animations.py` that mutate the enemy (`x`, `y`, `velocity`, `direction`, `move_index`). `Game.enemy_movement` lists the active ones (`line`, `zig_zag`; `circle` exists but is unused) and is indexed with `random.randint(0, 1)` — update that range when adding patterns. Enemies falling off the bottom are respawned at the top via `Enemy.set_init()`, so every enemy must be shot to clear a level.
- **Explosions are procedural** (`explosion.py`, no sprite): `Game.explosions` holds active `Explosion` objects, drawn each frame and dropped once `finished`. `main.py` only advances the level when no enemy is visible *and* `game.explosions` is empty, so the last kill's explosion is shown. `init_game()` clears them.
- **Background music** is `assets/sounds/music.wav` (a generated chiptune loop), started in `main.py` via `pygame.mixer.music` before the menu and paused/unpaused around `PauseMenu.handle()`.
- **Score and high scores.** `Game.score` grows by `10 * level` per enemy shot (via the bool returned by `Collision.check`). `HighScores` (`high_scores.py`) keeps the top 10 in `highscores.json` at the repo root (gitignored) and is shared by `main.py` and `Menu`. On game over, `main.py` uses `name_entry` (initials being typed, or `None`) and `score_recorded`; Y/N only respond once `score_recorded` is set.
- **Pause menu.** During active play (`not game.paused`), Esc/P opens `PauseMenu.handle()` (`pause_menu.py`), a blocking loop that draws over a snapshot of the last frame and returns `RESUME`, `MAIN_MENU` or `QUIT`. It's separate from `Game.paused`, which stays reserved for between rounds and game over. Esc still quits on those screens. `MAIN_MENU` re-runs `menu.handle()` and resets lives, level and score.
- **Weapons and power-ups.** `weapons.py` defines module-level `Weapon` instances (`cooldown` in frames, `shots` as `(x offset, dx)` pairs); `Game.weapon` is the current one and `Game.fire_cooldown` gates auto-fire while the fire key is held. A kill has a `POWER_UP_CHANCE` of dropping a `PowerUp` (`power_up.py`) into `Game.power_ups`; catching it sets `Game.weapon` for `POWER_UP_DURATION` frames (`weapon_timer`), then it falls back to `BLASTER`. Pickups use `hitbox.colliderect` directly, not `Collision.check`, which would hide the player. Losing a life resets the weapon; `init_game()` clears bullets and power-ups but keeps the weapon. Timers are frame counts, so they freeze while paused.
- **Settings.** `Settings` (`settings.py`) holds music/SFX volume (0–10) and `controls` (action → key code), persisted to `settings.json` at the repo root (gitignored, keys stored by `pygame.key.name`). It's created before `Game` and passed in; `Game.handle()` reads movement/fire keys from `settings.controls` instead of `pygame.K_*`. Every `pygame.mixer.Sound` must go through `settings.register_sound()` so the SFX volume applies, and `settings.apply()` must run after `pygame.mixer.music.load` (loading resets music volume). One `SettingsMenu` (`settings_menu.py`) is shared by `Menu` and `PauseMenu`; it's a blocking loop over a snapshot of the current screen. Menu navigation keys (↑/↓/Enter/Esc) and Esc/P/Space/Y/N in `main.py` stay hardcoded; P can't be bound.
- Window size is 640×480. Only `Game.__init__` calls `pygame.display.set_mode`; every other screen uses `pygame.display.get_surface()`. Calling `set_mode` every frame recreates the window and causes flicker. Sprite sizes (32×32 ship/enemy, 16×32 bullet) are also hardcoded across files.
