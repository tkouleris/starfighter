# Star Fighter

A simple vertical-scrolling **shoot 'em up (shmup)** written in Python with [Pygame](https://www.pygame.org/).
You pilot a small spaceship at the bottom of the screen and must destroy every enemy ship to advance.
Each new level adds one more enemy to the screen, so the game gets progressively harder.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [How to Play](#how-to-play)
  - [Controls](#controls)
  - [Rules](#rules)
  - [Scoring and High Scores](#scoring-and-high-scores)
  - [Settings](#settings)
- [Project Structure](#project-structure)
- [Code Overview](#code-overview)
- [Assets](#assets)
- [Customization](#customization)
- [Known Limitations](#known-limitations)
- [Possible Improvements](#possible-improvements)

---

## Features

- Main menu with **Start** / **High Scores** / **Settings** / **Quit** options and sound feedback
- Player spaceship with free movement in four directions
- Auto-fire with multiple bullets on screen and sound effects
- **Weapon power-ups** (Double, Spread, Rapid) dropped by destroyed enemies
- Enemies with different movement patterns (straight line and zig-zag) and random speeds
- Increasing difficulty: level *N* spawns *N* enemies
- Lives system (3 lives) with a "Game Over / Play again" screen
- Score counter and a persistent **top 10 high-score table** with initials entry
- **Pause menu** (Resume / Settings / Main Menu / Quit) during play
- **Settings menu** with music and sound-effect volume and rebindable movement/fire keys, saved between sessions
- Procedural **explosion animations** for destroyed enemies and the player's ship
- Looping chiptune **background music**
- Rotating backgrounds that change from level to level

---

## Requirements

- **Python 3.10 or newer** (the code uses the `match` statement introduced in Python 3.10)
- **Pygame 2.6.0** (listed in `requirements.txt`)

---

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd starfighter
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux / macOS:
     ```bash
     source venv/bin/activate
     ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Game

From the project root directory run:

```bash
python main.py
```

> **Note:** The game loads its images and sounds using paths relative to the current working directory
> (e.g. `assets/1.jpg`), and stores high scores in `highscores.json` in the same directory,
> so it must be launched from the project root.

---

## How to Play

### Controls

| Key | Where | Action |
|-----|-------|--------|
| `↑` / `↓` | Main menu / pause menu | Move between options |
| `Enter` | Main menu / pause menu | Confirm selection |
| `Enter` / `Esc` | High Scores screen | Return to the main menu |
| `←` / `→` | Settings menu (volume rows) | Lower / raise the volume |
| `Enter`, then any key | Settings menu (control rows) | Rebind that control (`Esc` cancels; `P` is reserved) |
| `Esc` | Settings menu | Return to the previous menu |
| `←` `→` `↑` `↓` | In game | Move the spaceship (rebindable) |
| `Space` | In game | Fire (rebindable) |
| `Esc` / `P` | In game | Open the pause menu (press again to resume) |
| `Space` | Level / lives screen | Continue to the next round |
| `A`–`Z`, `Backspace`, `Enter` | Game Over screen | Type your initials for a new high score and confirm |
| `Y` | Game Over screen | Play again (restarts from level 1 with 3 lives) |
| `N` | Game Over screen | Quit the game |
| `Esc` | Level / lives and Game Over screens | Quit the game |

### Rules

- You start at **level 1** with **3 lives**.
- Each level spawns as many enemies as the level number (level 1 → 1 enemy, level 5 → 5 enemies, ...).
- Enemies fly downwards using either a straight-line or a zig-zag pattern, at a random speed.
- Enemies that leave the bottom of the screen re-enter from the top at a random horizontal position,
  so **every enemy must be destroyed** to clear the level.
- Hold **Fire** to shoot continuously; each weapon has its own fire rate.
- Destroyed enemies have a 15% chance to drop a **power-up**. Fly into it to switch weapons for
  10 seconds (shown under the score), after which you go back to the Blaster:

  | Power-up | Weapon | Effect |
  |----------|--------|--------|
  | — | Blaster | Default single shot |
  | **D** (blue) | Double | Two parallel shots |
  | **S** (orange) | Spread | Three shots fanning out |
  | **R** (purple) | Rapid | Single shot, about three times the fire rate |

- Losing a life resets your weapon to the Blaster.
- If an enemy collides with your ship it explodes, you **lose a life** and the current level restarts.
- When all your lives are gone the **Game Over** screen appears and you can choose to play again.

### Scoring and High Scores

- Each enemy destroyed is worth **10 × the current level** points.
- The current score is shown in the top-left corner during play and on the in-between screens.
- If your final score makes the **top 10**, the Game Over screen asks for your initials (up to 3 letters).
- High scores are saved in `highscores.json` in the project root (ignored by git) and can be viewed
  from the main menu or on the Game Over screen.

### Settings

- Open **Settings** from the main menu or the pause menu.
- Music and sound-effect volume each range from 0 to 10.
- Each of the five gameplay controls can be bound to any key except `Esc` and `P`. Binding a key that
  another control already uses swaps the two.
- Settings are saved to `settings.json` in the project root (ignored by git) as soon as they change.

---

## Project Structure

```
starfighter/
├── main.py               # Entry point – initializes Pygame, runs the menu and the main game loop
├── menu.py               # Main menu (Start / High Scores / Settings / Quit)
├── pause_menu.py         # In-game pause menu (Resume / Settings / Main Menu / Quit)
├── settings.py           # Volume and key bindings, stored in settings.json
├── settings_menu.py      # Settings screen (volume sliders, key rebinding)
├── game.py               # Game state, level setup, input handling, scoring and rendering
├── player.py             # Player spaceship
├── enemy.py              # Enemy spaceship
├── enemy_animations.py   # Enemy movement patterns (line, zig_zag, circle)
├── bullet.py             # Player bullet
├── weapons.py            # Weapon definitions (Blaster, Double, Spread, Rapid)
├── power_up.py           # Falling weapon power-up
├── collision.py          # Hitbox-based collision detection
├── explosion.py          # Procedural particle explosion animation
├── high_scores.py        # Top 10 high-score table, stored in highscores.json
├── requirements.txt      # Python dependencies
└── assets/               # Images, backgrounds and sounds
    └── sounds/           # Sound effects and background music
```

---

## Code Overview

### `main.py`
The entry point. It initializes Pygame, starts the background music, shows the `Menu`, and then runs
the main loop at 60 FPS. It handles global events (quit, `Esc`, pause, continue / play-again keys,
initials entry), detects when all enemies are destroyed (and their explosions have finished) to
advance to the next level, and draws the in-between screens ("Lives / Level / Score" and "Game Over").

### `game.py` – `Game`
Holds the overall game state: current level, score, player, enemies, bullets, power-ups, the current
weapon, explosions,
backgrounds and sounds. It is the only place that creates the game window (`pygame.display.set_mode`);
every other screen draws onto the existing window.

- `init_game()` – creates `level` enemies with a random movement pattern and speed (3–5),
  clears explosions, resets the player position and un-pauses the game.
- `handle()` – processes keyboard input for movement and shooting, draws the background,
  bullets, player, enemies, power-ups, explosions, score and active weapon, respawns enemies that leave the screen and checks
  collisions (bullet ↔ enemy, enemy ↔ player and power-up ↔ player). After the player is hit, it waits for the
  explosion to finish before taking a life and pausing.

### `menu.py` – `Menu`
A blocking loop that renders the menu background with the **Start**, **High Scores**, **Settings**
and **Quit** options. The selected option is highlighted in green. Selecting **Start** returns control
to `main.py`, **High Scores** shows the high-score table, **Settings** opens the `SettingsMenu`, and
**Quit** exits the program.

### `pause_menu.py` – `PauseMenu`
A blocking loop that draws a dimmed snapshot of the last game frame with the **Resume**,
**Settings**, **Main Menu** and **Quit** options. **Settings** opens the `SettingsMenu` and comes back
to the pause menu; the other options are returned to `main.py`.
The background music is paused while it is open.

### `settings.py` – `Settings`
Holds the music and sound-effect volume (0–10) and the key bound to each gameplay action, and
loads/saves them in `settings.json`. Every sound effect is registered with `register_sound()` so
volume changes apply to it immediately. `Game.handle()` reads the bound keys from `controls`.

### `settings_menu.py` – `SettingsMenu`
A blocking loop, shared by the main menu and the pause menu, that draws volume bars and the
current key bindings over a dimmed snapshot of the screen. It adjusts volumes with `←`/`→` and
rebinds a control by waiting for the next key press.

### `high_scores.py` – `HighScores`
Loads and saves the top 10 scores in `highscores.json`, checks whether a score qualifies for the
table, and draws the table on a given screen.

### `explosion.py` – `Explosion`
A procedural particle explosion (no sprite): a bright flash, a shockwave ring and particles that
fade from white through orange to dark red. Each explosion lasts a fixed number of frames and
reports when it is `finished`.

### `player.py` – `Player`
The 32×32 player spaceship. Stores its position, hitbox, visibility and number of lives (3).

### `enemy.py` – `Enemy`
A 32×32 enemy ship. Each enemy receives a movement function (animation) and a velocity.
`draw()` moves the enemy using its animation, updates its hitbox and renders it.
`set_init()` repositions the enemy, assigns a new movement pattern and resets its pattern state.

### `enemy_animations.py`
Movement functions that operate on an enemy object:

- `line` – moves straight down.
- `zig_zag` – moves down while swinging left and right in legs of random length, bouncing off the window edges.
- `circle` – orbits a centre point that slowly sinks down the screen, clockwise or anticlockwise.

Enemies spawn at random horizontal positions, staggered above the screen, and fly in one by one.

### `bullet.py` – `Bullet`
A single player projectile; `Game` creates a new one per shot. It travels upward at 5 pixels per
frame, plus an optional sideways velocity (`dx`) used by the Spread weapon, and becomes invisible
when it leaves the screen or hits an enemy.

### `weapons.py` – `Weapon`
Each weapon has a name, a cooldown (frames between shots), a list of shots as
`(x offset, sideways velocity)` pairs and a power-up colour. `POWER_UPS` lists the weapons enemies
can drop.

### `power_up.py` – `PowerUp`
A procedurally drawn coloured circle with the weapon's initial that falls from where an enemy was
destroyed. It is collected by touching the player's hitbox.

### `collision.py` – `Collision`
`check(object_1, object_2, sound=None)` tests whether two visible objects' hitboxes overlap
(`pygame.Rect.colliderect`). On collision both objects are hidden, an optional sound is played,
and `True` is returned (used to award points).

---

## Assets

All graphics and audio are located in the `assets/` folder:

| File | Usage |
|------|-------|
| `1.jpg`, `2.jpg`, `3.jpg` | In-game backgrounds (rotated per level) |
| `menu_bg.png` | Main menu and high-score screen background |
| `32x32_spaceship.png` | Player spaceship |
| `32x32_enemy_1.png` | Enemy spaceship |
| `16x32_spaceship_shot_2.png` | Player bullet |
| `sounds/bullet.mp3` | Shooting sound |
| `sounds/explosion.mp3` | Explosion sound |
| `sounds/change.mp3` | Menu navigation sound |
| `sounds/music.wav` | Looping background music |

The folder also contains additional sprites (other sizes and variants) that are not currently used
but can be swapped in.

---

## Customization

Some easy tweaks you can make in the code:

- **Window size** – `window_width` / `window_height` in `game.py` (default 640×480).
- **Player speed** – `SHIP_SPEED` and `SHIP_RESPONSIVENESS` in `game.py`.
- **Bullet speed** – `bullet_velocity` in `bullet.py`.
- **Weapons** – `cooldown` and `shots` in `weapons.py`; add a new `Weapon` to `POWER_UPS` to make it droppable.
- **Power-up drop rate and duration** – `POWER_UP_CHANCE` and `POWER_UP_DURATION` in `game.py`.
- **Enemy speed** – the `random.randint(3, 5)` range in `Game.init_game()`.
- **Starting lives** – `self.lives` in `player.py`.
- **Points per enemy** – the `10 * self.level` value in `Game.handle()`.
- **High-score table size** – `MAX_ENTRIES` in `high_scores.py`.
- **Default volumes and controls** – `music_volume`, `sfx_volume` and `DEFAULT_CONTROLS` in `settings.py`
  (delete `settings.json` to return to them).
- **Explosion look** – `size`, `duration` and `colors` in `explosion.py`.
- **Movement patterns** – add new functions to `enemy_animations.py`, include them in
  `Game.enemy_movement`.

---

## Known Limitations

- The game must be started from the project root, otherwise assets cannot be found.
- The `circle` movement pattern is implemented but not used.

---

## Possible Improvements

- Add enemy projectiles and boss levels
- Randomized spawn positions at the start of each level
