import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import torch  # ✅ Ajout nécessaire
import tkinter as tk
from tkinter import messagebox

# === CLASSE TIC-TAC-TOE ===
class TicTacToe:
    def __init__(self):
        self.board = [[0]*3 for _ in range(3)]
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board = [[0]*3 for _ in range(3)]
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] != 0 or self.game_over:
            return False
        self.board[row][col] = self.current_player

        if self.check_winner(self.current_player):
            self.winner = self.current_player
            self.game_over = True
        elif all(cell != 0 for r in self.board for cell in r):
            self.winner = 0
            self.game_over = True
        else:
            self.current_player = 2 if self.current_player == 1 else 1
        return True

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def get_valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

# === ENVIRONNEMENT GYMNASIUM ===
class TicTacToeEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None):
        super(TicTacToeEnv, self).__init__()
        self.render_mode = render_mode
        self.game = TicTacToe()

        self.action_space = gym.spaces.Discrete(9)
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(9,), dtype=np.int32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset()
        return np.array(self.game.board).flatten(), {}

    def step(self, action):
        row = action // 3
        col = action % 3

        valid_moves = self.game.get_valid_moves()
        if (row, col) not in valid_moves:
            return np.array(self.game.board).flatten(), -20, True, False, {"invalid_move": True}

        old_board = [r[:] for r in self.game.board]
        self.game.make_move(row, col)

        reward = 0
        terminated = self.game.game_over
        info = {}

        if self.game.winner == 2:
            reward = 100
        elif self.game.winner == 1:
            reward = -100
        elif self.game.winner == 0:
            reward = 10
        else:
            reward += self.calculate_strategic_reward(old_board)

        return np.array(self.game.board).flatten(), reward, terminated, False, info

    def calculate_strategic_reward(self, old_board):
        board = self.game.board
        player = 2
        opponent = 1
        reward = 0

        for i in range(3):
            line = list(board[i])
            reward += self.evaluate_line(line, player, opponent)
            col = list([board[0][i], board[1][i], board[2][i]])
            reward += self.evaluate_line(col, player, opponent)

        diag1 = list([board[0][0], board[1][1], board[2][2]])
        diag2 = list([board[0][2], board[1][1], board[2][0]])
        reward += self.evaluate_line(diag1, player, opponent)
        reward += self.evaluate_line(diag2, player, opponent)

        if board[1][1] == player:
            reward += 2
        elif board[1][1] == opponent:
            reward -= 1

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for r, c in corners:
            if board[r][c] == player:
                reward += 1

        return reward

    def evaluate_line(self, line, player, opponent):
        p = line.count(player)
        o = line.count(opponent)
        e = line.count(0)

        if p == 3:
            return 100
        if o == 3:
            return -100
        if o == 0 and p == 2 and e == 1:
            return 10
        if o == 0 and p == 1 and e == 2:
            return 2
        if p == 0 and o == 2 and e == 1:
            return 15
        if p == 0 and o == 1 and e == 2:
            return 3
        return 0

# === ENTRAÎNEMENT ===
def train_ai(save_path="tictactoe_ppo"):
    env = TicTacToeEnv()
    check_env(env)

    model = PPO("MlpPolicy", env, verbose=1,
                learning_rate=0.0003,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                clip_range=0.2,
                ent_coef=0.01,
                policy_kwargs=dict(net_arch=[64, 64]))

    model.learn(total_timesteps=200000)
    model.save(save_path)
    return model

# === AGENT DRL CORRIGÉ ===
class DRLAgent:
    def __init__(self, model_path="tictactoe_ppo"):
        self.model = PPO.load(model_path)

    def predict(self, board, valid_moves):
        flat_board = np.array(board).flatten()
        action, _ = self.model.predict(flat_board, deterministic=True)
        row, col = divmod(action, 3)

        if (row, col) in valid_moves:
            return row, col

        valid_actions = [r * 3 + c for (r, c) in valid_moves]
        obs = torch.tensor([flat_board], dtype=torch.float32)  # ✅ CORRECTION ICI
        dist = self.model.policy.get_distribution(obs)
        probs = dist.distribution.probs.detach().numpy().flatten()

        valid_probs = np.zeros(9)
        valid_probs[valid_actions] = probs[valid_actions]
        best_action = valid_actions[np.argmax(valid_probs[valid_actions])]
        return divmod(best_action, 3)

# === INTERFACE TKINTER ===
class TicTacToeGUI:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.game = TicTacToe()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.root.title("Tic-Tac-Toe vs IA")
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Helvetica", 36), width=5, height=2,
                               command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, row, col):
        if self.game.game_over or self.game.board[row][col] != 0:
            return

        self.game.make_move(row, col)
        self.update_buttons()

        if self.game.game_over:
            self.show_result()
            return

        board = self.game.board
        valid_moves = self.game.get_valid_moves()
        ai_row, ai_col = self.agent.predict(board, valid_moves)
        self.game.make_move(ai_row, ai_col)
        self.update_buttons()

        if self.game.game_over:
            self.show_result()

    def update_buttons(self):
        symbols = {0: "", 1: "X", 2: "O"}
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=symbols[self.game.board[i][j]])

    def show_result(self):
        if self.game.winner == 1:
            msg = "🎉 Tu as gagné !"
        elif self.game.winner == 2:
            msg = "💻 L'IA a gagné !"
        else:
            msg = "🤝 Match nul."
        messagebox.showinfo("Fin de la partie", msg)
        self.root.destroy()

# === LANCEMENT ===
if __name__ == "__main__":
    print("Entraînement de l'IA...")
    train_ai()

    print("Démarrage de l'interface graphique...")
    root = tk.Tk()
    agent = DRLAgent("tictactoe_ppo")
    app = TicTacToeGUI(root, agent)
    root.mainloop()
