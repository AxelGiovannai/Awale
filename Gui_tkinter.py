import tkinter as tk
from typing import Optional, Callable
from Awale import Awale


class GuiTkinter:
    def __init__(self, game: Optional[Awale] = None):
        self.game = game if game is not None else Awale()
        self.root = tk.Tk()
        self.root.title("Awalé")

        self.cell_width = 110
        self.cell_height = 110
        self.margin_x = 40
        self.margin_y = 40
        self.row_gap = 70
        self.top_row_y = 120
        self.bottom_row_y = 320

        self.canvas_width = self.margin_x * 2 + self.cell_width * 6
        self.canvas_height = 470

        self._pit_bounds = {}
        self._game_over = False

        self.on_pit_click_callback: Optional[Callable[[int], None]] = None
        self.on_start_game_callback: Optional[Callable[[dict], None]] = None
        self.on_replay_callback: Optional[Callable[[], None]] = None
        self.on_back_to_menu_callback: Optional[Callable[[], None]] = None
        self.on_statistics_callback: Optional[Callable[[], None]] = None

        self._build_menu_ui()
        self._build_game_ui()

        self.show_menu()

    def _build_menu_ui(self) -> None:
        self.menu_frame = tk.Frame(self.root, padx=20, pady=20)

        title = tk.Label(self.menu_frame, text="Awale", font=("Arial", 24, "bold"))
        title.pack(pady=(0, 20))

        subtitle = tk.Label(
            self.menu_frame,
            text="Configuration de la partie",
            font=("Arial", 13),
        )
        subtitle.pack(pady=(0, 20))

        # Variables pour Joueur 0
        self.player0_type_var = tk.StringVar(value="Humain")
        self.player0_depth_var = tk.IntVar(value=4)
        self.player0_heuristic_var = tk.StringVar(value="score")
        self.player0_iterations_var = tk.IntVar(value=200)
        self.player0_time_var = tk.DoubleVar(value=1.0)
        self.player0_temperature_var = tk.DoubleVar(value=1.0)

        # Variables pour Joueur 1
        self.player1_type_var = tk.StringVar(value="Humain")
        self.player1_depth_var = tk.IntVar(value=4)
        self.player1_heuristic_var = tk.StringVar(value="score")
        self.player1_iterations_var = tk.IntVar(value=200)
        self.player1_time_var = tk.DoubleVar(value=1.0)
        self.player1_temperature_var = tk.DoubleVar(value=1.0)

        # Joueur 0 frame
        p0_frame = tk.LabelFrame(self.menu_frame, text="Joueur 0", padx=10, pady=10)
        p0_frame.pack(fill="x", pady=8)

        tk.Label(p0_frame, text="Type").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(
            p0_frame, self.player0_type_var, "Humain", "IA (Stupide)", "IA (MinMax)", "IA (MCTS)"
        ).grid(row=0, column=1, sticky="ew")

        # MinMax widgets pour Joueur 0
        self.p0_minmax_widgets = []

        label = tk.Label(p0_frame, text="Profondeur")
        label.grid(row=1, column=0, sticky="w")
        self.p0_minmax_widgets.append(label)

        spinbox = tk.Spinbox(p0_frame, from_=1, to=8, textvariable=self.player0_depth_var, width=5)
        spinbox.grid(row=1, column=1, sticky="w")
        self.p0_minmax_widgets.append(spinbox)

        label = tk.Label(p0_frame, text="Heuristique")
        label.grid(row=2, column=0, sticky="w")
        self.p0_minmax_widgets.append(label)

        optmenu = tk.OptionMenu(p0_frame, self.player0_heuristic_var, "score", "mobility")
        optmenu.grid(row=2, column=1, sticky="ew")
        self.p0_minmax_widgets.append(optmenu)

        # MCTS widgets pour Joueur 0
        self.p0_mcts_widgets = []

        label = tk.Label(p0_frame, text="Iterations")
        label.grid(row=3, column=0, sticky="w")
        self.p0_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p0_frame, from_=10, to=5000, increment=10, textvariable=self.player0_iterations_var, width=8)
        spinbox.grid(row=3, column=1, sticky="w")
        self.p0_mcts_widgets.append(spinbox)

        label = tk.Label(p0_frame, text="Temps max (s)")
        label.grid(row=4, column=0, sticky="w")
        self.p0_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p0_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.player0_time_var, width=8)
        spinbox.grid(row=4, column=1, sticky="w")
        self.p0_mcts_widgets.append(spinbox)

        label = tk.Label(p0_frame, text="Temperature")
        label.grid(row=5, column=0, sticky="w")
        self.p0_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p0_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.player0_temperature_var, width=8)
        spinbox.grid(row=5, column=1, sticky="w")
        self.p0_mcts_widgets.append(spinbox)

        # Joueur 1 frame
        p1_frame = tk.LabelFrame(self.menu_frame, text="Joueur 1", padx=10, pady=10)
        p1_frame.pack(fill="x", pady=8)

        tk.Label(p1_frame, text="Type").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(
            p1_frame, self.player1_type_var, "Humain", "IA (Stupide)", "IA (MinMax)", "IA (MCTS)"
        ).grid(row=0, column=1, sticky="ew")

        # MinMax widgets pour Joueur 1
        self.p1_minmax_widgets = []

        label = tk.Label(p1_frame, text="Profondeur")
        label.grid(row=1, column=0, sticky="w")
        self.p1_minmax_widgets.append(label)

        spinbox = tk.Spinbox(p1_frame, from_=1, to=8, textvariable=self.player1_depth_var, width=5)
        spinbox.grid(row=1, column=1, sticky="w")
        self.p1_minmax_widgets.append(spinbox)

        label = tk.Label(p1_frame, text="Heuristique")
        label.grid(row=2, column=0, sticky="w")
        self.p1_minmax_widgets.append(label)

        optmenu = tk.OptionMenu(p1_frame, self.player1_heuristic_var, "score", "mobility")
        optmenu.grid(row=2, column=1, sticky="ew")
        self.p1_minmax_widgets.append(optmenu)

        # MCTS widgets pour Joueur 1
        self.p1_mcts_widgets = []

        label = tk.Label(p1_frame, text="Iterations")
        label.grid(row=3, column=0, sticky="w")
        self.p1_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p1_frame, from_=10, to=5000, increment=10, textvariable=self.player1_iterations_var, width=8)
        spinbox.grid(row=3, column=1, sticky="w")
        self.p1_mcts_widgets.append(spinbox)

        label = tk.Label(p1_frame, text="Temps max (s)")
        label.grid(row=4, column=0, sticky="w")
        self.p1_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p1_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.player1_time_var, width=8)
        spinbox.grid(row=4, column=1, sticky="w")
        self.p1_mcts_widgets.append(spinbox)

        label = tk.Label(p1_frame, text="Temperature")
        label.grid(row=5, column=0, sticky="w")
        self.p1_mcts_widgets.append(label)

        spinbox = tk.Spinbox(p1_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.player1_temperature_var, width=8)
        spinbox.grid(row=5, column=1, sticky="w")
        self.p1_mcts_widgets.append(spinbox)

        # Trace des changements de type
        self.player0_type_var.trace("w", lambda *args: self._update_player_widgets(0))
        self.player1_type_var.trace("w", lambda *args: self._update_player_widgets(1))

        # Boutons
        start_button = tk.Button(
            self.menu_frame,
            text="Demarrer la partie",
            font=("Arial", 12, "bold"),
            command=self._handle_start_from_menu,
            padx=12,
            pady=8,
        )
        start_button.pack(pady=(20, 8))

        statistics_button = tk.Button(
            self.menu_frame,
            text="Statistiques",
            command=self._handle_statistics_from_menu,
            padx=12,
            pady=8,
        )
        statistics_button.pack(pady=(0, 8))

        quit_button = tk.Button(
            self.menu_frame,
            text="Quitter",
            command=self.root.destroy,
            padx=12,
            pady=6,
        )
        quit_button.pack()

        # Affiche les widgets au démarrage
        self._update_player_widgets(0)
        self._update_player_widgets(1)

    def _update_player_widgets(self, player_num: int) -> None:
        if player_num == 0:
            player_type = self.player0_type_var.get()
            minmax_widgets = self.p0_minmax_widgets
            mcts_widgets = self.p0_mcts_widgets
        else:
            player_type = self.player1_type_var.get()
            minmax_widgets = self.p1_minmax_widgets
            mcts_widgets = self.p1_mcts_widgets

        # Cache tous les widgets
        for widget in minmax_widgets + mcts_widgets:
            widget.grid_remove()

        # Affiche selon le type
        if player_type == "IA (MinMax)":
            for widget in minmax_widgets:
                widget.grid()
        elif player_type == "IA (MCTS)":
            for widget in mcts_widgets:
                widget.grid()

    def _build_game_ui(self) -> None:
        self.game_frame = tk.Frame(self.root)

        self.canvas = tk.Canvas(
            self.game_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#1f6f4a",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        self.info_frame = tk.Frame(self.game_frame)
        self.info_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.score_var = tk.StringVar()
        self.turn_var = tk.StringVar()
        self.message_var = tk.StringVar()

        self.score_label = tk.Label(
            self.info_frame,
            textvariable=self.score_var,
            font=("Arial", 12, "bold"),
        )
        self.score_label.pack(anchor="w")

        self.turn_label = tk.Label(
            self.info_frame,
            textvariable=self.turn_var,
            font=("Arial", 12),
        )
        self.turn_label.pack(anchor="w")

        self.message_label = tk.Label(
            self.info_frame,
            textvariable=self.message_var,
            font=("Arial", 11),
            fg="#333333",
        )
        self.message_label.pack(anchor="w")

        self.button_frame = tk.Frame(self.game_frame)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.new_round_button = tk.Button(
            self.button_frame,
            text="Nouvelle manche",
            command=self._handle_replay,
        )
        self.new_round_button.pack(side="left")

        self.menu_button = tk.Button(
            self.button_frame,
            text="Menu",
            command=self._handle_back_to_menu,
        )
        self.menu_button.pack(side="left", padx=(8, 0))

        self.quit_button = tk.Button(
            self.button_frame,
            text="Quitter",
            command=self.root.destroy,
        )
        self.quit_button.pack(side="right")

        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def run(self) -> None:
        self.root.mainloop()

    def start(self) -> None:
        self.run()

    def show_menu(self) -> None:
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
        self.message_var.set("")
        self._game_over = False

    def show_game(self) -> None:
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.refresh()

    def _handle_start_from_menu(self) -> None:
        config = {
            "player0": {
                "type": self.player0_type_var.get(),
                "depth": self.player0_depth_var.get(),
                "heuristic": self.player0_heuristic_var.get(),
                "iterations": self.player0_iterations_var.get(),
                "time": self.player0_time_var.get(),
                "temperature": self.player0_temperature_var.get(),
            },
            "player1": {
                "type": self.player1_type_var.get(),
                "depth": self.player1_depth_var.get(),
                "heuristic": self.player1_heuristic_var.get(),
                "iterations": self.player1_iterations_var.get(),
                "time": self.player1_time_var.get(),
                "temperature": self.player1_temperature_var.get(),
            },
        }
        if self.on_start_game_callback:
            self.on_start_game_callback(config)
        else:
            self.show_game()

    def _handle_replay(self) -> None:
        if self.on_replay_callback:
            self.on_replay_callback()

    def _handle_statistics_from_menu(self) -> None:
        if self.on_statistics_callback:
            self.on_statistics_callback()

    def _handle_back_to_menu(self) -> None:
        if self.on_back_to_menu_callback:
            self.on_back_to_menu_callback()
        else:
            self.show_menu()

    def set_game(self, game: Awale) -> None:
        self.game = game
        self._game_over = False
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.refresh()

    def notify(self, message: str) -> None:
        self.message_var.set(message)

    def refresh(self) -> None:
        self.canvas.delete("all")
        self._pit_bounds = {}

        self._draw_background()
        self._draw_titles()
        self._draw_pits()
        self._draw_scores()
        self._update_texts()

    def map_coords_to_pit(self, x: int, y: int) -> Optional[int]:
        for pit, (x0, y0, x1, y1) in self._pit_bounds.items():
            if x0 <= x <= x1 and y0 <= y <= y1:
                return pit
        return None

    def _on_canvas_click(self, event) -> None:
        if self._game_over:
            return

        pit = self.map_coords_to_pit(event.x, event.y)
        if pit is None:
            return

        if self.on_pit_click_callback:
            self.on_pit_click_callback(pit)

    def _draw_background(self) -> None:
        self.canvas.create_rectangle(
            0, 0, self.canvas_width, self.canvas_height,
            fill="#1f6f4a",
            outline="#1f6f4a",
        )
        self.canvas.create_rectangle(
            18, 90, self.canvas_width - 18, 420,
            fill="#2f8a5d",
            outline="#145438",
            width=3,
        )

    def _draw_titles(self) -> None:
        self.canvas.create_text(
            self.canvas_width / 2,
            35,
            text="Awale",
            fill="white",
            font=("Arial", 22, "bold"),
        )

        self.canvas.create_text(
            self.canvas_width / 2,
            95,
            text="Joueur 1",
            fill="white",
            font=("Arial", 12, "bold"),
        )

        self.canvas.create_text(
            self.canvas_width / 2,
            425,
            text="Joueur 0",
            fill="white",
            font=("Arial", 12, "bold"),
        )

    def _draw_scores(self) -> None:
        score0, score1 = self.game.get_score()
        self.canvas.create_text(
            90,
            60,
            text=f"Score J0: {score0}",
            fill="white",
            font=("Arial", 11, "bold"),
            anchor="w",
        )
        self.canvas.create_text(
            self.canvas_width - 90,
            60,
            text=f"Score J1: {score1}",
            fill="white",
            font=("Arial", 11, "bold"),
            anchor="e",
        )

    def _draw_pits(self) -> None:
        board = self.game.get_board()

        top_positions = [11, 10, 9, 8, 7, 6]
        bottom_positions = [0, 1, 2, 3, 4, 5]

        for column, pit in enumerate(top_positions):
            x0 = self.margin_x + column * self.cell_width
            y0 = self.top_row_y
            self._draw_pit(pit, x0, y0, board[pit])

        for column, pit in enumerate(bottom_positions):
            x0 = self.margin_x + column * self.cell_width
            y0 = self.bottom_row_y
            self._draw_pit(pit, x0, y0, board[pit])

    def _draw_pit(self, pit: int, x0: int, y0: int, seeds: int) -> None:
        x1 = x0 + self.cell_width - 15
        y1 = y0 + self.cell_height - 15
        self._pit_bounds[pit] = (x0, y0, x1, y1)

        player = 0 if pit < 6 else 1
        active_player = self.game.get_current_player()
        fill_color = "#f4d6a0" if player == active_player else "#d8b57a"
        outline_color = "#5a3d1a"

        self.canvas.create_oval(
            x0, y0, x1, y1,
            fill=fill_color,
            outline=outline_color,
            width=3,
        )

        self.canvas.create_text(
            (x0 + x1) / 2,
            (y0 + y1) / 2 - 8,
            text=str(seeds),
            fill="#2d1b0f",
            font=("Arial", 18, "bold"),
        )

        self.canvas.create_text(
            (x0 + x1) / 2,
            y1 + 12,
            text=str(pit),
            fill="white",
            font=("Arial", 9),
        )

    def _update_texts(self) -> None:
        score0, score1 = self.game.get_score()
        current_player = self.game.get_current_player()

        self.score_var.set(f"Scores - Joueur 0: {score0} | Joueur 1: {score1}")
        self.turn_var.set(f"Tour du joueur {current_player}")

    def show_game_over(self) -> None:
        self._game_over = True
        self.canvas.unbind("<Button-1>")

        winner = self.game.get_winner()
        score0, score1 = self.game.get_score()

        if winner is None:
            self.notify(f"Fin de manche: egalite ({score0} - {score1}).")
            text = "Match nul"
        else:
            self.notify(f"Fin de manche: joueur {winner} gagne ({score0} - {score1}).")
            text = f"Joueur {winner} gagne"

        self.canvas.create_rectangle(
            90, 180, self.canvas_width - 90, 260,
            fill="#ffffff",
            outline="#ffffff",
        )
        self.canvas.create_text(
            self.canvas_width / 2,
            220,
            text=text,
            fill="#1f6f4a",
            font=("Arial", 20, "bold"),
        )
