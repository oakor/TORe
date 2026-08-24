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



task_0_EXAMPLES_multi = {
  "EXAMPLE_1": {
    "table_info": """
table_name: basketball_match
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
     | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3
row 3 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3

table_name: university
col : School_ID | School | Location | Founded | Affiliation | Enrollment | Nickname | Primary_conference
row 1 : 1 | University of Delaware | Newark, DE | 1743.0 | Public | 19067.0 | Fightin' Blue Hens | Colonial Athletic Association ( D-I )
row 2 : 2 | Lebanon Valley College | Annville, PA | 1866.0 | Private/Methodist | 2100.0 | Flying Dutchmen | MAC Commonwealth Conference ( D-III )
row 3 : 3 | University of Rhode Island | Kingston, RI | 1892.0 | Public | 19095.0 | Rams | Atlantic 10 Conference ( D-I )
row 4 : 4 | Rutgers University | New Brunswick, NJ | 1766.0 | Public | 56868.0 | Scarlet Knights | American Athletic Conference ( D-I )
row 5 : 5 | Stony Brook University | Stony Brook, NY | 1957.0 | Public | 23997.0 | Seawolves | America East Conference ( D-I )

foreign_key: school_id
    """,
    "question": "How many schools do not participate in the basketball match?",
    "answer": "1",
    "explanation": "This question requires stitching tables using basketball_match.School_ID and university.School_ID by right join method to keep all columns of the second table, selecting relevant columns for counting schools participating in the basketball match, and select the row that has no School_ID, which is row 3",
    "chain": [
      "f_stitch_tables()",
      "f_select_column()",
      "f_select_row()",
      "END"
    ],
    "filled_chain":[
      "f_stitch_tables(basketball_match.School_ID, university.School_ID, right)",
      "f_select_column(Team_ID)",
      "f_select_row(row 3)",
      "END"
    ],
    "explanations": [
        "Stitching tables using basketball_match.School_ID and university.School_ID by right join method to keep all columns of the second table",
        "Selecting relevant columns for counting schools participating in the basketball match",
        "Select the row that has no School_ID, which is row 3"
    ],
    "intermediate_tables": [
"""
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral | School | Location | Founded | Affiliation | Enrollment | Nickname | Primary_conference
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1 | University of Delaware | Newark, DE | 1743.0 | Public | 19067.0 | "Fightin' Blue Hens" | Colonial Athletic Association ( D-I )
row 2 : 2 | 2 | Duke | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3 | Lebanon Valley College | Annville, PA | 1866.0 | Private/Methodist | 2100.0 | Flying Dutchmen | MAC Commonwealth Conference ( D-III )
row 3 : nan | 3 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | University of Rhode Island | Kingston, RI | 1892.0 | Public | 19095.0 | Rams | Atlantic 10 Conference ( D-I )
row 4 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3 | Rutgers University | New Brunswick, NJ | 1766.0 | Public | 56868.0 | Scarlet Knights | American Athletic Conference ( D-I )
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3 | Stony Brook University | Stony Brook, NY | 1957.0 | Public | 23997.0 | Seawolves | America East Conference ( D-I )
""",
"""
col : Team_ID
row 1 : 1
row 2 : 2
row 3 : nan
row 4 : 3
row 5 : 4
""",
"""
col : Team_ID
row 3 : nan
"""
    ]
  },

  "EXAMPLE_2": {
    "table_info": """
table_name: journal
col : Journal_ID | Date | Theme | Sales
row 1 : 1 | September 9, 2001 | Miami Dolphins | 798
row 2 : 2 | September 23, 2001 | at Jacksonville Jaguars | 994
row 3 : 4 | October 7, 2001 | at Baltimore Ravens | 7494
row 4 : 5 | October 14, 2001 | Tampa Bay Buccaneers | 4798
row 5 : 6 | October 21, 2001 | at Detroit Lions | 2940
row 6 : 7 | October 29, 2001 | at Pittsburgh Steelers | 1763
row 7 : 8 | November 4, 2001 | Jacksonville Jaguars | 1232
row 8 : 9 | November 12, 2001 | Baltimore Ravens | 6532
row 9 : 10 | November 18, 2001 | at Cincinnati Bengals | 3421
row 10 : 11 | November 25, 2001 | Pittsburgh Steelers | 3342
row 11 : 12 | December 2, 2001 | at Cleveland Browns | 3534
row 12 : 13 | December 9, 2001 | at Minnesota Vikings | 4271
row 13 : 14 | December 16, 2001 | Green Bay Packers | 2804
row 14 : 15 | December 22, 2001 | at Oakland Raiders | 1934
row 15 : 16 | December 30, 2001 | Cleveland Browns | 3798
row 16 : 17 | January 6, 2002 | Cincinnati Bengals | 5342

table_name: journal_committee
col : Editor_ID | Journal_ID | Work_Type
row 1 : 1 | 13 | Photo
row 2 : 8 | 17 | Article
row 3 : 6 | 11 | Photo
row 4 : 4 | 2 | Article
row 5 : 3 | 6 | Title
row 6 : 9 | 12 | Photo
row 7 : 8 | 4 | Photo

foreign_key: journal_id, editor_id
    """,
    "question": "What is the average sales of the journals that have an editor whose work type is 'Photo'?",
    "answer": "4660.25",
    "explanation": "This question requires stitching tables using journal.Journal_ID and journal_committee.Journal_ID by inner join method to connect journals with their editors, selecting rows where the editor's work type is 'Photo', selecting the Sales column, and adding an inferred column to calculate the average sales value.",
    "chain": [
      "f_stitch_tables()",
      "f_select_row()",
      "f_select_column()",
      "f_add_inferred_column()",
      "END"
    ],
    "filled_chain":[
      "f_stitch_tables(journal.Journal_ID, journal_committee.Journal_ID, inner)",
      "f_select_row(row 1, row 3, row 6, row 7)",
      "f_select_column(Sales)",
      "f_add_inferred_column(Average_Sales)",
      "END"
    ],
    "explanations": [
        "Stitching tables using journal.Journal_ID and journal_committee.Journal_ID by inner join method to connect journals with their editors",
        "Selecting rows where the editor's work type is 'Photo'",
        "Selecting only the Sales column for calculating the average",
        "Adding an inferred column to calculate the average sales value"
    ],
    "intermediate_tables": [
"""
col : Journal_ID | Date | Theme | Sales | Editor_ID | Work_Type
row 1 : 13 | December 9, 2001 | at Minnesota Vikings | 4271 | 1 | Photo
row 2 : 17 | January 6, 2002 | Cincinnati Bengals | 5342 | 8 | Article
row 3 : 11 | November 25, 2001 | Pittsburgh Steelers | 3342 | 6 | Photo
row 4 : 2 | September 23, 2001 | at Jacksonville Jaguars | 994 | 4 | Article
row 5 : 6 | October 21, 2001 | at Detroit Lions | 2940 | 3 | Title
row 6 : 12 | December 2, 2001 | at Cleveland Browns | 3534 | 9 | Photo
row 7 : 4 | October 7, 2001 | at Baltimore Ravens | 7494 | 8 | Photo
""",
"""
col : Journal_ID | Date | Theme | Sales | Editor_ID | Work_Type
row 1 : 13 | December 9, 2001 | at Minnesota Vikings | 4271 | 1 | Photo
row 3 : 11 | November 25, 2001 | Pittsburgh Steelers | 3342 | 6 | Photo
row 6 : 12 | December 2, 2001 | at Cleveland Browns | 3534 | 9 | Photo
row 7 : 4 | October 7, 2001 | at Baltimore Ravens | 7494 | 8 | Photo
""",
"""
col : Sales
row 1 : 4271
row 3 : 3342
row 6 : 3534
row 7 : 7494
""",
"""
col : Sales | Average_Sales
row 1 : 4271 | 4660.25
row 3 : 3342 | 4660.25
row 6 : 3534 | 4660.25
row 7 : 7494 | 4660.25
"""
    ]
  },

  "EXAMPLE_3": {
    "table_info": """
table_name: editor
col : Editor_ID | Name | Age
row 1 : 1 | Kamila Porczyk | 34.0
row 2 : 2 | Anna Powierza | 35.0
row 3 : 3 | Marek Siudym | 21.0
row 4 : 4 | Piotr PrÄgowski | 43.0
row 5 : 5 | Szymon Wydra | 20.0
row 6 : 6 | WÅadysÅaw Grzywna | 24.0
row 7 : 7 | Mariusz Zalejski | 25.0
row 8 : 8 | GraÅ¼yna Wolszczak | 54.0
row 9 : 9 | Maria GÃ³ralczyk | 38.0

table_name: journal_committee
col : Editor_ID | Journal_ID | Work_Type
row 1 : 1 | 13 | Photo
row 2 : 8 | 17 | Article
row 3 : 6 | 11 | Photo
row 4 : 4 | 2 | Article
row 5 : 3 | 6 | Title
row 6 : 9 | 12 | Photo
row 7 : 8 | 4 | Photo

foreign_key: journal_id, editor_id
    """,
    "question": "Show the names of editors that are on at least two journal committees.",
    "answer": "GraÅ¼yna Wolszczak",
    "explanation": "This question requires stitching tables using editor.Editor_ID and journal_committee.Editor_ID by inner join method to connect editors with their committee assignments, selecting only the Name and Journal_ID columns for counting committee assignments, grouping by editor name to count committee assignments, adding an inferred column to count the number of committees per editor, and selecting editors who are on at least two committees.",
    "chain": [
      "f_stitch_tables()",
      "f_select_column()",
      "f_group_column()",
      "f_add_inferred_column()",
      "f_select_row()",
      "END"
    ],
    "filled_chain":[
      "f_stitch_tables(editor.Editor_ID, journal_committee.Editor_ID, inner)",
      "f_select_column(Name, Journal_ID)",
      "f_group_column(Name)",
      "f_add_inferred_column(Committee_Count)",
      "f_select_row(row 2)",
      "END"
    ],
    "explanations": [
        "Stitching tables using editor.Editor_ID and journal_committee.Editor_ID by inner join method to connect editors with their committee assignments",
        "Selecting only the Name and Journal_ID columns for counting committee assignments",
        "Grouping by editor name to aggregate committee assignments",
        "Adding an inferred column to count the number of committees per editor",
        "Selecting only the editors who are on at least two committees"
    ],
    "intermediate_tables": [
"""
col : Editor_ID | Name | Age | Journal_ID | Work_Type
row 1 : 1 | Kamila Porczyk | 34.0 | 13 | Photo
row 2 : 8 | GraÅ¼yna Wolszczak | 54.0 | 17 | Article
row 3 : 6 | WÅadysÅaw Grzywna | 24.0 | 11 | Photo
row 4 : 4 | Piotr PrÄgowski | 43.0 | 2 | Article
row 5 : 3 | Marek Siudym | 21.0 | 6 | Title
row 6 : 9 | Maria GÃ³ralczyk | 38.0 | 12 | Photo
row 7 : 8 | GraÅ¼yna Wolszczak | 54.0 | 4 | Photo
""",
"""
col : Name | Journal_ID
row 1 : Kamila Porczyk | 13
row 2 : GraÅ¼yna Wolszczak | 17
row 3 : WÅadysÅaw Grzywna | 11
row 4 : Piotr PrÄgowski | 2
row 5 : Marek Siudym | 6
row 6 : Maria GÃ³ralczyk | 12
row 7 : GraÅ¼yna Wolszczak | 4
""",
"""
col : Name | count
row 1 : Kamila Porczyk | 1
row 2 : GraÅ¼yna Wolszczak | 2
row 3 : WÅadysÅaw Grzywna | 1
row 4 : Piotr PrÄgowski | 1
row 5 : Marek Siudym | 1
row 6 : Maria GÃ³ralczyk | 1
""",
"""
col : Name | count | Committee_Count
row 1 : Kamila Porczyk | 1 | 1
row 2 : GraÅ¼yna Wolszczak | 2 | 2
row 3 : WÅadysÅaw Grzywna | 1 | 1
row 4 : Piotr PrÄgowski | 1 | 1
row 5 : Marek Siudym | 1 | 1
row 6 : Maria GÃ³ralczyk | 1 | 1
""",
"""
col : Name | count | Committee_Count
row 2 : GraÅ¼yna Wolszczak | 2 | 2
"""
    ]
  },
  
  "EXAMPLE_4": {
    "table_info": """
table_name: basketball_match
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
row 2 : 2 | 2 | Duke | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3
row 3 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3
    """,
    "question": "What is the team name and acc regular season score of the school that has the most all games percent?",
    "answer": "North Carolina, 14â2",
    "explanation": "This question requires sorting the table by the All_Games_Percent column in descending order to find the school with the highest percentage, selecting the first row which corresponds to the school with the highest All_Games_Percent, and then selecting the Team_Name and ACC_Regular_Season columns for that school.",
    "chain": [
      "f_sort_column()",
      "f_select_row()",
      "f_select_column()",
      "END"
    ],
    "filled_chain":[
      "f_sort_column(All_Games_Percent)",
      "f_select_row(row 1)",
      "f_select_column(Team_Name, ACC_Regular_Season)",
      "END"
    ],
    "explanations": [
        "Sorting by the All_Games_Percent column in descending order to find the school with the highest percentage",
        "Selecting the first row which corresponds to the school with the highest All_Games_Percent",
        "Selecting only the Team_Name and ACC_Regular_Season columns for the result"
    ],
    "intermediate_tables": [
"""
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
row 2 : 2 | 2 | Duke | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3
row 3 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3
""",
"""
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
""",
"""
col : Team_Name | ACC_Regular_Season
row 1 : North Carolina | 14â2
"""
    ]
  },

  "EXAMPLE_5": {
    "table_info": """
table_name: match_season
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison

table_name: player
col : Player_ID | Player | Years_Played | Total_WL | Singles_WL | Doubles_WL | Team
row 1 : 1 | Cho Soong-Jae (630) | 1 (2011) | 2â0 | 1â0 | 1â0 | 1
row 2 : 2 | Chung Hong (717) | 1 (2011) | 0â0 | 0â0 | 0â0 | 1
row 3 : 3 | Im Kyu-tae (492) | 8 (2003â2005, 2007â2011) | 6â9 | 5â7 | 1â2 | 1
row 4 : 4 | Jeong Suk-Young (793) | 2 (2010â2011) | 1â2 | 1â2 | 0â0 | 1
row 5 : 5 | Kim Hyun-Joon (908) | 2 (2010â2011) | 3â4 | 2â1 | 1â3 | 2
row 6 : 6 | Kim Young-Jun (474) | 4 (2003â2004, 2010â2011) | 6â4 | 6â3 | 0â1 | 4
row 7 : 7 | Lim Yong-Kyu (288) | 3 (2009â2011) | 7â6 | 5â6 | 2â0 | 6
row 8 : 8 | Seol Jae-Min (none) | 2 (2010-2011) | 2â2 | 0â0 | 2â2 | 1
row 9 : 9 | An Jae-Sung | 3 (2005, 2007â2008) | 4â3 | 3â2 | 1â1 | 1
row 10 : 10 | Bae Nam-Ju | 2 (1988, 1990) | 1â3 | 0â2 | 1â1 | 8

foreign_key: team, country, team
    """,
    "question": "Show the draft class of the players that are from college UCLA.",
    "answer": "2000 MLS SuperDraft, 2006 MLS SuperDraft",
    "explanation": "This question requires selecting rows where the College column equals 'UCLA', and selecting the Draft_Class column to show the draft classes of players from UCLA.",
    "chain": [
      "f_select_table()",
      "f_select_row()",
      "f_select_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_table(match_season)",
      "f_select_row(row 5, row 11)",
      "f_select_column(Draft_Class)",
      "END"
    ],
    "explanations": [
        "Selecting the match_season table to get the draft classes of players from UCLA",
        "Selecting rows where the College column equals 'UCLA', which are rows 5 and 11",
        "Selecting only the Draft_Class column to show the draft classes of players from UCLA"
    ],
    "intermediate_tables": [
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison
""",
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
""",
"""
col : Draft_Class
row 5 : 2000 MLS SuperDraft
row 11 : 2006 MLS SuperDraft
"""
    ]
  },

  "EXAMPLE_6": {
    "table_info": """
table_name: team
col : Team_id | Name
row 1 : 1 | Columbus Crew
row 2 : 2 | Evalyn Feil
row 3 : 3 | Anais VonRueden
row 4 : 4 | Miami Fusion
row 5 : 5 | Enrique Osinski
row 6 : 6 | Brown Erdman
row 7 : 7 | Los Angeles Galaxy
row 8 : 8 | Berneice Hand
row 9 : 9 | Ryley Goldner
row 10 : 10 | D.C. United

table_name: match_season
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison

foreign_key: team, country, team
    """,
    "question": "Count the number of different colleges that players who play for Columbus Crew are from.",
    "answer": "1",
    "explanation": "This question requires stitching tables using match_season.Team and team.Team_id by right join method to connect players with their teams, selecting rows where the team name is 'Columbus Crew', selecting only the College column for counting distinct colleges, grouping by College to eliminate duplicates, and adding an inferred column to count the number of distinct colleges.",
    "chain": [
      "f_stitch_tables()",
      "f_select_row()",
      "f_select_column()",
      "f_group_column()",
      "f_add_inferred_column()",
      "END"
    ],
    "filled_chain":[
      "f_stitch_tables(match_season.Team, team.Team_id, right)",
      "f_select_row(row 1)",
      "f_select_column(College)",
      "f_group_column(College)",
      "f_add_inferred_column(College_Count)",
      "END"
    ],
    "explanations": [
        "Stitching tables using match_season.Team and team.Team_id by right join method to connect players with their teams",
        "Selecting rows where the team name is 'Columbus Crew'",
        "Selecting only the College column for counting distinct colleges",
        "Grouping by College to eliminate duplicates",
        "Adding an inferred column to count the number of distinct colleges"
    ],
    "intermediate_tables": [
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College | Team_id | Name
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International | 1 | Columbus Crew
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV | 2 | Evalyn Feil
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia | 3 | Anais VonRueden
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke | 4 | Miami Fusion
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA | 5 | Enrique Osinski
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College | 5 | Enrique Osinski
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia | 3 | Anais VonRueden
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut | 2 | Evalyn Feil
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman | 3 | Anais VonRueden
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest | 4 | Miami Fusion
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA | 10 | D.C. United
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland | 9 | Ryley Goldner
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge | 5 | Enrique Osinski
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland | 5 | Enrique Osinski
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none | 5 | Enrique Osinski
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison | 3 | Anais VonRueden
""",
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College | Team_id | Name
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International | 1 | Columbus Crew
""",
"""
col : College
row 1 : Florida International
""",
"""
col : College | count
row 1 : Florida International | 1
""",
"""
col : College | count | College_Count
row 1 : Florida International | 1 | 1
"""
    ]
  }
}
  
task_0_EXAMPLES_single = {
  "EXAMPLE_1": {
    "table_info": """
col : School_ID | School | Location | Founded | Affiliation | Enrollment | Nickname | Primary_conference
row 1 : 1 | University of Delaware | Newark, DE | 1743.0 | Public | 19067.0 | Fightin' Blue Hens | Colonial Athletic Association ( D-I )
row 2 : 2 | Lebanon Valley College | Annville, PA | 1866.0 | Private/Methodist | 2100.0 | Flying Dutchmen | MAC Commonwealth Conference ( D-III )
row 3 : 3 | University of Rhode Island | Kingston, RI | 1892.0 | Public | 19095.0 | Rams | Atlantic 10 Conference ( D-I )
row 4 : 4 | Rutgers University | New Brunswick, NJ | 1766.0 | Public | 56868.0 | Scarlet Knights | American Athletic Conference ( D-I )
row 5 : 5 | Stony Brook University | Stony Brook, NY | 1957.0 | Public | 23997.0 | Seawolves | America East Conference ( D-I )
    """,
    "question": "How many schools was public and founded before 1900?",
    "answer": "3",
    "explanation": "This question requires selecting relevant columns for foundation year and affiliation analysis, selecting rows where Founded is before 1900, and then group by Affiliation to count the number of public schools founded before 1900",
    "chain": [
      "f_select_column()",
      "f_select_row()",
      "f_group_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_column(Founded, Affiliation)",
      "f_select_row(row 1, row 2, row 3, row 4)",
      "f_group_column(Affiliation)",
      "END"
    ],
    "explanations": [
        "Selecting relevant columns for foundation year and affiliation analysis",
        "Select the rows that are founded before 1900",
        "Grouping by affiliation to count the number of public schools founded before 1900"
    ],
    "intermediate_tables": [
"""
col :  Founded | Affiliation 
row 1 : 1743.0 | Public
row 2 : 1866.0 | Private/Methodist
row 3 : 1892.0 | Public
row 4 : 1766.0 | Public
row 5 : 1957.0 | Public
""",
"""
col :  Founded | Affiliation 
row 1 : 1743.0 | Public
row 2 : 1866.0 | Private/Methodist
row 3 : 1892.0 | Public
row 4 : 1766.0 | Public
""",
"""
col : Affiliation | count
row 1 : Public | 3
row 2 : Private/Methodist | 1
"""
    ]
  },

  "EXAMPLE_2": {
    "table_info": """
col : Journal_ID | Date | Theme | Sales
row 1 : 1 | September 9, 2001 | Miami Dolphins | 798
row 2 : 2 | September 23, 2001 | at Jacksonville Jaguars | 994
row 3 : 4 | October 7, 2001 | at Baltimore Ravens | 7494
row 4 : 5 | October 14, 2001 | Tampa Bay Buccaneers | 4798
row 5 : 6 | October 21, 2001 | at Detroit Lions | 2940
row 6 : 7 | October 29, 2001 | at Pittsburgh Steelers | 1763
row 7 : 8 | November 4, 2001 | Jacksonville Jaguars | 1232
row 8 : 9 | November 12, 2001 | Baltimore Ravens | 6532
row 9 : 10 | November 18, 2001 | at Cincinnati Bengals | 3421
row 10 : 11 | November 25, 2001 | Pittsburgh Steelers | 3342
row 11 : 12 | December 2, 2001 | at Cleveland Browns | 3534
row 12 : 13 | December 9, 2001 | at Minnesota Vikings | 4271
row 13 : 14 | December 16, 2001 | Green Bay Packers | 2804
row 14 : 15 | December 22, 2001 | at Oakland Raiders | 1934
row 15 : 16 | December 30, 2001 | Cleveland Browns | 3798
row 16 : 17 | January 6, 2002 | Cincinnati Bengals | 5342
    """,
    "question": "What is the average sales of the journals that was published in October?",
    "answer": "3665.87",
    "explanation": "This question requires selecting rows where the Date column contains 'October', selecting the Sales column, and adding an inferred column to calculate the average sales value for those journals.",
    "chain": [
      "f_select_row()",
      "f_select_column()",
      "f_add_inferred_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_row(row 3, row 4, row 5, row 6)",
      "f_select_column(Sales)",
      "f_add_inferred_column(Average_Sales)",
      "END"
    ],
    "explanations": [
        "Selecting rows where the Date column contains 'October', which are rows 3, 4, 5, and 6",
        "Selecting only the Sales column for calculating the average",
        "Adding an inferred column to calculate the average sales value for October journals"
    ],
    "intermediate_tables": [
"""
col : Journal_ID | Date | Theme | Sales
row 3 : 4 | October 7, 2001 | at Baltimore Ravens | 7494
row 4 : 5 | October 14, 2001 | Tampa Bay Buccaneers | 4798
row 5 : 6 | October 21, 2001 | at Detroit Lions | 2940
row 6 : 7 | October 29, 2001 | at Pittsburgh Steelers | 1763
""",
"""
col : Sales
row 3 : 7494
row 4 : 4798
row 5 : 2940
row 6 : 1763
""",
"""
col : Sales | Average_Sales
row 3 : 7494 | 3665.87
row 4 : 4798 | 3665.87
row 5 : 2940 | 3665.87
row 6 : 1763 | 3665.87
"""
    ]
  },

  "EXAMPLE_3": {
    "table_info": """
col : Editor_ID | Name | Age
row 1 : 1 | Kamila Porczyk | 34.0
row 2 : 2 | Anna Powierza | 35.0
row 3 : 3 | Marek Siudym | 21.0
row 4 : 4 | Piotr PrÄgowski | 43.0
row 5 : 5 | Szymon Wydra | 20.0
row 6 : 6 | WÅadysÅaw Grzywna | 24.0
row 7 : 7 | Mariusz Zalejski | 25.0
row 8 : 8 | GraÅ¼yna Wolszczak | 54.0
row 9 : 9 | Maria GÃ³ralczyk | 38.0
    """,
    "question": "Show the names of editors that are at least 40 years old",
    "answer": "Piotr PrÄgowski, GraÅ¼yna Wolszczak",
    "explanation": "This question requires selecting rows where the Age column is at least 40, and selecting the Name column to show the names of editors who meet this age criterion.",
    "chain": [
      "f_select_row()",
      "f_select_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_row(row 4, row 8)",
      "f_select_column(Name)",
      "END"
    ],
    "explanations": [
        "Selecting rows where the Age column is at least 40, which are rows 4 and 8",
        "Selecting only the Name column to show the names of editors who meet the age criterion"
    ],
    "intermediate_tables": [
"""
col : Editor_ID | Name | Age
row 4 : 4 | Piotr PrÄgowski | 43.0
row 8 : 8 | GraÅ¼yna Wolszczak | 54.0
""",
"""
col : Name
row 4 : Piotr PrÄgowski
row 8 : GraÅ¼yna Wolszczak
"""
    ]
  },
  
  "EXAMPLE_4": {
    "table_info": """
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
row 2 : 2 | 2 | Duke | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3
row 3 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3
    """,
    "question": "What is the team name and acc regular season score of the school that has the most all games percent?",
    "answer": "North Carolina, 14â2",
    "explanation": "This question requires sorting the table by the All_Games_Percent column in descending order to find the school with the highest percentage, selecting the first row which corresponds to the school with the highest All_Games_Percent, and then selecting the Team_Name and ACC_Regular_Season columns for that school.",
    "chain": [
      "f_sort_column()",
      "f_select_row()",
      "f_select_column()",
      "END"
    ],
    "filled_chain":[
      "f_sort_column(All_Games_Percent)",
      "f_select_row(row 1)",
      "f_select_column(Team_Name, ACC_Regular_Season)",
      "END"
    ],
    "explanations": [
        "Sorting by the All_Games_Percent column in descending order to find the school with the highest percentage",
        "Selecting the first row which corresponds to the school with the highest All_Games_Percent",
        "Selecting only the Team_Name and ACC_Regular_Season columns for the result"
    ],
    "intermediate_tables": [
"""
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
row 2 : 2 | 2 | Duke | 13â3 | .813 | 7â1 | 6â2 | 28â6 | 0.824 | 15â1 | 8â2 | 5â3
row 3 : 3 | 4 | Clemson | 10â6 | .625 | 7â1 | 3â5 | 24â10 | 0.706 | 14â2 | 6â5 | 4â3
row 4 : 4 | 5 | Virginia Tech | 9â7 | .563 | 6â2 | 3â5 | 21â14 | 0.6 | 14â3 | 4â8 | 3â3
""",
"""
col : Team_ID | School_ID | Team_Name | ACC_Regular_Season | ACC_Percent | ACC_Home | ACC_Road | All_Games | All_Games_Percent | All_Home | All_Road | All_Neutral
row 1 : 1 | 1 | North Carolina | 14â2 | .875 | 6â2 | 8â0 | 35â2 | 0.946 | 14â2 | 13â0 | 9â1
""",
"""
col : Team_Name | ACC_Regular_Season
row 1 : North Carolina | 14â2
"""
    ]
  },

  "EXAMPLE_5": {
    "table_info": """
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison
    """,
    "question": "Show the draft class of the players that are from college UCLA.",
    "answer": "2000 MLS SuperDraft, 2006 MLS SuperDraft",
    "explanation": "This question requires selecting rows where the College column equals 'UCLA', and selecting the Draft_Class column to show the draft classes of players from UCLA.",
    "chain": [
      "f_select_row()",
      "f_select_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_row(row 5, row 11)",
      "f_select_column(Draft_Class)",
      "END"
    ],
    "explanations": [
        "Selecting rows where the College column equals 'UCLA', which are rows 5 and 11",
        "Selecting only the Draft_Class column to show the draft classes of players from UCLA"
    ],
    "intermediate_tables": [
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
""",
"""
col : Draft_Class
row 5 : 2000 MLS SuperDraft
row 11 : 2006 MLS SuperDraft
"""
    ]
  },

  "EXAMPLE_6": {
    "table_info": """
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 1 : 1996.0 | Steve Ralston Category:Articles with hCards | Midfielder | 6 | 1 | 18 | 1996 MLS College Draft | Florida International
row 2 : 1997.0 | Mike Duhaney Category:Articles with hCards | Defender | 6 | 2 | 87 | 1996 MLS Inaugural Player Draft | UNLV
row 3 : 1998.0 | Ben Olsen Category:Articles with hCards | Midfielder | 4 | 3 | 2 | Project-40 | Virginia
row 4 : 1999.0 | Jay Heaps Category:Articles with hCards | Defender | 5 | 4 | 5 | 1999 MLS College Draft | Duke
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 6 : 2001.0 | Rodrigo Faria Category:Articles with hCards | Forward | 4 | 5 | 13 | 2001 MLS SuperDraft | Concordia College
row 7 : 2002.0 | Kyle Martino Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2002 MLS SuperDraft | Virginia
row 8 : 2003.0 | Damani Ralph Category:Articles with hCards | Forward | 1 | 2 | 18 | 2003 MLS SuperDraft | Connecticut
row 9 : 2004.0 | Clint Dempsey Category:Articles with hCards | Midfielder | 6 | 3 | 8 | 2004 MLS SuperDraft | Furman
row 10 : 2005.0 | Michael Parkhurst Category:Articles with hCards | Defender | 6 | 4 | 9 | 2005 MLS SuperDraft | Wake Forest
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
row 12 : 2007.0 | Maurice Edu Category:Articles with hCards | Midfielder | 4 | 9 | 1 | 2007 MLS SuperDraft | Maryland
row 13 : 2008.0 | Sean Franklin Category:Articles with hCards | Defender | 6 | 5 | 4 | 2008 MLS SuperDraft | Cal State Northridge
row 14 : 2009.0 | Omar Gonzalez Category:Articles with hCards | Defender | 6 | 5 | 3 | 2009 MLS SuperDraft | Maryland
row 15 : 2010.0 | Andy Najar Category:Articles with hCards | Midfielder | 4 | 5 | 6 | D.C. United Academy | none
row 16 : 2011.0 | C. J. Sapong Category:Articles with hCards | Forward | 6 | 3 | 10 | 2011 MLS SuperDraft | James Madison
    """,
    "question": "Count the number of different draft classes that players who play for UCLA are from.",
    "answer": "2",
    "explanation": "This question requires selecting rows where the College column equals 'UCLA', selecting the Draft_Class column, grouping by Draft_Class to count distinct values, and then adding an inferred column to count the number of distinct draft classes.",
    "chain": [
      "f_select_row()",
      "f_select_column()",
      "f_group_column()",
      "f_add_inferred_column()",
      "END"
    ],
    "filled_chain":[
      "f_select_row(row 5, row 11)",
      "f_select_column(Draft_Class)",
      "f_group_column(Draft_Class)",
      "f_add_inferred_column(Count_Draft_Classes)",
      "END"
    ],
    "explanations": [
        "Selecting rows where the College column equals 'UCLA', which are rows 5 and 11",
        "Selecting only the Draft_Class column for counting distinct values",
        "Grouping by Draft_Class to eliminate duplicates",
        "Adding an inferred column to count the number of distinct draft classes"
    ],
    "intermediate_tables": [
"""
col : Season | Player | Position | Country | Team | Draft_Pick_Number | Draft_Class | College
row 5 : 2000.0 | Carlos Bocanegra Category:Articles with hCards | Defender | 5 | 5 | 4 | 2000 MLS SuperDraft | UCLA
row 11 : 2006.0 | Jonathan Bornstein Category:Articles with hCards | Defender | 6 | 10 | 37 | 2006 MLS SuperDraft | UCLA
""",
"""
col : Draft_Class
row 5 : 2000 MLS SuperDraft
row 11 : 2006 MLS SuperDraft
""",
"""
col : Draft_Class | count
row 1 : 2000 MLS SuperDraft | 1
row 2 : 2006 MLS SuperDraft | 1
""",
"""
col : Draft_Class | count | Count_Draft_Classes
row 1 : 2000 MLS SuperDraft | 1 | 2
row 2 : 2006 MLS SuperDraft | 1 | 2
"""
    ]
  }
}