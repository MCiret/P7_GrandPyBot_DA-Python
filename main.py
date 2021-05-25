#!/usr/bin/env python3

from app import app
from app.grandpy_bot import GrandpyBot

if __name__ == '__main__':
    print(GrandpyBot.answer("22 rue sainte careme france"))
    #app.run(debug=True)
