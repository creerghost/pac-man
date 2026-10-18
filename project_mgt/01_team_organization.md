# Team Organization

## 1. Project overview

Two-person team implementing the 42 project "Pac-Man": a playable Pac-Man in Python with
Pygame (behind our own `Platform`/`Canvas` wrappers, MLX-compatible calls only), mazes
from an assigned A-Maze-ing package, JSON config with comments, persistent highscores,
cheat mode, and an itch.io build. The project started on 2026-10-07 and is
planned over a four-week window (see [Timeline and Progress](./02_timeline_and_progress.md)).

| Team member | Role | Scope |
|---|---|---|
| `vborysov` | Tech lead, platform and game core | Architecture and interface contracts, `Platform`/`Canvas` and their Pygame implementations (`PygamePlatform`, `PygameCanvas`), `GameplayScene` and the gameplay model (`GameState`, `Pacman`, ghosts and their AI, `Maze` adapter over the A-Maze-ing package, collisions, levels, timer, cheat-mode logic). Reviews every PR against the contracts. |
| `vlnikola` | Scenes, UI and data | `Scene` contract, `Transition`, `SceneManager`, the non-gameplay scenes (`MainMenuScene`, `InstructionsScene`, `HighscoresScene`, `GameOverScene`, victory and pause screens), `GameView` and HUD rendering, config loading and faulty-config handling, highscore persistence, itch.io packaging. |
| Both | Integration and delivery | Entry point `pac-man.py`, `Makefile`, `README.md`, project-management documents, acceptance testing, evaluation preparation. |

These are areas of primary ownership, not silos. Both members must be able to explain and
modify any part of the code at peer evaluation (live recode), so each reviews the other's
PRs and the owner walks the reviewer through any non-obvious piece.

## 2. Architecture and decision making

`vborysov` designed the class diagram (engine, scenes, platform/canvas abstraction,
model/view split) and owns the contracts. The rules that follow from it:

- **Contracts first.** An interface (abstract class or `Protocol`) is written and agreed
  before its implementations. Implementations are added as work progresses.
- **Polymorphism instead of branching.** Behaviour varies by swapping objects, not by
  `if`/`else` chains: each screen is a `Scene`, scene changes are a `Transition` value
  routed by `SceneManager` through a mapping, and input arrives as abstract `Command`s.
- **Renderer independence.** Game code talks only to `Platform` and `Canvas`; Pygame is one
  implementation, and another backend can be added without touching scenes or the model.
  Every drawing call must have an MLX equivalent (subject rule).
- **Model/view split.** `GameState` holds gameplay data and never draws; `GameView` reads
  it and draws; `GameplayScene` connects them with a fixed time step.
- **Config owns every tunable.** No module-level settings; values come from the config
  model with safe defaults.

Decision process: the tech lead proposes, both discuss in the related GitHub issue or PR,
and the outcome is recorded there. A change to a contract (method signature, enum value,
shared file) needs agreement from both before it is merged.

## 3. GitHub workflow

Repository: `creerghost/pac-man`. Work is tracked with GitHub Issues and merged through
pull requests into `main`.

### Issues

- One issue per task, with a clear description, an owner, and a label (`core`, `platform`,
  `ui`, `data`, `shared`, `docs`, `bug`).
- An issue is closed by the PR that completes it (`Closes #N`).

### Branches

- `main` stays playable and passes `make lint`.
- Short-lived feature branches per issue: `<area>/<short-name>`, e.g. `core/scene-manager`,
  `platform/pygame-canvas`, `data/highscores`.

### Workflow per task

1. Open or pick an issue and assign it.
2. Branch from `main`, implement, keep commits small.
3. Run `make lint` and a short gameplay smoke test.
4. Open a PR linking the issue; the other member reviews.
5. Merge after approval; the issue closes.

## 4. Communication and coordination

- **Daily sync:** short message on progress, next step, and blockers.
- **Shared files** (`pac-man.py`, `Makefile`, `README.md`, the contract modules) are
  announced before editing to avoid conflicts.
- **Blockers** affecting both sides (e.g. graphics library behaviour, generator interface) get an issue
  and are recorded in the blocking-points document.
- **Pairing:** `vlnikola` pairs with `vborysov` on the engine loop and the gameplay model
  at least once, so both can defend the core at evaluation.

## 5. Definition of done

A task is done when:

- It matches the issue description and the subject's rules.
- `make lint` passes (flake8, mypy with the required flags, type hints, docstrings).
- No traceback on bad input; errors end in a clear message.
- The game still starts and is playable after the merge.
- The other member reviewed the PR and can explain the change.

---
**Next:** [Timeline and Progress ➔](./02_timeline_and_progress.md)
