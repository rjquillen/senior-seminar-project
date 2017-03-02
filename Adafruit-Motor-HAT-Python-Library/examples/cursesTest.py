import curses

stdscr=curses.initscr()

curses.cbreak()
print "q to wuit"
end=False

while not (end):
    c=stdscr.getch()
    print curses.keyname(c)
    if(curse.keyname=='q'):
        end=True
curses.endwin()
