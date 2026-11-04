# pac-man
42 next core curriculum project (milestone 4)

## Configuration

`hud_height` reserves space at the top of the game window in pixels. It must
be an integer of at least 20; a missing or invalid value produces a warning and
uses the default of 40. If it leaves no room for the maze, the view warns and
uses the default instead, provided the maze fits.
