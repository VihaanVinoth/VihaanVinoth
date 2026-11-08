import os
import json
import sys

def update_game():
    issue_title = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    
    state_path = ".github/carrom_state.json"
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    else:
            state = {"game_number": 1, "striker_position": "Center", "total_moves": 0}

    striker_x = 300
    pos_label = "Center"
    if "left" in issue_title:
        striker_x = 200
        pos_label = "Left Baseline"
    elif "right" in issue_title:
        striker_x = 400
        pos_label = "Right Baseline"
    elif "center" in issue_title:
        striker_x = 300
        pos_label = "Center Baseline"

    state["total_moves"] += 1
    state["striker_position"] = pos_label

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    svg_content = f'''<svg width="600" height="600" xmlns="http://www.w3.org/2000/svg">
  <!-- Board Background -->
  <rect width="600" height="600" rx="12" fill="#3d2314" />
  <rect x="30" y="30" width="540" height="540" rx="6" fill="#f7e4c8" />

  <!-- Corner Pockets -->
  <circle cx="65" cy="65" r="28" fill="#1e272e" />
  <circle cx="535" cy="65" r="28" fill="#1e272e" />
  <circle cx="65" cy="535" r="28" fill="#1e272e" />
  <circle cx="535" cy="535" r="28" fill="#1e272e" />

  <!-- Center Circles -->
  <circle cx="300" cy="300" r="45" fill="none" stroke="#d63031" stroke-width="2" />
  <circle cx="300" cy="300" r="8" fill="#d63031" />

  <!-- Baselines -->
  <line x1="160" y1="470" x2="440" y2="470" stroke="#b2bec3" stroke-width="3" stroke-dasharray="6,6" />
  <circle cx="160" cy="470" r="12" fill="#b2bec3" />
  <circle cx="440" cy="470" r="12" fill="#b2bec3" />

  <line x1="160" y1="130" x2="440" y2="130" stroke="#b2bec3" stroke-width="3" stroke-dasharray="6,6" />
  <circle cx="160" cy="130" r="12" fill="#b2bec3" />
  <circle cx="440" cy="130" r="12" fill="#b2bec3" />

  <!-- Center Queen (Red) -->
  <circle cx="300" cy="300" r="12" fill="#d63031" stroke="#2d3436" stroke-width="1.5" />

  <!-- Surrounding Coins Ring -->
  <circle cx="300" cy="275" r="11" fill="#ffffff" stroke="#2d3436" stroke-width="1.5" />
  <circle cx="322" cy="290" r="11" fill="#2d3436" stroke="#ffffff" stroke-width="1.5" />
  <circle cx="315" cy="318" r="11" fill="#ffffff" stroke="#2d3436" stroke-width="1.5" />
  <circle cx="285" cy="318" r="11" fill="#2d3436" stroke="#ffffff" stroke-width="1.5" />
  <circle cx="278" cy="290" r="11" fill="#ffffff" stroke="#2d3436" stroke-width="1.5" />

  <!-- Dynamic Striker (Blue) -->
  <circle cx="{striker_x}" cy="470" r="16" fill="#0984e3" stroke="#2d3436" stroke-width="2" />
  <text x="{striker_x}" y="474" font-size="9" fill="white" font-weight="bold" text-anchor="middle">STRIKER</text>
</svg>'''

    os.makedirs("images", exist_ok=True)
    with open("images/carrom_board.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    import re
    status_text = f"Game **#{state['game_number']}** • Last Strike: **{pos_label}** (Move #{state['total_moves']})"
    pattern = r"(<!-- START_SECTION:carrom_status -->)(.*?)(<!-- END_SECTION:carrom_status -->)"
    replacement = f"\\1\n{status_text}\n\\3"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=r're.DOTALL' if 're.DOTALL' else 0)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    update_game()