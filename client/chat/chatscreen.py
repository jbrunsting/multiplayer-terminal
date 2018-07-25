import curses
import threading

class ChatScreen:
    def __init__(self, stdscr):
        self.lock = threading.Lock()
        self.stdscr = stdscr
        self.messages = []
        self.current_input = ""
        self.current_prompt = ""
        self.refresh()

    def add_message(self, message):
        with self.lock:
            self.messages.append(message)
        self.refresh()

    def refresh(self):
        self.stdscr.clear()
        with self.lock:
            for message in self.messages:
                self.stdscr.addstr(message)
                y,x = self.stdscr.getyx()
                self.stdscr.move(y + 1, 0)
        self.stdscr.addstr("")
        self.stdscr.addstr(self.current_prompt)
        self.stdscr.addstr(self.current_input)
        self.stdscr.refresh()

    def set_prompt(self, prompt):
        self.current_prompt = prompt

    def accept_input(self, message, on_input):
        self.on_input = on_input
        thread = threading.Thread(target = self.listen_for_input, args = (message,))
        thread.start()

    def listen_for_input(self, message):
        self.current_prompt = message
        while True:
            self.current_input = ""
            self.refresh()
            c = self.stdscr.getch()
            while c != curses.KEY_ENTER and c != 10 and c != 13:
                self.current_input += chr(c)
                self.refresh()
                c = self.stdscr.getch()
            result = self.current_input
            self.current_input = ""
            self.refresh()
            self.on_input(result)
