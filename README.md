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
- [Project Structure](#project-structure)
- [Code Overview](#code-overview)
- [Assets](#assets)
- [Customization](#customization)
- [Known Limitations](#known-limitations)
- [Possible Improvements](#possible-improvements)

---

## Features

- Main menu with **Start** / **Quit** options and sound feedback
- Player spaceship with free movement in four directions
- Shooting with sound effects
- Enemies with different movement patterns (straight line and zig-zag) and random speeds
- Increasing difficulty: level *N* spawns *N* enemies
- Lives system (3 lives) with a "Game Over / Play again" screen
- Rotating backgrounds that change from level to level
- Explosion sound when an enemy is hit

---

## Requirements

- **Python 3.10 or newer** (the menu uses the `match` statement introduced in Python 3.10)
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
> (e.g. `assets/1.jpg`), so it must be launched from the project root.

---

## How to Play

### Controls

| Key | Where | Action |
|-----|-------|--------|
| `↑` / `↓` | Menu | Move between **Start** and **Quit** |
| `Enter` | Menu | Confirm selection |
| `←` `→` `↑` `↓` | In game | Move the spaceship |
| `Space` | In game | Fire |
| `Space` | Level / lives screen | Continue to the next round |
| `Y` | Game Over screen | Play again (restarts from level 1 with 3 lives) |
| `N` | Game Over screen | Quit the game |
| `Esc` | Anytime in game | Quit the game |

### Rules

- You start at **level 1** with **3 lives**.
- Each level spawns as many enemies as the level number (level 1 → 1 enemy, level 5 → 5 enemies, ...).
- Enemies fly downwards using either a straight-line or a zig-zag pattern, at a random speed.
- Enemies that leave the bottom of the screen re-enter from the top at a random horizontal position,
  so **every enemy must be destroyed** to clear the level.
- Only **one bullet** can be on screen at a time; you can fire again once the previous bullet hits a
  target or leaves the screen.
- If an enemy collides with your ship you **lose a life** and the current level restarts.
- When all your lives are gone the **Game Over** screen appears and you can choose to play again.

---

## Project Structure

```
starfighter/
├── main.py               # Entry point – initializes Pygame, runs the menu and the main game loop
├── menu.py               # Main menu (Start / Quit)
├── game.py               # Game state, level setup, input handling and rendering
├── player.py             # Player spaceship
├── enemy.py              # Enemy spaceship
├── enemy_animations.py   # Enemy movement patterns (line, zig_zag, circle)
├── bullet.py             # Player bullet
├── collision.py          # Hitbox-based collision detection
├── requirements.txt      # Python dependencies
└── assets/               # Images, backgrounds and sounds
    └── sounds/           # Sound effects (bullet, menu change, explosion)
```

---

## Code Overview

### `main.py`
The entry point. It initializes Pygame, shows the `Menu`, and then runs the main loop at 60 FPS.
It handles global events (quit, `Esc`, continue / play-again keys), detects when all enemies are
destroyed to advance to the next level, and draws the in-between screens ("Lives / Level" and
"Game Over").

### `game.py` – `Game`
Holds the overall game state: current level, player, enemies, bullet, backgrounds and sounds.

- `init_game()` – creates `level` enemies with a random movement pattern and speed (3–5),
  resets the player position and un-pauses the game.
- `handle()` – processes keyboard input for movement and shooting, draws the background,
  bullet, player and enemies, respawns enemies that leave the screen and checks collisions
  (bullet ↔ enemy and enemy ↔ player).

### `menu.py` – `Menu`
A blocking loop that renders the menu background with the **Start** and **Quit** options.
The selected option is highlighted in green. Selecting **Start** returns control to `main.py`;
selecting **Quit** exits the program.

### `player.py` – `Player`
The 32×32 player spaceship. Stores its position, hitbox, visibility and number of lives (3).

### `enemy.py` – `Enemy`
A 32×32 enemy ship. Each enemy receives a movement function (animation) and a velocity.
`draw()` moves the enemy using its animation, updates its hitbox and renders it.
`set_init()` repositions the enemy and assigns a new movement pattern.

### `enemy_animations.py`
Movement functions that operate on an enemy object:

- `line` – moves straight down.
- `zig_zag` – moves down while swinging left and right, staying within the window bounds.
- `circle` – a small looping offset pattern (currently defined but not used by the game).

### `bullet.py` – `Bullet`
The player's projectile. It travels upward at 5 pixels per frame and becomes invisible when it
reaches the top of the screen.

### `collision.py` – `Collision`
`check(object_1, object_2, sound=None)` tests whether two visible objects' hitboxes overlap
(`pygame.Rect.colliderect`). On collision both objects are hidden and an optional sound is played.

---

## Assets

All graphics and audio are located in the `assets/` folder:

| File | Usage |
|------|-------|
| `1.jpg`, `2.jpg`, `3.jpg` | In-game backgrounds (rotated per level) |
| `menu_bg.png` | Main menu background |
| `32x32_spaceship.png` | Player spaceship |
| `32x32_enemy_1.png` | Enemy spaceship |
| `16x32_spaceship_shot_2.png` | Player bullet |
| `sounds/bullet.mp3` | Shooting sound |
| `sounds/explosion.mp3` | Enemy destroyed sound |
| `sounds/change.mp3` | Menu navigation sound |

The folder also contains additional sprites (other sizes and variants) that are not currently used
but can be swapped in.

---

## Customization

Some easy tweaks you can make in the code:

- **Window size** – `window_width` / `window_height` in `game.py` (default 640×480).
- **Player speed** – the `± 2` steps in `Game.handle()`.
- **Bullet speed** – `bullet_velocity` in `bullet.py`.
- **Enemy speed** – the `random.randint(3, 5)` range in `Game.init_game()`.
- **Starting lives** – `self.lives` in `player.py`.
- **Movement patterns** – add new functions to `enemy_animations.py` and include them in
  `Game.enemy_movement`.

---

## Known Limitations

- The game must be started from the project root, otherwise assets cannot be found.
- Only one bullet can be on screen at a time.
- There is no score counter or high-score persistence.
- At the start of each level all enemies spawn at the same position.
- The `circle` movement pattern is implemented but not used.

---

## Possible Improvements

- Add a score system and a high-score table
- Allow multiple bullets / different weapons
- Add enemy projectiles and boss levels
- Explosion animations and background music
- Randomized spawn positions at the start of each level
- Pause menu
