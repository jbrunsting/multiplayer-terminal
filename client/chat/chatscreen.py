import curses

class ChatScreen:
    def show(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        self.refresh()

    def refresh(self):
        self.stdscr.clear()
        for message in self.messages:
            print(message)

    def hide(self):
        curses.endwin()
