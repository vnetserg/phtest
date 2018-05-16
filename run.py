#!/usr/bin/env python3

import config
from phtest import app

def main():
    app.run(debug=config.DEBUG, use_reloader=config.DEBUG)

if __name__ == "__main__":
    main()
