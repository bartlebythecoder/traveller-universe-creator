# traveller-universe-creator
Build a SQLite database of Traveller systems using First In and T5 hybrid rules

Running traveller_master.py will produce:

- A text file of a full sector of mainworlds that can be loaded into travellermap.com for a custom booklet or poster
- A complete SQLite database of statted worlds for a sector including:
	- tb_stellar, tb_secondary, and tb_tertiary for star stats
	- tb_t5 for T5 stats of each mainworld
	- tb_non_mainworld for T5 stats for each non-mainworld
	- tb_orbital_bodies for First In stats for each orbital body
	- tb_far_trader for WTN, GWP, and exchange rate for each mainworld
