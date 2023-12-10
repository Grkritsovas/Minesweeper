# Minesweeper
Classic Minesweeper game in Python with Tkinter GUI. Uncover mines, flag danger, and strategize.

# Minesweeper Game

Welcome to the Minesweeper game! This project is a simple implementation of Minesweeper using Python and Tkinter.

## How to Play

Follow these steps to run the Minesweeper game on your local machine:

**Clone the Repository**:
Open a terminal window (Command Prompt on Windows, or Terminal on macOS/Linux) and run the following command:
    ```bash
    
    git clone https://github.com/Grkritsovas/Minesweeper.git

This command downloads a copy of the repository to your local machine.

Navigate to the Cloned Repository:
After cloning, you need to change your terminal's current directory to the location where the repository was cloned. If you've used the default settings, the repository will be in a folder with the same name as your repository.

For example, if your repository is named minesweeper, run:   cd Minesweeper

This command changes your current directory to the minesweeper folder, which is the local copy of your GitHub repository.
The cd Minesweeper instruction assumes that the repository was cloned into a folder with the same name as your repository. If you used a different folder name during cloning, replace Minesweeper with the correct folder name.

Install Dependencies:
If there are any external dependencies, install them:
Tkinter:
Tkinter is the standard GUI toolkit for Python. It is used to create the graphical user interface for your Minesweeper game.

You can include the following command for users to install Tkinter using pip:  pip install tk

PIL (Python Imaging Library):
PIL is used for working with images. In this case, it's utilized for loading and displaying smiley icons in the game.

You can install PIL using the following command:  pip install pillow

You need to download or clone the entire repository, including the images folder, for the game to run correctly.

**Run the Minesweeper Game**:
To run the Minesweeper game, execute the following command in your terminal within the project directory:
    python mines.py

Playing the Game:
Here are some brief instructions on how to play the Minesweeper game:
-Left-click to reveal a cell.
-Right-click to place or remove a flag.
-Objective: Uncover all cells without hitting a mine.


Features:
Three difficulty levels (easy, medium, difficult).
Flagging system to mark potential mine locations.
You can use as many flags as you want(They are displayed with just a red color filler for the cells)
The Mines_left label updates based on how many flags you have placed
The Mines_left label only updates as long as you place flags <= mines_left in the board
But you can still choose to put down as many flags as you want!

Contributions:
All contributions are welcome!

License:
This Minesweeper project is licensed under the [MIT License](LICENSE).

Acknowledgments

- [Tkinter](https://docs.python.org/3/library/tkinter.html): Standard GUI toolkit for Python.
- [Pillow](https://pillow.readthedocs.io/): Python Imaging Library used for working with images.

**Happy mining**
