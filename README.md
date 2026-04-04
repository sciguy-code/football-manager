# ⚽ Football Manager — Career Mode

A terminal-based football management simulation game written in Python. Pick a club, set your tactics, watch matches unfold minute by minute, and fight your way to the top of the league table.

---

## 📸 Preview

```
============================================================
⚽ FOOTBALL MANAGER - WEEK 4
============================================================
Club: Liverpool
Points: 9 | Elo: 1312 | GD: +5
Record: 3W-0D-1L
============================================================

1. ▶️  Play Next Match
2. 📊 League Table
3. 👥 View Squad
4. ⚙️  Change Tactics
5. 💾 Save Game
6. 🚪 Save & Exit
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies — uses only the Python standard library

### Installation

```bash
git clone https://github.com/your-username/football-manager.git
cd football-manager
```

### Running the Game

```bash
python main.py
```

If a save file (`career_save.json`) is detected, you will be prompted to continue your existing career or start a new one.

---

## 🎮 Gameplay

### Starting a New Career

1. The game generates **20 Premier League clubs**, each with an 18-player squad and a unique Elo rating.
2. You are presented with a ranked team selection screen.
3. Pick your club (or press **Enter** for a random selection) and begin your career.

### Main Menu Options

| Option | Description |
|---|---|
| ▶️ Play Next Match | Simulate the current gameweek. Rival fixtures auto-simulate while your match plays live. |
| 📊 League Table | View full standings: points, record, goals, goal difference, and Elo. |
| 👥 View Squad | Browse your squad by position with ratings, age, and goals scored. |
| ⚙️ Change Tactics | Switch between Attack, Balanced, or Defend to affect match outcomes. |
| 💾 Save Game | Persist your career progress to `career_save.json`. |
| 🚪 Save & Exit | Save and quit the game. |

### Watching a Match

Matches simulate across 90 minutes with live commentary:

```
45': ⚽ GOAL!!! Steven Miller (80 rated) scores! | 1-0
67': Great save by the Arsenal keeper!
83': ⚠️  Yellow Card for Mark Jones!

==============================
⏱️  FULL TIME: Liverpool 2 - 1 Arsenal
Updated Elo: Liverpool 1334 | Arsenal 1219
==============================
```

---

## ⚙️ Game Systems

### Squad & Players

Each team is generated with 18 players across four positions:

| Position | Code |
|---|---|
| Goalkeeper | `GK` |
| Defender | `DEF` |
| Midfielder | `MID` |
| Forward | `FWD` |

Each player has a **name**, **age** (18–35), and an **overall rating** (50–99) that directly influences match performance.

### Team Strength

Match strength is calculated from the average rating of the top 11 players, then adjusted by the active tactic:

```
strength = avg(top_11_ratings) × tactic_multiplier
```

### Tactics

| Tactic | Multiplier | Effect |
|---|---|---|
| Attack | ×1.2 | Boosts offensive strength |
| Balanced | ×1.0 | No modifier |
| Defend | ×0.8 | Reduces overall strength |

### Match Engine

- Each of the 90 minutes has a base **18% chance** of an event occurring.
- Events can be: a goal attempt, a yellow card, or a commentary moment.
- Goal probability scales with the **shooter's overall rating** and includes randomness.
- Late-game logic: scoreless matches see increased event frequency after the 70th minute; losing teams press harder after the 80th.

### Elo Rating System

Teams use an **Elo rating** system to track relative strength over time. After each match:

```
new_elo = old_elo + K × (actual_result − expected_result) × goal_diff_multiplier
```

- **K-factor:** 32
- **Goal difference multiplier:** increases Elo swings for convincing wins
- Elo is used alongside team strength to determine win probability

### Win Probability Formula

```
win_chance = (strength_prob × 0.6) + (elo_prob × 0.4)
```

Home teams receive an additional **+10% strength bonus**.

---

## 💾 Save System

Progress is automatically persisted to `career_save.json` in the project directory. The save file stores:

- Current week number
- Your selected team
- All 20 teams with full stats, Elo ratings, squad data, and individual player goals

---

## 📁 Project Structure

```
football-manager/
├── main.py            # All game logic
├── career_save.json   # Auto-generated save file (created on first save)
└── README.md
```

---

## 🗺️ Roadmap

- [ ] Transfer market and player signing system
- [ ] Player development and aging over multiple seasons
- [ ] Multiple tactical formations (4-3-3, 4-4-2, etc.)
- [ ] Cup competitions alongside the league
- [ ] Manager reputation and club prestige system
- [ ] Season end promotion / relegation

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)


Visca el Barça!!
