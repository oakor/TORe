import os
import sys
import json
import time
import random

select_demos = {
            "f_add_column": """If the table does not have the needed column to answer the question, we use f_add_column() to add a new column for it. For example,
/*
col : rank | lane | player | time
row 1 : 1 | 5 | olga tereshkova (kaz) | 51.86
row 2 : 2 | 6 | manjeet kaur (ind) | 52.17
row 3 : 3 | 3 | asami tanno (jpn) | 53.04
*/
Question: How many athletes are from japan?
Explanation: The question is about the number of athletes from japan. We need to known the country of each athlete. There is no column of the country of athletes. We add a column "country of athlete".
Function: f_add_column(country of athlete)
""",

            "f_sort_column": """If the question is about the order of items in a column, we use f_sort_column() to sort the items. For example,
/*
col : position | club | played | points
row 1 : 1 | malaga cf | 42 | 79
row 10 : 10 | cp merida | 42 | 59
row 3 : 3 | cd numancia | 42 | 73
*/
Question: which club placed in the last position.
Explanation: The question wants to check which club placed in the last position. We need to know the order of position from last to front. We sort the rows according to column "position".
Function: f_sort_column(position)
""",

            "f_select_column": """If the table only needs a few columns to answer the question, we use f_select_column() to select these columns for it. For example,
/*
col : code | county | former province | area (km2) | population | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/
Question: Which county has population higher than 500000?
Explanation: The statement wants to check which county has population higher than 500000. We need to know the county and its population. We select the column "county" and column "population".
Function: f_select_column(county, population)
""",
            "f_select_row": """If the table only needs a few rows to answer the question, we use f_select_row() to select these rows for it. For example,
/*
table caption : jeep grand cherokee.
col : years | displacement | engine | power | torque
row 1 : 1999 - 2004 | 4.0l (242cid) | power tech i6 | - | 3000 rpm
row 2 : 1999 - 2004 | 4.7l (287cid) | powertech v8 | - | 3200 rpm
row 3 : 2002 - 2004 | 4.7l (287cid) | high output powertech v8 | - | -
row 4 : 1999 - 2001 | 3.1l diesel | 531 ohv diesel i5 | - | -
row 5 : 2002 - 2004 | 2.7l diesel | om647 diesel i5 | - | -
*/
Question: Which power has the third lowest numbered displacement? 
Explanation: The question wants to check which power had third lowest numbered displacement. We need to know the first three low numbered displacement. We select the row 1, row 4, row 5.
Function: f_select_row(row 1, row 4, row 5)
""",

            "f_group_column": """If the question is about items with the same value and the number of these items, we use f_group_column() to group the items. For example,
/*
col : district | name | party | residence | first served
row 1 : district 1 | nelson albano | dem | vineland | 2006
row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
row 3 : district 2 | john f. amodeo | rep | margate | 2008
*/
Question: How many districts are democratic
Explanation: The question wants to check how many districts are democratic. We need to know the number of dem in the table. We group the rows according to column "party".
Function: f_group_column(party)
""",

            "END": """If the question doesn't need any other process, we use END to end the process. For example
/*
col : Country | Gold
row 1 : China | 38 
*/
Question: Which country won the most gold medals?
Explanation: The question wants to know which country won the most gold medals. We don't need any other information to know the answer.
Function: END
Answer: China
"""
        }

f_add_column_demos = """To answer the question, we can first use f_add_column() to add more columns to the table.

The added columns should have these data types:
1. Numerical: the numerical strings that can be used in sort, sum
2. Datetype: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : place | player | country | score | to par
row 1 : 1 | hale irwin | united states | 68 + 68 = 136 | - 4
row 2 : 2 | fuzzy zoeller | united states | 71 + 66 = 137 | - 3
row 3 : t3 | david canipe | united states | 69 + 69 = 138 | - 2
row 4 : 4 | kahu | United Kingdom | 67 + 69 = 136 | - 3
*/
Question: Whict player has 138 score?
The existing columns are: place, player, country, score, to par.
Explanation: To answer the question, we need to know the score values of each player. We extract the value from column "score" and create a different column "score value" for each row. The datatype is numerical.
Therefore, the answer is: f_add_column(score value). The value: [136 ,137, 138, 136]
New Table:
/*
col : place | player | country | score | to par | score value
row 1 : 1 | hale irwin | united states | 68 + 68 = 136 | - 4 | 136
row 2 : 2 | fuzzy zoeller | united states | 71 + 66 = 137 | - 3 | 137
row 3 : t3 | david canipe | united states | 69 + 69 = 138 | - 2 | 138
row 4 : 4 | kahu | United Kingdom | 67 + 69 = 136 | - 3 | 136
*/

## Example 2
/*
col : code | county | former province | area (km2) | population; census 2009 | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/
Question: Whict county has a population in 2009 higher than 500,000?
The existing columns are: code, county, former province, area (km2), population; census 2009, capital.
Explanation: To answer the question, we need to know the population of each county. We extract the value from column "population; census 2009" and create a different column "population" for each row. The datatype is numerical.
Therefore, the answer is: f_add_column(population). The value: [939370, 649311, 1109735]
New Table:
/*
col : code | county | former province | area (km2) | population; census 2009 | capital | population
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city) | 939370
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale | 649311
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi | 1109735
*/

## Example 3
"""

f_sort_column_demos = """To answer the question, we can first use f_sort() to sort the values in a column to get the order of the items. The order can be "large to small" or "small to large".

The column to sort should have these data types:
1. Numerical: the numerical strings that can be used in sort
2. DateType: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
row 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28
row 4 : 4 | cd tarragona | 42 | 70 | 20 | 11 | 11 | 67 | 42 | +25
row 5 : 5 | cd logrones | 42 | 68 | 19 | 12 | 11 | 65 | 43 | +22
*/
Question: Which club placed in the last position?
The existing columns are: position, club, played, points, wins, draws, losses, goals for, goals against, goal difference.
Explanation: The question wants to check which club is in the last position. Each row is about a club. We need to know the order of position from last to front. There is a column for position and the column name is position. The datatype is Numerical.
Therefore, the answer is: f_sort(position), the order is "large to small".
New Table:
/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25
row 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28
row 4 : 4 | cd tarragona | 42 | 70 | 20 | 11 | 11 | 67 | 42 | +25
row 5 : 5 | cd logrones | 42 | 68 | 19 | 12 | 11 | 65 | 43 | +22
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
*/

## Example 2
/*
col : year | team | games | combined tackles | tackles | assisted tackles |
row 1 : 2004 | hou | 16 | 63 | 51 | 12 |
row 2 : 2005 | hou | 12 | 35 | 24 | 11 |
row 3 : 2006 | hou | 15 | 26 | 19 | 7 |
*/
Question: Which city had the least amount of tackles in 2006?
The existing columns are: year, team, games, combined tackles, tackles, assisted tackles.
Explanation: The question wants to know which city had the least amount of tackles in 2006. Each row is about a year. We need to know the order of tackles from the least to the most. There is a column for tackles and the column name is tackles. The datatype is Numerical.
Therefore, the answer is: f_sort(tackles), the order is "small to large".
New Table:
/*
col : year | team | games | combined tackles | tackles | assisted tackles |
row 1 : 2006 | hou | 15 | 26 | 19 | 7 |
row 2 : 2005 | hou | 12 | 35 | 24 | 11 |
row 3 : 2004 | hou | 16 | 63 | 51 | 12 |
*/

## Example 3
"""

f_select_column_demos = """To answer the question, we can first use f_select_column() to select the columns that we need. 

The column to select should have these data types:
1. Numerical: the numerical strings that can be used in sort, sum
2. DateType: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
row 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28
*/
Question: Which club placed in the last position?
The existing columns are: position, club, played, points, wins, draws, losses, goals for, goals against, goal difference.
Explanation: The question wants to check which club is in the last position. Each row is about a club. We need to select the column "club" and the column "position" to answer the question.
Therefore, the answer is: f_select_column(club, position).
New Table:
/*
col : club | position
row 1 : malaga cf | 1
row 10 : cp merida | 10
row 3 : cd numancia | 3
*/

## Example 2
/*
col : year | team | games | combined tackles | tackles | assisted tackles |
row 1 : 2004 | hou | 16 | 63 | 51 | 12 |
row 2 : 2005 | hou | 12 | 35 | 24 | 11 |
row 3 : 2006 | hou | 15 | 26 | 19 | 7 |
row 4 : 2006 | ny | 17 | 29 | 20 | 6 |
*/
Question: Which city had the least amount of tackles in 2006?
The existing columns are: year, team, games, combined tackles, tackles, assisted tackles.
Explanation: The question wants to know which city had the least amount of tackles in 2006. Each row is about a year. We need to select the column "team", the column "tackles" and the column "year" to answer the question.
Therefore, the answer is: f_select_column(team, tackles, year).
New Table:
/*
col : team | tackles | year
row 1 : hou | 51 | 2004
row 2 : hou | 24 | 2005
row 3 : hou | 19 | 2006
row 4 : ny | 20 | 2006
*/

## Example 3
"""

f_select_row_demos = """To answer the question, we can first use f_select_row() to select the rows that we need. 

## Example 1
/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 1 : 1 | malaga cf | 42 | 79 | 22 | 13 | 7 | 72 | 47 | +25
row 3 : 3 | cd numancia | 42 | 73 | 21 | 10 | 11 | 68 | 40 | +28
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
*/
Question: Which club placed in the last position?
The existing columns are: position, club, played, points, wins, draws, losses, goals for, goals against, goal difference.
Explanation: The question wants to check which club is in the last position. Each row is about a club. The row 10 is the last position. We need to select the row 10 to answer the question.
Therefore, the answer is: f_select_row(row 10).
New Table:
/*
col : position | club | played | points | wins | draws | losses | goals for | goals against | goal difference
row 10 : 10 | cp merida | 42 | 59 | 15 | 14 | 13 | 48 | 41 | +7
*/

## Example 2
/*
col : place | player | country | score | to par
row 1 : 1 | hale irwin | united states | 68 + 68 = 136 | - 4
row 2 : 2 | fuzzy zoeller | united states | 71 + 66 = 137 | - 3
row 3 : t3 | david canipe | united states | 69 + 69 = 138 | - 2
row 4 : 4 | kahu | United Kingdom | 67 + 69 = 136 | - 3
*/
Question: Which player has 138 score?
The existing columns are: place, player, country, score, to par.
Explanation: The question wants to check which player has 138 score. Each row is about a player. The row 3 is the player with 138 score. We need to select the row 3 to answer the question.
Therefore, the answer is: f_select_row(row 3).
New Table:
/*
col : place | player | country | score | to par
row 3 : t3 | david canipe | united states | 69 + 69 = 138 | - 2
*/

## Example 3
"""

f_group_column_demos = """To answer the question, we can first use f_group() to group the values in a column.

## Example 1
/*
col : rank | lane | athlete | time | country
row 1 : 1 | 6 | manjeet kaur (ind) | 52.17 | ind
row 2 : 2 | 5 | olga tereshkova (kaz) | 51.86 | kaz
row 3 : 3 | 4 | pinki pramanik (ind) | 53.06 | ind
row 4 : 4 | 1 | tang xiaoyin (chn) | 53.66 | chn
row 5 : 5 | 8 | marina maslyonko (kaz) | 53.99 | kaz
*/
Question: How many athletes are from japan?
The existing columns are: rank, lane, athlete, time, country.
Explanation: The question asks the number of athletes from japan. Each row is about an athlete. We can group column "country" to group the athletes from the same country.
Therefore, the answer is: f_group(country).
New Table:
/*
col : country | count
row 1 : ind | 2
row 2 : kaz | 2
row 3 : chn | 1
*/

## Example 2
/*
col : district | name | party | residence | first served
row 1 : district 1 | nelson albano | dem | vineland | 2006
row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
row 3 : district 2 | john f. amodeo | rep | margate | 2008
row 4 : district 2 | chris a. brown | rep | ventnor | 2012
row 5 : district 3 | john j. burzichelli | dem | paulsboro | 2002
row 6 : district 3 | joseph d. rocco | rep | paulsboro | 2002
row 7 : district 4 | joseph d. rocco | rep | paulsboro | 2002
*/
Question: what's the number of districts that are democratic.
The existing columns are: district, name, party, residence, first served.
Explanation: The question asks the number of districts that are democratic. Each row is about a district. We can group the column "party" to group the districts from the same party.
Therefore, the answer is: f_group(party).
New Table:
/*
col : party | count
row 1 : dem | 3
row 2 : rep | 4
*/

## Example 3
"""


