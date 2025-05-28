###
Batch run CIGALE simulations and generate corner plot - requires installation of CIGALE v2022.1
###

Dependencies: astropy, numpy, matplotlib

Hi!
This function runs as many CIGALE simulations as you want and plots (currently three) simulations against each other in a corner plot file.

- Run with python -m main.py (or environment equivalent using main.py)

- Edit main.py to add/remove pcigale.ini parses/CIGALE runs/chart generations

- Edit auto_sed.py to modify processing functions

- Edit ryder_graphing.py to view Ryder's xtreme graphing funcs

- Edit read_ini at your own peril

todo: 
streamline ini and graphing input
-create function for ini input template
-versatility for corner plot generation
