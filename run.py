#!/usr/bin/env python3

import os

from phtest import app

def main():
    app.secret_key = os.urandom(12)
    app.run(debug=True, use_reloader=True)

if __name__ == "__main__":
    main()
