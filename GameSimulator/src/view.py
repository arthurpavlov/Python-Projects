# Assignment 2 - Puzzle Platform
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
""" Assignment 2 - View classes

This module contains three classes responsible for displaying information
to the user and reacting to user actions.

Note that these views behave independently of which puzzle is being played,
and so the allowable user inputs (e.g., ':SOLVE') cannot depend on the
particular puzzle, either.

You should *not* change this file.
"""
# Extra imports to run a web-based view
import http.server
import socketserver
from urllib.parse import parse_qs, urlparse


class View:
    """Abstract class representing the view of a puzzle game.

    Responsible for displaying state to the user and interpreting user input.
    """
    # === Private attributes ===
    # @type _controller: Controller
    #     The associated controller that interprets actions sent by the view.

    def __init__(self, controller):
        """Create a new view.

        @type self: View
        @type controller: Controller
        @rtype: None
        """
        self._controller = controller

    def run(self):
        """Start the game.

        This is the method which is called to begin interacting with the user.

        @type self: View
        @rtype: None
        """
        raise NotImplementedError()


class TextView(View):
    """View implementation based on console interaction.

    Uses 'print' and 'input' to display information and get actions.
    """
    # === Private attributes ===
    # @type _welcome: str
    #     A message to be printed to the user when the game begins.
    # @type _goodbye: str
    #     A message to be printed to the user when the game ends.
    def __init__(self, controller):
        View.__init__(self, controller)
        self._welcome = 'Welcome to the puzzle game!'
        self._goodbye = 'Hope you had fun playing!'

    def run(self):
        print(self._welcome)
        print(self._controller.state())
        while True:
            print('Enter a command:')
            user_input = input('> ')
            msg, should_quit = self._controller.act(user_input.strip())
            print(msg)
            if should_quit:
                break
        print(self._goodbye)


# ----------------------------------------------------------------------------
# Web view. You are *NOT* responsible for understanding this code.
# ----------------------------------------------------------------------------
class WebView(View):
    """Web implementation of a game view.

    Here is how to run this view:

    1. In the "if __name__ == '__main__'" block for controller.py,
       call the constructor with a second argument 'web'.
    2. Run the program.
    3. Open a web browser, and type in 'localhost:8000' in the URL bar.
    4. Enjoy!

    You aren't responsible for understanding this code, but you might have
    some fun looking into how to modify the file 'game.html' to make the
    webpage look more attractive.
    """
    def __init__(self, controller):
        View.__init__(self, controller)

    def run(self):
        """Start the game with a web view."""
        thisview = self

        class GameRequestHandler(http.server.BaseHTTPRequestHandler):
            """Implementation of basic HTTP request handler for game view.

            This exists as an inner class because I wanted to reference self
            in a method here, but had to pass in the class to TCPServer below.
            """
            done = False

            def do_GET(self):
                """Overridden method for handling GET requests."""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if 'actions' in self.path:
                    query_params = parse_qs(urlparse(self.path).query)
                    action = query_params.get('action', [''])[0]
                    val = self.handle_action(action).replace('\n', '<br>')
                    self.wfile.write(bytes(val, 'UTF-8'))
                else:
                    with open('game.html') as f:
                        self.wfile.write(bytes(f.read(), 'UTF-8'))

            def handle_action(self, action):
                """Helper which calls controller actions based on query param.

                @type self: GameRequestHandler
                @type action: str
                @rtype: str
                """
                print(GameRequestHandler.done)
                if not GameRequestHandler.done:
                    msg, should_quit = thisview._controller.act(action.strip())
                    GameRequestHandler.done = should_quit
                    return msg
                else:
                    return ''

        httpd = socketserver.TCPServer(('', 8000), GameRequestHandler)
        print('Server running!')
        print('Open a web browser and go to "http://localhost:8000"')
        httpd.serve_forever()
