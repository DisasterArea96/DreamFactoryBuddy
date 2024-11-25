# Battle Factory Buddy

## What is this?
The Battle Factory is a game mode in Pokemon Emerald where you as the player are given a choice of 6 pokemon to make a team of 3 out of. You then battle other trainers, being given the option to swap one of your pokemon for one of theirs after each win.

The player is given some very cryptic information before each battle, using that information and our knowledge of how the in-game AI works lets us narrow down what the opposing pokemon are capable of - this WebApp automates some of that process.

Check out this <a href="https://youtu.be/kMAyGfeFTOw?si=pB4kvKfc3yH6U0Py">video guide by LRXC</a> if you'd like to learn more about the factory.

## Quickest Start - Video guide on setup
<a href="https://youtu.be/fw08PYYXvaA">Battle Factory Buddy Setup Guide<a>

## Quick Start - First time setup for running on your own PC.
* Check you've got at least 400MB to spare on your hard disk. That's not a lot, but you'll be sad if you use it all.
* Download this repository as a ZIP file (click the Green Code button) and extract it somewhere on your PC.
* If you don't already have python. Go to <a href="https://www.python.org/downloads/">python.org<a> and download the latest version of python and install it (you'll probably want the Windows-64 bit installer when given a big list of things to download).
* Open file explorer and double click on setup. It should run for a few minutes and is done when you see `Starting development server`. If you don't see that (likely a black window flashes up and closes) then try running setuppython instead, which does the same thing in a slightly different way.
* Open your browser and `http://127.0.0.1:8000/`, you should see the main battle factory page.
* Close the Command prompt window when you're done.
 
## Quick Start - Restarting a server after setup has been done.
Next time just double click on `runserver` instead and go to the same place in your browser.

## Hosting the WebApp on the internet.
I only know how to do this in Azure, where the app needs a fairly beefy (like $40 a month) App service plan. You can do this by running `az login` with an existing Azure account and then running `az webapp up --runtime PYTHON:3.11 --sku B1 --logs`. You'll then probably need to go and tweak the plan in the Azure Portal.

However, this is a relatively run of the mill Django app, it should be very possible to host it elsewhere.

## Editing
See contributing.md for a bit about contributing to this project.
If you want to make an alternative version for custom versions of the factory then search the codebase for ALTSETS for some pointers.

## Acks / Shoutouts
Big thanks to everyone in the Emerald Battle Facilities and Battle Factory communities. Specific thanks to:
- LRXC for lighting the fire.
- Donlyphans and Xavion for their incredible work pulling together Factory resources.
- Turskain, Kaboissonneault and others who have maintained, hosted and contributed to forks of the damage calculator for facilities use.
- Everyone in The Bergg discord for being awesome. Notably (but not limited to) BPark, Nnico, Wildcat, Goomer, Tinto, Magpie, Scraf, Sespe, DisasterArea (sorry if I've missed you off and shouldn't have!)
- Roger Wrightshoe for providing all the data for the team builder by simulating a bajillion AI vs AI battles.