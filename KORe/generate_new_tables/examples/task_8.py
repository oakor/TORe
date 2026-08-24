# Task 8 Examples - SQL/Table Analysis (Aggregation and Calculation)

operations = """
Available Operations and their parameter requirements:
- f_add_knowledge_column(column_name): Add a new column that requires external knowledge
- f_add_inferred_column(column_name): Add a new column that can be calculated or inferred from existing columns
- f_sort_column(column_name): Sort the table by a specific column
- f_select_column(column1, column2, ...): Select specific columns from the table
- f_select_row(row1, row2, ...): Select specific rows from the table
- f_group_column(column_name): Group the table by a specific column
- f_change_column_name(old_name, new_name): Rename a column"""

task_8_EXAMPLES = {
    "EXAMPLE_1": {
        "table_info": """
col : ethnic group | 2001 (%) | 2001 (people) | 2006 (%) | 2006 (people)
row 1 : new zealand european | 66.9 | 684237 | 56.5 | 698622
row 2 : pacific islander | 14.9 | 152508 | 14.4 | 177936
row 3 : asian | 14.6 | 149121 | 18.9 | 234222
row 4 : māori | 11.5 | 117513 | 11.1 | 137133
row 5 : middle easterners / latin americans / africans | n / a | n / a | 1.5 | 18555
row 6 : others | 1.3 | 13455 | 0.1 | 648
row 7 : 'new zealanders' | n / a | n / a | 8.0 | 99258
        """,
        "chain": [
            "f_select_column()",
            "f_select_row()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(ethnic group, 2001 (people), 2006 (people))",
            "f_select_row(row 3)",
            "f_add_inferred_column(population_change)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for population comparison between 2001 and 2006",
            "Selecting the Asian ethnic group for population comparison which is row 3",
            "Adding a column to calculate the population change between 2001 and 2006"
        ],
        "intermediate_tables": [
            """
col : ethnic group | 2001 (people) | 2006 (people)
row 1 : new zealand european | 684237 | 698622
row 2 : pacific islander | 152508 | 177936
row 3 : asian | 149121 | 234222
row 4 : māori | 117513 | 137133
row 5 : middle easterners / latin americans / africans | n / a | 18555
row 6 : others | 13455 | 648
row 7 : 'new zealanders' | n / a | 99258
            """,
            """
col : ethnic group | 2001 (people) | 2006 (people)
row 3 : asian | 149121 | 234222
            """,
            """
col : ethnic group | 2001 (people) | 2006 (people) | population_change
row 3 : asian | 149121 | 234222 | 85101
            """
        ],
        "question": "What is the difference in the population count of the Asian ethnic group between the years 2001 and 2006?",
        "answer": "85101",
        "explanation": "This question requires selecting the relevant columns for the Asian ethnic group and calculating the difference between the 2006 and 2001 population counts. The calculation is 234222 - 149121 = 85101."
    },
    "EXAMPLE_2": {
        "table_info": """
col : central forest reserve | size in km square | total plant species | tree species | endemic | threatened (cr , vu , en)
row 1 : kashoya - kitomi | 385 | 901 | 419 | 41 | 17
row 2 : kalinzu | 140 | 787 | 442 | 34 | 12
row 3 : budongo | 817 | 1064 | 449 | 29 | 18
row 4 : echuya | 36 | 423 | 131 | 32 | 1
row 5 : bugoma | 400 | 256 | 245 | 7 | 12
row 6 : mafuga | 37 | 115 | 100 | 7 | 2
row 7 : kagombe | 178 | 211 | 201 | 3 | 5
row 8 : itwara | 87 | 258 | 248 | 7 | 10
row 9 : kitechura | 53 | 113 | 108 | 2 | 0
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(central forest reserve, total plant species)",
            "f_add_inferred_column(avg_plant_species)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for plant species analysis",
            "Adding a column to calculate the average number of total plant species across all central forest reserves"
        ],
        "intermediate_tables": [
            """
col : central forest reserve | total plant species
row 1 : kashoya - kitomi | 901
row 2 : kalinzu | 787
row 3 : budongo | 1064
row 4 : echuya | 423
row 5 : bugoma | 256
row 6 : mafuga | 115
row 7 : kagombe | 211
row 8 : itwara | 258
row 9 : kitechura | 113
            """,
            """
col : central forest reserve | total plant species | avg_plant_species
row 1 : kashoya - kitomi | 901 | 458.56
row 2 : kalinzu | 787 | 393.5 | 458.56
row 3 : budongo | 1064 | 532 | 458.56
row 4 : echuya | 423 | 211.5 | 458.56
row 5 : bugoma | 256 | 128 | 458.56
row 6 : mafuga | 115 | 57.5 | 458.56
row 7 : kagombe | 211 | 105.5 | 458.56
row 8 : itwara | 258 | 129 | 458.56
row 9 : kitechura | 113 | 56.5 | 458.56
            """
        ],
        "question": "What is the average number of total plant species across all central forest reserves?",
        "answer": "458.67",
        "explanation": "This question requires calculating the average of the total plant species across all forest reserves. The calculation is (901 + 787 + 1064 + 423 + 256 + 115 + 211 + 258 + 113) / 9 = 4128 / 9 = 458.67."
    },
    "EXAMPLE_3": {
        "table_info": """
col : season | ep | season premiere | season finale | ranking | viewers (households in millions) | rating
row 1 : season 1 | 24 | september 17 , 1972 | march 25 , 1973 | 46 | n / a | n / a
row 2 : season 2 | 24 | september 15 , 1973 | march 2 , 1974 | 4 | 17.02 | 25.7
row 3 : season 3 | 24 | september 10 , 1974 | march 18 , 1975 | 5 | 18.76 | 27.4
row 4 : season 4 | 24 | september 12 , 1975 | february 24 , 1976 | 15 | 15.93 | 22.9
row 5 : season 5 | 24 | september 21 , 1976 | march 15 , 1977 | 4 | 18.44 | 25.9
row 6 : season 6 | 24 | september 20 , 1977 | march 27 , 1978 | 9 | 16.91 | 23.2
row 7 : season 7 | 25 | september 18 , 1978 | march 12 , 1979 | 7 | 18.92 | 25.4
row 8 : season 8 | 25 | september 17 , 1979 | march 24 , 1980 | 5 | 19.30 | 25.3
row 9 : season 9 | 20 | november 17 , 1980 | may 4 , 1981 | 4 | 20.53 | 25.7
row 10 : season 10 | 21 | october 26 , 1981 | april 12 , 1982 | 9 | 18.17 | 22.3
row 11 : season 11 | 16 | october 25 , 1982 | february 28 , 1983 | 3 | 18.82 | 22.6
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "f_sort_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(season, ep)",
            "f_add_inferred_column(cumulative_episodes)",
            "f_sort_column(cumulative_episodes)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for episode count analysis",
            "Adding a column to calculate cumulative episode count across seasons",
            "Sorting by cumulative episodes to see progression"
        ],
        "intermediate_tables": [
            """
col : season | ep
row 1 : season 1 | 24
row 2 : season 2 | 24
row 3 : season 3 | 24
row 4 : season 4 | 24
row 5 : season 5 | 24
row 6 : season 6 | 24
row 7 : season 7 | 25
row 8 : season 8 | 25
row 9 : season 9 | 20
row 10 : season 10 | 21
row 11 : season 11 | 16
            """,
            """
col : season | ep | cumulative_episodes
row 1 : season 1 | 24 | 24
row 2 : season 2 | 24 | 48
row 3 : season 3 | 24 | 72
row 4 : season 4 | 24 | 96
row 5 : season 5 | 24 | 120
row 6 : season 6 | 24 | 144
row 7 : season 7 | 25 | 169
row 8 : season 8 | 25 | 194
row 9 : season 9 | 20 | 214
row 10 : season 10 | 21 | 235
row 11 : season 11 | 16 | 251
            """,
            """
col : season | ep | cumulative_episodes
row 1 : season 11 | 16 | 251
row 2 : season 10 | 21 | 235
row 3 : season 9 | 20 | 214
row 4 : season 8 | 25 | 194
row 5 : season 7 | 25 | 169
row 6 : season 6 | 24 | 144
row 7 : season 5 | 24 | 120
row 8 : season 4 | 24 | 96
row 9 : season 3 | 24 | 72
row 10 : season 2 | 24 | 48
row 11 : season 1 | 24 | 24
            """
        ],
        "question": "What is the total number of episodes across all seasons?",
        "answer": "251",
        "explanation": "This question requires summing the episode counts from all seasons. The calculation is 24 + 24 + 24 + 24 + 24 + 24 + 25 + 25 + 20 + 21 + 16 = 251 episodes in total."
    },
    "EXAMPLE_4": {
        "table_info": """
col : season | series | episode title | original air date | nick prod
row 1 : 1 | 156 | mario | april 30 , 2005 | 1001
row 2 : 2 | 157 | fantasia barrino | may 7 , 2005 | 1002
row 3 : 3 | 158 | jesse mccartney | may 14 , 2005 | 1003
row 4 : 4 | 159 | jojo | may 28 , 2005 | 1009
row 5 : 5 | 160 | tyler hilton | june 4 , 2005 | 1004
row 6 : 6 | 161 | drake bell | june 11 , 2005 | 1010
row 7 : 7 | 162 | bow wow | unaired | 1011
row 8 : 8 | 163 | avril lavigne | june 18 , 2005 | 1014
row 9 : 9 | 164 | lil romeo / b2k | september 10 , 2005 | 1013
row 10 : 10 | 165 | ashlee simpson | september 17 , 2005 | 1015
row 11 : 11 | 166 | frankie j | september 24 , 2005 | 1016
row 12 : 12 | 167 | morgan smith | october 1 , 2005 | 1005
row 13 : 13 | 168 | brooke valentine | october 8 , 2005 | 1006
row 14 : 14 | 169 | american hi - fi | october 15 , 2005 | 1007
row 15 : 15 | 170 | brie larson | unaired | 1012
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(nick prod)",
            "f_add_inferred_column(sum_nick_prod)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for production code analysis",
            "Adding a column to sum the production codes"
        ],
        "intermediate_tables": [
            """
col : nick prod
row 1 : 1001
row 2 : 1002
row 3 : 1003
row 4 : 1009
row 5 : 1004
row 6 : 1010
row 7 : 1011
row 8 : 1014
row 9 : 1013
row 10 : 1015
row 11 : 1016
row 12 : 1005
row 13 : 1006
row 14 : 1007
row 15 : 1012
            """,
            """
col : nick prod | sum_nick_prod
row 1 : 1001 | 1001
row 2 : 1002 | 2003
row 3 : 1003 | 3006
row 4 : 1009 | 4015
row 5 : 1004 | 5019
row 6 : 1010 | 6029
row 7 : 1011 | 7040
row 8 : 1014 | 8054
row 9 : 1013 | 9067
row 10 : 1015 | 10082
row 11 : 1016 | 11098
row 12 : 1005 | 12103
row 13 : 1006 | 13109
row 14 : 1007 | 14116
row 15 : 1012 | 15128
            """
        ],
        "question": "What is the total sum of the 'nick prod' values for all episodes listed in the table?",
        "answer": "15028",
        "explanation": "This question requires summing all the production code values from the 'nick prod' column. The calculation is 1001 + 1002 + 1003 + 1009 + 1004 + 1010 + 1011 + 1014 + 1013 + 1015 + 1016 + 1005 + 1006 + 1007 + 1012 = 15028."
    },
    "EXAMPLE_5": {
        "table_info": """
col : name | rank | out of | source | year
row 1 : environmental sustainability index | 132 | 146 | yale university | 2005
row 2 : greenhouse emissions per capita | 74 | world | world resources institute | 2000
row 3 : number of species under threat of extinction | 37 | 158 | united nations | 1999
row 4 : happy planet index | 81 | 178 | new economics foundation | 2009
row 5 : environmental performance index | 78 | 153 | yale university / columbia university | 2010
row 6 : total renewable water resources | 58 | 151 | cia world factbook | 2008
row 7 : water availability per capita | 116 | 141 | united nations | 2001
row 8 : biodiversity richness | 13 | 53 | world conservation monitoring centre | 1994
row 9 : carbon efficiency | 28 | 141 | carbon dioxide information analysis center | 2005
row 10 : coral reefs area | 19 | 28 | united nations | 2005
row 11 : endangered species protection | 71 | 141 | cites | 2000
row 12 : land use statistics by country | 16 | 176 | cia world factbook | 2005
row 13 : carbon dioxide emissions per capita | 70 | 210 | united nations | 2003
row 14 : total carbon dioxide emissions | 11 | 210 | united nations | 2006
row 15 : total forest area | 47 | 220 | united nations | 2007
row 16 : fresh water withdrawal | 11 | 168 | cia world factbook | 2000
row 17 : industrial water pollution | 14 | 129 | world bank | 2003
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(rank)",
            "f_add_inferred_column(avg_rank)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for rank analysis",
            "Adding a column to calculate the average rank"
        ],
        "intermediate_tables": [
            """
col : rank
row 1 : 132
row 2 : 74
row 3 : 37
row 4 : 81
row 5 : 78
row 6 : 58
row 7 : 116
row 8 : 13
row 9 : 28
row 10 : 19
row 11 : 71
row 12 : 16
row 13 : 70
row 14 : 11
row 15 : 47
row 16 : 11
row 17 : 14
            """,
            """
col : rank | avg_rank
row 1 : 132 | 51.53
row 2 : 74 | 51.53
row 3 : 37 | 51.53
row 4 : 81 | 51.53
row 5 : 78 | 51.53
row 6 : 58 | 51.53
row 7 : 116 | 51.53
row 8 : 13 | 51.53
row 9 : 28 | 51.53
row 10 : 19 | 51.53
row 11 : 71 | 51.53
row 12 : 16 | 51.53
row 13 : 70 | 51.53
row 14 : 11 | 51.53
row 15 : 47 | 51.53
row 16 : 11 | 51.53
row 17 : 14 | 51.53
            """
        ],
        "question": "What is the average rank of all the indices listed in the table?",
        "answer": "51.53",
        "explanation": "This question requires calculating the average of all rank values in the table. The calculation is (132 + 74 + 37 + 81 + 78 + 58 + 116 + 13 + 28 + 19 + 71 + 16 + 70 + 11 + 47 + 11 + 14) / 17 = 876 / 17 = 51.53."
    },
    "EXAMPLE_6": {
        "table_info": """
col : Gun | July 1914 | December 1914 | May 1915 | August 1917
row 1 : 10 inch 45 caliber model 1891 | 0 | 16 | 16 | 24
row 2 : 11 inch model 1877 | 10 | 19 | 20 | 12
row 3 : 6 inch 45 caliber model 1892 Canet | 12 | 12 | 12 | 16+4
row 4 : 6 in (152 mm) 22 caliber siege gun model 1877 | 29 | 2 | 0 | 0
row 5 : 75 mm 50 caliber model 1892 Canet | 0 | 14 | 20 | 12
row 6 : 57 mm 48 caliber Nordenfelt | 2 | 15 | 15 | 20
row 7 : 11 inch model 1877 mortar | 9 | 8 | 4 | 0
        """,
        "chain": [
            "f_add_inferred_column()",
            "f_select_column()",
            "END"
        ],
        "filled_chain": [
            "f_add_inferred_column(total_guns_august_1917)",
            "f_select_column(Gun, August 1917, total_guns_august_1917)",
            "END"
        ],
        "explanations": [
            "Adding a column to calculate the total number of guns in August 1917",
            "Selecting relevant columns for the total number of guns in August 1917"
        ],
        "intermediate_tables": [
            """
col : Gun | July 1914 | December 1914 | May 1915 | August 1917 | total_guns_august_1917
row 1 : 10 inch 45 caliber model 1891 | 0 | 16 | 16 | 24 | 24
row 2 : 11 inch model 1877 | 10 | 19 | 20 | 12 | 36
row 3 : 6 inch 45 caliber model 1892 Canet | 12 | 12 | 12 | 16+4 | 56
row 4 : 6 in (152 mm) 22 caliber siege gun model 1877 | 29 | 2 | 0 | 0 | 56
row 5 : 75 mm 50 caliber model 1892 Canet | 0 | 14 | 20 | 12 | 68
row 6 : 57 mm 48 caliber Nordenfelt | 2 | 15 | 15 | 20 | 88
row 7 : 11 inch model 1877 mortar | 9 | 8 | 4 | 0 | 88
            """,
            """
col : Gun | August 1917 | total_guns_august_1917
row 1 : 10 inch 45 caliber model 1891 | 24 | 24
row 2 : 11 inch model 1877 | 12 | 36
row 3 : 6 inch 45 caliber model 1892 Canet | 16+4 | 56
row 4 : 6 in (152 mm) 22 caliber siege gun model 1877 | 0 | 56
row 5 : 75 mm 50 caliber model 1892 Canet | 12 | 68
row 6 : 57 mm 48 caliber Nordenfelt | 20 | 88
row 7 : 11 inch model 1877 mortar | 0 | 88
            """
        ],
        "question": "What is the total number of guns in August 1917 across all models?",
        "answer": "88",
        "explanation": "This question requires summing the values in the August 1917 column for all gun models. The calculation is 24 + 12 + 20 + 0 + 12 + 20 + 0 = 88 guns."
    },
    "EXAMPLE_7": {
        "table_info": """
col : rank | company | headquarters | industry | sales (billion ) | profits (billion ) | assets (billion ) | market value (billion )
row 1 : 1 | citigroup | usa | banking | 146.56 | 21.54 | 1884.32 | 247.42
row 2 : 2 | bank of america | usa | banking | 116.57 | 21.13 | 1459.74 | 226.61
row 3 : 3 | hsbc | uk | banking | 121.51 | 16.63 | 1860.76 | 202.29
row 4 : 4 | general electric | usa | conglomerate | 163.39 | 20.83 | 697.24 | 358.98
row 5 : 5 | jpmorgan chase | usa | banking | 99.3 | 14.44 | 1351.52 | 170.97
row 6 : 6 | american international group | usa | insurance | 113.19 | 14.01 | 979.41 | 174.47
row 7 : 7 | exxonmobil | usa | oil and gas | 335.09 | 39.5 | 223.95 | 410.65
row 8 : 8 | royal dutch shell | netherlands | oil and gas | 318.85 | 25.44 | 232.31 | 208.25
row 9 : 9 | ubs | switzerland | diversified financials | 105.59 | 9.78 | 1776.89 | 116.84
row 10 : 10 | ing group | netherlands | diversified financials | 153.44 | 9.65 | 1615.05 | 93.99
row 11 : 11 | bp | uk | oil and gas | 265.91 | 22.29 | 217.6 | 198.14
row 12 : 12 | toyota | japan | automotive | 179.02 | 11.68 | 243.6 | 217.69
row 13 : 13 | the royal bank of scotland | uk | banking | 77.41 | 12.51 | 1705.35 | 124.13
row 14 : 14 | bnp paribas | france | banking | 89.16 | 9.64 | 1898.19 | 97.03
row 15 : 15 | allianz | germany | insurance | 125.33 | 8.81 | 1380.88 | 87.22
row 16 : 16 | berkshire hathaway | usa | diversified financials | 98.54 | 11.02 | 248.44 | 163.79
row 17 : 17 | walmart | usa | retailing | 348.65 | 11.29 | 151.19 | 201.36
row 18 : 18 | barclays | uk | banking | 67.71 | 8.95 | 1949.17 | 94.79
row 19 : 19 | chevron | usa | oil and gas | 195.34 | 17.14 | 132.63 | 149.37
        """,
        "chain": [
            "f_select_column()",
            "f_select_row()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(company, sales (billion ))",
            "f_select_row(row 1)",
            "f_add_inferred_column(projected_sales)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for sales analysis",
            "Select the row of Citigroup which is row 1",
            "Adding a column to calculate projected sales with 10% increase"
        ],
        "intermediate_tables": [
            """
col : company | sales (billion )
row 1 : citigroup | 146.56
row 2 : bank of america | 116.57
row 3 : hsbc | 121.51
row 4 : general electric | 163.39
row 5 : jpmorgan chase | 99.3
row 6 : american international group | 113.19
row 7 : exxonmobil | 335.09
row 8 : royal dutch shell | 318.85
row 9 : ubs | 105.59
row 10 : ing group | 153.44
row 11 : bp | 265.91
row 12 : toyota | 179.02
row 13 : the royal bank of scotland | 77.41
row 14 : bnp paribas | 89.16
row 15 : allianz | 125.33
row 16 : berkshire hathaway | 98.54
row 17 : walmart | 348.65
row 18 : barclays | 67.71
row 19 : chevron | 195.34
            """,
            """
col : company | sales (billion )
row 1 : citigroup | 146.56
            """,
            """
col : company | sales (billion ) | projected_sales
row 1 : citigroup | 146.56 | 161.216
            """
        ],
        "question": "If the sales of Citigroup increase by 10% next year, approximately how much will the sales be?",
        "answer": "161.216",
        "explanation": "This question requires calculating a 10% increase on Citigroup's current sales. The calculation is 146.56 × 1.10 = 146.56 + 14.656 = 161.216 billion."
    },
    "EXAMPLE_8": {
        "table_info": """
col : year | revenue | expenses | profit | employees
row 1 : 2015 | 12500000 | 10000000 | 2500000 | 150
row 2 : 2016 | 15000000 | 11500000 | 3500000 | 175
row 3 : 2017 | 17500000 | 13000000 | 4500000 | 200
row 4 : 2018 | 20000000 | 15000000 | 5000000 | 225
row 5 : 2019 | 22500000 | 17000000 | 5500000 | 250
row 6 : 2020 | 18000000 | 16000000 | 2000000 | 200
row 7 : 2021 | 24000000 | 18000000 | 6000000 | 275
        """,
        "chain": [
            "f_select_column()",
            "f_add_inferred_column()",
            "END"
        ],
        "filled_chain": [
            "f_select_column(year, profit)",
            "f_add_inferred_column(avg_profit)",
            "END"
        ],
        "explanations": [
            "Selecting relevant columns for profit analysis",
            "Adding a column to calculate the average profit"
        ],
        "intermediate_tables": [
            """
col : year | profit
row 1 : 2015 | 2500000
row 2 : 2016 | 3500000
row 3 : 2017 | 4500000
row 4 : 2018 | 5000000
row 5 : 2019 | 5500000
row 6 : 2020 | 2000000
row 7 : 2021 | 6000000
            """,
            """
col : year | profit | avg_profit
row 1 : 2015 | 2500000 | 4142857.14
row 2 : 2016 | 3500000 | 4142857.14
row 3 : 2017 | 4500000 | 4142857.14
row 4 : 2018 | 5000000 | 4142857.14
row 5 : 2019 | 5500000 | 4142857.14
row 6 : 2020 | 2000000 | 4142857.14
row 7 : 2021 | 6000000 | 4142857.14
            """
        ],
        "question": "What was the average annual profit between 2015 and 2021?",
        "answer": "4142857.14",
        "explanation": "This question requires calculating the average profit across all years. The calculation is (2500000 + 3500000 + 4500000 + 5000000 + 5500000 + 2000000 + 6000000) / 7 = 29000000 / 7 = 4142857.14."
    }
}