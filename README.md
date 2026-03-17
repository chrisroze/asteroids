# Asteroids

A modern reimagining of the classic 1979 arcade game, built in Python with Pygame. Pilot your spaceship through waves of asteroids, rack up points, and survive as long as you can as the difficulty ramps up across stages.

---

## Features

- **Auto-shooting** — your ship fires automatically so you can focus on dodging
- **Momentum-based physics** — smooth acceleration and deceleration give the spaceship a realistic feel
- **Scoring system** — earn 10 points for destroying a large asteroid and 15 points for a small one; floating point text appears on each hit
- **Stage progression** — advance to the next stage every 200 points, with a visual stage-up notification
- **Dynamic difficulty** — asteroid spawn rate increases with every stage, but so does your fire rate to keep things balanced
- **Weapon upgrades** — reach Stage 4 to unlock a rear shot; reach Stage 10 to add spread shots at ±30°
- **Particle effects** — asteroids explode into particles when destroyed
- **Screen wrapping** — fly off one edge and reappear on the opposite side, classic arcade style

---

## How to Install

### Requirements

- Python 3.13 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip

### Using uv (recommended)

```bash
# Install dependencies and create a virtual environment
uv sync

# Run the game
uv run python main.py
```

### Using pip

```bash
pip install pygame==2.6.1
python main.py
```

---

## How to Play

### Controls

| Key | Action |
|-----|--------|
| **↑ Up Arrow** | Accelerate forward |
| **↓ Down Arrow** | Decelerate / move slowly backward |
| **← Left Arrow** | Rotate ship left |
| **→ Right Arrow** | Rotate ship right |
| **Space** | Pause / Resume |
| **Enter** | Start game / Restart after game over |
| **Escape** | Quit game |

### Gameplay Tips

- Your ship fires automatically — concentrate on steering around asteroids
- Large asteroids split into two smaller ones when hit; finish off the fragments to score bonus points
- Watch the **Stage** counter: each new stage brings faster spawns, so plan your escape routes early
- Survive to **Stage 4** to gain a rear shot that clears threats behind you
- Survive to **Stage 10** to unlock spread shots that cover a wide arc in front of you
- The HUD displays your current **Stage**, **Score**, and the number of **Asteroids** remaining on screen
