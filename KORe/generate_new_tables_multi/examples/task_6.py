operations = """
Available Operations and their parameter requirements:
- f_add_knowledge_column(column_name): Add a new column that requires external knowledge
- f_add_inferred_column(column_name): Add a new column that can be calculated or inferred from existing columns
- f_sort_column(column_name): Sort the table by a specific column
- f_select_column(column1, column2, ...): Select specific columns from the table
- f_select_row(row1, row2, ...): Select specific rows from the table
- f_group_column(column_name): Group the table by a specific column
- f_change_column_name(old_name, new_name): Rename a column
- f_stitch_tables(table1.column1, table2.column2, join_method): Stitch two tables together by a specific column, choose join_method in [inner, left, right]
- f_select_table(table_name): Select a specific table from the database
"""


task_6_EXAMPLES_single = {
    "EXAMPLE_1": {
    "table_info": """
col : position | channel | launch date | owner | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 (p)
row 1 : 1 | rai 1 | 1954 | rai | 22.86 | 22.99 | 22.33 | 21.80 | 20.63 | 19.86 | 18.1 | 18.3 | 19.12
row 2 : 2 | canale 5 | 1980 | mediaset | 21.82 | 20.96 | 20.67 | 20.33 | 20.50 | 18.78 | 17.0 | 15.9 | 15.25
row 3 : 3 | rai 3 | 1979 | rai | 9.11 | 9.31 | 9.06 | 9.07 | 8.46 | 7.75 | 8.5 | 7.7 | 7.93
row 4 : 4 | rai 2 | 1961 | rai | 11.29 | 11.27 | 10.38 | 10.60 | 8.90 | 9.02 | 8.3 | 7.6 | 6.81
row 5 : 5 | italia 1 | 1982 | mediaset | 11.48 | 11.09 | 11.18 | 10.83 | 10.68 | 9.22 | 8.3 | 6.18 | 6.48
row 6 : 6 | rete 4 | 1982 | mediaset | 8.63 | 8.22 | 8.68 | 8.28 | 7.47 | 6.79 | 6.7 | 5.42 | 5.26
row 7 : 7 | la7 | 2001 | cairo communication | 2.71 | 3.02 | 2.97 | 3.08 | 2.90 | 3.67 | 3.8 | 3.68 | 4.29
row 8 : 8 | real time | 2005 | discovery networks | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | 1.09 | 1.4 | 1.49
row 9 : 9 | iris | 2007 | mediaset | ne | ne | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | 1.1 | 1.27
row 10 : 10 | rai yoyo | 2006 | rai | ne | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | 0.90 | 1.24
row 11 : 11 | dmax | 2011 | discovery networks | ne | ne | ne | ne | ne | ne | <0.90 | <0.90 | 1.17
row 12 : 12 | rai premium | 2003 | rai | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | 1.25 | 1.11
row 13 : 13 | rai movie | 1999 | rai | ne | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | <0.90 | 0.92 | 0.93
row 14 : 14 | rai 4 | 2008 | rai | ne | ne | ne | <0.90 | <0.90 | <0.90 | 0.98 | 1.1 | 0.91
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(position, channel, owner, 2005)",
        "f_select_row(row1, row4)",
        "END"
    ],
    "explanations": [
        "Selecting the columns position, channel, owner, and 2005 from the table",
        "Selecting the rows that are owned by 'rai' and have a viewership percentage greater than 10% in 2005, which are row1 and row4"
    ],
    "intermediate_tables": [
        """
col : position | channel | owner | 2005
row 1 : 1 | rai 1 | rai | 22.86
row 2 : 2 | canale 5 | mediaset | 21.82
row 3 : 3 | rai 3 | rai | 9.11
row 4 : 4 | rai 2 | rai | 11.29
row 5 : 5 | italia 1 | mediaset | 11.48
row 6 : 6 | rete 4 | mediaset | 8.63
row 7 : 7 | la7 | cairo communication | 2.71
row 8 : 8 | real time | discovery networks | <0.90
row 9 : 9 | iris | mediaset | ne
row 10 : 10 | rai yoyo | rai | ne
row 11 : 11 | dmax | discovery networks | ne
row 12 : 12 | rai premium | rai | <0.90
row 13 : 13 | rai movie | rai | ne
row 14 : 14 | rai 4 | rai | ne
        """,
        """
col : position | channel | owner | 2005
row 1 : 1 | rai 1 | rai | 22.86
row 4 : 4 | rai 2 | rai | 11.29
        """
    ],
    "question": "Which channels had a viewership percentage greater than 10% in 2005 and are owned by 'rai'?",
    "answer": "rai 1, rai 2",
    "explanation": "This question requires finding channels with specific owner and viewership criteria. First, I select the columns position, channel, owner, and 2005 from the table to focus on relevant information. Then, I select rows 1 and 4 which correspond to channels owned by 'rai' that have a viewership percentage greater than 10% in 2005. From this filtered data, I can see that two channels meet both criteria: 'rai 1' with 22.86% viewership and 'rai 2' with 11.29% viewership."
    },


    "EXAMPLE_2": {
    "table_info": """
col : draw | language | artist | english translation | place | points
row 1 : 1 | polish | justyna | alone | 18 | 15
row 2 : 2 | english | eddie friel | - | 14 | 44
row 3 : 3 | german | stone & stone | in love with you | 23 | 1
row 4 : 4 | bosnian | davorin popović | the 21st century | 19 | 14
row 5 : 5 | norwegian | secret garden | - | 1 | 148
row 6 : 6 | russian | philipp kirkorov | lullaby for a volcano | 17 | 17
row 7 : 7 | icelandic | bo halldórsson | now | 15 | 31
row 8 : 8 | german | stella jones | the world turns the wrong way | 13 | 67
row 9 : 9 | spanish | anabel conde | come back to me | 2 | 119
row 10 : 10 | turkish | arzu ece | love | 16 | 21
    """,
    "chain": [
        "f_select_column()",
        "f_sort_column()",
        "f_change_column_name()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(language, points)",
        "f_sort_column(points)",
        "f_change_column_name(points, average_points)",
        "END"
    ],
    "explanations": [
        "Selecting the columns language and points from the table",
        "Sorting the table by the points column",
        "Renaming the points column to average_points"
    ],
    "intermediate_tables": [
        """
col : language | points
row 1 : polish | 15
row 2 : english | 44
row 3 : german | 1
row 4 : bosnian | 14
row 5 : norwegian | 148
row 6 : russian | 17
row 7 : icelandic | 31
row 8 : german | 67
row 9 : spanish | 119
row 10 : turkish | 21
        """,
        """
col : language | average_points
row 1 : norwegian | 148
row 2 : spanish | 119
row 3 : german | 67
row 4 : english | 44
row 5 : icelandic | 31
row 6 : turkish | 21
row 7 : russian | 17
row 8 : polish | 15
row 9 : bosnian | 14
row 10 : german | 1
        """,
        """
col : language | average_points
row 1 : norwegian | 148
row 2 : spanish | 119
row 3 : german | 67
row 4 : english | 44
row 5 : icelandic | 31
row 6 : turkish | 21
row 7 : russian | 17
row 8 : polish | 15
row 9 : bosnian | 14
row 10 : german | 1
        """
    ],
    "question": "Which language has the highest average points for the songs listed in the table?",
    "answer": "norwegian",
    "explanation": "This question requires finding the language with the highest average points. First, I select the language and points columns from the table to focus on relevant data. Then I sort the table by points in descending order to identify the language with the highest score. Finally, I rename the 'points' column to 'average_points' to better reflect what the values represent. From the sorted data, I can see that 'norwegian' has the highest score with 148 points."
    },


    "EXAMPLE_3": {
    "table_info": """
col : song | international jury | luleå | umeå | sundsvall | falun | karlstad | örebro | norrköping | göteborg | växjö | malmö | stockholm | total
row 1 : hope & glory | 6 | 10 | 12 | 6 | 10 | 2 | 4 | 2 | 12 | 10 | 10 | 12 | 96
row 2 : snälla snälla | 10 | 12 | 8 | - | 4 | - | 2 | 6 | 4 | 6 | - | 1 | 51
row 3 : love love love | - | 1 | 4 | 8 | 2 | 1 | - | - | - | - | 6 | 10 | 40
row 4 : 1000 miles | - | 2 | 6 | 2 | 1 | 12 | - | 4 | 1 | 8 | 12 | - | 58
row 5 : you 're my world | 4 | - | - | - | 12 | - | 8 | - | - | 4 | - | 8 | 28
row 6 : stay the night | - | 6 | 10 | 12 | - | 10 | 1 | 10 | 8 | 1 | 1 | 6 | 67
row 7 : moving on | 12 | 4 | 1 | 4 | 6 | 6 | 10 | 8 | 2 | 12 | 8 | 2 | 75
row 8 : baby goodbye | - | - | - | 10 | 8 | 8 | 12 | 1 | 6 | - | - | 4 | 49
row 9 : alla | 8 | - | - | - | - | - | - | - | - | - | 4 | - | 12
row 10 : så vill stjärnorna | 2 | - | - | - | - | - | - | - | - | - | - | - | 2
row 11 : la voix | 1 | 8 | 2 | 1 | - | 4 | 6 | 12 | - | 2 | 2 | - | 38
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(song, international jury)",
        "f_select_row(row 1)",
        "END"
    ],
    "explanations": [
        "Selecting the columns song and international jury to isolate the relevant information",
        "Selecting row 1 which contains the data for the song 'hope & glory'"
    ],
    "intermediate_tables": [
        """
col : song | international jury
row 1 : hope & glory | 6
row 2 : snälla snälla | 10
row 3 : love love love | -
row 4 : 1000 miles | -
row 5 : you 're my world | 4
row 6 : stay the night | -
row 7 : moving on | 12
row 8 : baby goodbye | -
row 9 : alla | 8
row 10 : så vill stjärnorna | 2
row 11 : la voix | 1
        """,
        """
col : song | international jury
row 1 : hope & glory | 6
        """
    ],
    "question": "Did the song \"hope & glory\" receive a score of 6 from the international jury?",
    "answer": "Yes",
    "explanation": "To answer this question, I need to verify the score given by the international jury to the song 'hope & glory'. First, I select the columns song and international jury to isolate the relevant information from the table. Then, I select row 1 which contains the data for the song 'hope & glory'. From this data, I can see that the international jury gave 'hope & glory' a score of 6, confirming that the answer is 'Yes'."
    },


    "EXAMPLE_4": {
    "table_info": """
col : Club | Season | League | League | League | Cup | Cup | Continental | Continental | Total | Total
row 1 : Club | Season | Division | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals
row 2 : Ajax | 1992–93 | Eredivisie | 12 | 1 | 3 | 0 | 3 | 0 | 18 | 1
row 3 : Ajax | 1993–94 | Eredivisie | 19 | 4 | 3 | 0 | 2 | 0 | 24 | 4
row 4 : Ajax | 1994–95 | Eredivisie | 34 | 6 | 3 | 0 | 11 | 0 | 48 | 6
row 5 : Ajax | Total | Total | 65 | 11 | 9 | 0 | 16 | 0 | 90 | 11
row 6 : Sampdoria | 1995–96 | Serie A | 32 | 3 | 2 | 1 | – | – | 34 | 4
row 7 : Sampdoria | Total | Total | 32 | 3 | 2 | 1 | – | – | 34 | 4
row 8 : Real Madrid | 1996–97 | La Liga | 38 | 6 | 4 | 0 | – | – | 42 | 6
row 9 : Real Madrid | 1997–98 | La Liga | 36 | 6 | 2 | 1 | 11 | 0 | 49 | 7
row 10 : Real Madrid | 1998–99 | La Liga | 37 | 3 | 5 | 1 | 10 | 3 | 52 | 7
row 11 : Real Madrid | 1999–2000 | La Liga | 10 | 0 | 0 | 0 | 6 | 0 | 16 | 0
row 12 : Real Madrid | Total | Total | 121 | 15 | 11 | 2 | 27 | 3 | 159 | 20
    """,
    "chain": [
        "f_select_row()",
        "f_select_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_row(row 9)",
        "f_select_column(Club, Season, League Goals, Cup Goals, Continental Goals, Total Goals)",
        "f_add_inferred_column(goals_percentage)",
        "END"
    ],
    "explanations": [
        "Selecting row 9 which contains data for Real Madrid in the 1997-98 season",
        "Selecting the columns for Club, Season, League Goals, Cup Goals, Continental Goals, Total Goals",
        "Adding an inferred column to calculate the percentage contribution of each competition to total goals"
    ],
    "intermediate_tables": [
        """
col : Club | Season | League | League | League | Cup | Cup | Continental | Continental | Total | Total
row 9 : Real Madrid | 1997–98 | 6 | 1 | 0 | 7
        """,
        """
col : Club | Season | League Goals | Cup Goals | Continental Goals | Total Goals
row 9 : Real Madrid | 1997–98 | 6 | 1 | 0 | 7
        """,
        """
col : Club | Season | League Goals | Cup Goals | Continental Goals | Total Goals | goals_percentage
row 9 : Real Madrid | 1997–98 | 6 | 1 | 0 | 7 | 85.7% League, 14.3% Cup, 0% Continental
        """
    ],
    "question": "How many goals did the player score for Real Madrid in the 1997–98 season across all competitions?",
    "answer": "7",
    "explanation": "To answer this question, we need to find the row for Real Madrid's 1997-98 season and sum up the goals from all competitions. From the table, we can see that in the 1997-98 season, the player scored:\n- League Goals: 6\n- Cup Goals: 1\n- Continental Goals: 0\n\nSumming these up: 6 + 1 + 0 = 7 goals across all competitions."
    },


    "EXAMPLE_5": {
    "table_info": """
col : rank | nation | gold | silver | bronze | total
row 1 : 1 | east germany (gdr) | 9 | 9 | 6 | 24
row 2 : 2 | soviet union (urs) | 6 | 10 | 9 | 25
row 3 : 3 | united states (usa) | 4 | 4 | 0 | 8
row 4 : 4 | finland (fin) | 4 | 3 | 6 | 13
row 5 : 5 | sweden (swe) | 4 | 2 | 2 | 8
row 6 : 6 | norway (nor) | 3 | 2 | 4 | 9
row 7 : 7 | switzerland (sui) | 2 | 2 | 1 | 5
row 8 : 8 | canada (can) | 2 | 1 | 1 | 4
row 9 : 8 | west germany (frg) | 2 | 1 | 1 | 4
row 10 : 10 | italy (ita) | 2 | 0 | 0 | 2
row 11 : 14 | yugoslavia (yug) | 0 | 1 | 0 | 1
    """,
    "chain": [
        "f_select_row()",
        "f_select_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_row(row 4)",
        "f_select_column(nation, total)",
        "END"
    ],
    "explanations": [
        "Selecting row 4 which represents the nation ranked 4th",
        "Selecting the columns for nation name and total medals"
    ],
    "intermediate_tables": [
        """
col : rank | nation | gold | silver | bronze | total
row 4 : 4 | finland (fin) | 4 | 3 | 6 | 13
        """,
        """
col : nation | total
row 4 : finland (fin) | 13
        """
    ],
    "question": "Which nation ranked 4th and how many total medals did it win?",
    "answer": "finland (fin), 13",
    "explanation": "To answer this question, we need to identify the nation with rank 4 in the table and count its total medals. From the table, we can see that finland (fin) is ranked 4th and won a total of 13 medals."
    },


    "EXAMPLE_6": {
    "table_info": """
col : raion (district) or city | total | ukrainians | moldovans | bessarabian bulgarians | russians | gagauzians | other ethnic groups square
row 1 : artsyzskyi raion | 51700 | 14200 | 3300 | 20200 | 11500 | 900 | 1600
row 2 : bilhorod - dnistrovskyi raion | 62300 | 51000 | 3900 | 800 | 5500 | 200 | 900
row 3 : bolhradskyi raion | 75000 | 5700 | 1200 | 45600 | 6000 | 14000 | 2500
row 4 : izmayilskyi raion | 54700 | 15800 | 15100 | 14100 | 8900 | 200 | 600
row 5 : kiliyskyi raion | 59800 | 26700 | 9400 | 2600 | 18000 | 2300 | 800
row 6 : reniyskyi raion | 40700 | 7200 | 19900 | 3400 | 6100 | 3200 | 900
row 7 : saratskyi raion | 49900 | 21900 | 9400 | 10000 | 7900 | 200 | 500
row 8 : tarutynskyi raion | 45200 | 11100 | 7500 | 17000 | 6300 | 2700 | 600
row 9 : tatarbunarskyi raion | 41700 | 29700 | 3900 | 4800 | 2700 | - | 600
row 10 : city of izmayil | 85100 | 32500 | 3700 | 8600 | 37200 | 800 | 2300
row 11 : city of bilhorod - dnistrovskyi | 51100 | 32200 | 1000 | 1900 | 14400 | 200 | 1400
row 12 : total | 617200 | 248000 | 78300 | 129000 | 124500 | 24700 | 12700
    """,
    "chain": [
        "f_select_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(city, ukrainians)",
        "f_add_inferred_column(population_added)",
        "END"
    ],
    "explanations": [
        "Selecting columns for city names and Ukrainian population",
        "Adding a column to calculate the population when adding the population of Ukrainians in the city of Izmayil, which is 32500"
    ],
    "intermediate_tables": [
        """
col : raion (district) or city | ukrainians
row 1 : artsyzskyi raion | 51700
row 2 : bilhorod - dnistrovskyi raion | 62300
row 3 : bolhradskyi raion | 75000
row 4 : izmayilskyi raion | 54700
row 5 : kiliyskyi raion | 59800
row 6 : reniyskyi raion | 40700
row 7 : saratskyi raion | 49900
row 8 : tarutynskyi raion | 45200
row 9 : tatarbunarskyi raion | 41700
row 10 : city of izmayil | 32500
row 11 : city of bilhorod - dnistrovskyi | 32200
        """,
        """
col : raion (district) or city | ukrainians | population_added
row 1 : artsyzskyi raion | 51700 | 84200
row 2 : bilhorod - dnistrovskyi raion | 62300 | 94800
row 3 : bolhradskyi raion | 75000 | 17500
row 4 : izmayilskyi raion | 54700 | 87200
row 5 : kiliyskyi raion | 59800 | 92300
row 6 : reniyskyi raion | 40700 | 73200
row 7 : saratskyi raion | 49900 | 82400
row 8 : tarutynskyi raion | 45200 | 77700
row 9 : tatarbunarskyi raion | 41700 | 74200
row 10 : city of izmayil | 32500 | 65000
row 11 : city of bilhorod - dnistrovskyi | 32200 | 64700
        """
    ],
    "question": "Which district has a population of Ukrainians that, when added to the population of Ukrainians in the city of Izmayil, equals the total population of Ukrainians in the city of Bilhorod-Dnistrovskyi?",
    "answer": "None",
    "explanation": "To solve this problem, we need to find a district where the Ukrainian population, when added to the Ukrainian population in Izmayil (32,500), equals the Ukrainian population in Bilhorod-Dnistrovskyi (32,200). This means we're looking for a district which adds up to 32,200 when adding the population of Ukrainians in the city of Izmayil, which is 32,500. From the table, we can see that the district of Izmayil has a population of Ukrainians of 32,500, which is exactly the same as the population of Ukrainians in the city of Izmayil. Therefore, the answer is None."
    },


    "EXAMPLE_7": {
    "table_info": """
col : round | pick | overall | name | position | college
row 1 : 1 | 32 | 32 | anthony gonzalez | wide receiver | ohio state
row 2 : 2 | 10 | 42 | tony ugoh | offensive tackle | arkansas
row 3 : 3 | 31 | 95 | daymeion hughes | cornerback | california
row 4 : 3 | 34 | 98 | quinn pitcock | defensive tackle | ohio state
row 5 : 4 | 32 | 131 | brannon condren | safety | troy
row 6 : 4 | 37 | 136 | clint session | linebacker | pittsburgh
row 7 : 5 | 32 | 169 | roy hall | wide receiver | ohio state
row 8 : 5 | 36 | 173 | michael coe | cornerback | alabama state
row 9 : 7 | 32 | 232 | keyunta dawson | linebacker | texas tech
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(name, round, college)",
        "f_select_row(row 7)",
        "END"
    ],
    "explanations": [
        "Selecting columns for player name, draft round, and college to focus on the relevant information",
        "Selecting row 7 which contains the Ohio State player drafted in the 5th round"
    ],
    "intermediate_tables": [
        """
col : name | round | college
row 1 : anthony gonzalez | 1 | ohio state
row 2 : tony ugoh | 2 | arkansas
row 3 : daymeion hughes | 3 | california
row 4 : quinn pitcock | 3 | ohio state
row 5 : brannon condren | 4 | troy
row 6 : clint session | 4 | pittsburgh
row 7 : roy hall | 5 | ohio state
row 8 : michael coe | 5 | alabama state
row 9 : keyunta dawson | 7 | texas tech
        """,
        """
col : name | round | college
row 7 : roy hall | 5 | ohio state
        """
    ],
    "question": "According to the table, which player was drafted from Ohio State in the 5th round?",
    "answer": "roy hall",
    "explanation": "To answer this question, we need to find the player who was drafted from Ohio State in the 5th round. Looking at the table, we can see that there are three players from Ohio State: Anthony Gonzalez (round 1), Quinn Pitcock (round 3), and Roy Hall (round 5). Since the question specifically asks about the 5th round, the answer is Roy Hall."
    },


    "EXAMPLE_8": {
    "table_info": """
col : № | Title | Directed by: | Released:
row 1 : 1 | "Kloot's Kounty" | Hawley Pratt | 1973
row 2 : 2 | "Apache on the County Seat" | Hawley Pratt | 1973
row 3 : 3 | "The Shoe Must Go On" | Gerry Chiniquy | 1973
row 4 : 4 | "A Self Winding Sidewinder" | Roy Morita | 1973
row 5 : 5 | "Pay Your Buffalo Bill" | Gerry Chiniquy | 1973
row 6 : 6 | "Stirrups and Hiccups" | Gerry Chiniquy | 1973
row 7 : 7 | "Ten Miles to the Gallop" | Arthur Leonardi | 1973
row 8 : 8 | "Phony Express" | Gerry Chiniquy | 1974
row 9 : 9 | "Giddy Up Woe" | Sid Marcus | 1974
row 10 : 10 | "Gold Struck" | Roy Morita | 1974
row 11 : 11 | "As the Tumbleweeds Turn" | Gerry Chiniquy | 1974
row 12 : 12 | "The Badge and the Beautiful" | Bob Balsar | 1974
row 13 : 13 | "Big Beef at O.K. Corral" | Bob Balsar | 1974
row 14 : 14 | "By Hoot or By Crook" | Bob Balsar | 1974
row 15 : 15 | "Strange on the Range" | Durward Bonaye | 1974
row 16 : 16 | "Mesa Trouble" | Sid Marcus | 1974
row 17 : 17 | "Saddle Soap Opera" | Gerry Chiniquy | 1974
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Directed by:, Released:)",
        "f_select_row(row 8, row 9, row 10, row 11, row 12, row 13, row 14, row 15, row 16, row 17)",
        "f_group_column(Directed by:)",
        "END"
    ],
    "explanations": [
        "Selecting columns for director and release year",
        "Selecting rows for works released in 1974",
        "Grouping the column for director"
    ],
    "intermediate_tables": [
        """
col : Directed by: | Released:
row 1 : Hawley Pratt | 1973
row 2 : Hawley Pratt | 1973
row 3 : Gerry Chiniquy | 1973
row 4 : Roy Morita | 1973
row 5 : Gerry Chiniquy | 1973
row 6 : Gerry Chiniquy | 1973
row 7 : Arthur Leonardi | 1973
row 8 : Gerry Chiniquy | 1974
row 9 : Sid Marcus | 1974
row 10 : Roy Morita | 1974
row 11 : Gerry Chiniquy | 1974
row 12 : Bob Balsar | 1974
row 13 : Bob Balsar | 1974
row 14 : Bob Balsar | 1974
row 15 : Durward Bonaye | 1974
row 16 : Sid Marcus | 1974
row 17 : Gerry Chiniquy | 1974
        """,
        """
col : Directed by: | Released:
row 8 : Gerry Chiniquy | 1974
row 9 : Sid Marcus | 1974
row 10 : Roy Morita | 1974
row 11 : Gerry Chiniquy | 1974
row 12 : Bob Balsar | 1974
row 13 : Bob Balsar | 1974
row 14 : Bob Balsar | 1974
row 15 : Durward Bonaye | 1974
row 16 : Sid Marcus | 1974
row 17 : Gerry Chiniquy | 1974
        """,
        """
col : Directed by | count
row 1 : Gerry Chiniquy | 3
row 2 : Sid Marcus | 2
row 3 : Roy Morita | 1
row 4 : Bob Balsar | 3
row 5 : Durward Bonaye | 1
        """
    ],
    "question": "According to the table, how many works did Gerry Chiniquy direct in 1974?",
    "answer": "3",
    "explanation": """To answer this question, we need to count the number of works directed by Gerry Chiniquy in 1974. From the table, we can see that Gerry Chiniquy directed the following works in 1974:\n1. "Phony Express" (row 8)\n2. "As the Tumbleweeds Turn" (row 11)\n3. "Saddle Soap Opera" (row 17)\n\nTherefore, Gerry Chiniquy directed 3 works in 1974."""
    },


    "EXAMPLE_9": {
    "table_info": """
col : institution | nickname | location | founded | type | enrollment | joined | left
row 1 : university of cincinnati | bearcats | cincinnati , ohio | 1819 | public | 41357 | 1991 | 1995
row 2 : university of dayton | flyers | dayton , ohio | 1850 | private | 11186 | 1993 | 1995
row 3 : depaul university | blue demons | chicago , illinois | 1898 | private | 24966 | 1991 | 1995
row 4 : marquette university | golden eagles | milwaukee , wisconsin | 1881 | private | 12002 | 1991 | 1995
row 5 : university of memphis | tigers | memphis , tennessee | 1912 | public | 22365 | 1991 | 1995
row 6 : saint louis university | billikens | st louis , missouri | 1818 | private | 13785 | 1991 | 1995
    """,
    "chain": [
        "f_select_row()",
        "f_select_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_row(row 1)",
        "f_select_column(nickname, type, enrollment)",
        "END"
    ],
    "explanations": [
        "Selecting row 1 which contains information about the institution founded in 1819",
        "Selecting columns for nickname, type, and enrollment to extract the requested information"
    ],
    "intermediate_tables": [
        """
col : institution | nickname | location | founded | type | enrollment | joined | left
row 1 : university of cincinnati | bearcats | cincinnati , ohio | 1819 | public | 41357 | 1991 | 1995
        """,
        """
col : nickname | type | enrollment
row 1 : bearcats | public | 41357
        """
    ],
    "question": "What is the nickname of the institution founded in 1819, and what is its type and enrollment?",
    "answer": "bearcats, public, 41357",
    "explanation": "To answer this question, we need to identify the institution founded in 1819 and then find its nickname, type, and enrollment. From the table, we can see that the University of Cincinnati was founded in 1819. Its nickname is 'bearcats', it is a 'public' institution, and its enrollment is 41,357."
    },


    "EXAMPLE_10": {
    "table_info": """
col : Club | Season | League Division | League Apps | League Goals | FA Cup Apps | FA Cup Goals | Total Apps | Total Goals
row 1 : Crewe Alexandra | 1946–47 | Third Division North | 23 | 3 | 0 | 0 | 23 | 3
row 2 : Crewe Alexandra | 1947–48 | Third Division North | 42 | 3 | 4 | 0 | 46 | 3
row 3 : Crewe Alexandra | 1948–49 | Third Division North | 41 | 1 | 3 | 0 | 44 | 1
row 4 : Crewe Alexandra | 1949–50 | Third Division North | 39 | 1 | 5 | 0 | 44 | 1
row 5 : Crewe Alexandra | 1950–51 | Third Division North | 25 | 0 | 3 | 0 | 28 | 0
row 6 : Crewe Alexandra | 1951–52 | Third Division North | 6 | 0 | 0 | 0 | 6 | 0
row 7 : Crewe Alexandra | 1952–53 | Third Division North | 2 | 0 | 0 | 0 | 2 | 0
row 8 : Career Total | Career Total | Career Total | 178 | 8 | 15 | 0 | 193 | 8
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "f_change_column_name()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Club, Season, League Goals, Total Apps)",
        "f_select_row(row 1, row 2)",
        "f_change_column_name(Total Apps, Total Appearances)",
        "END"
    ],
    "explanations": [
        "Selecting columns for club, season, league goals, total apps",
        "Selecting rows for the seasons where the player scored 3 goals in the league",
        "Change the column name from Total Apps to Total Appearances"
    ],
    "intermediate_tables": [
        """
col : Club | Season | League Goals | Total Apps
row 1 : Crewe Alexandra | 1946–47 | 3 | 23
row 2 : Crewe Alexandra | 1947–48 | 3 | 46
row 3 : Crewe Alexandra | 1948–49 | 1 | 44
row 4 : Crewe Alexandra | 1949–50 | 1 | 44
row 5 : Crewe Alexandra | 1950–51 | 0 | 28
row 6 : Crewe Alexandra | 1951–52 | 0 | 6
row 7 : Crewe Alexandra | 1952–53 | 0 | 2
row 8 : Career Total | Career Total | Career Total | Career Total
        """,
        """
col : Club | Season | League Goals | Total Apps
row 1 : Crewe Alexandra | 1946–47 | 3 | 23 
row 2 : Crewe Alexandra | 1947–48 | 3 | 46 
        """,
        """
col : Club | Season | League Goals | Total Appearances
row 1 : Crewe Alexandra | 1946–47 | 3 | 23 
row 2 : Crewe Alexandra | 1947–48 | 3 | 46 
        """
    ],
    "question": "In which season did the player score 3 goals in the league, and what was the total number of appearances in that season?",
    "answer": "1946–47, 23, 1947–48, 46",
    "explanation": "To answer this question, we need to identify the seasons in which the player scored 3 goals in the league and find the total number of appearances for those seasons. From the table, we can see that the player scored 3 goals in the league in two seasons:\n1. 1946–47, with 23 total appearances\n2. 1947–48, with 46 total appearances\n\nTherefore, the answer includes both seasons and their respective appearance totals."
    }
}

task_6_EXAMPLES_multi = {
    "EXAMPLE_0": {
            "table_info": """
table_name: Dance Competition
col : rank | couple | judges | public | total | vote percentage | result
row 1 : 1 | ray and maria | 11 | 9 | 20 | 16.179% | safe
row 2 : 2 | coleen and stuart | 7 | 10 | 17 | 24.125% | safe
row 3 : 3 | roxanne and daniel | 8 | 8 | 16 | 7.969% | safe
row 4 : 4 | melinda and fred | 9 | 5 | 14 | 3.253% | safe
row 5 : 5 | jessica and pavel | 10 | 4 | 14 | 2.249% | safe
row 6 : 6 | todd and susie | 1 | 11 | 12 | 33.962% | safe
row 7 : 7 | zoe and matt | 5 | 6 | 11 | 3.399% | safe
row 8 : 8 | donal and florentine | 2 | 7 | 9 | 3.677% | safe
row 9 : 9 | michael and melanie | 7 | 2 | 9 | 1.860% | safe
row 10 : 10 | ellery and frankie | 4 | 3 | 7 | 2.111% | bottom two

table_name: Voting Analysis
col : couple | judges_score_percentage | public_score_percentage | avg_judge_score | performance_rating
row 1 : ray and maria | 55 | 45 | 2.75 | Excellent
row 2 : coleen and stuart | 41.18 | 58.82 | 1.75 | Good
row 3 : roxanne and daniel | 50 | 50 | 2 | Good
row 4 : melinda and fred | 64.29 | 35.71 | 2.25 | Good
row 5 : jessica and pavel | 71.43 | 28.57 | 2.5 | Excellent
row 6 : todd and susie | 8.33 | 91.67 | 0.25 | Poor
row 7 : zoe and matt | 45.45 | 54.55 | 1.25 | Average
row 8 : donal and florentine | 22.22 | 77.78 | 0.5 | Poor
row 9 : michael and melanie | 77.78 | 22.22 | 1.75 | Average
row 10 : ellery and frankie | 57.14 | 42.86 | 1 | Average

foreign_key: couple
""",
"question": "Which couples had a total score greater than 15 and are in the 'safe' result category?",
"answer": "ray and maria, coleen and stuart, roxanne and daniel",
"explanation": "To answer this question, I need to find couples with high scores who are safe from elimination. First, I select the Dance Competition table which contains information about couples' scores and results. Then, I select rows 1, 2, and 3 which correspond to couples with total scores greater than 15 and a 'safe' result. Finally, I select only the couple column to display the names of these couples. From this analysis, I can see that 'ray and maria' (total 20), 'coleen and stuart' (total 17), and 'roxanne and daniel' (total 16) all meet the criteria.",
"chain": [
    "f_select_table()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Dance Competition)",
    "f_select_row(row 1, row 2, row 3)",
    "f_select_column(couple)",
    "END"
],
"explanations": [
    "Selecting the Dance Competition table to work with the data containing total scores and results",
    "Selecting rows 1, 2, and 3 which contain couples with total scores greater than 15 and 'safe' result",
    "Selecting only the couple column to display the names of the couples that meet the criteria"
],
"intermediate_tables": [
    """
col : rank | couple | judges | public | total | vote percentage | result
row 1 : 1 | ray and maria | 11 | 9 | 20 | 16.179% | safe
row 2 : 2 | coleen and stuart | 7 | 10 | 17 | 24.125% | safe
row 3 : 3 | roxanne and daniel | 8 | 8 | 16 | 7.969% | safe
row 4 : 4 | melinda and fred | 9 | 5 | 14 | 3.253% | safe
row 5 : 5 | jessica and pavel | 10 | 4 | 14 | 2.249% | safe
row 6 : 6 | todd and susie | 1 | 11 | 12 | 33.962% | safe
row 7 : 7 | zoe and matt | 5 | 6 | 11 | 3.399% | safe
row 8 : 8 | donal and florentine | 2 | 7 | 9 | 3.677% | safe
row 9 : 9 | michael and melanie | 7 | 2 | 9 | 1.860% | safe
row 10 : 10 | ellery and frankie | 4 | 3 | 7 | 2.111% | bottom two
    """,
    """
col : rank | couple | judges | public | total | vote percentage | result
row 1 : 1 | ray and maria | 11 | 9 | 20 | 16.179% | safe
row 2 : 2 | coleen and stuart | 7 | 10 | 17 | 24.125% | safe
row 3 : 3 | roxanne and daniel | 8 | 8 | 16 | 7.969% | safe
    """,
    """
col : couple
row 1 : ray and maria
row 2 : coleen and stuart
row 3 : roxanne and daniel
    """
]
},
"EXAMPLE_1": {
            "table_info": """
table_name: Companies
col : rank | company | headquarters | industry | employees | reference date
row 1 : 1 | iss | copenhagen , denmark | facility management | 534500 | 2011
row 2 : 2 | securitas | stockholm , sweden | security services | 272425 | 2011
row 3 : 3 | nokia | espoo , finland | technology | 130050 | 2011
row 4 : 4 | ap mãller - maersk | copenhagen , denmark | transportation | 117080 | 2011
row 5 : 5 | ericsson | stockholm , sweden | telecommunication | 104525 | 2011
row 6 : 6 | volvo | gothenburg , sweden | automotive | 98162 | 2011
row 7 : 7 | h&m | stockholm , sweden | retailing | 64874 | 2011
row 8 : 8 | electrolux | stockholm , sweden | manufacturing | 52916 | 2011
row 9 : 9 | skanska | stockholm , sweden | construction | 52557 | 2011
row 10 : 10 | sandvik | sandviken , sweden | capital goods | 50030 | 2011

table_name: Industries
col : industry | total_companies | average_employees
row 1 : telecommunication | 4 | 125000
row 2 : security services | 2 | 136250
row 3 : manufacturing | 3 | 175000
row 4 : facility management | 1 | 534500
row 5 : technology | 1 | 130050
row 6 : retailing | 1 | 64874
row 7 : transportation | 1 | 117080

foreign_key: industry
""",
"question": "Which industry has the highest average employees for the companies listed in the table?",
"answer": "facility management",
"explanation": "To answer this question, I need to find the industry with the highest average number of employees. First, I select the Industries table which contains aggregated data about average employees by industry. Then, I select the columns for industry name and average employees which are relevant to the question. Next, I sort by average employees in descending order to find the industry with the highest value. Finally, I select the first row which contains the industry with the highest average employees. From this analysis, I can see that 'facility management' has the highest average with 534,500 employees.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_sort_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_select_table(Industries)",
    "f_select_column(industry, average_employees)",
    "f_sort_column(average_employees)",
    "f_select_row(row 1)",
    "END"
],
"explanations": [
    "Selecting the Industries table which contains aggregated data about average employees by industry",
    "Selecting columns for industry name and average employees which are relevant to the question",
    "Sorting by average employees in descending order to find the industry with the highest value",
    "Selecting the first row which will contain the industry with the highest average employees"
],
"intermediate_tables": [
    """
col : industry | total_companies | average_employees
row 1 : telecommunication | 4 | 125000
row 2 : security services | 2 | 136250
row 3 : manufacturing | 3 | 175000
row 4 : facility management | 1 | 534500
row 5 : technology | 1 | 130050
row 6 : retailing | 1 | 64874
row 7 : transportation | 1 | 117080
    """,
    """
col : industry | average_employees
row 1 : telecommunication | 125000
row 2 : security services | 136250
row 3 : manufacturing | 175000
row 4 : facility management | 534500
row 5 : technology | 130050
row 6 : retailing | 64874
row 7 : transportation | 117080
    """,
    """
col : industry | average_employees
row 1 : facility management | 534500
row 2 : manufacturing | 175000
row 3 : security services | 136250
row 4 : technology | 130050
row 5 : telecommunication | 125000
row 6 : transportation | 117080
row 7 : retailing | 64874
    """,
    """
col : industry | average_employees
row 1 : facility management | 534500
    """
]
},
"EXAMPLE_2": {
            "table_info": """
table_name: Peaks
col : peak | country | elevation (m) | prominence (m) | col (m)
row 1 : piton des neiges | france ( rãunion ) | 3069 | 3069 | 0
row 2 : maromokotro | madagascar | 2876 | 2876 | 0
row 3 : mount karthala | comoros ( grande comore ) | 2361 | 2361 | 0
row 4 : pic boby | madagascar | 2658 | 1875 | 783
row 5 : tsiafajavona | madagascar | 2643 | 1663 | 980
row 6 : ntingui | comoros ( anjouan ) | 1595 | 1595 | 0

table_name: Countries
col : country | total_peaks | average_elevation
row 1 : france ( rãunion ) | 1 | 3069
row 2 : madagascar | 3 | 2752
row 3 : comoros ( grande comore ) | 1 | 2361
row 4 : madagascar | 1 | 2658
row 5 : comoros ( anjouan ) | 1 | 1595

foreign_key: country
""",
"question": "Did the peak \"piton des neiges\" have an elevation of 3069 meters and the country it belongs to has a total of 1 peak?",
"answer": "yes",
"explanation": "To answer this question, I need to verify two facts: the elevation of 'piton des neiges' and whether its country has exactly 1 peak. First, I join the Peaks and Countries tables to connect peak information with country data. Then, I select row 1 which corresponds to the peak 'piton des neiges'. Finally, I select the columns for peak name, elevation, country, and total peaks to isolate the relevant information. From this data, I can confirm that 'piton des neiges' has an elevation of 3069 meters and its country 'france ( rãunion )' has a total of 1 peak, so the answer is 'yes'.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Peaks, Countries)",
    "f_select_row(row 1)",
    "f_select_column(peak, elevation (m), country, total_peaks)",
    "END"
],
"explanations": [
    "Joining the Peaks and Countries tables to get the country of the peak",
    "Selecting row 1 which corresponds to the peak 'piton des neiges'",
    "Selecting the columns for peak name, elevation, country, and total peaks to isolate the relevant information"
],
"intermediate_tables": [
    """
col : peak | country | elevation (m) | prominence (m) | col (m)
row 1 : piton des neiges | france ( rãunion ) | 3069 | 3069 | 0
row 2 : maromokotro | madagascar | 2876 | 2876 | 0
row 3 : mount karthala | comoros ( grande comore ) | 2361 | 2361 | 0
row 4 : pic boby | madagascar | 2658 | 1875 | 783
row 5 : tsiafajavona | madagascar | 2643 | 1663 | 980
row 6 : ntingui | comoros ( anjouan ) | 1595 | 1595 | 0
    """,
    """
col : peak | country | elevation (m) | prominence (m) | col (m)
row 1 : piton des neiges | france ( rãunion ) | 3069 | 3069 | 0
    """,
    """
col : peak | elevation (m) | country | total_peaks
row 1 : piton des neiges | 3069 | france ( rãunion ) | 1
    """
]
},
"EXAMPLE_3": {
            "table_info": """
table_name: Couples
col : couple | style | music | trine dehli cleve | tor fløysvik | karianne gulliksen | christer tornell | total
row 1 : åsleik & nadia | cha - cha - cha | ymca - village people | 8 | 8 | 8 | 8 | 32
row 2 : stig & alexandra | pasodoble | eye of the tiger - survivor | 6 | 5 | 6 | 7 | 24
row 3 : stine & tom - erik | rumba | la isla bonita - madonna | 6 | 6 | 7 | 6 | 25
row 4 : cecilie & tobias | tango | twist in my sobriety - tanita tikaram | 5 | 4 | 6 | 6 | 21
row 5 : håvard & elena | cha - cha - cha | never gonna give you up - rick astley | 8 | 7 | 8 | 7 | 30
row 6 : maria & asmund | english waltz | i have nothing - whitney houston | 7 | 5 | 7 | 6 | 25
row 7 : aylar & egor | tango | that don't impress me much - shania twain | 8 | 9 | 8 | 8 | 33

table_name: Songs
col : song | artist | album | year | genre
row 1 : YMCA - Village People | Village People | YMCA | 1978 | Disco
row 2 : Eye of the Tiger - Survivor | Survivor | Eye of the Tiger | 1982 | Rock
row 3 : La Isla Bonita - Madonna | Madonna | Like a Virgin | 1984 | Pop
row 4 : Suspicious Minds - Johnny Nash | Johnny Nash | Suspicious Minds | 1972 | Reggae
row 5 : Never Gonna Give You Up - Rick Astley | Rick Astley | Whenever You Need Somebody | 1987 | Pop
row 6 : I Have Nothing - Whitney Houston | Whitney Houston | The Bodyguard | 1992 | R&B
row 7 : That Don't Impress Me Much - Shania Twain | Shania Twain | Come On Over | 1999 | Country

foreign_key: music
""",
"question": "How many total points did the couple \"åsleik & nadia\" score across all judges in the dance competition?",
"answer": "32",
"explanation": "To answer this question, I need to find the total points scored by the couple 'åsleik & nadia'. First, I select the Couples table which contains the scoring information. Then, I select row 1 which corresponds to 'åsleik & nadia'. Finally, I select the couple name and total columns to isolate the relevant information. From this data, I can see that 'åsleik & nadia' scored a total of 32 points across all judges.",
"chain": [
    "f_select_table()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Couples)",
    "f_select_row(row 1)",
    "f_select_column(couple, total)",
    "END"
],
"explanations": [
    "Selecting the Couples table which contains information about couples' scores",
    "Selecting row 1 which corresponds to the couple 'åsleik & nadia'",
    "Selecting the columns for couple name and total score to isolate the relevant information"
],
"intermediate_tables": [
    """
col : couple | style | music | trine dehli cleve | tor fløysvik | karianne gulliksen | christer tornell | total
row 1 : åsleik & nadia | cha - cha - cha | ymca - village people | 8 | 8 | 8 | 8 | 32
row 2 : stig & alexandra | pasodoble | eye of the tiger - survivor | 6 | 5 | 6 | 7 | 24
row 3 : stine & tom - erik | rumba | la isla bonita - madonna | 6 | 6 | 7 | 6 | 25
row 4 : cecilie & tobias | tango | twist in my sobriety - tanita tikaram | 5 | 4 | 6 | 6 | 21
row 5 : håvard & elena | cha - cha - cha | never gonna give you up - rick astley | 8 | 7 | 8 | 7 | 30
row 6 : maria & asmund | english waltz | i have nothing - whitney houston | 7 | 5 | 7 | 6 | 25
row 7 : aylar & egor | tango | that don't impress me much - shania twain | 8 | 9 | 8 | 8 | 33
    """,
    """
col : couple | style | music | trine dehli cleve | tor fløysvik | karianne gulliksen | christer tornell | total
row 1 : åsleik & nadia | cha - cha - cha | ymca - village people | 8 | 8 | 8 | 8 | 32
    """,
    """
col : couple | total
row 1 : åsleik & nadia | 32
    """
]
},
"EXAMPLE_4": {
            "table_info": """
table_name: Channels
col : Position | Channel | Owner | Share of total viewing (%) in 2018 | Share of total viewing (%) in 2011 | Comparison 2018/2011
row 1 : 1 | ZDF | ZDFo | 13.9 | 12.1 | (1.8)
row 2 : 2 | Das Erste | ARD | 11.5 | 12.4 | (0.9)
row 3 : 3 | RTL | RTL Group | 8.3 | 14.1 | (5.8)
row 4 : 4 | SAT.1 | ProSiebenSat.1 Media | 6.2 | 10.1 | (3.9)
row 5 : 5 | VOX | RTL Group | 4.8 | 5.6 | (0.8)
row 6 : 6 | ProSieben | ProSiebenSat.1 Media | 4.4 | 6.2 | (1.8)
row 7 : 7 | kabel eins | ProSiebenSat.1 Media | 3.5 | 4.1 | (0.6)
row 8 : 8 | ZDFneo | ZDF | 3.2 | 0.4 | (2.8)
row 9 : 9 | RTL II | RTL Group | 3.0 | 3.6 | (0.6)

table_name: Owners
col : Owner | total_channels | average_share
row 1 : ZDFo | 3 | 13.9
row 2 : ARD | 2 | 11.5
row 3 : RTL Group | 3 | 14.1
row 4 : ProSiebenSat.1 Media | 2 | 10.1
row 5 : RTL Group | 2 | 5.6
row 6 : ProSieben | 1 | 6.2
row 7 : ProSiebenSat.1 Media | 1 | 4.1
row 8 : ZDF | 1 | 0.4
row 9 : RTL Group | 1 | 3.6

foreign_key: Owner
""",
"question": "What is the channel name of the channel owned by ZDF, and what is its viewing share in 2018? and the owner's total channels?",
"answer": "ZDFneo, 3.2%, 1",
"explanation": "To answer this question, I need to find the channel owned by ZDF and determine its viewing share and the owner's total channels. First, I join the Channels and Owners tables to combine the information. Then, I select row 8 which corresponds to 'ZDFneo' owned by 'ZDF'. Finally, I select the relevant columns to display the channel name, position, viewing share in 2018, owner, and total channels. From this data, I can see that ZDFneo has a viewing share of 3.2% in 2018 and the owner (ZDF) has 1 total channel.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Channels, Owners)",
    "f_select_row(row 8)",
    "f_select_column(Channel, Position, Share of total viewing (%) in 2018, Owner, total_channels)",
    "END"
],
"explanations": [
    "Joining the Channels and Owners tables to get the owner of the channel",
    "Selecting row 8 which corresponds to the channel 'ZDFneo' owned by 'ZDF'",
    "Selecting the columns for channel name, position, share of total viewing in 2018, owner, and total channels to isolate the relevant information"
],
"intermediate_tables": [
    """
col : Position | Channel | Owner | Share of total viewing (%) in 2018 | Share of total viewing (%) in 2011 | Comparison 2018/2011
row 1 : 1 | ZDF | ZDFo | 13.9 | 12.1 | (1.8)
row 2 : 2 | Das Erste | ARD | 11.5 | 12.4 | (0.9)
row 3 : 3 | RTL | RTL Group | 8.3 | 14.1 | (5.8)
row 4 : 4 | SAT.1 | ProSiebenSat.1 Media | 6.2 | 10.1 | (3.9)
row 5 : 5 | VOX | RTL Group | 4.8 | 5.6 | (0.8)
row 6 : 6 | ProSieben | ProSiebenSat.1 Media | 4.4 | 6.2 | (1.8)
row 7 : 7 | kabel eins | ProSiebenSat.1 Media | 3.5 | 4.1 | (0.6)
row 8 : 8 | ZDFneo | ZDF | 3.2 | 0.4 | (2.8)
row 9 : 9 | RTL II | RTL Group | 3.0 | 3.6 | (0.6)
    """,
    """
col : Position | Channel | Owner | Share of total viewing (%) in 2018 | Share of total viewing (%) in 2011 | Comparison 2018/2011
row 8 : 8 | ZDFneo | ZDF | 3.2 | 0.4 | (2.8)
    """,
    """
col : Channel | Position | Share of total viewing (%) in 2018 | Owner | total_channels
row 8 : ZDFneo | 8 | 3.2 | ZDF | 1
    """
]
},
"EXAMPLE_5": {
            "table_info": """
table_name: Population Demographics
col : Particulars | Total | Male | Female
row 1 : Total No. of Houses | 92 | - | -
row 2 : Population | 479 | 250 | 229
row 3 : Child (0-6) | 49 | 23 | 26
row 4 : Schedule Caste | 228 | 117 | 111
row 5 : Schedule Tribe | 0 | 0 | 0
row 6 : Literacy | 78.14 % | 87.67 % | 67.49 %
row 7 : Total Workers | 144 | 130 | 14
row 8 : Main Worker | 138 | 0 | 0
row 9 : Marginal Worker | 6 | 4 | 2

table_name: Employment Analysis
col : Worker Type | Gender | Count | Percentage
row 1 : Main Worker | Male | 0 | 0.00
row 2 : Main Worker | Female | 0 | 0.00
row 3 : Marginal Worker | Male | 4 | 66.67
row 4 : Marginal Worker | Female | 2 | 33.33
row 5 : Total Worker | Male | 130 | 90.28
row 6 : Total Worker | Female | 14 | 9.72
row 7 : Non-Worker | Male | 120 | 35.82
row 8 : Non-Worker | Female | 215 | 64.18

foreign_key: Worker Type
""",
"question": "Which worker type and gender has a percentage of workers that, when added to the percentage of female total workers, equals 43.05%?",
"answer": "Marginal Worker, Female",
"explanation": "To answer this question, I need to find a worker type and gender combination that, when added to female total workers, equals 43.05%. First, I select the Employment Analysis table which contains worker percentages. Then, I select rows 4 (Marginal Worker, Female) and 6 (Total Worker, Female) to analyze their percentages. Next, I add an inferred column to calculate the combined percentage of each row with the female total worker percentage (9.72%). Then, I select the row where the combined percentage equals 43.05%, which is row 1 of the result. Finally, I select the relevant columns to display the worker type, gender, individual percentage (33.33%), and combined percentage (43.05%). This shows that 'Marginal Worker, Female' is the answer.",
"chain": [
    "f_select_table()",
    "f_select_row()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Employment Analysis)",
    "f_select_row(row 4, row 6)",
    "f_add_inferred_column(combined_percentage)",
    "f_select_row(row 1)",
    "f_select_column(Worker Type, Gender, Percentage, combined_percentage)",
    "END"
],
"explanations": [
    "Selecting the Employment Analysis table which contains information about worker percentages",
    "Selecting row 4 (Marginal Worker, Female) and row 6 (Total Worker, Female) to analyze their percentages",
    "Adding an inferred column to calculate the combined percentage of each row with the female total worker percentage",
    "Selecting the row where the combined percentage equals 43.05%",
    "Selecting relevant columns to display the worker type, gender, individual percentage, and combined percentage"
],
"intermediate_tables": [
    """
col : Worker Type | Gender | Count | Percentage
row 1 : Main Worker | Male | 0 | 0.00
row 2 : Main Worker | Female | 0 | 0.00
row 3 : Marginal Worker | Male | 4 | 66.67
row 4 : Marginal Worker | Female | 2 | 33.33
row 5 : Total Worker | Male | 130 | 90.28
row 6 : Total Worker | Female | 14 | 9.72
row 7 : Non-Worker | Male | 120 | 35.82
row 8 : Non-Worker | Female | 215 | 64.18
    """,
    """
col : Worker Type | Gender | Count | Percentage
row 4 : Marginal Worker | Female | 2 | 33.33
row 6 : Total Worker | Female | 14 | 9.72
    """,
    """
col : Worker Type | Gender | Count | Percentage | combined_percentage
row 4 : Marginal Worker | Female | 2 | 33.33 | 43.05
row 6 : Total Worker | Female | 14 | 9.72 | 19.44
    """,
    """
col : Worker Type | Gender | Count | Percentage | combined_percentage
row 4 : Marginal Worker | Female | 2 | 33.33 | 43.05
    """,
    """
col : Worker Type | Gender | Percentage | combined_percentage
row 4 : Marginal Worker | Female | 33.33 | 43.05
    """
]
}
}