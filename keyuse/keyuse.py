import os
import keyuse.pyxhook as pyxhook
import json
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

DATA = {}

CANCEL = 'grave'

JOIN = True

def on_key_press(event):
    global DATA, CANCEL, JOIN
    if event.Key == CANCEL or event.Ascii == CANCEL:
        if JOIN is True and os.path.isfile('keys.json'):
            new = {}
            with open('keys.json', 'r') as file:
                new = json.load(file)
            for key, value in new.items():
                if key in DATA:
                    DATA[key][1] += value[1]
                else:
                    DATA[key] = value
        with open('keys.json', 'w') as file:
            json.dump(DATA, file)
        sys.exit(1)
    if event.Key in DATA:
        DATA[event.Key][1] += 1
    else:
        DATA[event.Key] = [event.Ascii, 1]

def logger(args):
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = on_key_press
    new_hook.HookKeyboard()
    try:
        new_hook.start()
    except :
        print("EXIT")

def plot(args):
    global DATA
    with open(args.file, 'r') as file:
        DATA = json.load(file)
    values = [x[1] for _, x in DATA.items()]
    name = [chr(x[0]) if x[0] != 0 else _ for _, x in DATA.items()]
    cap = max(values)
    colors = []
    for x in values:
        r = 0.0
        g = 1.0 - (x / cap)
        b = x / cap
        colors.append((r,g,b))
    plt.bar(np.arange(len(values)), values, color=colors)
    plt.xticks(np.arange(len(values)), name)
    plt.show()

def data(args):
    global DATA
    with open(args.file, 'r') as file:
        DATA = json.load(file)
    values = [x[1] for _, x in DATA.items()]
    name = [chr(x[0]) if x[0] != 0 else _ for _, x in DATA.items()]
    name_len = len(max(name))
    for i, name in enumerate(name):
        print("{:{}}:{}".format(name, name_len, values[i]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices={'logger', 'plot', 'list'})
    parser.add_argument('cancel', nargs='?', default='grave')
    parser.add_argument('file', nargs='?', default='keys.json')
    parser.add_argument('--no-join', action='store_false')
    args = parser.parse_args()
    global CANCEL
    CANCEL = args.cancel
    if args.action == 'logger':
        logger(args)
    elif args.action == 'plot':
        plot(args)
    elif args.action == 'list':
        data(args)


if __name__ == "__main__":
    main()
