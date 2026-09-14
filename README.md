# The Forgotten

## Run the game

Extract the complete project folder, then run `Main.py` from that folder:

```powershell
python Main.py
```

Controls: WASD moves, H heals, M equips the bow, and hold the left mouse
button to shoot. The quiver starts with 10 arrows; press R to begin a
30-second restock when it is not full. During game over, R keeps its restart
behavior instead.

Keep `Settings.py`, `Player.py`, `Map.py`, `Arrow.py`, `Enemy.py`, `Main.py`, and
the `tiny-RPG-forest-files` assets folder together. Running `Main.py` from a
different directory can cause `ModuleNotFoundError: No module named 'Settings'`.

A Test of Judgement — Fullscreen Python game project (prototype and full game) built with pygame-ce.

This repository will contain the game "The Forgotten" — a 2D top-down RPG inspired by Undertale-style conversation battles and choices. The initial commit creates the repo so development branches can be added.

Branching:
- feature/fullgame — main development branch for the full game.

See the project board and issues for planned features.
