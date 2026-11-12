import tkinter as tk
import pygame
import time
import os

# ---------------- AUDIO SETUP ----------------

pygame.mixer.init()

audio_file = os.path.join(
    os.path.dirname(__file__),
    "comeover.mp3.mpeg.mp3"
)

pygame.mixer.music.load(audio_file)

# ---------------- LYRICS ----------------

LYRICS = [
    (0.0, "Over, over, over, over, over"),
    (2.0, "Over, over, over, over"),
    (5.0, "You'll never love me like the way you did before"),
    (15.0, "But would you open up if I knocked on your door?"),
]

# ---------------- DESIGN SETTINGS ----------------

BOX_W, BOX_H = 350, 300

FONT = ("Helvetica", 25, "bold")

BG_COLOR = "#fdfdf5"
FG_COLOR = "#111111"

RISE_SPEED = 70
BOTTOM_SPAWN_OFFSET = 150
STACK_SPACING = 20

TYPEWRITER_DELAY = 100


# ---------------- LYRIC CARD ----------------

class LyricCard:

    def __init__(self, parent, text, x, y):

        self.win = tk.Toplevel(parent)

        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)

        self.win.geometry(
            f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}"
        )

        self.win.resizable(False, False)

        self.full_text = text

        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 25,
            justify="center"
        )

        self.label.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=15
        )

        self.typewriter_index = 0

        self.x = x
        self.y = float(y)

        self.win.after(
            TYPEWRITER_DELAY,
            self.typewriter
        )

    # Move lyric card upwards
    def rise(self, dy):

        self.y -= dy

        self.win.geometry(
            f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}"
        )

    # Check whether card has left the screen
    def is_offscreen(self):

        return self.y + BOX_H < -50

    # Display lyrics using typewriter effect
    def typewriter(self):

        if self.typewriter_index <= len(self.full_text):

            self.label.config(
                text=self.full_text[:self.typewriter_index]
            )

            self.typewriter_index += 1

            self.win.after(
                TYPEWRITER_DELAY,
                self.typewriter
            )


# ---------------- MAIN APPLICATION ----------------

class LyricFloatApp:

    def __init__(self, root):

        self.root = root

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        self.next_lyric_idx = 0

        self.boxes = []

        self.last_frame_time = None

        self.current_side = "left"

        self.final_box = None
        self.closing = False

        self.start()

    # Alternate between left and right
    def random_safe_x(self):

        center_x = self.screen_w // 2

        spacing = BOX_W + 60

        left_x = center_x - spacing
        right_x = center_x + 60

        if self.current_side == "left":

            self.current_side = "right"

            return left_x

        else:

            self.current_side = "left"

            return right_x

    # Find position for next lyric
    def lowest_y(self):

        if not self.boxes:

            return self.screen_h - BOX_H - BOTTOM_SPAWN_OFFSET

        return max(
            box.y for box in self.boxes
        ) + BOX_H + STACK_SPACING

    # Start music and animation
    def start(self):

        self.root.withdraw()

        self.start_time = time.time()

        self.last_frame_time = self.start_time

        pygame.mixer.music.play()

        self.tick()

    # Main animation loop
    def tick(self):

        if self.closing:
            return

        # Check whether the song has finished
        if not pygame.mixer.music.get_busy():

            self.close_app()
            return

        now = time.time()

        elapsed = max(
            0,
            pygame.mixer.music.get_pos() / 1000
        )

        dt = now - self.last_frame_time

        self.last_frame_time = now

        # Create lyric cards at their timestamps
        while (
            self.next_lyric_idx < len(LYRICS)
            and LYRICS[self.next_lyric_idx][0] <= elapsed
        ):

            t, text = LYRICS[self.next_lyric_idx]

            x = self.random_safe_x()

            y = self.lowest_y()

            box = LyricCard(
                self.root,
                text,
                x,
                y
            )

            self.boxes.append(box)

            # Remember the final lyric box
            if self.next_lyric_idx == len(LYRICS) - 1:
                self.final_box = box

            self.next_lyric_idx += 1

        # Move lyric cards upwards
        dy = RISE_SPEED * dt

        for box in self.boxes:

            if box == self.final_box:

                # Let final lyric float into position
                target_y = self.screen_h // 2 - BOX_H // 2

                if box.y > target_y:

                    movement = min(dy, box.y - target_y)

                    box.rise(movement)

                # Stay in position after reaching target

            else:

                box.rise(dy)

        # Remove cards that have left the screen
        still_visible = []

        for box in self.boxes:

            if box.is_offscreen() and box != self.final_box:

                try:
                    box.win.destroy()
                except tk.TclError:
                    pass

            else:

                still_visible.append(box)

        self.boxes = still_visible

        # Continue animation
        self.root.after(16, self.tick)

    # Close the entire application
    def close_app(self):

        if self.closing:
            return

        self.closing = True

        # Stop music
        pygame.mixer.music.stop()

        # Close all lyric windows
        for box in self.boxes:

            try:
                box.win.destroy()
            except tk.TclError:
                pass

        self.boxes.clear()

        # Close main window
        try:
            self.root.destroy()
        except tk.TclError:
            pass

        # Shut down Pygame
        pygame.quit()


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    root = tk.Tk()

    app = LyricFloatApp(root)

    root.mainloop()