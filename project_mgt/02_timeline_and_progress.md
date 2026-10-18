# Timeline and Progress

## 1. Summary

- **Start:** 2026-10-07
- **Planned window:** four weeks, implementation in weeks 1–3, integration and packaging
  in week 4, last days kept as a buffer for evaluation preparation.
- **Planned end:** 2026-11-04 *(adjust to the real deadline)*
- **Tracking:** GitHub Issues and pull requests on `creerghost/pac-man`; this document
  compares the plan with actual progress and is updated at the end of each week.

Status legend: ⬜ planned · 🟨 in progress · ✅ done · ⚠️ late / blocked

## 2. Weekly plan

### Week 1 (2026-10-07 → 10-13) — Setup and architecture

| Task | Owner | Status |
|---|---|---|
| Repository, `uv` project, `.gitignore`, `Makefile` (`install`, `run`, `debug`, `clean`, `lint`) | Both | ✅ |
| Vendor MLX and the assigned A-Maze-ing package | Both | ✅ |
| Class diagram: engine, scenes, platform/canvas, model/view | `vborysov` | ✅ |
| Project structure and `pac-man.py` entry point | `vborysov` | ✅ |

### Week 2 (10-14 → 10-20) — First test scene

Steps from the [Roadmap](./roadmap.md).

| Task | Owner | Status |
|---|---|---|
| Shared contracts on `main`: `Canvas`, `Color`, `Command` | Both | ⬜ |
| `platform` branch: `Platform`, `PygameCanvas`, `PygamePlatform` | `vborysov` | ⬜ |
| `scene-manager` branch: `Scene`, `Transition`, `SceneManager`, two test scenes | `vlnikola` | ⬜ |
| Merge both, `GameEngine` loop, wire `pac-man.py` | Both | ⬜ |
| Team organization, timeline and roadmap documents | Both | 🟨 |

### Week 3 (10-21 → 10-27) — Gameplay and screens

| Task | Owner | Status |
|---|---|---|
| `Maze` adapter over the generator (seed 42 for level 1, random after, error handling) | `vborysov` | ⬜ |
| `GameState`, `Pacman`, movement and collisions with fixed time step | `vborysov` | ⬜ |
| Ghosts: chase / flee / respawn in corner | `vborysov` | ⬜ |
| Levels (≥10), level timer, lives, scoring | `vborysov` | ⬜ |
| `MainMenuScene`, `InstructionsScene`, `HighscoresScene` | `vlnikola` | ⬜ |
| `GameView` and HUD (score, lives, level, time) | `vlnikola` | ⬜ |
| Highscores: top 10, name validation, robust load/save | `vlnikola` | ⬜ |

### Week 4 (10-28 → 11-04) — Integration, polish, delivery

| Task | Owner | Status |
|---|---|---|
| Pause menu, game-over and victory screens with name entry | `vlnikola` | ⬜ |
| Cheat mode (invincibility, level skip, ghost freeze, extra lives, speed) | `vborysov` | ⬜ |
| No-traceback audit: bad config, generator failure, file errors, window creation failure | Both | ⬜ |
| itch.io build and packaging script at repo root | `vlnikola` | ⬜ |
| `README.md` with all required sections | Both | ⬜ |
| Risk analysis, blocking points, acceptance test plan | Both | ⬜ |
| Evaluation preparation: walk through each other's code, practice recode | Both | ⬜ |

## 3. Milestones

| Milestone | Target | Actual |
|---|---|---|
| Test scene runs through the `Platform`/`Canvas` contracts | 10-20 | |
| Pac-Man moves in a generated maze and eats pacgums | 10-24 | |
| Full game loop: menu → game → game over → name → menu | 10-27 | |
| Feature-complete, `make lint` clean | 11-01 | |
| itch.io build published, documents complete | 11-04 | |

## 4. Progress log

Update at the end of each week: what was done, what slipped and why, plan changes.

| Week | Done | Slipped / changes |
|---|---|---|
| 1 | Setup, vendored packages, class diagram, project structure | — |
| 2 | | |
| 3 | | |
| 4 | | |

---
**⬅ Previous:** [Team Organization](./01_team_organization.md) | **Next:** Risk Analysis *(to be written)*
