# Dream Factory Buddy

## What is this?
The Battle Factory is a game mode in Pokemon Emerald where you as the player are given a choice of 6 pokemon to make a team of 3 out of. You then battle other trainers, being given the option to swap one of your pokemon for one of theirs after each win.

The player is given some very cryptic information before each battle, using that information and our knowledge of how the in-game AI works lets us narrow down what the opposing pokemon are capable of - this WebApp automates some of that process.

Check out this <a href="https://youtu.be/kMAyGfeFTOw?si=pB4kvKfc3yH6U0Py">video guide by LRXC</a> if you'd like to learn more about the factory.

This is a fork of the Battle Factory Buddy by DaveGlorbus, which is intended to work with the romhack Dream Factory, rather than the original Battle Factory. The GitHub Repo for Dream Factory can be found <a href="https://github.com/DisasterArea96/pokeemerald_dreamfactory">here</a>.

## Quick Start - First time setup for running on your own PC.
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
