import os
import json
import random
import re
import math

def update_game():
    os.makedirs("images", exist_ok=True)
    os.makedirs(".github", exist_ok=True)

    state_path = ".github/pachisi_state.json"
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {
            "game_number": 1,
            "current_turn": "Red",
            "total_rolls": 0,
            "red_pos": 0,
            "yellow_pos": 0,
            "last_roll": 0
        }

    possible_rolls = [2, 3, 4, 6, 10, 25]
    roll_val = random.choice(possible_rolls)
    state["last_roll"] = roll_val
    state["total_rolls"] += 1

    if state["current_turn"] == "Red":
        state["red_pos"] = (state["red_pos"] + roll_val) % 52
        state["current_turn"] = "Yellow"
        turn_indicator = "Yellow Team 🟡"
    else:
        state["yellow_pos"] = (state["yellow_pos"] + roll_val) % 52
        state["current_turn"] = "Red"
        turn_indicator = "Red Team 🔴"

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    def get_coords(pos_index, is_yellow=False):
        cx, cy = 300, 300
        angle = (pos_index / 52.0) * 2 * math.pi
        dist = 140 if not is_yellow else 110
        import math
        x = cx + math.cos(angle) * dist
        y = cy + math.sin(angle) * dist
        return int(x), int(y)

    rx, ry = get_coords(state["red_pos"])
    yx, yy = get_coords(state["yellow_pos"], is_yellow=True)

    svg_content = f'''<svg width="600" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="600" rx="16" fill="#1b120c" />
  <rect x="225" y="45" width="150" height="510" fill="#a03020" stroke="#f1c40f" stroke-width="3" rx="4" />
  <rect x="45" y="225" width="510" height="150" fill="#a03020" stroke="#f1c40f" stroke-width="3" rx="4" />
  <rect x="225" y="225" width="150" height="150" fill="#2c3e50" stroke="#f1c40f" stroke-width="3" />
  <text x="300" y="305" font-size="14" fill="#f1c40f" font-weight="bold" text-anchor="middle">CHARKONI</text>
  <text x="300" y="85" font-size="24" fill="#f1c40f" text-anchor="middle">✖</text>
  <text x="300" y="535" font-size="24" fill="#f1c40f" text-anchor="middle">✖</text>
  <text x="75" y="310" font-size="24" fill="#f1c40f" text-anchor="middle">✖</text>
  <text x="525" y="310" font-size="24" fill="#f1c40f" text-anchor="middle">✖</text>
  <circle cx="{rx}" cy="{ry}" r="18" fill="#e74c3c" stroke="#ffffff" stroke-width="3" />
  <text x="{rx}" y="{ry+5}" font-size="12" fill="white" font-weight="bold" text-anchor="middle">R</text>
  <circle cx="{yx}" cy="{yy}" r="18" fill="#f1c40f" stroke="#ffffff" stroke-width="3" />
  <text x="{yx}" y="{yy+5}" font-size="12" fill="#2c3e50" font-weight="bold" text-anchor="middle">Y</text>
</svg>'''

    with open("images/pachisi_board.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()

        status_text = f"Game **#{state['game_number']}** • Rolled **{roll_val}** 🐚 • Next Turn: **{turn_indicator}**"
        pattern = r"(<!-- START_SECTION:pachisi_status -->)(.*?)(<!-- END_SECTION:pachisi_status -->)"
        replacement = f"\\1\n{status_text}\n\\3"

        updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)

if __name__ == "__main__":
    update_game()