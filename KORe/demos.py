import os
import sys
import json
import time
import random

select_demos = {
            "f_add_knowledge_column": """
/*
col : rank | gold | country
row 1 : 1 | 36 | China
row 2 : 2 | 18 | America
row 3 : 3 | 11 | Russia
row 4 : 4 | 9 | United Kingdom
*/
Question: How many gold medals has Asian country win?
Explanation: The question is about the gold medals of Asian. We need to known the region of each country. There is no column of the region of each country. If the table does not have the needed column to answer the question and the column need extra knowledge, we use f_add_knowledge_column() to add a new column for it. We add a column "region of country".
Function: f_add_knowledge_column(region of country)
""",

            "f_add_inferred_column": """
/*
col : rank | lane | player | time
row 1 : 1 | 5 | olga tereshkova (kaz) | 51.86
row 2 : 2 | 6 | manjeet kaur (ind) | 52.17
row 3 : 3 | 3 | asami tanno (jpn) | 53.04
*/
Question: How many athletes are from japan?
Explanation: The question is about the number of athletes from japan. We need to known the country of each athlete. There is no column of the country of athletes. If the table does not have the needed column to answer the question and the column could be inferred from existing columns, we use f_add_inferred_column() to add a new column for it. We add a column "country of athlete".
Function: f_add_inferred_column(country of athlete)
""",

            "f_sort_column": """
/*
col : position | club | played | points
row 1 : 1 | malaga cf | 42 | 79
row 10 : 10 | cp merida | 42 | 59
row 3 : 3 | cd numancia | 42 | 73
*/
Question: which club placed in the last position.
Explanation: The question wants to check which club placed in the last position. We need to know the order of position from last to front. If the question is about the order of items in a column, we use f_sort_column() to sort the items. We sort the rows according to column "position".
Function: f_sort_column(position)
""",

            "f_select_column": """
/*
col : code | county | former province | area (km2) | population | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/
Question: Which county has population higher than 500000?
Explanation: The statement wants to check which county has population higher than 500000. We need to know the county and its population. If the table only needs a few columns to answer the question, we use f_select_column() to select these columns for it. We select the column "county" and column "population".
Function: f_select_column(county, population)
""",
            "f_select_row": """
/*
col : years | displacement | engine | power | torque
row 1 : 1999 - 2004 | 4.0l (242cid) | power tech i6 | - | 3000 rpm
row 2 : 1999 - 2004 | 4.7l (287cid) | powertech v8 | - | 3200 rpm
row 3 : 2002 - 2004 | 4.7l (287cid) | high output powertech v8 | - | -
row 4 : 1999 - 2001 | 3.1l diesel | 531 ohv diesel i5 | - | -
row 5 : 2002 - 2004 | 2.7l diesel | om647 diesel i5 | - | -
*/
Question: Which power has the third lowest numbered displacement? 
Explanation: The question wants to check which power had third lowest numbered displacement. We need to know the first three low numbered displacement. If the table only needs a few rows to answer the question, we use f_select_row() to select these rows for it. We select the row 1, row 4, row 5.
Function: f_select_row(row 1, row 4, row 5)
""",

            "f_group_column": """
/*
col : district | name | party | residence | first served
row 1 : district 1 | nelson albano | dem | vineland | 2006
row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
row 3 : district 2 | john f. amodeo | rep | margate | 2008
*/
Question: How many districts are democratic
Explanation: The question wants to check how many districts are democratic. We need to know the number of dem in the table. If the question is about items with the same value and the number of these items, we use f_group_column() to group the items. We group the rows according to column "party".
Function: f_group_column(party)
""",

            "f_stitch_tables": """
/*
table_name: gymnast
col: Gymnast_ID | Floor_Exercise_Points | Pommel_Horse_Points | Rings_Points | Vault_Points | Parallel_Bars_Points | Horizontal_Bar_Points | Total_Points
row 1: 1 | 9.725 | 9.737 | 9.512 | 9.575 | 9.762 | 9.75 | 58.061
row 2: 2 | 9.7 | 9.625 | 9.625 | 9.65 | 9.587 | 9.737 | 57.924

table_name: people
col: People_ID | Name | Age | Height | Hometown
row 1: 1 | Paul Hamm | 24.0 | 1.71 | Santo Domingo
row 2: 2 | Lorraine SÃºarez Carmona | 21.0 | 1.75 | Bonao

foreign_key: gymnast_id, people_id
*/
Question: What is the name and total points of the gymnast with ID 1?
Explanation: The question requires information from both the gymnast and people tables. We need to combine these two tables to answer the question. If the question needs information from two tables, we use f_stitch_tables() to join them based on the foreign key.
Function: f_stitch_tables(gymnast.Gymnast_ID, people.People_ID)
""",

            "f_change_column_name": """
/*
col : rank | pts for | pts against | club
row 1 : 1 | 860 | 450 | Manchester United
row 2 : 2 | 740 | 520 | Liverpool
row 3 : 3 | 680 | 580 | Arsenal
*/
Question: What is the total points scored by each team?
Explanation: The question wants to know the total points scored by each team. The column "pts for" represents the points scored, but its name is not clear enough. We should rename it to make it more descriptive. If we need to make a column name more clear and descriptive, we use f_change_column_name() to rename it.
Function: f_change_column_name("pts for", "total_points")
""",

            "END": """
/*
col : Country | Gold
row 1 : China | 38 
*/
Question: Which country won the most gold medals?
Explanation: The question wants to know which country won the most gold medals. We don't need any other information to know the answer. If the question doesn't need any other process, we use END to end the process.
Function: END
Answer: China
"""
        }

f_add_column_demos = """To answer the question, we can first use f_add_column() to add one column to the table.

The added column should have these data types:
1. Numerical: the numerical strings that can be used in sort, sum
2. Datetype: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : place | player | country | score | to par
row 1 : 1 | hale irwin | united states | 68 + 68 = 136 | - 4
row 2 : 2 | fuzzy zoeller | united states | 71 + 66 = 137 | - 3
row 3 : 3 | david canipe | united states | 69 + 69 = 138 | - 2
row 4 : 4 | kahu | United Kingdom | 67 + 69 = 136 | - 3
*/
Question: Whict player has 138 score?
The existing columns are: place, player, country, score, to par.
Explanation: To answer the question, we need to know the score values of each player. We extract the value from column "score" and create a different column "score value" for each row. The datatype is numerical.
Therefore, the answer is: f_add_column(score value). The value: [136, 137, 138, 136]
New Table:
/*
col : place | player | country | score | to par | score value
row 1 : 1 | hale irwin | united states | 68 + 68 = 136 | - 4 | 136
row 2 : 2 | fuzzy zoeller | united states | 71 + 66 = 137 | - 3 | 137
row 3 : 3 | david canipe | united states | 69 + 69 = 138 | - 2 | 138
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

f_sort_column_demos = """To answer the question, we can first use f_sort_column() to sort the values in a column to get the order of the items. The order can be "large to small" or "small to large".

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
Therefore, the answer is: f_sort_column(position), the order is "large to small".
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
Therefore, the answer is: f_sort_column(tackles), the order is "small to large".
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
row 3 : 3 | david canipe | united states | 69 + 69 = 138 | - 2
row 4 : 4 | kahu | United Kingdom | 68 + 70 = 138 | - 3
*/
Question: Which players have 138 score?
The existing columns are: place, player, country, score, to par.
Explanation: The question wants to check which players have 138 score. Each row is about a player. The row 3 and row 4 are the players with 138 score. We need to select the row 3 and row 4 to answer the question.
Therefore, the answer is: f_select_row(row 3, row 4).
New Table:
/*
col : place | player | country | score | to par
row 3 : 3 | david canipe | united states | 69 + 69 = 138 | - 2
row 4 : 4 | kahu | United Kingdom | 68 + 70 = 138 | - 3
*/

## Example 3
"""

f_group_column_demos = """To answer the question, we can use f_group_column() to group the values in a column.

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
Therefore, the answer is: f_group_column(country).
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
Therefore, the answer is: f_group_column(party).
New Table:
/*
col : party | count
row 1 : dem | 3
row 2 : rep | 4
*/

## Example 3
"""

f_add_knowledge_column_demos = """To answer the question, we can use f_add_knowledge_column() to add one column to the table. This function is used when we need to add a column that requires external knowledge.

The added column should have these data types:
1. Numerical: the numerical strings that can be used in sort, sum
2. Datetype: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : rank | gold | country
row 1 : 1 | 36 | China
row 2 : 2 | 18 | America
row 3 : 3 | 11 | Russia
row 4 : 4 | 9 | United Kingdom
row 5 : 5 | 8 | France
*/
Question: How many gold medals has Asian country win?
The existing columns are: rank, gold, country.
Explanation: The question wants to know the gold medals of Asian countries. We need to know which countries are in Asia. This information is not in the table and requires external knowledge. We add a column "region" to indicate the continent of each country.
Therefore, the answer is: f_add_knowledge_column(region). The value: ["Asia", "America", "Europe", "Europe", "Europe]
New Table:
/*
col : rank | gold | country | region
row 1 : 1 | 36 | China | Asia
row 2 : 2 | 18 | America | America
row 3 : 3 | 11 | Russia | Europe
row 4 : 4 | 9 | United Kingdom | Europe
row 5 : 5 | 8 | France | Europe
*/

## Example 2
/*
col : name | age | city
row 1 : John | 25 | New York
row 2 : Maria | 30 | Tokyo
row 3 : Ahmed | 28 | Cairo
row 4 : Sarah | 35 | London
*/
Question: How many people are from English-speaking countries?
The existing columns are: name, age, city.
Explanation: The question wants to know how many people are from English-speaking countries. We need to know which countries are English-speaking. This information is not in the table and requires external knowledge. We add a column "language" to indicate the primary language of each country.
Therefore, the answer is: f_add_knowledge_column(language). The value: ["English", "Japanese", "Arabic", "English"]
New Table:
/*
col : name | age | city | language
row 1 : John | 25 | New York | English
row 2 : Maria | 30 | Tokyo | Japanese
row 3 : Ahmed | 28 | Cairo | Arabic
row 4 : Sarah | 35 | London | English
*/

## Example 3
"""

f_add_inferred_column_demos = """To answer the question, we can use f_add_inferred_column() to add one column to the table. This function is used when we need to add a column that can be calculated or inferred from existing columns.

The added column should have these data types:
1. Numerical: the numerical strings that can be used in sort, sum
2. Datetype: the strings that describe a date, such as year, month, day
3. String: other strings

## Example 1
/*
col : year | team | games | wins | losses | points
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64
*/
Question: What is the win percentage for each season?
The existing columns are: year, team, games, wins, losses, points.
Explanation: The question wants to know the win percentage for each season. We can calculate this by dividing the number of wins by the total number of games and multiplying by 100. We add a column "win_percentage" to show the percentage of games won each season.
Therefore, the answer is: f_add_inferred_column(win_percentage). The value: [63.41, 51.22, 40.24, 39.02]
New Table:
/*
col : year | team | games | wins | losses | points | win_percentage
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | 63.41
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | 51.22
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | 40.24
row 4 | 2023 | Lakers | 82  | 32 | 50 | 64 | 39.02
*/

## Example 2
/*
col : year | team | games | combined tackles | tackles | assisted tackles
row 1 : 2004 | hou | 16 | 63 | 51 | 12
row 2 : 2005 | hou | 12 | 35 | 24 | 11
row 3 : 2006 | hou | 15 | 26 | 19 | 7
*/
Question: What is the average tackles per game for each year?
The existing columns are: year, team, games, combined tackles, tackles, assisted tackles.
Explanation: The question wants to know the average tackles per game for each year. We can calculate this by dividing the tackles by the number of games. We add a column "avg_tackles" to show the average tackles per game.
Therefore, the answer is: f_add_inferred_column(avg_tackles). The value: [3.19, 2.00, 1.27]
New Table:
/*
col : year | team | games | combined tackles | tackles | assisted tackles | avg_tackles
row 1 : 2004 | hou | 16 | 63 | 51 | 12 | 3.19
row 2 : 2005 | hou | 12 | 35 | 24 | 11 | 2.00
row 3 : 2006 | hou | 15 | 26 | 19 | 7 | 1.27
*/

## Example 3
"""

f_stitch_tables_demos = """To answer the question, we can first use f_stitch_tables() to combine two tables. This function is used when we need to merge two tables that are linked by a foreign key, and f_stitch_tables() can only input two column from each table.

## Example 1
/*
table_name: gymnast
col : Gymnast_ID | Total_Points
row 1 : 1 | 58.061
row 2 : 2 | 57.924
row 3 : 4 | 57.649

table_name: people
col : People_ID | Name
row 1 : 1 | Paul Hamm
row 2 : 2 | Lorraine SÃºarez Carmona
row 3 : 4 | Elizabeth QuiÃ±Ã³nez Aroyo

foreign_key: gymnast_id
*/
Question: What is the name of the gymnast with the highest total points?
The existing tables are: gymnast, people.
Explanation: The question asks for the name of the gymnast with the most points. The 'gymnast' table contains points and the 'people' table contains names. To link them, we must use the foreign key gymnast_id to stitch the tables.
Therefore, the answer is: f_stitch_tables(gymnast.Gymnast_ID, people.People_ID)
New Table:
/*
col : Gymnast_ID | Total_Points | People_ID | Name
row 1 : 1 | 58.061 | 1 | Paul Hamm
row 2 : 2 | 57.924 | 2 | Lorraine SÃºarez Carmona
row 3 : 4 | 57.649 | 4 | Elizabeth QuiÃ±Ã³nez Aroyo
*/

## Example 2
/*
table_name: Person
col : name | age | city | gender | job
row 1 : Alice | 25 | new york city | female | student
row 2 : Bob | 35 | salt lake city | male | engineer
row 3 : Zach | 45 | austin | male | doctor
row 4 : Dan | 26 | chicago | female | student

table_name: PersonFriend
col : name | friend | year
row 1 : Alice | Bob | 10
row 2 : Zach | Dan | 12
row 3 : Bob | Zach | 5
row 4 : Zach | Alice | 6

foreign_key: name, friend, name
*/
Question: Find the name and age of the person who is a friend of both Dan and Alice.
The existing tables are: Person, PersonFriend.
Explanation: The question asks for the age of the person who is a friend of both Dan and Alice. We must use the foreign key name, friend, name to stitch the tables and find the friends of Both Dan and Alice.
Therefore, the answer is: f_stitch_tables(Person.name, PersonFriend.friend)
New Table:
/*
col : name | age | city | gender | job | friend | year | name_of_PersonFriend
row 1 : Alice | 25 | new york city | female | student | Alice | 6 | Zach
row 2 : Bob | 35 | salt lake city | male | engineer | Bob | 10 | Alice
row 3 : Zach | 45 | austin | male | doctor | Zach | 5 | Bob
row 4 : Dan | 26 | chicago | female | student | Dan | 12 | Zach
*/

## Example 3
"""

f_change_column_name_demos = """To answer the question, we can use f_change_column_name() to rename a column. This function is used when we need to make a column name more clear and descriptive.

## Example 1
/*
col : rank | pts for | pts against | club
row 1 : 1 | 860 | 450 | Manchester United
row 2 : 2 | 740 | 520 | Liverpool
row 3 : 3 | 680 | 580 | Arsenal
row 4 : 4 | 620 | 640 | Chelsea
*/
Question: What is the total points scored by each team?
The existing columns are: rank, pts for, pts against, club.
Explanation: The question wants to know the total points scored by each team. The column "pts for" represents the points scored, but its name is not clear enough. We should rename it to make it more descriptive.
Therefore, the answer is: f_change_column_name("pts for", "total_points")
New Table:
/*
col : rank | total_points | pts against | club
row 1 : 1 | 860 | 450 | Manchester United
row 2 : 2 | 740 | 520 | Liverpool
row 3 : 3 | 680 | 580 | Arsenal
row 4 : 4 | 620 | 640 | Chelsea
*/

## Example 2
/*
col : code | county | former province | area (km2) | population; census 2009 | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/
Question: What is the population of each county in 2009?
The existing columns are: code, county, former province, area (km2), population; census 2009, capital.
Explanation: The question wants to know the population of each county in 2009. The column "population; census 2009" has a complex name. We should rename it to make it simpler and clearer.
Therefore, the answer is: f_change_column_name("population; census 2009", "population_2009")
New Table:
/*
col : code | county | former province | area (km2) | population_2009 | capital
row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
*/

## Example 3
"""

stitch_decision_prompt_template = """
# Instruction
You are a table processing assistant. Your task is to analyze a question and a set of tables and decide the first step to take.

## Output Format
You MUST follow one of these exact formats:

1. If you need to combine information from two tables:
Explanation: [explanation of why you need to combine tables]
Function: f_stitch_tables(table_name1.column_name, table_name2.column_name)

2. If the answer can be found in a single table:
Explanation: [explanation of why only one table is needed]
Function: f_select_table(table_name)

## Rules
1. You MUST choose exactly one function: `f_stitch_tables` or `f_select_table`.
2. For `f_stitch_tables`, you MUST specify the two tables and the columns to join on.
3. For `f_select_table`, you MUST specify the name of the table to keep.

## Example 1 (Stitching is needed)
/*
table_name: gymnast
col : Gymnast_ID | Total_Points
row 1 : 1 | 58.061
row 2 : 2 | 57.924

table_name: people
col : People_ID | Name
row 1 : 1 | Paul Hamm
row 2 : 2 | Lorraine SÃºarez Carmona

foreign_key: people_id
*/
Question: What is the name of the gymnast with the highest total points?
Explanation: The question asks for the gymnast's name, which is in the 'people' table, based on the total points, which is in the 'gymnast' table. Therefore, I need to combine information from both tables.
Function: f_stitch_tables(gymnast.Gymnast_ID, people.People_ID)

## Example 2 (Single table is sufficient)
/*
table_name: gymnast
col : Gymnast_ID | Total_Points | Rings_Points
row 1 : 1 | 58.061 | 9.512
row 2 : 2 | 57.924 | 9.625

table_name: people
col : People_ID | Name | Age
row 1 : 1 | Paul Hamm | 24.0
row 2 : 2 | Lorraine SÃºarez Carmona | 21.0

foreign_key: people_id
*/
Question: What is the age of Paul Hamm?
Explanation: The question asks for the age of a person named Paul Hamm. All the necessary information (Name, Age) is available in the 'people' table. I do not need the 'gymnast' table.
Function: f_select_table(people)

## Current Tables and Question
{prompt_content}
"""


