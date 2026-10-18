# Roadmap: first test scene

**Goal:** `python3 pac-man.py config.json` opens a window and shows test scenes drawn only
through our `Canvas` contract: rectangles, a circle that moves with arrow keys/WASD, and a
line of text. ENTER switches to a second test scene and back through `SceneManager`. ESC
or the close button exits without a traceback.

**Library:** Pygame, used only behind `PygamePlatform` and `PygameCanvas` (as in the class
diagram). Nothing outside those two classes imports `pygame`. Each `Canvas` method must
map to something MLX can do too (subject rule).

Out of scope: config, maze, gameplay, real menus.

## Work split

Two branches in parallel. They meet only at the shared contracts, so those are agreed and
merged into `main` first.

| Branch | Owner | Contents |
|---|---|---|
| `main` (step 0) | both | Shared contracts: `Canvas`, `Color`, `Command` |
| `platform` | `vborysov` | `Platform` contract, `PygameCanvas`, `PygamePlatform` |
| `scene-manager` | `vlnikola` | `Scene` contract, `Transition`, `SceneManager`, two test scenes |
| `main` (step 3) | both | `GameEngine`, `pac-man.py` wiring, done check |

```
          ┌─► platform (vborysov) ──────┐
0 contracts                              ├─► 3 GameEngine + wiring ─► done
          └─► scene-manager (vlnikola) ─┘
```

---

## Step 0 — Shared contracts (together, merged to `main` first)

Small, no `pygame` import, agreed by both before branching:

- `Color = tuple[int, int, int]`; named or hex colours (`"yellow"`, `"#1919A6"`) are
  turned into this tuple with `webcolors.name_to_rgb` / `hex_to_rgb` (pure Python, no
  dependencies, renderer-neutral, also usable for colours in the config later; unknown
  name → `ValueError`). Needs `uv add webcolors`.
- `Canvas` (abstract): `clear(color)`, `draw_rect(x, y, w, h, color)`,
  `draw_circle(x, y, radius, color)`, `draw_text(text, x, y, size, color)`
- `Command` enum: `UP`, `DOWN`, `LEFT`, `RIGHT`, `CONFIRM`, `CANCEL`

After this merge, nobody changes these files without telling the other.

## Step 1a — `platform` branch (`vborysov`)

- `Platform` (abstract): `initialize()`, `poll_commands() -> tuple[bool, list[Command]]`
  (`bool` = keep running), `tick(target_fps) -> float` (`dt` in seconds),
  `get_canvas() -> Canvas`, `present()`, `shutdown()`; usable as a context manager.
- `PygameCanvas`: wraps a `pygame.Surface`, one Pygame call per method, fonts cached by
  size.
- `PygamePlatform`: window, `Clock`, event queue → `Command` via `dict[int, Command]`
  (arrows, WASD, ENTER, ESC); `QUIT` event or ESC → not running. Init failure → our own
  clear error.
- `uv add pygame`.

**Done (alone):** a throwaway script opens the window, draws with `PygameCanvas`, prints
received commands, exits on ESC; pytest checks a pixel colour on an off-screen surface;
`make lint` passes.

## Step 1b — `scene-manager` branch (`vlnikola`)

- `Scene` (abstract): `on_enter(payload)`, `on_exit()`, `handle_command(command)`,
  `update(dt) -> tuple[Transition, Any]`, `render(canvas)`.
- `Transition` enum: `NONE`, `NEXT_TEST_SCENE`, `PREV_TEST_SCENE`, `EXIT_APP` (real names
  like `START_GAME` replace these later).
- `SceneManager`: holds the current scene and a routing table
  `dict[Transition, Callable[[], Scene]]`; `handle_command`, `update(dt)`, `render(canvas)`
  delegate to the current scene; `_route_transition` looks the transition up, calls
  `on_exit` / `on_enter(payload)`. `NONE` and `EXIT_APP` are handled by the table too, not
  by `if` chains (decide how, e.g. `EXIT_APP` sets `should_quit`).
- `TestScene`: rectangles, a circle moved by `speed * dt` with direction from a
  `dict[Command, tuple[int, int]]`, a text line; `CONFIRM` → `NEXT_TEST_SCENE`.
- `SecondTestScene`: different colours and text; `CONFIRM` → `PREV_TEST_SCENE`.

**Done (alone, no window needed):** a `RecordingCanvas` test double in `tests/` that
stores draw calls; pytest checks that `render` draws what you expect, that `CONFIRM`
switches scenes and calls `on_exit`/`on_enter`, and that `update(dt)` moves the circle;
`make lint` passes.

## Step 2 — Merge both branches into `main`

Each opens a PR, the other reviews. Conflicts should only be in `pyproject.toml` /
`uv.lock` (from `uv add pygame`).

## Step 3 — `GameEngine` and wiring (together, on `main`)

```
with platform:
    while not scene_manager.should_quit:
        running, commands = platform.poll_commands()
        ...                       # running False → stop
        for command in commands: scene_manager.handle_command(command)
        scene_manager.update(platform.tick(target_fps))
        scene_manager.render(platform.get_canvas())
        platform.present()
```

`pac-man.py` builds `PygamePlatform`, `SceneManager` with the test scenes, `GameEngine`,
calls `run()`; any exception → one clear error line, no traceback. Window size, title and
FPS are constructor parameters for now (they move to the config model later).

**Done when:**

- [ ] Window opens and shows rectangles, circle and text.
- [ ] Arrows and WASD move the circle smoothly at any frame rate.
- [ ] ENTER switches between the two test scenes.
- [ ] ESC and the close button exit with status 0, no traceback.
- [ ] Only the two Pygame classes import `pygame`.
- [ ] `make lint` clean, pytest green.
- [ ] Each of us can explain the other's branch.

## After this goal

Next roadmap: main menu scene with real `Transition`s, config loading, then the maze.
