#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:43:14 2020

@author: david
"""

from bs4 import BeautifulSoup
import requests as rq
from datetime import datetime
import pandas as pd
import numpy as np

url = 'https://www.basketball-reference.com/teams/HOU/2019.html'

agent = {'User-Agent': 'Mozilla/5.0'}

url_text = rq.get(url, headers=agent).text

soup = BeautifulSoup(url_text, 'html.parser')



##################################################################################
# Roster Table
##################################################################################

roster_table = soup.find('table', attrs={'id': 'roster'})

roster_col_names = ['Number', 'Player', 'Pos', 'Height', 'Weight', 'BirthDate', 'BirthCountry', 'YearsExperience', 'College']

player_number = []
player_name = []
player_pos = []
player_height = []
player_weight = []
player_birth_date = []
player_birth_country = []
player_years_exp = []
player_college = []


for th in roster_table.find_all('th', attrs={'data-stat': 'number', 'scope': 'row'}):
    player_number.append(int(th.text))
    
for td in roster_table.find_all('td'):
    
    if td['data-stat'] == 'player':
        player_name.append(td.text)
    
    elif td['data-stat'] == 'pos':
        player_pos.append(td.text)
    
    elif td['data-stat'] == 'height':
        ht = td.text.split('-')
        ft = int(ht[0]) * 12
        inch = int(ht[1])
        player_height.append(ft + inch)
    
    elif td['data-stat'] == 'weight':
        player_weight.append(int(td.text))
    
    elif td['data-stat'] == 'birth_date':
        player_birth_date.append(datetime.strptime(td.text, '%B %d, %Y').date())
        
    elif td['data-stat'] == 'birth_country':
        player_birth_country.append(td.text)
    
    elif td['data-stat'] == 'years_experience':
        if td.text == 'R':
            player_years_exp.append(0)
        else:
            player_years_exp.append(int(td.text))
        
    elif td['data-stat'] == 'college':
        player_college.append(td.text)

roster_dict = {'Number': player_number, 'Player': player_name, 'Pos': player_pos, \
               'Height': player_height, 'Weight': player_weight, 'BirthDate': player_birth_date, \
                   'BirthCountry': player_birth_country, 'YearsExperience': player_years_exp, 'College': player_college}

roster_df = pd.DataFrame(roster_dict)

roster_df.to_excel('/home/david/python_files/nba_stats/rockets_roster.xlsx', index=False)

#########################################################################################
# Per game table
#########################################################################################

per_game = soup.find('div', attrs={'id': 'all_per_game'})

per_game_table = BeautifulSoup(per_game.contents[5], 'lxml')

per_game_col_names = ['Rank', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', \
                      '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', \
                          'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', \
                              'BLK', 'TOV', 'PF', 'PTSpG']

    
per_game_rank = []
per_game_player = []
per_game_age = []
per_game_g = []
per_game_gs = []
per_game_mp = []
per_game_fg = []
per_game_fga = []
per_game_fgperc = []
per_game_3p = []
per_game_3pa = []
per_game_3pperc = []
per_game_2p = []
per_game_2pa = []
per_game_2pperc = []
per_game_efgperc = []
per_game_ft = []
per_game_fta = []
per_game_ftperc = []
per_game_orb = []
per_game_drb = []
per_game_trb = []
per_game_ast = []
per_game_stl = []
per_game_blk = []
per_game_tov = []
per_game_pf = []
per_game_ptspg = []

for th in per_game_table.find_all('th', attrs={'scope': 'row', 'data-stat': 'ranker'}):
    per_game_rank.append(int(th.text))

for td in per_game_table.find_all('td'):
    if td['data-stat'] == 'player':
            per_game_player.append(td.text)

    elif td['data-stat'] == 'age':
        try:
            per_game_age.append(int(td.text))
        except:
            per_game_age.append(np.NaN)
        
    elif td['data-stat'] == 'g':
        try:
            per_game_g.append(int(td.text))
        except:
            per_game_g.append(np.NaN)            
    
    elif td['data-stat'] == 'gs':
        try:
            per_game_gs.append(int(td.text))
        except:
            per_game_gs.append(np.NaN)
            
    elif td['data-stat'] == 'mp_per_g':
        try:
            per_game_mp.append(float(td.text))
        except:
            per_game_mp.append(np.NaN)
            
    elif td['data-stat'] == 'fg_per_g':
        try:
            per_game_fg.append(float(td.text))
        except:
            per_game_fg.append(np.NaN)

    elif td['data-stat'] == 'fga_per_g':
        try:
            per_game_fga.append(float(td.text))
        except:
            per_game_fga.append(np.NaN)
            
    elif td['data-stat'] == 'fg_pct':
        try:
            per_game_fgperc.append(float(td.text))
        except:
            per_game_fgperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_per_g':
        try:
            per_game_3p.append(float(td.text))
        except:
            per_game_3p.append(np.NaN)
            
    elif td['data-stat'] == 'fg3a_per_g':
        try:
            per_game_3pa.append(float(td.text))
        except:
            per_game_3pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_pct':
        try:
            per_game_3pperc.append(float(td.text))
        except:
            per_game_3pperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_per_g':
        try:
            per_game_2p.append(float(td.text))
        except:
            per_game_2p.append(np.NaN)
            
    elif td['data-stat'] == 'fg2a_per_g':
        try:
            per_game_2pa.append(float(td.text))
        except:
            per_game_2pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_pct':
        try:
            per_game_2pperc.append(float(td.text))
        except:
            per_game_2pperc.append(np.NaN)
            
    elif td['data-stat'] == 'efg_pct':
        try:
            per_game_efgperc.append(float(td.text))
        except:
            per_game_efgperc.append(np.NaN)
            
    elif td['data-stat'] == 'ft_per_g':
        try:
            per_game_ft.append(float(td.text))
        except:
            per_game_ft.append(np.NaN)
            
    elif td['data-stat'] == 'fta_per_g':
        try:
            per_game_fta.append(float(td.text))
        except:
            per_game_fta.append(np.NaN)
            
    elif td['data-stat'] == 'ft_pct':
        try:
            per_game_ftperc.append(float(td.text))
        except:
            per_game_ftperc.append(np.NaN)
            
    elif td['data-stat'] == 'orb_per_g':
        try:
            per_game_orb.append(float(td.text))
        except:
            per_game_orb.append(np.NaN)
            
    elif td['data-stat'] == 'drb_per_g':
        try:
            per_game_drb.append(float(td.text))
        except:
            per_game_drb.append(np.NaN)
            
    elif td['data-stat'] == 'trb_per_g':
        try:
            per_game_trb.append(float(td.text))
        except:
            per_game_trb.append(np.NaN)
            
    elif td['data-stat'] == 'ast_per_g':
        try:
            per_game_ast.append(float(td.text))
        except:
            per_game_ast.append(np.NaN)
            
    elif td['data-stat'] == 'stl_per_g':
        try:
            per_game_stl.append(float(td.text))
        except:
            per_game_stl.append(np.NaN)
            
    elif td['data-stat'] == 'blk_per_g':
        try:
            per_game_blk.append(float(td.text))
        except:
            per_game_blk.append(np.NaN)
            
    elif td['data-stat'] == 'tov_per_g':
        try:
            per_game_tov.append(float(td.text))
        except:
            per_game_tov.append(np.NaN)
            
    elif td['data-stat'] == 'pf_per_g':
        try:
            per_game_pf.append(float(td.text))
        except:
            per_game_pf.append(np.NaN)
            
    elif td['data-stat'] == 'pts_per_g':
        try:
            per_game_ptspg.append(float(td.text))
        except:
            per_game_ptspg.append(np.NaN)        
        
    
per_game_dict = {'Rank': per_game_rank, 'Player': per_game_player, 'Age': per_game_age, \
                 'G': per_game_g, 'GS': per_game_gs, 'MP': per_game_mp, 'FG': per_game_fg, \
                     'FGA': per_game_fga, 'FG%': per_game_fgperc, '3P': per_game_3p, \
                         '3PA': per_game_3pa, '3P%': per_game_3pperc, '2P': per_game_2p, \
                             '2PA': per_game_2pa, '2P%': per_game_2pperc, 'eFG%': per_game_efgperc, \
                                 'FT': per_game_ft, 'FTA': per_game_fta, 'FT%': per_game_ftperc, 'ORB': per_game_orb, \
                                     'DRB': per_game_drb, 'TRB': per_game_trb, 'AST': per_game_ast, 'STL': per_game_stl, \
                                     'BLK': per_game_blk, 'TOV': per_game_tov, 'PF': per_game_pf, 'PTSpG': per_game_ptspg}
    
per_game_df = pd.DataFrame(per_game_dict)

per_game_df.to_excel('/home/david/python_files/nba_stats/rockets_per_game.xlsx', index=False)

##################################################################################################
# Totals Table
##################################################################################################

all_totals = soup.find('div', attrs={'id': 'all_totals'})

all_totals_table = BeautifulSoup(per_game.contents[5], 'lxml')

all_totals_col_names = ['Rank', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', \
                      '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', \
                          'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', \
                              'BLK', 'TOV', 'PF', 'PTSpG']

    
all_totals_rank = []
all_totals_player = []
all_totals_age = []
all_totals_g = []
all_totals_gs = []
all_totals_mp = []
all_totals_fg = []
all_totals_fga = []
all_totals_fgperc = []
all_totals_3p = []
all_totals_3pa = []
all_totals_3pperc = []
all_totals_2p = []
all_totals_2pa = []
all_totals_2pperc = []
all_totals_efgperc = []
all_totals_ft = []
all_totals_fta = []
all_totals_ftperc = []
all_totals_orb = []
all_totals_drb = []
all_totals_trb = []
all_totals_ast = []
all_totals_stl = []
all_totals_blk = []
all_totals_tov = []
all_totals_pf = []
all_totals_ptspg = []

for th in all_totals_table.find_all('th', attrs={'scope': 'row', 'data-stat': 'ranker'}):
    all_totals_rank.append(int(th.text))

for td in all_totals_table.find_all('td'):
    if td['data-stat'] == 'player':
            all_totals_player.append(td.text)

    elif td['data-stat'] == 'age':
        try:
            all_totals_age.append(int(td.text))
        except:
            all_totals_age.append(np.NaN)
        
    elif td['data-stat'] == 'g':
        try:
            all_totals_g.append(int(td.text))
        except:
            all_totals_g.append(np.NaN)            
    
    elif td['data-stat'] == 'gs':
        try:
            all_totals_gs.append(int(td.text))
        except:
            all_totals_gs.append(np.NaN)
            
    elif td['data-stat'] == 'mp_per_g':
        try:
            all_totals_mp.append(float(td.text))
        except:
            all_totals_mp.append(np.NaN)
            
    elif td['data-stat'] == 'fg_per_g':
        try:
            all_totals_fg.append(float(td.text))
        except:
            all_totals_fg.append(np.NaN)

    elif td['data-stat'] == 'fga_per_g':
        try:
            all_totals_fga.append(float(td.text))
        except:
            all_totals_fga.append(np.NaN)
            
    elif td['data-stat'] == 'fg_pct':
        try:
            all_totals_fgperc.append(float(td.text))
        except:
            all_totals_fgperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_per_g':
        try:
            all_totals_3p.append(float(td.text))
        except:
            all_totals_3p.append(np.NaN)
            
    elif td['data-stat'] == 'fg3a_per_g':
        try:
            all_totals_3pa.append(float(td.text))
        except:
            all_totals_3pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_pct':
        try:
            all_totals_3pperc.append(float(td.text))
        except:
            all_totals_3pperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_per_g':
        try:
            all_totals_2p.append(float(td.text))
        except:
            all_totals_2p.append(np.NaN)
            
    elif td['data-stat'] == 'fg2a_per_g':
        try:
            all_totals_2pa.append(float(td.text))
        except:
            all_totals_2pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_pct':
        try:
            all_totals_2pperc.append(float(td.text))
        except:
            all_totals_2pperc.append(np.NaN)
            
    elif td['data-stat'] == 'efg_pct':
        try:
            all_totals_efgperc.append(float(td.text))
        except:
            all_totals_efgperc.append(np.NaN)
            
    elif td['data-stat'] == 'ft_per_g':
        try:
            all_totals_ft.append(float(td.text))
        except:
            all_totals_ft.append(np.NaN)
            
    elif td['data-stat'] == 'fta_per_g':
        try:
            all_totals_fta.append(float(td.text))
        except:
            all_totals_fta.append(np.NaN)
            
    elif td['data-stat'] == 'ft_pct':
        try:
            all_totals_ftperc.append(float(td.text))
        except:
            all_totals_ftperc.append(np.NaN)
            
    elif td['data-stat'] == 'orb_per_g':
        try:
            all_totals_orb.append(float(td.text))
        except:
            all_totals_orb.append(np.NaN)
            
    elif td['data-stat'] == 'drb_per_g':
        try:
            all_totals_drb.append(float(td.text))
        except:
            all_totals_drb.append(np.NaN)
            
    elif td['data-stat'] == 'trb_per_g':
        try:
            all_totals_trb.append(float(td.text))
        except:
            all_totals_trb.append(np.NaN)
            
    elif td['data-stat'] == 'ast_per_g':
        try:
            all_totals_ast.append(float(td.text))
        except:
            all_totals_ast.append(np.NaN)
            
    elif td['data-stat'] == 'stl_per_g':
        try:
            all_totals_stl.append(float(td.text))
        except:
            all_totals_stl.append(np.NaN)
            
    elif td['data-stat'] == 'blk_per_g':
        try:
            all_totals_blk.append(float(td.text))
        except:
            all_totals_blk.append(np.NaN)
            
    elif td['data-stat'] == 'tov_per_g':
        try:
            all_totals_tov.append(float(td.text))
        except:
            all_totals_tov.append(np.NaN)
            
    elif td['data-stat'] == 'pf_per_g':
        try:
            all_totals_pf.append(float(td.text))
        except:
            all_totals_pf.append(np.NaN)
            
    elif td['data-stat'] == 'pts_per_g':
        try:
            all_totals_ptspg.append(float(td.text))
        except:
            all_totals_ptspg.append(np.NaN)        
        
    
all_totals_dict = {'Rank': all_totals_rank, 'Player': all_totals_player, 'Age': all_totals_age, \
                 'G': all_totals_g, 'GS': all_totals_gs, 'MP': all_totals_mp, 'FG': all_totals_fg, \
                     'FGA': all_totals_fga, 'FG%': all_totals_fgperc, '3P': all_totals_3p, \
                         '3PA': all_totals_3pa, '3P%': all_totals_3pperc, '2P': all_totals_2p, \
                             '2PA': all_totals_2pa, '2P%': all_totals_2pperc, 'eFG%': all_totals_efgperc, \
                                 'FT': all_totals_ft, 'FTA': all_totals_fta, 'FT%': all_totals_ftperc, 'ORB': all_totals_orb, \
                                     'DRB': all_totals_drb, 'TRB': all_totals_trb, 'AST': all_totals_ast, 'STL': all_totals_stl, \
                                     'BLK': all_totals_blk, 'TOV': all_totals_tov, 'PF': all_totals_pf, 'PTSpG': all_totals_ptspg}
    
all_totals_df = pd.DataFrame(all_totals_dict)

all_totals_df.to_excel('/home/david/python_files/nba_stats/rockets_all_totals.xlsx', index=False)


##################################################################################################
# Per 36 Minutes Table
##################################################################################################

per_36_mins_text = soup.find('div', attrs={'id': 'all_per_minute'})

per_36_mins_table = BeautifulSoup(per_36_mins_text.contents[5], 'lxml')

per_36_mins_col_names = ['Rank', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', \
                      '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', \
                          'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', \
                              'BLK', 'TOV', 'PF', 'PTSpG']

    
per_36_mins_rank = []
per_36_mins_player = []
per_36_mins_age = []
per_36_mins_g = []
per_36_mins_gs = []
per_36_mins_mp = []
per_36_mins_fg = []
per_36_mins_fga = []
per_36_mins_fgperc = []
per_36_mins_3p = []
per_36_mins_3pa = []
per_36_mins_3pperc = []
per_36_mins_2p = []
per_36_mins_2pa = []
per_36_mins_2pperc = []
per_36_mins_ft = []
per_36_mins_fta = []
per_36_mins_ftperc = []
per_36_mins_orb = []
per_36_mins_drb = []
per_36_mins_trb = []
per_36_mins_ast = []
per_36_mins_stl = []
per_36_mins_blk = []
per_36_mins_tov = []
per_36_mins_pf = []
per_36_mins_ptspg = []

for th in per_36_mins_table.find_all('th', attrs={'scope': 'row', 'data-stat': 'ranker'}):
    per_36_mins_rank.append(int(th.text))

for td in per_36_mins_table.find_all('td'):
    if td['data-stat'] == 'player':
            per_36_mins_player.append(td.text)

    elif td['data-stat'] == 'age':
        try:
            per_36_mins_age.append(int(td.text))
        except:
            per_36_mins_age.append(np.NaN)
        
    elif td['data-stat'] == 'g':
        try:
            per_36_mins_g.append(int(td.text))
        except:
            per_36_mins_g.append(np.NaN)            
    
    elif td['data-stat'] == 'gs':
        try:
            per_36_mins_gs.append(int(td.text))
        except:
            per_36_mins_gs.append(np.NaN)
            
    elif td['data-stat'] == 'mp':
        try:
            per_36_mins_mp.append(float(td.text))
        except:
            per_36_mins_mp.append(np.NaN)
            
    elif td['data-stat'] == 'fg_per_mp':
        try:
            per_36_mins_fg.append(float(td.text))
        except:
            per_36_mins_fg.append(np.NaN)

    elif td['data-stat'] == 'fga_per_mp':
        try:
            per_36_mins_fga.append(float(td.text))
        except:
            per_36_mins_fga.append(np.NaN)
            
    elif td['data-stat'] == 'fg_pct':
        try:
            per_36_mins_fgperc.append(float(td.text))
        except:
            per_36_mins_fgperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_per_mp':
        try:
            per_36_mins_3p.append(float(td.text))
        except:
            per_36_mins_3p.append(np.NaN)
            
    elif td['data-stat'] == 'fg3a_per_mp':
        try:
            per_36_mins_3pa.append(float(td.text))
        except:
            per_36_mins_3pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_pct':
        try:
            per_36_mins_3pperc.append(float(td.text))
        except:
            per_36_mins_3pperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_per_mp':
        try:
            per_36_mins_2p.append(float(td.text))
        except:
            per_36_mins_2p.append(np.NaN)
            
    elif td['data-stat'] == 'fg2a_per_mp':
        try:
            per_36_mins_2pa.append(float(td.text))
        except:
            per_36_mins_2pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_pct':
        try:
            per_36_mins_2pperc.append(float(td.text))
        except:
            per_36_mins_2pperc.append(np.NaN)
            
    elif td['data-stat'] == 'ft_per_mp':
        try:
            per_36_mins_ft.append(float(td.text))
        except:
            per_36_mins_ft.append(np.NaN)
            
    elif td['data-stat'] == 'fta_per_mp':
        try:
            per_36_mins_fta.append(float(td.text))
        except:
            per_36_mins_fta.append(np.NaN)
            
    elif td['data-stat'] == 'ft_pct':
        try:
            per_36_mins_ftperc.append(float(td.text))
        except:
            per_36_mins_ftperc.append(np.NaN)
            
    elif td['data-stat'] == 'orb_per_mp':
        try:
            per_36_mins_orb.append(float(td.text))
        except:
            per_36_mins_orb.append(np.NaN)
            
    elif td['data-stat'] == 'drb_per_mp':
        try:
            per_36_mins_drb.append(float(td.text))
        except:
            per_36_mins_drb.append(np.NaN)
            
    elif td['data-stat'] == 'trb_per_mp':
        try:
            per_36_mins_trb.append(float(td.text))
        except:
            per_36_mins_trb.append(np.NaN)
            
    elif td['data-stat'] == 'ast_per_mp':
        try:
            per_36_mins_ast.append(float(td.text))
        except:
            per_36_mins_ast.append(np.NaN)
            
    elif td['data-stat'] == 'stl_per_mp':
        try:
            per_36_mins_stl.append(float(td.text))
        except:
            per_36_mins_stl.append(np.NaN)
            
    elif td['data-stat'] == 'blk_per_mp':
        try:
            per_36_mins_blk.append(float(td.text))
        except:
            per_36_mins_blk.append(np.NaN)
            
    elif td['data-stat'] == 'tov_per_mp':
        try:
            per_36_mins_tov.append(float(td.text))
        except:
            per_36_mins_tov.append(np.NaN)
            
    elif td['data-stat'] == 'pf_per_mp':
        try:
            per_36_mins_pf.append(float(td.text))
        except:
            per_36_mins_pf.append(np.NaN)
            
    elif td['data-stat'] == 'pts_per_mp':
        try:
            per_36_mins_ptspg.append(float(td.text))
        except:
            per_36_mins_ptspg.append(np.NaN)        
        
    
per_36_mins_dict = {'Rank': per_36_mins_rank, 'Player': per_36_mins_player, 'Age': per_36_mins_age, \
                 'G': per_36_mins_g, 'GS': per_36_mins_gs, 'MP': per_36_mins_mp, 'FG': per_36_mins_fg, \
                     'FGA': per_36_mins_fga, 'FG%': per_36_mins_fgperc, '3P': per_36_mins_3p, \
                         '3PA': per_36_mins_3pa, '3P%': per_36_mins_3pperc, '2P': per_36_mins_2p, \
                             '2PA': per_36_mins_2pa, '2P%': per_36_mins_2pperc,\
                                 'FT': per_36_mins_ft, 'FTA': per_36_mins_fta, 'FT%': per_36_mins_ftperc, 'ORB': per_36_mins_orb, \
                                     'DRB': per_36_mins_drb, 'TRB': per_36_mins_trb, 'AST': per_36_mins_ast, 'STL': per_36_mins_stl, \
                                     'BLK': per_36_mins_blk, 'TOV': per_36_mins_tov, 'PF': per_36_mins_pf, 'PTSpG': per_36_mins_ptspg}
    
per_36_mins_df = pd.DataFrame(per_36_mins_dict)

per_36_mins_df.to_excel('/home/david/python_files/nba_stats/rockets_36_mins.xlsx', index=False)

##################################################################################################
# Per 100 Poss Table
##################################################################################################

per_100_poss = soup.find('div', attrs={'id': 'all_per_poss'})

per_100_poss_table = BeautifulSoup(per_100_poss.contents[5], 'lxml')

per_100_poss_col_names = ['Rank', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', \
                      '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', \
                          'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', \
                              'BLK', 'TOV', 'PF', 'PTSpG', 'ORtg', 'DRtg']

    
per_100_poss_rank = []
per_100_poss_player = []
per_100_poss_age = []
per_100_poss_g = []
per_100_poss_gs = []
per_100_poss_mp = []
per_100_poss_fg = []
per_100_poss_fga = []
per_100_poss_fgperc = []
per_100_poss_3p = []
per_100_poss_3pa = []
per_100_poss_3pperc = []
per_100_poss_2p = []
per_100_poss_2pa = []
per_100_poss_2pperc = []
per_100_poss_ft = []
per_100_poss_fta = []
per_100_poss_ftperc = []
per_100_poss_orb = []
per_100_poss_drb = []
per_100_poss_trb = []
per_100_poss_ast = []
per_100_poss_stl = []
per_100_poss_blk = []
per_100_poss_tov = []
per_100_poss_pf = []
per_100_poss_ptspg = []
per_100_poss_ortg = []
per_100_poss_drtg = []

for th in per_100_poss_table.find_all('th', attrs={'scope': 'row', 'data-stat': 'ranker'}):
    per_100_poss_rank.append(int(th.text))

for td in per_100_poss_table.find_all('td'):
    if td['data-stat'] == 'player':
            per_100_poss_player.append(td.text)

    elif td['data-stat'] == 'age':
        try:
            per_100_poss_age.append(int(td.text))
        except:
            per_100_poss_age.append(np.NaN)
        
    elif td['data-stat'] == 'g':
        try:
            per_100_poss_g.append(int(td.text))
        except:
            per_100_poss_g.append(np.NaN)            
    
    elif td['data-stat'] == 'gs':
        try:
            per_100_poss_gs.append(int(td.text))
        except:
            per_100_poss_gs.append(np.NaN)
            
    elif td['data-stat'] == 'mp':
        try:
            per_100_poss_mp.append(float(td.text))
        except:
            per_100_poss_mp.append(np.NaN)
            
    elif td['data-stat'] == 'fg_per_poss':
        try:
            per_100_poss_fg.append(float(td.text))
        except:
            per_100_poss_fg.append(np.NaN)

    elif td['data-stat'] == 'fga_per_poss':
        try:
            per_100_poss_fga.append(float(td.text))
        except:
            per_100_poss_fga.append(np.NaN)
            
    elif td['data-stat'] == 'fg_pct':
        try:
            per_100_poss_fgperc.append(float(td.text))
        except:
            per_100_poss_fgperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_per_poss':
        try:
            per_100_poss_3p.append(float(td.text))
        except:
            per_100_poss_3p.append(np.NaN)
            
    elif td['data-stat'] == 'fg3a_per_poss':
        try:
            per_100_poss_3pa.append(float(td.text))
        except:
            per_100_poss_3pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg3_pct':
        try:
            per_100_poss_3pperc.append(float(td.text))
        except:
            per_100_poss_3pperc.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_per_poss':
        try:
            per_100_poss_2p.append(float(td.text))
        except:
            per_100_poss_2p.append(np.NaN)
            
    elif td['data-stat'] == 'fg2a_per_poss':
        try:
            per_100_poss_2pa.append(float(td.text))
        except:
            per_100_poss_2pa.append(np.NaN)
            
    elif td['data-stat'] == 'fg2_pct':
        try:
            per_100_poss_2pperc.append(float(td.text))
        except:
            per_100_poss_2pperc.append(np.NaN)
            
    elif td['data-stat'] == 'ft_per_poss':
        try:
            per_100_poss_ft.append(float(td.text))
        except:
            per_100_poss_ft.append(np.NaN)
            
    elif td['data-stat'] == 'fta_per_poss':
        try:
            per_100_poss_fta.append(float(td.text))
        except:
            per_100_poss_fta.append(np.NaN)
            
    elif td['data-stat'] == 'ft_pct':
        try:
            per_100_poss_ftperc.append(float(td.text))
        except:
            per_100_poss_ftperc.append(np.NaN)
            
    elif td['data-stat'] == 'orb_per_poss':
        try:
            per_100_poss_orb.append(float(td.text))
        except:
            per_100_poss_orb.append(np.NaN)
            
    elif td['data-stat'] == 'drb_per_poss':
        try:
            per_100_poss_drb.append(float(td.text))
        except:
            per_100_poss_drb.append(np.NaN)
            
    elif td['data-stat'] == 'trb_per_poss':
        try:
            per_100_poss_trb.append(float(td.text))
        except:
            per_100_poss_trb.append(np.NaN)
            
    elif td['data-stat'] == 'ast_per_poss':
        try:
            per_100_poss_ast.append(float(td.text))
        except:
            per_100_poss_ast.append(np.NaN)
            
    elif td['data-stat'] == 'stl_per_poss':
        try:
            per_100_poss_stl.append(float(td.text))
        except:
            per_100_poss_stl.append(np.NaN)
            
    elif td['data-stat'] == 'blk_per_poss':
        try:
            per_100_poss_blk.append(float(td.text))
        except:
            per_100_poss_blk.append(np.NaN)
            
    elif td['data-stat'] == 'tov_per_poss':
        try:
            per_100_poss_tov.append(float(td.text))
        except:
            per_100_poss_tov.append(np.NaN)
            
    elif td['data-stat'] == 'pf_per_poss':
        try:
            per_100_poss_pf.append(float(td.text))
        except:
            per_100_poss_pf.append(np.NaN)
            
    elif td['data-stat'] == 'pts_per_poss':
        try:
            per_100_poss_ptspg.append(float(td.text))
        except:
            per_100_poss_ptspg.append(np.NaN)        

    elif td['data-stat'] == 'off_rtg':
        try:
            per_100_poss_ortg.append(int(td.text))
        except:
            per_100_poss_ortg.append(np.NaN)
            
    elif td['data-stat'] == 'def_rtg':
        try:
            per_100_poss_drtg.append(int(td.text))
        except:
            per_100_poss_drtg.append(int(td.text))
    
per_100_poss_dict = {'Rank': per_100_poss_rank, 'Player': per_100_poss_player, 'Age': per_100_poss_age, \
                 'G': per_100_poss_g, 'GS': per_100_poss_gs, 'MP': per_100_poss_mp, 'FG': per_100_poss_fg, \
                     'FGA': per_100_poss_fga, 'FG%': per_100_poss_fgperc, '3P': per_100_poss_3p, \
                         '3PA': per_100_poss_3pa, '3P%': per_100_poss_3pperc, '2P': per_100_poss_2p, \
                             '2PA': per_100_poss_2pa, '2P%': per_100_poss_2pperc,\
                                 'FT': per_100_poss_ft, 'FTA': per_100_poss_fta, 'FT%': per_100_poss_ftperc, 'ORB': per_100_poss_orb, \
                                     'DRB': per_100_poss_drb, 'TRB': per_100_poss_trb, 'AST': per_100_poss_ast, 'STL': per_100_poss_stl, \
                                     'BLK': per_100_poss_blk, 'TOV': per_100_poss_tov, 'PF': per_100_poss_pf, 'PTSpG': per_100_poss_ptspg, \
                                         'ORtg': per_100_poss_ortg, 'DRtg': per_100_poss_drtg}
    
per_100_poss_df = pd.DataFrame(per_100_poss_dict)


per_100_poss_df.to_excel('/home/david/python_files/nba_stats/rockets_per_100.xlsx', index=False)







