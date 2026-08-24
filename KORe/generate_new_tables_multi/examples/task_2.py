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

task_2_EXAMPLES_single = {
    "EXAMPLE_1": {
        "table_info": """
table_name: Swimming Results
col : Rank | Name | Nationality | Time | Notes
row 1 : 1 | Janelle Atkinson | Jamaica | 4:16.89 | Q
row 2 : 2 | - | - | - | Q
row 3 : 3 | Kaitlin Sandeno | United States | 4:18.97 | Q
row 4 : 4 | Julia Stowers | United States | 4:19.84 | Q
row 5 : 5 | - | - | - | Q
row 6 : 6 | - | - | - | Q
row 7 : 7 | - | - | - | Q
row 8 : 8 | - | - | - | Q

table_name: Swimmer Details
col : Event ID | Swimmer | Competition Phase | Personal Best
row 1 : E001 | Janelle Atkinson | Heats | 4:14.22
row 2 : E001 | Unknown | Heats | N/A
row 3 : E001 | Kaitlin Sandeno | Heats | 4:17.15
row 4 : E001 | Julia Stowers | Heats | 4:18.50
row 5 : E001 | Unknown | Heats | N/A
row 6 : E001 | Unknown | Heats | N/A
row 7 : E001 | Unknown | Heats | N/A
row 8 : E001 | Unknown | Heats | N/A

foreign_key: Name, Swimmer
""",
        "chain": [
            "f_select_table()",
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_table(Swimming Results)",
            "f_select_column(Rank)",
            "f_add_inferred_column(count)",
            "END"
        ],
        "explanations": [
            "Selecting the Swimming Results table which contains the list of all competing swimmers",
            "Selecting the Rank column which uniquely identifies each swimmer position",
            "Adding an inferred column to count the total number of swimmers listed"
        ],
        "intermediate_tables": [
            """
col : Rank | Name | Nationality | Time | Notes
row 1 : 1 | Janelle Atkinson | Jamaica | 4:16.89 | Q
row 2 : 2 | - | - | - | Q
row 3 : 3 | Kaitlin Sandeno | United States | 4:18.97 | Q
row 4 : 4 | Julia Stowers | United States | 4:19.84 | Q
row 5 : 5 | - | - | - | Q
row 6 : 6 | - | - | - | Q
row 7 : 7 | - | - | - | Q
row 8 : 8 | - | - | - | Q
            """,
            """
col : Rank
row 1 : 1
row 2 : 2
row 3 : 3
row 4 : 4
row 5 : 5
row 6 : 6
row 7 : 7
row 8 : 8
            """,
            """
col : Rank | count
row 1 : Total | 8
            """
        ],
        "question": "How many swimmers are listed?",
        "answer": "8",
        "explanation": "To determine how many swimmers are listed, I need to count all the swimmers in the event. While some swimmers' names are not given (shown as '-' in the Swimming Results table), each row represents a distinct swimmer who qualified for the competition. By selecting the Rank column from the Swimming Results table and adding an inferred column to count the total entries, I can determine that there are 8 swimmers listed in total."
    },
    
    "EXAMPLE_2": {
        "table_info": """
table_name: Chinese Names
col :  | Chinese | Pinyin | Cantonese Yale | Hakka pinjim
row 1 : Ma Ling-Yee | 馬寧兒 | Mǎ Níngér | Ma5 Ning4 Yi4 | 
row 2 : Fung Do-Dak | 馮道德 | Féng Dàodé | Fung4 Dou6 Dak1 | 
row 3 : Gwong Wai | 廣慧禪師 | Guǎng Huì Chán Shī | Gwong2 Wai6 Sim3 Si1 | 
row 4 : Juk Faat Wan | 竺法雲禪師 | Zhú Fǎ Yún Chán Shī | Juk1 Faat3 Wan4 Sim3 Si1 | 
row 5 : Fung Foh Do Yan | 風火道人 | Fēng Huǒ Dào Rén | Fung1 Fo2 Dou6 Yan4 | 
row 6 : Lau Siu-Leung | 刘少良 | Liú Shǎoliáng | Lau4 Siu2 Leung4 | 
row 7 : Shek Lam | 石林 | Shí Lín | Sek6 Lam4 | Shak8 Lam2
row 8 : Wanderer Style | 流民派 | Liúmín Pài | Lau4 man4 Paai1 | Liu2 min2 Pai5
row 9 : Lei Mung | 李朦 | Lǐ Méng | Lei5 Mung4 | Li3 Mung2
row 10 : Lin Sang | 蓮生 | Lián Shēng | Lin4 Sang1 | Len2 Sang1

table_name: Name Details
col : Name | Region | Style | Historical Period
row 1 : Ma Ling-Yee | Northern China | Traditional | Ming Dynasty
row 2 : Fung Do-Dak | Southern China | Traditional | Qing Dynasty
row 3 : Gwong Wai | Canton | Monastic | Early Republic
row 4 : Juk Faat Wan | Canton | Monastic | Ming Dynasty
row 5 : Fung Foh Do Yan | Central China | Taoist | Tang Dynasty
row 6 : Lau Siu-Leung | Hong Kong | Modern | Contemporary
row 7 : Shek Lam | Hakka Region | Traditional | Qing Dynasty
row 8 : Wanderer Style | Various | Nomadic | Various
row 9 : Lei Mung | Southern China | Modern | Republic
row 10 : Lin Sang | Eastern China | Traditional | Song Dynasty

foreign_key: Name
""",
        "chain": [
            "f_select_table()",
            "f_select_row()",
            "f_select_column()",
            "f_stitch_tables()",
            "f_select_column()",
            "f_select_row()",
            "END"
        ],
        "filled_chain": [
            "f_select_table(Name Details)",
            "f_select_row(row 4)",
            "f_select_column(Historical Period)",
            "f_stitch_tables(Name Details.Name, Chinese Names., inner)",
            "f_select_column(Name, Historical Period)",
            "f_select_row(row 1, row 4)",
            "END"
        ],
        "explanations": [
            "Selecting the Name Details table to access historical period information",
            "Selecting row 4 which corresponds to Juk Faat Wan to identify their historical period",
            "Selecting the Historical Period column to see that Juk Faat Wan lived during the Ming Dynasty",
            "Joining the Name Details table with the Chinese Names table to get complete information",
            "Selecting Name and Historical Period columns to focus on identifying people from the same period",
            "Selecting rows for individuals from the Ming Dynasty period (same as Juk Faat Wan)"
        ],
        "intermediate_tables": [
            """
col : Name | Region | Style | Historical Period
row 1 : Ma Ling-Yee | Northern China | Traditional | Ming Dynasty
row 2 : Fung Do-Dak | Southern China | Traditional | Qing Dynasty
row 3 : Gwong Wai | Canton | Monastic | Early Republic
row 4 : Juk Faat Wan | Canton | Monastic | Ming Dynasty
row 5 : Fung Foh Do Yan | Central China | Taoist | Tang Dynasty
row 6 : Lau Siu-Leung | Hong Kong | Modern | Contemporary
row 7 : Shek Lam | Hakka Region | Traditional | Qing Dynasty
row 8 : Wanderer Style | Various | Nomadic | Various
row 9 : Lei Mung | Southern China | Modern | Republic
row 10 : Lin Sang | Eastern China | Traditional | Song Dynasty
            """,
            """
col : Name | Region | Style | Historical Period
row 1 : Juk Faat Wan | Canton | Monastic | Ming Dynasty
            """,
            """
col : Historical Period
row 1 : Ming Dynasty
            """,
            """
col : Name | Chinese | Pinyin | Cantonese Yale | Hakka pinjim | Region | Style | Historical Period
row 1 : Ma Ling-Yee | 馬寧兒 | Mǎ Níngér | Ma5 Ning4 Yi4 |  | Northern China | Traditional | Ming Dynasty
row 2 : Fung Do-Dak | 馮道德 | Féng Dàodé | Fung4 Dou6 Dak1 |  | Southern China | Traditional | Qing Dynasty
row 3 : Gwong Wai | 廣慧禪師 | Guǎng Huì Chán Shī | Gwong2 Wai6 Sim3 Si1 |  | Canton | Monastic | Early Republic
row 4 : Juk Faat Wan | 竺法雲禪師 | Zhú Fǎ Yún Chán Shī | Juk1 Faat3 Wan4 Sim3 Si1 |  | Canton | Monastic | Ming Dynasty
row 5 : Fung Foh Do Yan | 風火道人 | Fēng Huǒ Dào Rén | Fung1 Fo2 Dou6 Yan4 |  | Central China | Taoist | Tang Dynasty
row 6 : Lau Siu-Leung | 刘少良 | Liú Shǎoliáng | Lau4 Siu2 Leung4 |  | Hong Kong | Modern | Contemporary
row 7 : Shek Lam | 石林 | Shí Lín | Sek6 Lam4 | Shak8 Lam2 | Hakka Region | Traditional | Qing Dynasty
row 8 : Wanderer Style | 流民派 | Liúmín Pài | Lau4 man4 Paai1 | Liu2 min2 Pai5 | Various | Nomadic | Various
row 9 : Lei Mung | 李朦 | Lǐ Méng | Lei5 Mung4 | Li3 Mung2 | Southern China | Modern | Republic
row 10 : Lin Sang | 蓮生 | Lián Shēng | Lin4 Sang1 | Len2 Sang1 | Eastern China | Traditional | Song Dynasty
            """,
            """
col : Name | Historical Period
row 1 : Ma Ling-Yee | Ming Dynasty
row 2 : Fung Do-Dak | Qing Dynasty
row 3 : Gwong Wai | Early Republic
row 4 : Juk Faat Wan | Ming Dynasty
row 5 : Fung Foh Do Yan | Tang Dynasty
row 6 : Lau Siu-Leung | Contemporary
row 7 : Shek Lam | Qing Dynasty
row 8 : Wanderer Style | Various
row 9 : Lei Mung | Republic
row 10 : Lin Sang | Song Dynasty
            """,
            """
col : Name | Historical Period
row 1 : Ma Ling-Yee | Ming Dynasty
row 2 : Juk Faat Wan | Ming Dynasty
            """
        ],
        "question": "Who lived in the same period as Juk Faat Wan?",
        "answer": "Ma Ling-Yee",
        "explanation": "To find who lived in the same period as Juk Faat Wan, I need to first identify which historical period Juk Faat Wan belongs to, then find other individuals from the same period. I start by selecting the Name Details table and finding row 4 which corresponds to Juk Faat Wan. By examining the Historical Period column, I can see that Juk Faat Wan lived during the Ming Dynasty. After joining both tables to get complete information, I focus on the Name and Historical Period columns and then select rows for individuals from the Ming Dynasty period, which reveals that Ma Ling-Yee also lived during this period."
    },
    
    "EXAMPLE_3": {
        "table_info": """
col : Date | Constituency | Gain | Loss | Note
row 1 : 30 May 1963 | Dublin North–East | Fine Gael | Fine Gael | Paddy Belton (FG) holds the seat vacated by the death of his brother Jack Belton (FG)
row 2 : 27 October 1963 | Dublin South–East | Labour Party | National Progressive Democrats | Noël Browne (NPD) disbands the National Progressive Democrats and joins the Labour Party
row 3 : 27 October 1963 | Roscommon | Labour Party | National Progressive Democrats | Jack McQuillan (NPD) disbands the National Progressive Democrats and joins the Labour Party
row 4 : 27 October 1963 | Dublin County | Labour Party | Independent | Seán Dunne (Ind) joins the Labour Party
row 5 : 19 February 1964 | Cork Borough | Fianna Fáil | Fianna Fáil | Sheila Galvin (FF) wins the seat vacated by the death of her husband John Galvin (FF)
row 6 : 19 February 1964 | Kildare | Fianna Fáil | Labour Party | Terence Boylan (FF) wins the seat vacated by the death of William Norton (Lab)
row 7 : 8 July 1964 | Roscommon | Fine Gael | Fine Gael | Joan Burke (FG) holds the seat vacated by the death of her husband James Burke (FG)
row 8 : 3 December 1964 | Galway East | Fine Gael | Clann na Talmhan | John Donnellan (FG) wins the seat vacated by the death of his father Michael Donnellan (CnaT)
row 9 : 10 March 1965 | Cork Mid | Labour Party | Labour Party | Eileen Desmond (Lab) holds the seat vacated by the death of her husband Dan Desmond (Lab)
        """,
        "chain": [
            "f_select_column()",
            "f_group_column()",
            "f_sort_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Date)",
            "f_group_column(Date)",
            "f_sort_column(count)",
            "END"
        ],
        "explanations": [
            "Selecting the Date column to analyze the dates listed in the table",
            "Grouping by Date to count the number of unique dates in the table",
            "Sorting by count to identify the most frequent dates"
        ],
        "intermediate_tables": [
            """
col : Date
row 1 : 30 May 1963
row 2 : 27 October 1963
row 3 : 27 October 1963
row 4 : 27 October 1963
row 5 : 19 February 1964
row 6 : 19 February 1964
row 7 : 8 July 1964
row 8 : 3 December 1964
row 9 : 10 March 1965
            """,
            """
col : Date | count
row 1 : 30 May 1963 | 1
row 2 : 27 October 1963 | 3
row 5 : 19 February 1964 | 2
row 7 : 8 July 1964 | 1
row 8 : 3 December 1964 | 1
row 9 : 10 March 1965 | 1
            """,
            """
col : Date | count
row 1 : 27 October 1963 | 3
row 2 : 19 February 1964 | 2
row 3 : 30 May 1963 | 1
row 4 : 8 July 1964 | 1
row 5 : 3 December 1964 | 1
row 6 : 10 March 1965 | 1
            """
        ],
        "question": "How many dates are listed?",
        "answer": "6",
        "explanation": "To determine the number of dates listed in the table, I selected the Date column to analyze all entries, then grouped them by unique date to count the occurrences of each. Finally, I sorted by count to identify the most frequent dates. While some dates appear multiple times (like 27 October 1963 appearing three times), the total number of unique dates is 6."
    },
    
    "EXAMPLE_4": {
        "table_info": """
table_name: Race Results
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
row 3 : 3 | 9 | Justin Wilson | RSPORTS | 73 | +3.480 | 2 | 25
row 4 : 4 | 15 | Simon Pagenaud | Team Australia | 73 | +5.643 | 4 | 23
row 5 : 5 | 19 | Bruno Junqueira | Dale Coyne Racing | 73 | +20.738 | 5 | 21
row 6 : 6 | 14 | Robert Doornbos | Minardi Team USA | 72 | + 1 Lap | 12 | 19
row 7 : 7 | 28 | Ryan Dalziel | Pacific Coast Motorsports | 72 | + 1 Lap | 11 | 17
row 8 : 8 | 8 | Alex Tagliani | RSPORTS | 71 | + 2 Laps | 6 | 15
row 9 : 9 | 1 | Sébastien Bourdais | N/H/L Racing | 67 | Contact | 1 | 16
row 10 : 10 | 7 | Oriol Servia | Forsythe Racing | 56 | Contact | 3 | 11
row 11 : 11 | 2 | Graham Rahal | N/H/L Racing | 52 | Contact | 15 | 10
row 12 : 12 | 4 | Dan Clarke | Minardi Team USA | 43 | Contact | 13 | 9
row 13 : 13 | 34 | Jan Heylen | Conquest Racing | 1 | Contact | 8 | 8
row 14 : 14 | 3 | Paul Tracy | Forsythe Racing | 0 | Contact | 10 | 7
row 15 : 15 | 22 | Tristan Gommendy | PKV Racing | 0 | Contact | 14 | 6
row 16 : 16 | 11 | Katherine Legge | Dale Coyne Racing | 0 | Contact | 16 | 5
row 17 : 17 | 29 | Alex Figge | Pacific Coast Motorsports | 0 | Contact | 17 | 4

table_name: Team Details
col : Team | Chassis | Engine | Tire | Base
row 1 : Team Australia | Panoz DP01 | Cosworth XFE | Bridgestone | Indianapolis
row 2 : PKV Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Indianapolis
row 3 : RSPORTS | Panoz DP01 | Cosworth XFE | Bridgestone | Michigan
row 4 : Dale Coyne Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Illinois
row 5 : Minardi Team USA | Panoz DP01 | Cosworth XFE | Bridgestone | Indiana
row 6 : Pacific Coast Motorsports | Panoz DP01 | Cosworth XFE | Bridgestone | California
row 7 : N/H/L Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Illinois
row 8 : Forsythe Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Arizona
row 9 : Conquest Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Indiana

foreign_key: Team
""",
        "question": "How many more points did the winner get than the second place driver?",
        "answer": "3",
        "explanation": "To find out how many more points the winner received compared to the second place driver, I need to identify the points for the first and second-place finishers and calculate the difference. Looking at the Race Results table, Will Power finished in first place with 31 points, while Neel Jani finished second with 28 points. The difference between them is 3 points (31 - 28 = 3).",
        "chain": [
            "f_select_table()",
            "f_select_row()",
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_table(Race Results)",
            "f_select_row(row 1, row 2)",
            "f_select_column(Driver, Points)",
            "f_add_inferred_column(points_difference)",
            "END"
        ],
        "explanations": [
            "Selecting the Race Results table to access driver positions and points information",
            "Selecting rows 1 and 2 which correspond to the first and second place drivers",
            "Selecting the Driver and Points columns to focus on the points each driver earned",
            "Adding an inferred column to calculate the difference in points between the first and second place drivers"
        ],
        "intermediate_tables": [
            """
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
row 3 : 3 | 9 | Justin Wilson | RSPORTS | 73 | +3.480 | 2 | 25
row 4 : 4 | 15 | Simon Pagenaud | Team Australia | 73 | +5.643 | 4 | 23
row 5 : 5 | 19 | Bruno Junqueira | Dale Coyne Racing | 73 | +20.738 | 5 | 21
row 6 : 6 | 14 | Robert Doornbos | Minardi Team USA | 72 | + 1 Lap | 12 | 19
row 7 : 7 | 28 | Ryan Dalziel | Pacific Coast Motorsports | 72 | + 1 Lap | 11 | 17
row 8 : 8 | 8 | Alex Tagliani | RSPORTS | 71 | + 2 Laps | 6 | 15
row 9 : 9 | 1 | Sébastien Bourdais | N/H/L Racing | 67 | Contact | 1 | 16
row 10 : 10 | 7 | Oriol Servia | Forsythe Racing | 56 | Contact | 3 | 11
row 11 : 11 | 2 | Graham Rahal | N/H/L Racing | 52 | Contact | 15 | 10
row 12 : 12 | 4 | Dan Clarke | Minardi Team USA | 43 | Contact | 13 | 9
row 13 : 13 | 34 | Jan Heylen | Conquest Racing | 1 | Contact | 8 | 8
row 14 : 14 | 3 | Paul Tracy | Forsythe Racing | 0 | Contact | 10 | 7
row 15 : 15 | 22 | Tristan Gommendy | PKV Racing | 0 | Contact | 14 | 6
row 16 : 16 | 11 | Katherine Legge | Dale Coyne Racing | 0 | Contact | 16 | 5
row 17 : 17 | 29 | Alex Figge | Pacific Coast Motorsports | 0 | Contact | 17 | 4
            """,
            """
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
            """,
            """
col : Driver | Points
row 1 : Will Power | 31
row 2 : Neel Jani | 28
            """,
            """
col : Driver | Points | points_difference
row 1 : Will Power | 31 | 3
row 2 : Neel Jani | 28 | -
            """
        ],
        "question": "How many more points did the winner get than the second place driver?",
        "answer": "3"
    },
    
    "EXAMPLE_5": {
        "table_info": """
col : Terminal | Operator | Depth (m) | Berths | Quay length (m) | Quay cranes | Area (m²) | Capacity (kTEUs)
row 1 : Terminal 1 (CT1) | MTL | 14 | 1 | | 4 | | 
row 2 : Terminal 2 (CT2) | MTL | 14 | 1 | | 5 | | 
row 3 : Terminal 3 (CT3) | DPI | 14 | 1 | 305 | 6 | 167,000 | >1,200
row 4 : Terminal 4 (CT4) | HIT | 12.5 | 3 | | 8 | | 
row 5 : Terminal 5 (CT5) | MTL | 14 | 1 | | 4 | | 
row 6 : Terminal 6 (CT6) | HIT | 12.5-15.5 | 3 | | 11 | | 
row 7 : Terminal 7 (CT7) | HIT | 15.5 | 4 | | 15 | | 
row 8 : Terminal 8 East (CT8E) | HIT/COSCO | 15.5 | 2 | 640 | 9 | 300,000 | 1,800
row 9 : Terminal 8 West (CT8W) | ACT | 15.5 | 2 | 740 | 8 | 285,000 | >2,000
row 10 : Terminal 9 North (CT9N) | HIT | 15.5 | 2 | 700 | 9 | 190,000 | >2,600 (N&S)
row 11 : Terminal 9 South (CT9S) | MTL | 15.5 | 4 | 1,240 | 13 | 490,000 | 
        """,
        "chain": [
            "f_select_column()",
            "f_sort_column()",
            "f_select_row()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Terminal, Quay cranes)",
            "f_sort_column(Quay cranes)",
            "f_select_row(row 1, row 2)",
            "END"
        ],
        "explanations": [
            "Selecting Terminal and Quay cranes columns to identify terminals with more cranes than Terminal 6",
            "Sorting the Quay cranes column in descending order to rank terminals from highest to lowest number of cranes",
            "Selecting rows for terminals with more quay cranes than Terminal 6, which has 11 cranes (rows 1 and 2 after sorting)"
        ],
        "intermediate_tables": [
            """
col : Terminal | Quay cranes
row 1 : Terminal 1 (CT1) | 4
row 2 : Terminal 2 (CT2) | 5
row 3 : Terminal 3 (CT3) | 6
row 4 : Terminal 4 (CT4) | 8
row 5 : Terminal 5 (CT5) | 4
row 6 : Terminal 6 (CT6) | 11
row 7 : Terminal 7 (CT7) | 15
row 8 : Terminal 8 East (CT8E) | 9
row 9 : Terminal 8 West (CT8W) | 8
row 10 : Terminal 9 North (CT9N) | 9
row 11 : Terminal 9 South (CT9S) | 13
            """,
            """
col : Terminal | Quay cranes
row 1 : Terminal 7 (CT7) | 15
row 2 : Terminal 9 South (CT9S) | 13
row 3 : Terminal 6 (CT6) | 11
row 4 : Terminal 8 East (CT8E) | 9
row 5 : Terminal 9 North (CT9N) | 9
row 6 : Terminal 8 West (CT8W) | 8
row 7 : Terminal 4 (CT4) | 8
row 8 : Terminal 3 (CT3) | 6
row 9 : Terminal 2 (CT2) | 5
row 10 : Terminal 1 (CT1) | 4
row 11 : Terminal 5 (CT5) | 4
            """,
            """
col : Terminal | Quay cranes
row 1 : Terminal 7 (CT7) | 15
row 2 : Terminal 9 South (CT9S) | 13
            """
        ],
        "question": "Which terminal had more quay cranes than Terminal 6?",
        "answer": "Terminal 7 (CT7), Terminal 9 South (CT9S)",
        "explanation": "To identify which terminals have more quay cranes than Terminal 6, we selected the Terminal and Quay cranes columns, then compared the number of cranes at each terminal to Terminal 6, which has 11 cranes. Terminal 7 (CT7) has 15 cranes and Terminal 9 South (CT9S) has 13 cranes, both exceeding Terminal 6's count."
    },
    
    "EXAMPLE_6": {
        "table_info": """
col : Week | Date | Opponent | Score | Result | Attendance | Record
row 1 : 1 | Thursday, Aug 11 | vs. Winnipeg Blue Bombers | 35–21 | Loss | 31,837 | 0–1
row 2 : 2 | Monday, Aug 15 | at Edmonton Eskimos | 33–14 | Loss | 17,500 | 0–2
row 3 : 3 | Saturday, Aug 20 | vs. Saskatchewan Roughriders | 27–12 | Win | 29,532 | 1–2
row 4 : 4 | Monday, Aug 22 | at Calgary Stampeders | 26–19 | Win | n/a | 2–2
row 5 : 5 | Monday, Aug 29 | vs. Edmonton Eskimos | 26–0 | Loss | 28,420 | 2–3
row 6 : 6 | Thursday, Sept 1 | at Winnipeg Blue Bombers | 19–14 | Loss | 18,297 | 2–4
row 7 : 7 | Monday, Sept 5 | at Saskatchewan Roughriders | 31–21 | Win | 14,105 | 3–4
row 8 : 8 | Monday, Sept 12 | vs. Calgary Stampeders | 21–21 | Tie | 27,759 | 3–4–1
row 9 : 9 | Saturday, Sept 17 | vs. Winnipeg Blue Bombers | 26–14 | Loss | 30,292 | 3–5–1
row 10 : 10 | Monday, Sept 19 | at Edmonton Eskimos | 18–10 | Loss | n/a | 3–6–1
row 11 : 11 | Saturday, Sept 24 | at Calgary Stampeders | 28–14 | Loss | 13,000 | 3–7–1
row 12 : 12 | Thursday, Oct 6 | vs. Edmonton Eskimos | 21–13 | Win | 21,707 | 4–7–1
row 13 : 13 | Thursday, Oct 13 | at Winnipeg Blue Bombers | 49–21 | Loss | 16,773 | 4–8–1
row 14 : 14 | Saturday, Oct 15 | at Saskatchewan Roughriders | 14–14 | Tie | 7,255 | 4–8–2
row 15 : 15 | Saturday, Oct 22 | vs. Calgary Stampeders | 22–10 | Loss | 29,599 | 4–9–2
row 16 : 16 | Saturday, Oct 29 | vs. Saskatchewan Roughriders | 38–0 | Win | 21,114 | 5–9–2
        """,
        "chain": [
            "f_select_column()",
            "f_select_row()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Date, Result, Attendance)",
            "f_select_row(row 12)",
            "END"
        ],
        "explanations": [
            "Selecting Date, Result, and Attendance columns to find games won in October",
            "Selecting the row containing the first game won in October"
        ],
        "intermediate_tables": [
            """
col : Date | Result | Attendance
row 1 : Thursday, Aug 11 | Loss | 31,837
row 2 : Monday, Aug 15 | Loss | 17,500
row 3 : Saturday, Aug 20 | Win | 29,532
row 4 : Monday, Aug 22 | Win | n/a
row 5 : Monday, Aug 29 | Loss | 28,420
row 6 : Thursday, Sept 1 | Loss | 18,297
row 7 : Monday, Sept 5 | Win | 14,105
row 8 : Monday, Sept 12 | Tie | 27,759
row 9 : Saturday, Sept 17 | Loss | 30,292
row 10 : Monday, Sept 19 | Loss | n/a
row 11 : Saturday, Sept 24 | Loss | 13,000
row 12 : Thursday, Oct 6 | Win | 21,707
row 13 : Thursday, Oct 13 | Loss | 16,773
row 14 : Saturday, Oct 15 | Tie | 7,255
row 15 : Saturday, Oct 22 | Loss | 29,599
row 16 : Saturday, Oct 29 | Win | 21,114
            """,
            """
col : Date | Result | Attendance
row 1 : Thursday, Oct 6 | Win | 21,707
            """
        ],
        "question": "Tell me the number of people that attended the first game they won in October.",
        "answer": "21,707",
        "explanation": "To find the attendance at the first game won in October, I selected the Date, Result, and Attendance columns to focus on when games were played, their outcomes, and attendance figures. Then I identified the first October game with a 'Win' result by selecting row 12. The data shows that on Thursday, Oct 6, they won against Edmonton Eskimos, and the attendance at this game was 21,707 people."
    },
    
    "EXAMPLE_7": {
        "table_info": """
col : World Record | Snatch | Akakios Kakiasvilis (GRE) | 188 kg | Athens, Greece | 27 November 1999
row 1 : World Record | Clean & Jerk | Szymon Kołecki (POL) | 232 kg | Sofia, Bulgaria | 29 April 2000
row 2 : World Record | Total | Akakios Kakiasvilis (GRE) | 412 kg | Athens, Greece | 27 November 1999
row 3 : Asian Record | Snatch | Kourosh Bagheri (IRI) | 187 kg | Sydney, Australia | 24 September 2000
row 4 : Asian Record | Clean & Jerk | Ilya Ilyin (KAZ) | 226 kg | Doha, Qatar | 5 December 2006
row 5 : Asian Record | Total | Kourosh Bagheri (IRI) | 407 kg | Antalya, Turkey | 9 November 2001
row 6 : Games Record | Snatch | Bakhyt Akhmetov (KAZ) | 185 kg | Busan, South Korea | 8 October 2002
row 7 : Games Record | Clean & Jerk | Ilya Ilyin (KAZ) | 226 kg | Doha, Qatar | 5 December 2006
row 8 : Games Record | Total | Bakhyt Akhmetov (KAZ) | 400 kg | Busan, South Korea | 8 October 2002
        """,
        "chain": [
            "f_select_column()",
            "f_select_row()",
            "f_add_knowledge_column()",
            "f_group_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(World Record, Snatch, Akakios Kakiasvilis (GRE))",
            "f_select_row(row 1, row 2)",
            "f_add_knowledge_column(Nationality)",
            "f_group_column(Nationality)",
            "END"
        ],
        "explanations": [
            "Selecting columns to identify the nationality of record holders",
            "Selecting the rows that hold the World Record which is row 1 and row 2",
            "Adding a knowledge column to identify the nationality of the record holders",
            "Grouping the rows by nationality to count the number of record holders"
        ],
        "intermediate_tables": [
            """
col : World Record | Snatch | Akakios Kakiasvilis (GRE)
row 1 : World Record | Clean & Jerk | Szymon Kołecki (POL)
row 2 : World Record | Total | Akakios Kakiasvilis (GRE)
row 3 : Asian Record | Snatch | Kourosh Bagheri (IRI)
row 4 : Asian Record | Clean & Jerk | Ilya Ilyin (KAZ)
row 5 : Asian Record | Total | Kourosh Bagheri (IRI)
row 6 : Games Record | Snatch | Bakhyt Akhmetov (KAZ)
row 7 : Games Record | Clean & Jerk | Ilya Ilyin (KAZ)
row 8 : Games Record | Total | Bakhyt Akhmetov (KAZ)
            """,
            """
col : World Record | Snatch | Akakios Kakiasvilis (GRE)
row 1 : World Record | Clean & Jerk | Szymon Kołecki (POL)
row 2 : World Record | Total | Akakios Kakiasvilis (GRE)
            """,
            """
col : World Record | Snatch | Akakios Kakiasvilis (GRE) | Nationality
row 1 : World Record | Clean & Jerk | Szymon Kołecki (POL) | Polish
row 2 : World Record | Total | Akakios Kakiasvilis (GRE) | Greek
            """,
            """
col : Nationality | count
row 1 : Polish | 1
row 2 : Greek | 1
            """
        ],
        "question": "What is the number of Polish nationals who hold world records?",
        "answer": "1",
        "explanation": "To find the number of Polish nationals who hold world records, I first selected the columns related to record holders, then identified the rows with World Record designation. After adding a knowledge column to identify the nationality of each athlete based on their country code (POL for Polish), I grouped by nationality and counted the number of Polish record holders. In the data, Szymon Kołecki (POL) holds the World Record for Clean & Jerk. No other Polish nationals hold world records, so the answer is 1."
    },
    
    "EXAMPLE_8": {
        "table_info": """
col : Model | Availability | Introduced | Length of use | Last of whiteness
row 1 : Crest Whitestrips Classic\npreviously Crest Whitestrips | Discontinued | May 2001 | 14 days | 12 months
row 2 : Crest Whitestrips Professional | Discontinued | 2001 | 10 days | 12 months
row 3 : Crest Whitestrips Supreme | Dentist and online | September 2003 | 21 days | 18 months
row 4 : Crest Whitestrips Premium | Discontinued | January 2004 | 7 days | 12 months
row 5 : Crest Whitestrips Pro\npreviously Crest Whitestrips Premium Plus | Discontinued | April 2005 | 10 days | 18 months
row 6 : Crest Whitestrips Renewal | Discontinued | January 2006 | 10 days | 18 months
row 7 : Crest Whitestrips Daily Multicare | Discontinued | March 2007 | Daily | White after using system
row 8 : Crest Whitestrips Advanced Seal | Discontinued | February 2009 | 14 days | 18 months
row 9 : Crest Whitestrips 3D Vivid | Instore and online | 2009 | 10 days | 12 months
row 10 : Crest Whitestrips 3D Advanced Vivid | Instore and online | March 2010 | 14 days | 12 months
row 11 : Crest Whitestrips 3D Professional Effects | Instore and online | March 2010 | 20 days | 12 months
row 12 : Crest 3D White 2 Hour Express | Instore and online | 2010 | 2 hours | 3 months
row 13 : Crest 3D Intensive Professional Effects | Instore and online | 2011 | 7 days | 12 months
        """,
        "chain": [
            "f_select_column()",
            "f_select_row()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Model, Introduced)",
            "f_select_row(row 10, row 11)",
            "END"
        ],
        "explanations": [
            "Selecting Model and Introduced columns to identify products introduced in the same month",
            "Identifying Crest Whitestrips 3D Advanced Vivid's introduction date and select the rows that have the same month"
        ],
        "intermediate_tables": [
            """
col : Model | Introduced
row 1 : Crest Whitestrips Classic\npreviously Crest Whitestrips | May 2001
row 2 : Crest Whitestrips Professional | 2001
row 3 : Crest Whitestrips Supreme | September 2003
row 4 : Crest Whitestrips Premium | January 2004
row 5 : Crest Whitestrips Pro\npreviously Crest Whitestrips Premium Plus | April 2005
row 6 : Crest Whitestrips Renewal | January 2006
row 7 : Crest Whitestrips Daily Multicare | March 2007
row 8 : Crest Whitestrips Advanced Seal | February 2009
row 9 : Crest Whitestrips 3D Vivid | 2009
row 10 : Crest Whitestrips 3D Advanced Vivid | March 2010
row 11 : Crest Whitestrips 3D Professional Effects | March 2010
row 12 : Crest 3D White 2 Hour Express | 2010
row 13 : Crest 3D Intensive Professional Effects | 2011
            """,
            """
col : Model | Introduced
row 1 : Crest Whitestrips 3D Advanced Vivid | March 2010
row 2 : Crest Whitestrips 3D Professional Effects | March 2010
            """
        ],
        "question": "What product was introduced in the same month as Crest Whitestrips 3D Advanced Vivid?",
        "answer": "Crest Whitestrips 3D Professional Effects",
        "explanation": "To identify products introduced in the same month as Crest Whitestrips 3D Advanced Vivid, I first selected the Model and Introduced columns to focus on product names and their introduction dates. Then I identified Crest Whitestrips 3D Advanced Vivid (row 10) and selected the rows that have the same introduction month. The data shows that Crest Whitestrips 3D Advanced Vivid was introduced in March 2010, and Crest Whitestrips 3D Professional Effects was also introduced in March 2010."
    },
    
    "EXAMPLE_9": {
        "table_info": """
col : Team | Manager | City | Stadium | Capacity
row 1 : LD Alajuelense | Oscar "El Machillo" Ramírez | Alajuela | Alejandro Morera Soto | 17,895
row 2 : Belén Siglo XXI | Vinicio Alvarado | Belén | Estadio Polideportivo de Belén | 3,000
row 3 : CS Cartaginés | Jhonny Chávez | Cartago | Fello Meza | 13,500
row 4 : CS Herediano | Jafet Soto | Heredia | Rosabal Cordero | 8,144
row 5 : Limón F.C. | Hernán Fernando Sossa | Limón | Estadio Nuevo de Limón/Estadio Juan Gobán | 3,000/2,000
row 6 : Orión F.C. | Martín Arreola | Tarrazú | Estadio Municipal de Tarrazú | 1,500
row 7 : Municipal Pérez Zeledón | Mauricio Wright | San Isidro | Municipal | 6,000
row 8 : Puntarenas FC | Luis Fernando Fallas | Puntarenas | "Lito" Pérez | 4,105
row 9 : Asociación Deportiva San Carlos | Marvin Solano | Ciudad Quesada | Carlos Álvarez | 5,600
row 10 : Santos de Guápiles | Gustavo Martínez | Guápiles | Ebal Rodríguez | 3,000
row 11 : Deportivo Saprissa | Alexander Guimaraes | Tibás | Ricardo Saprissa | 23,000
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Team)",
            "f_add_inferred_column(team_count)",
            "END"
        ],
        "explanations": [
            "Selecting the Team column to analyze the number of teams in the division",
            "Adding an inferred column to count the total number of teams in the division"
        ],
        "intermediate_tables": [
            """
col : Team
row 1 : LD Alajuelense
row 2 : Belén Siglo XXI
row 3 : CS Cartaginés
row 4 : CS Herediano
row 5 : Limón F.C.
row 6 : Orión F.C.
row 7 : Municipal Pérez Zeledón
row 8 : Puntarenas FC
row 9 : Asociación Deportiva San Carlos
row 10 : Santos de Guápiles
row 11 : Deportivo Saprissa
            """,
            """
col : Team | team_count
row 1 : LD Alajuelense | 1
row 2 : Belén Siglo XXI | 2
row 3 : CS Cartaginés | 3
row 4 : CS Herediano | 4
row 5 : Limón F.C. | 5
row 6 : Orión F.C. | 6
row 7 : Municipal Pérez Zeledón | 7
row 8 : Puntarenas FC | 8
row 9 : Asociación Deportiva San Carlos | 9
row 10 : Santos de Guápiles | 10
row 11 : Deportivo Saprissa | 11
            """
        ],
        "question": "What is the total number of teams playing in this division?",
        "answer": "11",
        "explanation": "To determine the total number of teams playing in this division, I selected the Team column to get a list of all teams and then added an inferred column to count the total number of teams. By counting the number of rows in the table, as each row represents a different team, I found that there are 11 teams playing in this division."
    },
    
    "EXAMPLE_10": {
        "table_info": """
col : Year | Final | Year | Final 1 | Semi | Year | Final 2 | Semi
row 1 : 1975 | Finland | 1988 | Luxembourg | No semi-finals | 2001 | Relegated | No semi-finals
row 2 : 1976 | United Kingdom | 1989 | Greece | No semi-finals | 2002 | Spain | No semi-finals
row 3 : 1977 | France | 1990 | France | No semi-finals | 2003 | Relegated | No semi-finals
row 4 : 1978 | Israel | 1991 | Spain | No semi-finals | 2004 | Serbia and Montenegro | Serbia and Montenegro
row 5 : 1979 | Spain | 1992 | France | No semi-finals | 2005 | Serbia and Montenegro | Portugal
row 6 : 1980 | Ireland | 1993 | Ireland | No semi-finals | 2006 | Bosnia and Herzegovina | Bosnia and Herzegovina
row 7 : 1981 | France | 1994 | Ireland | No semi-finals | 2007 | Serbia | Serbia
row 8 : 1982 | Germany | 1995 | Relegated | No semi-finals | 2008 | Serbia | Portugal
row 9 : 1983 | Netherlands | 1996 | Ireland | Unknown1 | 2009 | Turkey | Turkey
row 10 : 1984 | Ireland | 1997 | United Kingdom | No semi-finals | 2010 | Germany | Ireland
row 11 : 1985 | Turkey | 1998 | Germany | No semi-finals | 2011 | Bosnia and Herzegovina | Serbia
row 12 : 1986 | Sweden | 1999 | Relegated | No semi-finals | 2012 | Albania | Albania
row 13 : 1987 | Ireland | 2000 | Germany | No semi-finals | 2013 | Italy | Hungary
        """,
        "chain": [
            "f_select_column()",
            "f_group_column()",
            "f_sort_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(Final)",
            "f_group_column(Final)",
            "f_sort_column(count)",
            "END"
        ],
        "explanations": [
            "Selecting the Final column to analyze countries listed in finals",
            "Grouping by Final to count appearances of each country in finals",
            "Sorting the count column in descending order to rank countries by the number of finals"
        ],
        "intermediate_tables": [
            """
col : Final
row 1 : Finland
row 2 : United Kingdom
row 3 : France
row 4 : Israel
row 5 : Spain
row 6 : Ireland
row 7 : France
row 8 : Germany
row 9 : Netherlands
row 10 : Ireland
row 11 : Turkey
row 12 : Sweden
row 13 : Ireland
            """,
            """
col : Final | count
row 1 : Finland | 1
row 2 : Ireland | 3
row 3 : France | 2
row 4 : Germany | 1
row 5 : United Kingdom | 1
row 6 : Israel | 1
row 7 : Spain | 1
row 8 : Sweden | 1
row 9 : Turkey | 1
row 10 : Netherlands | 1
            """,
            """
col : Final | count
row 1 : Ireland | 3
row 2 : France | 2
row 3 : Finland | 1
row 4 : Germany | 1
row 5 : United Kingdom | 1
row 6 : Israel | 1
row 7 : Spain | 1
row 8 : Sweden | 1
row 9 : Turkey | 1
row 10 : Netherlands | 1
            """
        ],
        "question": "Which country is listed for the most finals?",
        "answer": "Ireland",
        "explanation": "To determine which country appears in the most finals, I selected the Final column to analyze all countries listed, then grouped by country to count occurrences of each, and finally sorted the results by count in descending order. The analysis shows that Ireland appears 3 times in the finals column, more than any other country (France appears twice, while others appear only once), making Ireland the country listed for the most finals."
    }
}


task_2_EXAMPLES_multi = {
"EXAMPLE_0": {
            "table_info": """
table_name: Parliament Groups
col : Group | Members | Caucusing | Total
row 1 : Socialist Group | 242 | 8 | 250
row 2 : RPR Group | 136 | 6 | 140
row 3 : UDF Group | 107 | 6 | 113
row 4 : Communist Group | 34 | 2 | 36
row 5 : Radical, Citizen and Green | 33 | 0 | 33
row 6 : Non-Inscrits | 5 | 0 | 5
row 7 : Total: | 555 | 22 | 577

table_name: Group Details
col : Group | Ideology | Founded Year
row 1 : Socialist Group | Center-left | 1958
row 2 : RPR Group | Conservative | 1976
row 3 : UDF Group | Center-right | 1978
row 4 : Communist Group | Far-left | 1947
row 5 : Radical, Citizen and Green | Progressive | 1995
row 6 : Non-Inscrits | Various | N/A

foreign_key: Group
""",
"question": "How many members are in the Socialist Group?",
"answer": "250",
"explanation": "To find the number of members in the Socialist Group, I first select the Parliament Groups table which contains membership information. Then I select the row corresponding to the Socialist Group, focusing on the Total column which gives the total number of members including caucusing members. The data shows that the Socialist Group has 250 members in total.",
"chain": [
    "f_select_table()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Parliament Groups)",
    "f_select_row(row 1)",
    "f_select_column(Group, Total)",
    "END"
],
"explanations": [
    "Selecting the Parliament Groups table since it contains the membership information we need",
    "Selecting row 1 which corresponds to the Socialist Group",
    "Selecting the Group and Total columns to focus on the group name and its total membership"
],
"intermediate_tables": [
    """
col : Group | Members | Caucusing | Total
row 1 : Socialist Group | 242 | 8 | 250
row 2 : RPR Group | 136 | 6 | 140
row 3 : UDF Group | 107 | 6 | 113
row 4 : Communist Group | 34 | 2 | 36
row 5 : Radical, Citizen and Green | 33 | 0 | 33
row 6 : Non-Inscrits | 5 | 0 | 5
row 7 : Total: | 555 | 22 | 577
    """,
    """
col : Group | Members | Caucusing | Total
row 1 : Socialist Group | 242 | 8 | 250
    """,
    """
col : Group | Total
row 1 : Socialist Group | 250
    """
]
            },
        
"EXAMPLE_1": {
            "table_info": """
table_name: Swimming Results
col : Rank | Name | Nationality | Time | Notes
row 1 : 1 | Janelle Atkinson | Jamaica | 4:16.89 | Q
row 2 : 2 | - | - | - | Q
row 3 : 3 | Kaitlin Sandeno | United States | 4:18.97 | Q
row 4 : 4 | Julia Stowers | United States | 4:19.84 | Q
row 5 : 5 | - | - | - | Q
row 6 : 6 | - | - | - | Q
row 7 : 7 | - | - | - | Q
row 8 : 8 | - | - | - | Q

table_name: Swimmer Details
col : Event ID | Swimmer | Competition Phase | Personal Best
row 1 : E001 | Janelle Atkinson | Heats | 4:14.22
row 2 : E001 | Unknown | Heats | N/A
row 3 : E001 | Kaitlin Sandeno | Heats | 4:17.15
row 4 : E001 | Julia Stowers | Heats | 4:18.50
row 5 : E001 | Unknown | Heats | N/A
row 6 : E001 | Unknown | Heats | N/A
row 7 : E001 | Unknown | Heats | N/A
row 8 : E001 | Unknown | Heats | N/A

foreign_key: Name, Swimmer
""",
"question": "How many swimmers are listed?",
"answer": "8",
"explanation": "To determine how many swimmers are listed, I need to count all the swimmers in the event. While some swimmers' names are not given (shown as '-' in the Swimming Results table), each row represents a distinct swimmer who qualified for the competition. By selecting and counting the rows from the Swimming Results table, I can determine that there are 8 swimmers listed in total.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_add_inferred_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Swimming Results)",
    "f_select_column(Rank)",
    "f_add_inferred_column(count)",
    "END"
],
"explanations": [
    "Selecting the Swimming Results table which contains the list of all competing swimmers",
    "Selecting the Rank column which uniquely identifies each swimmer position",
    "Adding an inferred column to count the total number of swimmers listed"
],
"intermediate_tables": [
    """
col : Rank | Name | Nationality | Time | Notes
row 1 : 1 | Janelle Atkinson | Jamaica | 4:16.89 | Q
row 2 : 2 | - | - | - | Q
row 3 : 3 | Kaitlin Sandeno | United States | 4:18.97 | Q
row 4 : 4 | Julia Stowers | United States | 4:19.84 | Q
row 5 : 5 | - | - | - | Q
row 6 : 6 | - | - | - | Q
row 7 : 7 | - | - | - | Q
row 8 : 8 | - | - | - | Q
            """,
            """
col : Rank
row 1 : 1
row 2 : 2
row 3 : 3
row 4 : 4
row 5 : 5
row 6 : 6
row 7 : 7
row 8 : 8
            """,
            """
col : Rank | count
row 1 : 1 | 1
row 2 : 2 | 2
row 3 : 3 | 3
row 4 : 4 | 4
row 5 : 5 | 5
row 6 : 6 | 6
row 7 : 7 | 7
row 8 : 8 | 8
            """
]
            },
        
"EXAMPLE_2": {
            "table_info": """
table_name: Chinese Names
col :  | Chinese | Pinyin | Cantonese Yale | Hakka pinjim
row 1 : Ma Ling-Yee | 馬寧兒 | Mǎ Níngér | Ma5 Ning4 Yi4 | 
row 2 : Fung Do-Dak | 馮道德 | Féng Dàodé | Fung4 Dou6 Dak1 | 
row 3 : Gwong Wai | 廣慧禪師 | Guǎng Huì Chán Shī | Gwong2 Wai6 Sim3 Si1 | 
row 4 : Juk Faat Wan | 竺法雲禪師 | Zhú Fǎ Yún Chán Shī | Juk1 Faat3 Wan4 Sim3 Si1 | 
row 5 : Fung Foh Do Yan | 風火道人 | Fēng Huǒ Dào Rén | Fung1 Fo2 Dou6 Yan4 | 
row 6 : Lau Siu-Leung | 刘少良 | Liú Shǎoliáng | Lau4 Siu2 Leung4 | 
row 7 : Shek Lam | 石林 | Shí Lín | Sek6 Lam4 | Shak8 Lam2
row 8 : Wanderer Style | 流民派 | Liúmín Pài | Lau4 man4 Paai1 | Liu2 min2 Pai5
row 9 : Lei Mung | 李朦 | Lǐ Méng | Lei5 Mung4 | Li3 Mung2
row 10 : Lin Sang | 蓮生 | Lián Shēng | Lin4 Sang1 | Len2 Sang1

table_name: Name Details
col : Name | Region | Style | Historical Period
row 1 : Ma Ling-Yee | Northern China | Traditional | Ming Dynasty
row 2 : Fung Do-Dak | Southern China | Traditional | Qing Dynasty
row 3 : Gwong Wai | Canton | Monastic | Early Republic
row 4 : Juk Faat Wan | Canton | Monastic | Ming Dynasty
row 5 : Fung Foh Do Yan | Central China | Taoist | Tang Dynasty
row 6 : Lau Siu-Leung | Hong Kong | Modern | Contemporary
row 7 : Shek Lam | Hakka Region | Traditional | Qing Dynasty
row 8 : Wanderer Style | Various | Nomadic | Various
row 9 : Lei Mung | Southern China | Modern | Republic
row 10 : Lin Sang | Eastern China | Traditional | Song Dynasty

foreign_key: Name
""",
"question": "Who lived in the same period as Juk Faat Wan?",
"answer": "Ma Ling-Yee",
"explanation": "To find who lived in the same period as Juk Faat Wan, I need to first identify which historical period Juk Faat Wan belongs to, then find other individuals from the same period. I start by selecting the Name Details table and extracting the Name and Historical Period columns to focus on relevant information. Then I select rows for individuals from the Ming Dynasty period (same as Juk Faat Wan), which reveals that Ma Ling-Yee also lived during this period.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_select_table(Name Details)",
    "f_select_column(Name, Historical Period)",
    "f_select_row(row 1, row 4)",
    "END"
],
"explanations": [
    "Selecting the Name Details table to access historical period information",
    "Selecting Name and Historical Period columns to focus on identifying people from the same period",
    "Selecting rows for individuals from the Ming Dynasty period (same as Juk Faat Wan)"
],
"intermediate_tables": [
    """
col : Name | Region | Style | Historical Period
row 1 : Ma Ling-Yee | Northern China | Traditional | Ming Dynasty
row 2 : Fung Do-Dak | Southern China | Traditional | Qing Dynasty
row 3 : Gwong Wai | Canton | Monastic | Early Republic
row 4 : Juk Faat Wan | Canton | Monastic | Ming Dynasty
row 5 : Fung Foh Do Yan | Central China | Taoist | Tang Dynasty
row 6 : Lau Siu-Leung | Hong Kong | Modern | Contemporary
row 7 : Shek Lam | Hakka Region | Traditional | Qing Dynasty
row 8 : Wanderer Style | Various | Nomadic | Various
row 9 : Lei Mung | Southern China | Modern | Republic
row 10 : Lin Sang | Eastern China | Traditional | Song Dynasty
            """,
            """
col : Name | Historical Period
row 1 : Ma Ling-Yee | Ming Dynasty
row 2 : Fung Do-Dak | Qing Dynasty
row 3 : Gwong Wai | Early Republic
row 4 : Juk Faat Wan | Ming Dynasty
row 5 : Fung Foh Do Yan | Tang Dynasty
row 6 : Lau Siu-Leung | Contemporary
row 7 : Shek Lam | Qing Dynasty
row 8 : Wanderer Style | Various
row 9 : Lei Mung | Republic
row 10 : Lin Sang | Song Dynasty
            """,
            """
col : Name | Historical Period
row 1 : Ma Ling-Yee | Ming Dynasty
row 4 : Juk Faat Wan | Ming Dynasty
            """
]
            },
        
"EXAMPLE_4": {
            "table_info": """
table_name: Race Results
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
row 3 : 3 | 9 | Justin Wilson | RSPORTS | 73 | +3.480 | 2 | 25
row 4 : 4 | 15 | Simon Pagenaud | Team Australia | 73 | +5.643 | 4 | 23
row 5 : 5 | 19 | Bruno Junqueira | Dale Coyne Racing | 73 | +20.738 | 5 | 21
row 6 : 6 | 14 | Robert Doornbos | Minardi Team USA | 72 | + 1 Lap | 12 | 19
row 7 : 7 | 28 | Ryan Dalziel | Pacific Coast Motorsports | 72 | + 1 Lap | 11 | 17

table_name: Team Details
col : Team | Chassis | Engine | Tire | Base
row 1 : Team Australia | Panoz DP01 | Cosworth XFE | Bridgestone | Indianapolis
row 2 : PKV Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Indianapolis
row 3 : RSPORTS | Panoz DP01 | Cosworth XFE | Bridgestone | Michigan
row 4 : Dale Coyne Racing | Panoz DP01 | Cosworth XFE | Bridgestone | Illinois
row 5 : Minardi Team USA | Panoz DP01 | Cosworth XFE | Bridgestone | Indiana
row 6 : Pacific Coast Motorsports | Panoz DP01 | Cosworth XFE | Bridgestone | California

foreign_key: Team
""",
"question": "How many more points did the winner get than the second place driver?",
"answer": "3",
"explanation": "To find out how many more points the winner received compared to the second place driver, I need to identify the points for the first and second-place finishers and calculate the difference. Looking at the Race Results table, Will Power finished in first place with 31 points, while Neel Jani finished second with 28 points. The difference between them is 3 points (31 - 28 = 3).",
"chain": [
    "f_select_table()",
    "f_select_row()",
    "f_select_column()",
    "f_add_inferred_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Race Results)",
    "f_select_row(row 1, row 2)",
    "f_select_column(Driver, Points)",
    "f_add_inferred_column(points_difference)",
    "END"
],
"explanations": [
    "Selecting the Race Results table to access driver positions and points information",
    "Selecting rows 1 and 2 which correspond to the first and second place drivers",
    "Selecting the Driver and Points columns to focus on the points each driver earned",
    "Adding an inferred column to calculate the difference in points between the first and second place drivers"
],
"intermediate_tables": [
    """
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
row 3 : 3 | 9 | Justin Wilson | RSPORTS | 73 | +3.480 | 2 | 25
row 4 : 4 | 15 | Simon Pagenaud | Team Australia | 73 | +5.643 | 4 | 23
row 5 : 5 | 19 | Bruno Junqueira | Dale Coyne Racing | 73 | +20.738 | 5 | 21
row 6 : 6 | 14 | Robert Doornbos | Minardi Team USA | 72 | + 1 Lap | 12 | 19
row 7 : 7 | 28 | Ryan Dalziel | Pacific Coast Motorsports | 72 | + 1 Lap | 11 | 17
            """,
            """
col : Pos | No | Driver | Team | Laps | Time/Retired | Grid | Points
row 1 : 1 | 5 | Will Power | Team Australia | 73 | 1:45:58.568 | 7 | 31
row 2 : 2 | 21 | Neel Jani | PKV Racing | 73 | +2.972 | 9 | 28
            """,
            """
col : Driver | Points
row 1 : Will Power | 31
row 2 : Neel Jani | 28
            """,
            """
col : Driver | Points | points_difference
row 1 : Will Power | 31 | 3
row 2 : Neel Jani | 28 | -
            """
]
            },
        
"EXAMPLE_5": {
            "table_info": """
table_name: Game Schedule
col : Date | Time | Opponent | Site | TV | Result | Attendance
row 1 : September 5 | 2:30 p.m. | Jackson State* | Davis Wade Stadium • Starkville, MS | ESPNU | W 45–7 | 54,232
row 2 : September 12 | 6:00 p.m. | at Auburn | Jordan–Hare Stadium • Auburn, AL | SECRN | L 24–49 | 85,269
row 3 : September 19 | 6:00 p.m. | at Vanderbilt | Vanderbilt Stadium • Nashville, TN | SECRN | W 15–3 | 31,840
row 4 : September 26 | 11:21 a.m. | #7 LSU | Davis Wade Stadium • Starkville, MS | SECN | L 26–30 | 53,612
row 5 : October 3 | 6:30 p.m. | #25 Georgia Tech* | Davis Wade Stadium • Starkville, MS | CSS | L 31–42 | 50,035
row 6 : October 10 | 11:30 a.m. | Houston* | Davis Wade Stadium • Starkville, MS | ESPNU | L 24–31 | 48,019
row 7 : October 17 | 11:30 a.m. | at Middle Tennessee* | Johnny "Red" Floyd Stadium • Murfreesboro, TN | ESPNU | W 27–6 | 23,882
row 8 : October 24 | 6:30 p.m. | #1 Florida | Davis Wade Stadium • Starkville, MS | ESPN | L 19–29 | 57,178
row 9 : October 31 | 6:00 p.m. | at Kentucky | Commonwealth Stadium • Lexington, KY | SECRN | W 31–24 | 67,953
row 10 : November 14 | 6:00 p.m. | #2 Alabama | Davis Wade Stadium • Starkville, MS (Rivalry) | ESPN | L 3–31 | 58,103
row 11 : November 21 | 11:21 a.m. | at Arkansas | War Memorial Stadium • Little Rock, AR | SECN | L 21–42 | 55,634
row 12 : November 28 | 11:21 a.m. | #25 Ole Miss | Davis Wade Stadium • Starkville, MS (Egg Bowl) | SECN | W 41–27 | 55,365

table_name: Opponent Details
col : Opponent | Conference | Season Record | Home/Away
row 1 : Jackson State* | SWAC | 3-8 | Home
row 2 : Auburn | SEC | 8-5 | Away
row 3 : Vanderbilt | SEC | 2-10 | Away
row 4 : LSU | SEC | 9-4 | Home
row 5 : Georgia Tech* | ACC | 11-3 | Home
row 6 : Houston* | C-USA | 10-4 | Home
row 7 : Middle Tennessee* | Sun Belt | 10-3 | Away
row 8 : Florida | SEC | 13-1 | Home
row 9 : Kentucky | SEC | 7-6 | Away
row 10 : Alabama | SEC | 14-0 | Home
row 11 : Arkansas | SEC | 8-5 | Away
row 12 : Ole Miss | SEC | 9-4 | Home

foreign_key: Opponent
""",
"question": "Which three TVs have the most attendance?",
"answer": "SECN, ESPNU, and SECRN",
"explanation": "To identify the three TV networks with the highest attendance, I need to analyze the attendance figures for games broadcast by each network. First, I select the Game Schedule table and focus on the TV and Attendance columns. Then I calculate the total attendance for each network by adding an inferred sum_attendance column. After sorting by total attendance in descending order, I can determine that SECRN broadcast games had 185,062 total attendees, SECN had 164,611, and ESPNU had 126,133. Therefore, the three TV networks with the highest attendance are SECRN, SECN, and ESPNU.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_sort_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_select_table(Game Schedule)",
    "f_select_column(TV, Attendance)",
    "f_add_inferred_column(sum_attendance)",
    "f_sort_column(sum_attendance)",
    "f_select_row(row 1, row 4, row 7)",
    "END"
],
"explanations": [
    "Selecting the Game Schedule table to access TV and attendance information",
    "Selecting TV and Attendance columns to focus on networks and their corresponding attendance figures",
    "Adding an inferred column to calculate the total attendance for each network",
    "Sorting by total attendance in descending order to find the networks with highest viewership",
    "Selecting the top three rows of distinct TV networks to identify the TV networks with the highest attendance, which are row 1, row 4, and row 7"
],
"intermediate_tables": [
    """
col : Date | Time | Opponent | Site | TV | Result | Attendance
row 1 : September 5 | 2:30 p.m. | Jackson State* | Davis Wade Stadium • Starkville, MS | ESPNU | W 45–7 | 54,232
row 2 : September 12 | 6:00 p.m. | at Auburn | Jordan–Hare Stadium • Auburn, AL | SECRN | L 24–49 | 85,269
row 3 : September 19 | 6:00 p.m. | at Vanderbilt | Vanderbilt Stadium • Nashville, TN | SECRN | W 15–3 | 31,840
row 4 : September 26 | 11:21 a.m. | #7 LSU | Davis Wade Stadium • Starkville, MS | SECN | L 26–30 | 53,612
row 5 : October 3 | 6:30 p.m. | #25 Georgia Tech* | Davis Wade Stadium • Starkville, MS | CSS | L 31–42 | 50,035
row 6 : October 10 | 11:30 a.m. | Houston* | Davis Wade Stadium • Starkville, MS | ESPNU | L 24–31 | 48,019
row 7 : October 17 | 11:30 a.m. | at Middle Tennessee* | Johnny "Red" Floyd Stadium • Murfreesboro, TN | ESPNU | W 27–6 | 23,882
row 8 : October 24 | 6:30 p.m. | #1 Florida | Davis Wade Stadium • Starkville, MS | ESPN | L 19–29 | 57,178
row 9 : October 31 | 6:00 p.m. | at Kentucky | Commonwealth Stadium • Lexington, KY | SECRN | W 31–24 | 67,953
row 10 : November 14 | 6:00 p.m. | #2 Alabama | Davis Wade Stadium • Starkville, MS (Rivalry) | ESPN | L 3–31 | 58,103
row 11 : November 21 | 11:21 a.m. | at Arkansas | War Memorial Stadium • Little Rock, AR | SECN | L 21–42 | 55,634
row 12 : November 28 | 11:21 a.m. | #25 Ole Miss | Davis Wade Stadium • Starkville, MS (Egg Bowl) | SECN | W 41–27 | 55,365
    """,
    """
col : TV | Attendance
row 1 : ESPNU | 54,232
row 2 : SECRN | 85,269
row 3 : SECRN | 31,840
row 4 : SECN | 53,612
row 5 : CSS | 50,035
row 6 : ESPNU | 48,019
row 7 : ESPNU | 23,882
row 8 : ESPN | 57,178
row 9 : SECRN | 67,953
row 10 : ESPN | 58,103
row 11 : SECN | 55,634
row 12 : SECN | 55,365
    """,
    """
col : TV | Attendance | sum_attendance
row 1 : ESPNU | 54,232 | 126,133
row 2 : SECRN | 85,269 | 185,062
row 3 : SECRN | 31,840 | 185,062
row 4 : SECN | 53,612 | 164,611
row 5 : CSS | 50,035 | 50,035
row 6 : ESPNU | 48,019 | 126,133
row 7 : ESPNU | 23,882 | 126,133
row 8 : ESPN | 57,178 | 115,281
row 9 : SECRN | 67,953 | 185,062
row 10 : ESPN | 58,103 | 115,281
row 11 : SECN | 55,634 | 164,611
row 12 : SECN | 55,365 | 164,611
    """,
    """
col : TV | Attendance | sum_attendance
row 1 : SECRN | 85,269 | 185,062
row 2 : SECRN | 31,840 | 185,062
row 3 : SECRN | 67,953 | 185,062
row 4 : SECN | 53,612 | 164,611
row 5 : SECN | 55,634 | 164,611
row 6 : SECN | 55,365 | 164,611
row 7 : ESPNU | 54,232 | 126,133
row 8 : ESPNU | 48,019 | 126,133
row 9 : ESPNU | 23,882 | 126,133
row 10 : ESPN | 57,178 | 115,281
row 11 : ESPN | 58,103 | 115,281
row 12 : CSS | 50,035 | 50,035
    """,
    """
col : TV | sum_attendance
row 1 : SECRN | 185,062
row 4 : SECN | 164,611
row 7 : ESPNU | 126,133
    """
]
            }
}