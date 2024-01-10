import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

def create_mine_table(size, mines):
    mine_table = [['hidden' for _ in range(size)] for _ in range(size)]

    for _ in range(mines):
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        while mine_table[row][col] == 'mine':
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        mine_table[row][col] = 'mine'

    return mine_table

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        image_path_normal = "smiley_normal.png"

        # Open the image with PIL
        pil_image = Image.open(image_path_normal)

        # Resize the image to fit in the small box (adjust the size as needed)
        pil_image = pil_image.resize((26, 26), Image.BICUBIC)

        # Convert the PIL image to a Tkinter-compatible PhotoImage
        self.smiley_normal = ImageTk.PhotoImage(pil_image)

        # Create a frame to organize widgets
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        # Load smiley icons with adjusted size
        self.face_button = tk.Button(self.main_frame, image=self.smiley_normal, command=self.show_difficulty_selection, width=26, height=26)
        self.face_button.grid(row=0, column=1)

        self.smiley_win = tk.PhotoImage(width=32, height=32)  # Replace with your image
        self.smiley_lose = tk.PhotoImage(width=32, height=32)  # Replace with your image

        # Initialize game variables
        self.size = 0
        self.mines = 0
        self.mines_left = 0
        self.mine_table = []
        self.buttons = []

        # Mines Left label
        self.mines_left_label = tk.Label(self.main_frame, text="Mines Left: 0")
        self.mines_left_label.grid(row=1, column=2, columnspan=3, sticky="w")  # Adjust columnspan as needed

        # Create difficulty selection button
        self.difficulty_button = tk.Button(self.main_frame, text="Choose Difficulty", command=self.show_difficulty_selection)
        self.difficulty_button.grid(row=0, column=2, pady=(10, 0), columnspan=3, sticky="w")  # Adjust columnspan and pady as needed

        # Initialize Mines Left label with the correct text
        self.update_mines_left_label()

        # Set the initial window size and center on the screen
        initial_width = 400
        initial_height = 400
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (initial_width / 2)
        y_coordinate = (screen_height / 2) - (initial_height / 2)
        master.geometry(f"{initial_width}x{initial_height}+{int(x_coordinate)}+{int(y_coordinate)}")

        # Make sure the window attributes are set correctly
        master.attributes("-alpha", 1.0)  # Set window transparency if needed
        master.resizable(True, True)  # Allow resizing in both directions

    def show_difficulty_selection(self):
        if hasattr(self, 'difficulty_window') and self.difficulty_window.winfo_exists():
            # If the difficulty window already exists, bring it to the front
            self.difficulty_window.lift()
        else:
            # Otherwise, create a new difficulty window
            self.difficulty_window = tk.Toplevel(self.master)
            self.difficulty_window.title("Choose Difficulty")

            difficulty_label = tk.Label(self.difficulty_window, text="Select Difficulty:")
            difficulty_label.grid(row=0, column=0, columnspan=3)

            difficulty_var = tk.StringVar(value=-1)
            difficulties = [('Easy', 5, 5), ('Medium', 10, 15), ('Difficult', 15, 35)]

            for i, (text, size, mines) in enumerate(difficulties):
                radio_button = tk.Radiobutton(self.difficulty_window, text=text, variable=difficulty_var, value=i)
                radio_button.grid(row=1, column=i)

            start_game_button = tk.Button(self.difficulty_window, text="Start Game", command=lambda: (self.difficulty_window.destroy(), self.start_game(int(difficulty_var.get()))))
            start_game_button.grid(row=2, column=0, columnspan=3)

            window_width = 300
            window_height = 150
            screen_width = self.difficulty_window.winfo_screenwidth()
            screen_height = self.difficulty_window.winfo_screenheight()
            x_coordinate = (screen_width / 2) - (window_width / 2)
            y_coordinate = (screen_height / 2) - (window_height / 2)
            self.difficulty_window.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    def start_game(self, difficulty):
        if difficulty is None:
            return

        # Reset the game first
        self.reset_game()

        # Set the game difficulty
        self.size, self.mines = [(5, 5), (10, 15), (15, 35)][difficulty]

        # Recreate Minesweeper game components
        self.create_mine_table()
        self.create_game_board()

        # Initialize mines left
        self.mines_left = self.mines
        self.update_mines_left_label()

        # Calculate the window size based on the size of the grid and difficulty level
        window_width = 50 * self.size  # Adjust the multiplier as needed

        # Define a dictionary for difficulty-specific constants
        difficulty_constants = {0: 50, 1: 100, 2: 150}

        # Adjust the window height dynamically based on the difficulty level
        window_height_constant = difficulty_constants.get(difficulty, 100)
        window_height = 50 * self.size + window_height_constant

        # Set the window size
        self.master.geometry(f"{window_width}x{window_height}")

        # Set the minimum size of the window
        min_width = 50 * self.size  # Adjust the multiplier as needed
        min_height = 50 * self.size + window_height_constant  # Adjust the multiplier for labels
        self.master.minsize(min_width, min_height)

        # Destroy and recreate the entire GUI layout
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        self.mines_left_label = tk.Label(self.main_frame, text=f"Mines Left: {self.mines_left}")
        self.mines_left_label.grid(row=1, column=2, columnspan=3, sticky="w")

        self.face_button = tk.Button(self.main_frame, image=self.smiley_normal, command=self.show_difficulty_selection, width=26, height=26)
        self.face_button.grid(row=0, column=1)

        self.difficulty_button = tk.Button(self.main_frame, text="Choose Difficulty", command=self.show_difficulty_selection)
        self.difficulty_button.grid(row=0, column=2, pady=(10, 0), columnspan=3, sticky="w")

        self.create_game_board()

        # Center the window
        self.center_window()

    def center_window(self):
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = (screen_width - self.master.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - self.master.winfo_reqheight()) // 2
        self.master.geometry(f"+{x_coordinate}+{y_coordinate}") 

    def create_mine_table(self):
        self.mine_table = create_mine_table(self.size, self.mines)

    def create_difficulty_button(self):
        self.difficulty_button.destroy()
        self.difficulty_button = tk.Button(self.main_frame, text="Choose Difficulty", command=self.show_difficulty_selection)
        self.difficulty_button.grid(row=1, column=1, columnspan=3)

    def destroy_buttons(self):
        for button_row in self.buttons:
            for button in button_row:
                button.destroy()
        self.buttons = []

    def create_game_board(self):
        # Create game board components here
        button_width = 3
        button_height = 2
        self.buttons = []

        # Create a separate frame for buttons
        buttons_frame = tk.Frame(self.main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=max(1, self.size))  # Ensure columnspan is at least 1

        # Configure row and column weights for the new frame
        for row in range(self.size):
            buttons_frame.rowconfigure(row, weight=1)
        for col in range(self.size):
            buttons_frame.columnconfigure(col, weight=1)

        # Add buttons to the frame
        for row in range(self.size):
            button_row = []  # Create an empty list for each row
            for col in range(self.size):
                button = tk.Button(buttons_frame, width=button_width, height=button_height, relief="raised", bd=2)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.reveal_cell(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.place_flag(r, c))
                button.grid(row=row, column=col, padx=1, pady=1, sticky='nsew')

                # Store buttons in self.buttons
                button_row.append(button)
            self.buttons.append(button_row)

        # Add an empty row below the buttons for spacing
        if self.size > 0:
            tk.Frame(self.main_frame, height=1, width=1, bg="black").grid(
                row=self.size + 2, column=0, columnspan=max(1, self.size), padx=1, pady=1, sticky='ew')

        # Configure row and column weights for the main frame
        for row in range(self.size + 3):  # Include the row with labels and the extra empty row
            self.main_frame.rowconfigure(row, weight=1)

        for col in range(self.size):
            self.main_frame.columnconfigure(col, weight=1)

    def update_mines_left_label(self):
        self.mines_left_label.config(text=f"Mines Left: {self.mines_left}")

    def reset_game(self):
        # Update the face button properties
        self.face_button.config(image=self.smiley_normal, command=self.show_difficulty_selection)

        # Destroy buttons and recreate difficulty button
        self.destroy_buttons()
        self.create_difficulty_button()

        # Destroy Mines Left label
        self.mines_left_label.destroy()

        # Recreate the face button with adjusted size
        self.face_button = tk.Button(self.main_frame, image=self.smiley_normal, command=self.show_difficulty_selection, width=26, height=26)
        self.face_button.grid(row=0, column=1)

        # Recreate difficulty button
        self.difficulty_button.destroy()
        self.difficulty_button = tk.Button(self.main_frame, text="Choose Difficulty", command=self.show_difficulty_selection)
        self.difficulty_button.grid(row=0, column=2, pady=(10, 0), columnspan=1, rowspan=1, sticky="w")  # Adjust columnspan and pady as needed

        # Recreate Mines Left label with adjusted layout
        self.mines_left = 0  # Reset mines_left to 0
        self.mines_left_label = tk.Label(self.main_frame, text=f"Mines Left: {self.mines_left}")
        self.mines_left_label.grid(row=1, column=2, columnspan=3, sticky="w")  # Adjust columnspan as needed

        # Initialize game variables
        self.size = 0
        self.mines = 0
        self.mine_table = []

        # Set the window size based on the size of the grid
        window_width = 400
        window_height = 400
        self.master.geometry(f"{window_width}x{window_height}")

        # Center the window
        self.center_window()

        # Force update the window
        self.master.update()

    def play_again(self):
        # Destroy the current difficulty window if it exists
        if hasattr(self, 'difficulty_window') and self.difficulty_window.winfo_exists():
            self.difficulty_window.destroy()

        # Reset the game to the initial state
        self.reset_game()

        # Update the Mines Left label
        self.update_mines_left_label()

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]

        # Generate the mine table if it hasn't been generated yet
        if not self.mine_table:
            self.create_mine_table()
            # Ensure that the first revealed cell is not a mine
            while self.mine_table[row][col] == 'mine':
                self.create_mine_table()

        if button.winfo_exists():
            if button.cget('bg') == 'red':
                pass
            elif self.mine_table[row][col] == 'mine':
                # Handle the case where the first cell is a mine
                if not getattr(self, 'first_cell_revealed', False):
                    self.first_cell_revealed = True
                    self.reveal_cell(row, col)
                else:
                    # Handle other cases of revealing a mine
                    self.show_loss_popup()
                    print("Game Over - You hit a mine!")
                    self.disable_all_buttons()
                #self.mine_table[row][col] = 'revealed' unecessary, cause loss window pops up anyway and game resets.
            else:
                if str(self.count_adjacent_mines(row, col)) == '0':
                    self.reveal_adjacent_cells(row, col)
                else:
                    button.config(text=str(self.count_adjacent_mines(row, col)), bg='grey')

                self.mine_table[row][col] = 'revealed'

        if self.check_win():
            self.show_win_popup()
            print("Congratulations! You won!")
            self.disable_all_buttons()

    def place_flag(self, row, col):
        button = self.buttons[row][col]

        # Check if the button still exists and the cell is not revealed
        if button.winfo_exists() and self.mine_table[row][col] != 'revealed':
            current_color = button.cget("bg")  # Get the current background color

            # Count the red flags
            red_flags = sum(button.cget("bg") == 'red' for row in self.buttons for button in row)

            if red_flags > self.mines:
                self.mines_left = 0
                if current_color == 'red':
                    button.config(bg='SystemButtonFace')  # Change back to the default background color
                else:
                    button.config(bg='red')  # Change to red if not flagged
            else:
                if current_color == 'red':
                    button.config(bg='SystemButtonFace')  # Change back to the default background color
                    if self.mines_left < self.mines:
                        self.mines_left += 1
                    elif self.mines_left > self.mines:
                        self.mines_left -= 1
                else:
                    button.config(bg='red')  # Change to red if not flagged

                    if self.mines_left > 0:
                        self.mines_left -= 1

                self.mines_left_label.config(text=f"Mines Left: {self.mines_left}")
                self.master.update()       

    def disable_all_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.size, row + 2)):
            for j in range(max(0, col - 1), min(self.size, col + 2)):
                if self.mine_table[i][j] == 'mine':
                    count += 1
        return count
    
    def reveal_adjacent_cells(self, start_row, start_col):
        stack = [(start_row, start_col)]

        while stack:
            row, col = stack.pop()

            if self.mine_table[row][col] != 'mine' and self.mine_table[row][col] != 'revealed':
                button = self.buttons[row][col]
                if button.winfo_exists():
                    if str(self.count_adjacent_mines(row, col)) == '0':
                        for i in range(max(0, row - 1), min(self.size, row + 2)):
                            for j in range(max(0, col - 1), min(self.size, col + 2)):
                                stack.append((i, j))
                                if self.mine_table[i][j] != 'mine' and self.mine_table[i][j] != 'revealed':
                                    self.buttons[i][j].config(bg='grey')  # Set the background color to grey
                    else:
                        button.config(text=str(self.count_adjacent_mines(row, col)), bg='grey')

                    self.mine_table[row][col] = 'revealed'
 
    def check_win(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.mine_table[row][col] != 'mine' and self.mine_table[row][col] != 'revealed':
                    # Check if the button still exists before considering it as revealed
                    if self.buttons[row][col].winfo_exists():
                        return False
        return True

    def show_win_popup(self):
        image_path = "smiley_win.png"
        self.show_popup("Congratulations! You won!", image_path)

    def show_loss_popup(self):
        image_path = "smiley_lose.png"
        self.show_popup("You hit a mine!", image_path)

    def show_popup(self, message, image_path):
        pil_image = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(pil_image)

        popup_window = tk.Toplevel(self.master)

        message_label = tk.Label(popup_window, text=message)
        message_label.pack()

        if tk_image:
            image_label = tk.Label(popup_window, image=tk_image)
            image_label.photo = tk_image
            image_label.pack()

        play_again_button = tk.Button(popup_window, text="Play Again", command=lambda: (popup_window.destroy(), self.play_again()))
        play_again_button.pack()

        popup_window.title(message)
        popup_window.geometry("+%d+%d" % (self.master.winfo_screenwidth() // 2 - popup_window.winfo_reqwidth() // 2,
                                          self.master.winfo_screenheight() // 2 - popup_window.winfo_reqheight() // 2))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper = MinesweeperGUI(root)

    # Center the main window
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    root.mainloop()