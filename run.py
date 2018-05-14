#!/usr/bin/env python3

from phtest import app

def main():
    app.run(debug=True, use_reloader=True)

if __name__ == "__main__":
    main()
