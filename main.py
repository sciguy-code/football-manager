import random
import time
import json
import os
import sys

# Basic settings
POSITIONS = ["GK", "DEF", "MID", "FWD"]
TACTICS = {"Attack": 1.2, "Balanced": 1.0, "Defend": 0.8}

# Lists for generating random names
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
               "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, name, position, age, overall):
        self.name = name
        self.position = position
        self.age = age
        self.overall = overall
        self.goals = 0

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        p = cls(data['name'], data['position'], data['age'], data['overall'])
        p.goals = data.get('goals', 0)
        return p

class Team:
    def __init__(self, name, tactic="Balanced"):
        self.name = name
        self.players = []
        
        # League stats
        self.points = 0
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_diff = 0
        
        self.tactic = tactic
        self.elo = 1200

    def add_player(self, player):
        self.players.append(player)

    def get_strength(self):
        if not self.players: 
            return 50
        
        best_players = sorted(self.players, key=lambda x: x.overall, reverse=True)[:11]
        avg_score = sum(p.overall for p in best_players) / len(best_players)
        
        multiplier = TACTICS.get(self.tactic, 1.0)
        return avg_score * multiplier

    def to_dict(self):
        return {
            "name": self.name,
            "points": self.points,
            "elo": self.elo,
            "tactic": self.tactic,
            "stats": {
                "played": self.played,
                "won": self.won,
                "drawn": self.drawn,
                "lost": self.lost,
                "goals_for": self.goals_for,
                "goals_against": self.goals_against,
                "goal_diff": self.goal_diff
            },
            "players": [p.to_dict() for p in self.players]
        }

    @classmethod
    def from_dict(cls, data):
        t = cls(data['name'], data.get('tactic', 'Balanced'))
        t.points = data['points']
        t.elo = data['elo']
        
        stats = data.get('stats', {})
        t.played = stats.get('played', 0)
        t.won = stats.get('won', 0)
        t.drawn = stats.get('drawn', 0)
        t.lost = stats.get('lost', 0)
        t.goals_for = stats.get('goals_for', 0)
        t.goals_against = stats.get('goals_against', 0)
        t.goal_diff = stats.get('goal_diff', 0)
        
        for p_data in data.get('players', []):
            t.add_player(Player.from_dict(p_data))
        
        return t

class Match:
    def __init__(self, home, away, is_user_watching=False):
        self.home = home
        self.away = away
        self.home_score = 0
        self.away_score = 0
        self.timer = 0
        self.watching = is_user_watching

    def start(self):
        h_power = self.home.get_strength() * 1.1
        a_power = self.away.get_strength()
        
        elo_diff = self.away.elo - self.home.elo
        elo_prob = 1 / (1 + 10 ** (elo_diff / 400))

        str_prob = h_power / (h_power + a_power) if (h_power + a_power) > 0 else 0.5
        home_win_chance = (str_prob * 0.6 + elo_prob * 0.4)

        if self.watching:
            print(f"\n{'='*60}")
            print(f"KICK OFF: {self.home.name} vs {self.away.name}")
            print(f"Ratings: {int(self.home.elo)} vs {int(self.away.elo)}")
            print(f"Home advantage: {int(home_win_chance*100)}%")
            print(f"{'='*60}\n")
            time.sleep(1.5)

        for minute in range(1, 91):
            self.timer = minute
            
            base_chance = 0.18
            
            # Make late game more exciting if scoreless
            if minute > 70 and self.home_score == 0 and self.away_score == 0:
                base_chance = 0.35
            
            # Losing team attacks more in final minutes
            if minute > 80:
                if self.home_score < self.away_score:
                    home_win_chance = min(home_win_chance + 0.15, 0.85)
                elif self.away_score < self.home_score:
                    home_win_chance = max(home_win_chance - 0.15, 0.15)

            if random.random() < base_chance: 
                self.handle_event(home_win_chance)
            
            if self.watching and minute % 3 == 0:
                sys.stdout.write(f"\r{minute}' | {self.home.name} {self.home_score} - {self.away_score} {self.away.name}   ")
                sys.stdout.flush()
                time.sleep(0.05)

        self.end_match()

    def handle_event(self, home_advantage):
        if random.random() < home_advantage:
            attacker = self.home
            defender = self.away
            is_home_goal = True
        else:
            attacker = self.away
            defender = self.home
            is_home_goal = False
        
        roll = random.random()
        
        if roll < 0.55:
            self.attempt_goal(attacker, is_home_goal)
        elif roll < 0.65:
            player = random.choice(defender.players) if defender.players else None
            if player:
                self.log_comment(f"⚠️  Yellow Card for {player.name}!")
        else:
            msgs = [
                f"Great save by the {defender.name} keeper!",
                f"{attacker.name} building an attack...",
                f"Corner kick for {attacker.name}!",
                f"Dangerous free kick opportunity!",
                f"Offside flag raised against {attacker.name}",
                f"Strong tackle by {defender.name}!"
            ]
            self.log_comment(random.choice(msgs))

    def attempt_goal(self, team, is_home):
        shooters = [p for p in team.players if p.position in ["FWD", "MID"]]
        if not shooters: 
            shooters = team.players
        
        if not shooters:
            return
            
        player = random.choice(shooters)
        
        # Skill-based shot chance with some randomness
        base_chance = (player.overall / 100) * 65
        shot_chance = base_chance + random.uniform(-10, 10)
        
        if random.uniform(0, 100) < shot_chance:
            if is_home: 
                self.home_score += 1
            else: 
                self.away_score += 1
            
            player.goals += 1
            self.log_comment(f"⚽ GOAL!!! {player.name} ({player.overall} rated) scores! | {self.home_score}-{self.away_score}")
            if self.watching:
                time.sleep(1.2)
        else:
            misses = [
                f"Shot by {player.name} goes wide!",
                f"{player.name} hits the crossbar!",
                f"Saved! Great reflexes from the keeper!",
                f"{player.name}'s shot blocked by a defender!"
            ]
            self.log_comment(random.choice(misses))

    def log_comment(self, text):
        if self.watching:
            print(f"\n{self.timer}': {text}")

    def end_match(self):
        self.update_stats(self.home, self.home_score, self.away_score)
        self.update_stats(self.away, self.away_score, self.home_score)
        self.update_elo()

        if self.watching:
            print(f"\n{'='*60}")
            print(f"⏱️  FULL TIME: {self.home.name} {self.home_score} - {self.away_score} {self.away.name}")
            print(f"Updated Elo: {self.home.name} {int(self.home.elo)} | {self.away.name} {int(self.away.elo)}")
            print(f"{'='*60}")
            input("\nPress Enter to continue...")

    def update_stats(self, team, goals_for, goals_against):
        team.played += 1
        team.goals_for += goals_for
        team.goals_against += goals_against
        team.goal_diff = team.goals_for - team.goals_against
        
        if goals_for > goals_against:
            team.won += 1
            team.points += 3
        elif goals_for == goals_against:
            team.drawn += 1
            team.points += 1
        else:
            team.lost += 1

    def update_elo(self):
        K_FACTOR = 32
        
        elo_diff = self.away.elo - self.home.elo
        
        exp_home = 1 / (1 + 10 ** (elo_diff / 400))
        exp_away = 1 - exp_home
        
        # Goal difference matters for Elo adjustment
        goal_diff_multiplier = 1 + abs(self.home_score - self.away_score) * 0.1
        
        if self.home_score > self.away_score:
            act_home, act_away = 1.0, 0.0
        elif self.home_score == self.away_score:
            act_home, act_away = 0.5, 0.5
        else:
            act_home, act_away = 0.0, 1.0
            
        self.home.elo += K_FACTOR * (act_home - exp_home) * goal_diff_multiplier
        self.away.elo += K_FACTOR * (act_away - exp_away) * goal_diff_multiplier

class Season:
    def __init__(self):
        self.teams = []
        self.my_team = None
        self.week = 1
        self.running = True
        self.fixtures = []

    def new_game(self):
        clear_screen()
        print("⚽ Initializing Football Manager Career Mode...")
        time.sleep(0.5)
        
        club_names = ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Chelsea", 
                      "Crystal Palace", "Everton", "Fulham", "Liverpool", "Luton Town", "Man City", 
                      "Man United", "Newcastle", "Nottm Forest", "Sheffield Utd", "Tottenham", 
                      "West Ham", "Wolves", "Leicester City"]
        
        for name in club_names:
            t = Team(name)
            base_skill = random.randint(72, 93)
            t.elo = 950 + (base_skill * 4)
            
            # Generate squad
            for _ in range(18):
                pos = random.choice(POSITIONS)
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                skill = max(50, min(99, base_skill + random.randint(-8, 8)))
                age = random.randint(18, 35)
                
                t.add_player(Player(f"{fname} {lname}", pos, age, skill))
                
            self.teams.append(t)
        
        print(f"✓ Generated {len(self.teams)} teams with full squads")
        time.sleep(0.5)
        self.choose_team()
        self.generate_fixtures()

    def generate_fixtures(self):
        """Create a proper round-robin fixture list"""
        self.fixtures = []
        teams = self.teams[:]
        n = len(teams)
        
        # Simple fixture generation - each team plays each other once per half-season
        for round_num in range(n - 1):
            round_fixtures = []
            for i in range(n // 2):
                home = teams[i]
                away = teams[n - 1 - i]
                round_fixtures.append((home, away))
            self.fixtures.append(round_fixtures)
            # Rotate teams (except first one)
            teams.insert(1, teams.pop())

    def choose_team(self):
        print("\n" + "="*60)
        print("SELECT YOUR TEAM:")
        print("="*60)
        
        sorted_teams = sorted(self.teams, key=lambda x: x.elo, reverse=True)
        
        for i, t in enumerate(sorted_teams):
            strength = "★" * (int(t.elo / 250))
            print(f"{i+1:2d}. {t.name:<20} Elo: {int(t.elo):<4} {strength}")
            
        while True:
            try:
                choice = input("\nEnter team number (or press Enter for random): ").strip()
                if choice == "":
                    self.my_team = random.choice(self.teams)
                    print(f"Random selection: {self.my_team.name}")
                    break
                else:
                    idx = int(choice) - 1
                    if 0 <= idx < len(sorted_teams):
                        self.my_team = sorted_teams[idx]
                        break
                    else:
                        print("Invalid number, try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\n✓ You are now the manager of {self.my_team.name}!")
        time.sleep(1)

    def save(self):
        try:
            data = {
                "week": self.week,
                "my_team": self.my_team.name,
                "teams": [t.to_dict() for t in self.teams]
            }
            with open("career_save.json", "w") as f:
                json.dump(data, f, indent=2)
            print("✓ Game saved successfully!")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️  Save failed: {e}")
            time.sleep(2)

    def load(self):
        try:
            with open("career_save.json", "r") as f:
                data = json.load(f)
            
            self.week = data.get("week", 1)
            my_team_name = data.get("my_team")
            
            self.teams = []
            for t_data in data.get("teams", []):
                team = Team.from_dict(t_data)
                self.teams.append(team)
                if team.name == my_team_name:
                    self.my_team = team
            
            self.generate_fixtures()
            print("✓ Save file loaded successfully!")
            time.sleep(1)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"⚠️  Load failed: {e}")
            time.sleep(2)
            return False

    def menu(self):
        while self.running:
            clear_screen()
            print("="*60)
            print(f"⚽ FOOTBALL MANAGER - WEEK {self.week}")
            print("="*60)
            print(f"Club: {self.my_team.name}")
            print(f"Points: {self.my_team.points} | Elo: {int(self.my_team.elo)} | GD: {self.my_team.goal_diff:+d}")
            print(f"Record: {self.my_team.won}W-{self.my_team.drawn}D-{self.my_team.lost}L")
            print("="*60)
            
            print("\n1. ▶️  Play Next Match")
            print("2. 📊 League Table")
            print("3. 👥 View Squad")
            print("4. ⚙️  Change Tactics")
            print("5. 💾 Save Game")
            print("6. 🚪 Save & Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.play_round()
            elif choice == "2":
                self.show_standings()
            elif choice == "3":
                self.view_squad()
            elif choice == "4":
                self.change_tactics()
            elif choice == "5":
                self.save()
            elif choice == "6":
                self.save()
                self.running = False
                print("\nThanks for playing! Good luck next season! 🏆")
            else:
                print("Invalid option, try again.")
                time.sleep(1)

    def play_round(self):
        if self.week > len(self.fixtures):
            print("\n🏆 Season Complete! Check final standings.")
            input("Press Enter...")
            return
        
        current_fixtures = self.fixtures[self.week - 1]
        my_match = None
        
        # Find user's match and sim others
        for home, away in current_fixtures:
            if home == self.my_team or away == self.my_team:
                my_match = (home, away)
            else:
                Match(home, away, is_user_watching=False).start()

        if my_match:
            clear_screen()
            print(f"\n🎮 YOUR MATCH - Week {self.week}")
            print(f"{my_match[0].name} (Home) vs {my_match[1].name} (Away)")
            input("\nPress Enter to start the match...")
            Match(my_match[0], my_match[1], is_user_watching=True).start()
        
        self.week += 1

    def show_standings(self):
        clear_screen()
        sorted_teams = sorted(self.teams, key=lambda x: (x.points, x.goal_diff, x.goals_for), reverse=True)
        
        print("="*80)
        print(f"{'Pos':<4}{'Team':<20}{'Elo':<6}{'Pts':<5}{'P':<4}{'W':<4}{'D':<4}{'L':<4}{'GF':<5}{'GA':<5}{'GD':<5}")
        print("="*80)
        
        for i, t in enumerate(sorted_teams):
            marker = "👉 " if t == self.my_team else "   "
            print(f"{marker}{i+1:<4}{t.name:<20}{int(t.elo):<6}{t.points:<5}{t.played:<4}{t.won:<4}{t.drawn:<4}{t.lost:<4}{t.goals_for:<5}{t.goals_against:<5}{t.goal_diff:+d}")
        
        print("="*80)
        input("\nPress Enter to return...")

    def view_squad(self):
        clear_screen()
        print(f"\n{'='*60}")
        print(f"{self.my_team.name.upper()} - SQUAD")
        print(f"{'='*60}\n")
        
        by_position = {"GK": [], "DEF": [], "MID": [], "FWD": []}
        for p in self.my_team.players:
            by_position[p.position].append(p)
        
        for pos in ["GK", "DEF", "MID", "FWD"]:
            print(f"\n{pos}:")
            sorted_players = sorted(by_position[pos], key=lambda x: x.overall, reverse=True)
            for p in sorted_players:
                stars = "⭐" * (p.overall // 20)
                print(f"  {p.name:<20} Age: {p.age:<3} Overall: {p.overall:<3} {stars} | Goals: {p.goals}")
        
        print(f"\n{'='*60}")
        input("\nPress Enter to return...")

    def change_tactics(self):
        clear_screen()
        print("\n⚙️  TACTICAL SETUP")
        print(f"Current: {self.my_team.tactic}\n")
        
        for i, (tactic, mult) in enumerate(TACTICS.items(), 1):
            effect = "Boosts attack" if mult > 1 else "Defensive focus" if mult < 1 else "Balanced approach"
            print(f"{i}. {tactic} (x{mult}) - {effect}")
        
        choice = input("\nSelect tactic (or press Enter to keep current): ").strip()
        
        tactics_list = list(TACTICS.keys())
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tactics_list):
                self.my_team.tactic = tactics_list[idx]
                print(f"✓ Tactic changed to: {self.my_team.tactic}")
        except:
            print("Keeping current tactic.")
        
        time.sleep(1)

# Main execution
if __name__ == "__main__":
    season = Season()
    
    if os.path.exists("career_save.json"):
        clear_screen()
        choice = input("💾 Save file found! Load it? (y/n): ").lower().strip()
        if choice == 'y':
            if season.load():
                season.menu()
            else:
                print("Starting new game instead...")
                time.sleep(1)
                season.new_game()
                season.menu()
        else:
            season.new_game()
            season.menu()
    else:
        season.new_game()
        season.menu()