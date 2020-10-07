#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bridge Hand Generator
Created on Mon Oct  5 00:08:03 2020

@author: edchen
"""

import numpy as np

# create 52 card deck
suits = ['S','H','D','C']
nums = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
cards = []
for i in range(len(suits)):
    for j in range(len(nums)):
        cards.append(suits[i]+nums[j])
len(cards)

# deal one hand
deal = np.random.choice(cards, size=52, replace=False)

# sort cards for one hand in suit_rank order
def card_order(a):
    shuffled = []
    for i in range(len(cards)):
        if cards[i] in set(a):
            shuffled.append(cards[i])
    return shuffled

# example: show one ordered hand
card_order(deal[0:13])

# sort dealt cards for one hand by suit
def display_hand(a):
    S, H, D, C = [],[],[],[]
    for i in range(len(a)):
        if a[i][0] == 'S':
            S.append(a[i][1])
        elif a[i][0] == 'H':
            H.append(a[i][1])
        elif a[i][0] == 'D':
            D.append(a[i][1])
        elif a[i][0] == 'C':
            C.append(a[i][1])
    return [S,H,D,C]

# example: show suit sorted hand
display_hand(card_order(deal[0:13]))

# deal number of hands passed as n
def deal_hand(n):
    # space variable for where to position East
    def tab_check(a):
        if len(East[a]) < 2:
            return '\t\t\t\t\t\t\t\t'
        elif len(East[a]) < 5:
            return '\t\t\t\t\t\t\t'
        elif len(East[a]) < 7:
            return '\t\t\t\t\t\t'
        elif len(East[a]) < 9:
            return '\t\t\t\t\t'
        elif len(East[a]) < 11:
            return '\t\t\t\t'
        else:
            return '\t\t\t'
    # choose dealer
    def dealer():
        return np.random.choice(['N','S','E','W'], size=1, replace=True)
    # choose vulnerability
    def vul():
        return np.random.choice(['N/S','E/W','None','Both'], size=1, replace=True)
    # deal hands
    for i in range(n):
        deal = np.random.choice(cards, size=52, replace=False)
        North = display_hand(card_order(deal[0:13]))
        South = display_hand(card_order(deal[13:26]))
        East = display_hand(card_order(deal[26:39]))
        West = display_hand(card_order(deal[39:52]))
        # if lists instantiated, store dealt hands for each direction
        try:
            All_North.append(North)
            All_South.append(South)
            All_East.append(East)
            All_West.append(West)
        except:
            pass
        # format and print out each hand for all directions
        print(i+1,'. Dealer:',dealer()[0],' Vulnerable:',vul()[0],'\r\n')
        print('\t\t\t\t','North','\r\n'
              '\t\t\t\t','S: ',', '.join(North[0]),'\r\n'
              '\t\t\t\t','H: ',', '.join(North[1]),'\r\n'
              '\t\t\t\t','D: ',', '.join(North[2]),'\r\n'
              '\t\t\t\t','C: ',', '.join(North[3]),'\r\n'
              'East','\t\t\t\t\t\t\t\t','West','\r\n'
              'S: ',', '.join(East[0]),tab_check(0),'S: ',', '.join(West[0]),'\r\n'
              'H: ',', '.join(East[1]),tab_check(1),'H: ',', '.join(West[1]),'\r\n'
              'D: ',', '.join(East[2]),tab_check(2),'D: ',', '.join(West[2]),'\r\n'
              'C: ',', '.join(East[3]),tab_check(3),'C: ',', '.join(West[3]),'\r\n'
              '\t\t\t\t','South','\r\n'
              '\t\t\t\t','S: ',', '.join(South[0]),'\r\n'
              '\t\t\t\t','H: ',', '.join(South[1]),'\r\n'
              '\t\t\t\t','D: ',', '.join(South[2]),'\r\n'
              '\t\t\t\t','C: ',', '.join(South[3]),'\r\n')

# example: deal 3 hands and extract hands in each direction
All_North = []
All_South = []
All_East = []
All_West = []
deal_hand(3)

# print hands for one side when All_North, All_South, All_East, and All_West are defined
def print_one_side(a):
    for i in range(len(a)):
        print(i+1,'. ')
        print('S: ',', '.join(a[i][0]),'\r\n'
              'H: ',', '.join(a[i][1]),'\r\n'
              'D: ',', '.join(a[i][2]),'\r\n'
              'C: ',', '.join(a[i][3]),'\r\n')

# example: print all the South hands dealt above
print_one_side(All_South)





    
    
    
    
    


