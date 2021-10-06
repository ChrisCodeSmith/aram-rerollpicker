# Aram Rerollpicker

This software is using pyscreeze to find occurances of LoL champions in the LoL Client. It is not harming the client or reading the memory. It just takes screenshots and compares them to a needleimage hold in the champions folder.

To add a champion, just create a folder named "champions" and copy your image into it.

## Problems

- At the moment this program only handles one champion in the folder and the selection for champs in the gui doesnt work yet. It only picks one champ therefore!
- At the moment it clicks infinitly if it sees your champ

## Todo:

- in order to enable more than one champ for your pick pool, we need to check which champ is selected, so if we already have Teemo(which is #1 in our pool), dont pick Singed(#2). -> locate region for picked champ ( use tip from Find gui regions )
- solve infinite clicking on champ. Half way solved when feature above is implemented. I.e. as soon as champ is selected, stop clicking

## Find gui regions with py

```
import pyscreeze
import pygetwindow

win = pgw.getWindowsWithTitle('League')[0]
win = (win.left, win.top, win.width-100, win.height)
img = pyscreeze.screenshot(region=win)
img.save(r"C:\YourPath\savedIMG.png")
```

use this and play with the region parameters e.g. subtract from win.width

remeber to have the window not minimized
