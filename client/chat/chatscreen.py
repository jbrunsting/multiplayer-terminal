import curses

class ChatScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.messages = []
        self.current_input = ""
        self.current_prompt = ""
        self.refresh()

    def add_message(self, message):
        self.messages.append(message)
        self.refresh()

    def refresh(self):
        self.stdscr.clear()
        for message in self.messages:
            self.stdscr.addstr(message)
        self.stdscr.addstr("")
        self.stdscr.addstr(self.current_prompt)
        self.stdscr.addstr(self.current_input)
        self.stdscr.refresh()

    async def get_input(self, message):
        self.current_prompt = message
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
        return result
