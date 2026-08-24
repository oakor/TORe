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


task_4_EXAMPLES_single = {
    "EXAMPLE_1": {
    "table_info": """
col : rank | gold | country
row 1 : 1 | 36 | China
row 2 : 2 | 18 | America
row 3 : 3 | 11 | Russia
row 4 : 4 | 9 | United Kingdom
    """,
    "chain": [
        "f_add_knowledge_column()",
        "f_group_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_knowledge_column(region)",
        "f_group_column(region)",
        "f_sort_column(count)",
        "END"
    ],
    "explanations": [
        "Adding region information to identify Asian countries",
        "Grouping by region to count gold medals by continent",
        "Sorting by count to find regions with most countries"
    ],
    "intermediate_tables": [
        """
col : rank | gold | country | region
row 1 : 1 | 36 | China | Asia
row 2 : 2 | 18 | America | America
row 3 : 3 | 11 | Russia | Europe
row 4 : 4 | 9 | United Kingdom | Europe
        """,
        """
col : region | count
row 1 : Asia | 1
row 2 : America | 1
row 3 : Europe | 2
        """,
        """
col : region | count
row 1 : Europe | 2
row 2 : Asia | 1
row 3 : America | 1
        """
    ],
    "question": "Which region has the most countries in the top 4?",
    "answer": "Europe",
    "explanation": "This question requires adding region information to identify the continents each country belongs to, grouping by region to count how many countries from each region are in the top 4, and then sorting by count to find the region with the most countries. The final table shows that Europe has the most countries (2) in the top 4."
},
    "EXAMPLE_2": {
    "table_info": """
col : year | team | games | wins | losses | points
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64
row 5 : 2024 | Lakers | 82 | 28 | 54 | 56
row 6 : 2025 | Lakers | 82 | 25 | 57 | 50
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_select_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(win_percentage)",
        "f_add_inferred_column(win_trend)",
        "f_sort_column(win_percentage)",
        "f_select_column(year, win_percentage, win_trend)",
        "END"
    ],
    "explanations": [
        "Calculating win percentage by dividing wins by total games",
        "Calculating win trend by comparing with previous season",
        "Sorting by win percentage to find the best performing season",
        "Selecting relevant columns for trend analysis"
    ],
    "intermediate_tables": [
        """
col : year | team | games | wins | losses | points | win_percentage
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | 63.41
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | 51.22
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | 40.24
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64 | 39.02
row 5 : 2024 | Lakers | 82 | 28 | 54 | 56 | 34.15
row 6 : 2025 | Lakers | 82 | 25 | 57 | 50 | 30.49
        """,
        """
col : year | team | games | wins | losses | points | win_percentage | win_trend
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | 63.41 | N/A
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | 51.22 | -12.19
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | 40.24 | -10.98
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64 | 39.02 | -1.22
row 5 : 2024 | Lakers | 82 | 28 | 54 | 56 | 34.15 | -4.87
row 6 : 2025 | Lakers | 82 | 25 | 57 | 50 | 30.49 | -3.66
        """,
        """
col : year | team | games | wins | losses | points | win_percentage | win_trend
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | 63.41 | N/A 
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | 51.22 | -12.19
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | 40.24 | -10.98
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64 | 39.02 | -1.22
row 5 : 2024 | Lakers | 82 | 28 | 54 | 56 | 34.15 | -4.87
row 6 : 2025 | Lakers | 82 | 25 | 57 | 50 | 30.49 | -3.66
        """,
        """
col : year | win_percentage | win_trend
row 1 : 2020 | 63.41 | N/A
row 2 : 2021 | 51.22 | -12.19
row 3 : 2022 | 40.24 | -10.98
row 4 : 2023 | 39.02 | -1.22
row 5 : 2024 | 34.15 | -4.87
row 6 : 2025 | 30.49 | -3.66
        """
    ],
    "question": "What was the biggest year-over-year decline in win percentage for the Lakers?",
    "answer": "2021 season",
    "explanation": "This question requires calculating win percentage by dividing wins by total games for each season, then calculating the win trend by comparing with the previous season, sorting by win percentage to see performance over time, and selecting relevant columns for trend analysis. The final table shows that 2021 had the biggest decline in win percentage (-12.19 points) compared to the previous season."
},
    "EXAMPLE_3": {
    "table_info": """
col : name | age | city | salary | department
row 1 : John | 35 | New York | 85000 | Sales
row 2 : Mary | 28 | Boston | 72000 | Marketing
row 3 : Tom | 42 | Chicago | 95000 | Sales
row 4 : Sarah | 31 | New York | 78000 | HR
row 5 : Mike | 39 | Boston | 88000 | Sales
row 6 : Lisa | 26 | Chicago | 65000 | Marketing
row 7 : David | 45 | New York | 92000 | Sales
row 8 : Emma | 33 | Boston | 75000 | HR
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(name, city, salary, department)",
        "f_select_row(row 1, row 3, row 5, row 7)",
        "f_add_inferred_column(salary_level)",
        "f_sort_column(salary)",
        "f_group_column(city)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for salary analysis",
        "Filtering rows to show only Sales department employees",
        "Adding salary level based on salary ranges",
        "Sorting by salary to find highest paid employees",
        "Grouping by city to analyze salary distribution"
    ],
    "intermediate_tables": [
        """
col : name | city | salary | department
row 1 : John | New York | 85000 | Sales
row 2 : Mary | Boston | 72000 | Marketing
row 3 : Tom | Chicago | 95000 | Sales
row 4 : Sarah | New York | 78000 | HR
row 5 : Mike | Boston | 88000 | Sales
row 6 : Lisa | Chicago | 65000 | Marketing
row 7 : David | New York | 92000 | Sales
row 8 : Emma | Boston | 75000 | HR
        """,
        """
col : name | city | salary | department
row 1 : John | New York | 85000 | Sales
row 3 : Tom | Chicago | 95000 | Sales
row 5 : Mike | Boston | 88000 | Sales
row 7 : David | New York | 92000 | Sales
        """,
        """
col : name | city | salary | department | salary_level
row 1 : John | New York | 85000 | Sales | High
row 3 : Tom | Chicago | 95000 | Sales | High
row 5 : Mike | Boston | 88000 | Sales | High
row 7 : David | New York | 92000 | Sales | High
        """,
        """
col : name | city | salary | department | salary_level
row 1 : Tom | Chicago | 95000 | Sales | High
row 2 : David | New York | 92000 | Sales | High
row 3 : Mike | Boston | 88000 | Sales | High
row 4 : John | New York | 85000 | Sales | High
        """,
        """
col : city | avg_salary | count
row 1 : Chicago | 95000 | 1
row 2 : New York | 88500 | 2
row 3 : Boston | 88000 | 1
        """
    ],
    "question": "Which city has the highest average salary for Sales employees?",
    "answer": "Chicago",
    "explanation": "This question requires selecting relevant columns for salary analysis, filtering rows to show only Sales department employees, adding salary level based on salary ranges, sorting by salary to find highest paid employees, and grouping by city to analyze salary distribution. The final table shows that Chicago has the highest average salary ($95,000) for Sales employees."
},
    "EXAMPLE_4": {
    "table_info": """
col : Tenure | Coach | Years | Record | Pct.
row 1 : 1892 | Shelby Fletcher | 1 | 1–0 | 1.000
row 2 : 1893 | W. M. Walker | 1 | 4–6–1 | .409
row 3 : 1894 | J. H. Lyons | 1 | 10–3 | .769
row 4 : 1895 | J. F. Jenkins | 1 | 9–3 | .750
row 5 : 1896 | Eli Abbott | 1 | 5–5 | .500
row 6 : 1897 | "Kid" Peeples | 1 | 10–0 | 1.000
row 7 : 1898 | Joseph Black | 1 | 2–3 | .400
row 8 : 1899 | F. C. Owen | 1 | 3–6 | .333
row 9 : 1900 | Ardis Smith | 1 | 9–3 | .750
row 10 : 1901–1905 | Thomas Stouch | 5 | 49–25–1 | .660
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_group_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(experience_category)",
        "f_select_column(Coach, Years, experience_category)",
        "f_group_column(experience_category)",
        "f_sort_column(avg_years)",
        "END"
    ],
    "explanations": [
        "Adding a column to categorize coaches based on their years of experience",
        "Selecting relevant columns for analysis",
        "Grouping by experience category to calculate average years",
        "Sorting by average years to find experience distribution"
    ],
    "intermediate_tables": [
        """
col : Tenure | Coach | Years | Record | Pct. | experience_category
row 1 : 1892 | Shelby Fletcher | 1 | 1–0 | 1.000 | Short-term
row 2 : 1893 | W. M. Walker | 1 | 4–6–1 | .409 | Short-term
row 3 : 1894 | J. H. Lyons | 1 | 10–3 | .769 | Short-term
row 4 : 1895 | J. F. Jenkins | 1 | 9–3 | .750 | Short-term
row 5 : 1896 | Eli Abbott | 1 | 5–5 | .500 | Short-term
row 6 : 1897 | "Kid" Peeples | 1 | 10–0 | 1.000 | Short-term
row 7 : 1898 | Joseph Black | 1 | 2–3 | .400 | Short-term
row 8 : 1899 | F. C. Owen | 1 | 3–6 | .333 | Short-term
row 9 : 1900 | Ardis Smith | 1 | 9–3 | .750 | Short-term
row 10 : 1901–1905 | Thomas Stouch | 5 | 49–25–1 | .660 | Long-term
        """,
        """
col : Coach | Years | experience_category
row 1 : Shelby Fletcher | 1 | Short-term
row 2 : W. M. Walker | 1 | Short-term
row 3 : J. H. Lyons | 1 | Short-term
row 4 : J. F. Jenkins | 1 | Short-term
row 5 : Eli Abbott | 1 | Short-term
row 6 : "Kid" Peeples | 1 | Short-term
row 7 : Joseph Black | 1 | Short-term
row 8 : F. C. Owen | 1 | Short-term
row 9 : Ardis Smith | 1 | Short-term
row 10 : Thomas Stouch | 5 | Long-term
        """,
        """
col : experience_category | count | avg_years
row 1 : Short-term | 9 | 1.0
row 2 : Long-term | 1 | 5.0
        """,
        """
col : experience_category | count | avg_years
row 1 : Long-term | 1 | 5.0
row 2 : Short-term | 9 | 1.0
        """
    ],
    "question": "What was the average number of years served by coaches in each experience category?",
    "answer": "Long-term coaches: 5.0 years; Short-term coaches: 1.0 year",
    "explanation": "This question requires adding a column to categorize coaches based on their years of experience, selecting relevant columns for analysis, grouping by experience category to calculate average years, and sorting by average years to find experience distribution. The final table shows that long-term coaches served an average of 5.0 years, while short-term coaches served an average of 1.0 year."
},
    "EXAMPLE_5": {
    "table_info": """
col : Year | Car | Start | Qual | Rank | Finish | Laps | Led | Retired
row 1 : 1961 | 98 | 5 | 146.080 | 7 | 12 | 192 | 27 | Flagged
row 2 : 1962 | 98 | 1 | 150.370 | 1 | 7 | 200 | 120 | Running
row 3 : 1963 | 98 | 1 | 151.153 | 1 | 1 | 200 | 167 | Running
row 4 : 1964 | 98 | 4 | 155.099 | 4 | 23 | 55 | 7 | Pit fire
row 5 : 1965 | 98 | 5 | 158.625 | 5 | 2 | 200 | 0 | Running
row 6 : 1966 | 98 | 4 | 162.484 | 4 | 14 | 87 | 0 | Wheel Bearing
row 7 : 1967 | 40 | 6 | 166.075 | 6 | 6 | 196 | 171 | Bearing
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(speed_increase)",
        "f_select_column(Year, Car, Qual, speed_increase)",
        "f_sort_column(Qual)",
        "f_select_row(row 7)",
        "END"
    ],
    "explanations": [
        "Adding a column to calculate the speed increase from the previous year",
        "Selecting relevant columns for qualification speed analysis",
        "Sorting by qualification speed to find the fastest car",
        "Selecting the row with the highest qualification speed"
    ],
    "intermediate_tables": [
        """
col : Year | Car | Start | Qual | Rank | Finish | Laps | Led | Retired | speed_increase
row 1 : 1961 | 98 | 5 | 146.080 | 7 | 12 | 192 | 27 | Flagged | N/A
row 2 : 1962 | 98 | 1 | 150.370 | 1 | 7 | 200 | 120 | Running | 4.290
row 3 : 1963 | 98 | 1 | 151.153 | 1 | 1 | 200 | 167 | Running | 0.783
row 4 : 1964 | 98 | 4 | 155.099 | 4 | 23 | 55 | 7 | Pit fire | 3.946
row 5 : 1965 | 98 | 5 | 158.625 | 5 | 2 | 200 | 0 | Running | 3.526
row 6 : 1966 | 98 | 4 | 162.484 | 4 | 14 | 87 | 0 | Wheel Bearing | 3.859
row 7 : 1967 | 40 | 6 | 166.075 | 6 | 6 | 196 | 171 | Bearing | 3.591
        """,
        """
col : Year | Car | Qual | speed_increase
row 1 : 1961 | 98 | 146.080 | N/A
row 2 : 1962 | 98 | 150.370 | 4.290
row 3 : 1963 | 98 | 151.153 | 0.783
row 4 : 1964 | 98 | 155.099 | 3.946
row 5 : 1965 | 98 | 158.625 | 3.526
row 6 : 1966 | 98 | 162.484 | 3.859
row 7 : 1967 | 40 | 166.075 | 3.591
        """,
        """
col : Year | Car | Qual | speed_increase
row 1 : 1967 | 40 | 166.075 | 3.591
row 2 : 1966 | 98 | 162.484 | 3.859
row 3 : 1965 | 98 | 158.625 | 3.526
row 4 : 1964 | 98 | 155.099 | 3.946
row 5 : 1963 | 98 | 151.153 | 0.783
row 6 : 1962 | 98 | 150.370 | 4.290
row 7 : 1961 | 98 | 146.080 | N/A
        """,
        """
col : Year | Car | Qual | speed_increase
row 1 : 1967 | 40 | 166.075 | 3.591
        """
    ],
    "question": "What car achieved the highest qualification speed?",
    "answer": "Car 40",
    "explanation": "This question requires adding a column to calculate the speed increase from the previous year, selecting relevant columns for qualification speed analysis, sorting by qualification speed to find the fastest car, and selecting the row with the highest qualification speed. The final table shows that Car 40 achieved the highest qualification speed (166.075) in 1967."
},
    "EXAMPLE_6": {
    "table_info": """
col : Treaty | Organization | Introduced | Signed | Ratified
row 1 : Convention on the Prevention and Punishment of the Crime of Genocide | United Nations | 1948 | - | 1958
row 2 : International Convention on the Elimination of All Forms of Racial Discrimination | United Nations | 1966 | 1967 | 1970
row 3 : International Covenant on Economic, Social and Cultural Rights | United Nations | 1966 | 1977 | 1979
row 4 : International Covenant on Civil and Political Rights | United Nations | 1966 | 1977 | 1979
row 5 : Convention on the Elimination of All Forms of Discrimination against Women | United Nations | 1979 | - | 1993
row 6 : Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment | United Nations | 1984 | 1986 | 1993
row 7 : Convention on the Rights of the Child | United Nations | 1989 | 1990 | 1993
row 8 : International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families | United Nations | 1990 | 1991 | 1993
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_group_column()",
        "f_select_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(ratification_delay)",
        "f_group_column(Ratified)",
        "f_select_column(Ratified, count, treaties)",
        "f_sort_column(count)",
        "END"
    ],
    "explanations": [
        "Adding a column to calculate the delay between introduction and ratification",
        "Grouping by ratification year to count treaties ratified each year",
        "Selecting relevant columns for analysis",
        "Sorting by count to find years with most ratifications"
    ],
    "intermediate_tables": [
        """
col : Treaty | Organization | Introduced | Signed | Ratified | ratification_delay
row 1 : Convention on the Prevention and Punishment of the Crime of Genocide | United Nations | 1948 | - | 1958 | 10
row 2 : International Convention on the Elimination of All Forms of Racial Discrimination | United Nations | 1966 | 1967 | 1970 | 4
row 3 : International Covenant on Economic, Social and Cultural Rights | United Nations | 1966 | 1977 | 1979 | 13
row 4 : International Covenant on Civil and Political Rights | United Nations | 1966 | 1977 | 1979 | 13
row 5 : Convention on the Elimination of All Forms of Discrimination against Women | United Nations | 1979 | - | 1993 | 14
row 6 : Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment | United Nations | 1984 | 1986 | 1993 | 9
row 7 : Convention on the Rights of the Child | United Nations | 1989 | 1990 | 1993 | 4
row 8 : International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families | United Nations | 1990 | 1991 | 1993 | 3
        """,
        """
col : Ratified | count | treaties
row 1 : 1958 | 1 | Convention on the Prevention and Punishment of the Crime of Genocide
row 2 : 1970 | 1 | International Convention on the Elimination of All Forms of Racial Discrimination
row 3 : 1979 | 2 | International Covenant on Economic, Social and Cultural Rights, International Covenant on Civil and Political Rights
row 4 : 1993 | 4 | Convention on the Elimination of All Forms of Discrimination against Women, Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment, Convention on the Rights of the Child, International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families
        """,
        """
col : Ratified | count | treaties
row 1 : 1958 | 1 | Convention on the Prevention and Punishment of the Crime of Genocide
row 2 : 1970 | 1 | International Convention on the Elimination of All Forms of Racial Discrimination
row 3 : 1979 | 2 | International Covenant on Economic, Social and Cultural Rights, International Covenant on Civil and Political Rights
row 4 : 1993 | 4 | Convention on the Elimination of All Forms of Discrimination against Women, Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment, Convention on the Rights of the Child, International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families
        """,
        """
col : Ratified | count | treaties
row 1 : 1993 | 4 | Convention on the Elimination of All Forms of Discrimination against Women, Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment, Convention on the Rights of the Child, International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families
row 2 : 1979 | 2 | International Covenant on Economic, Social and Cultural Rights, International Covenant on Civil and Political Rights
row 3 : 1970 | 1 | International Convention on the Elimination of All Forms of Racial Discrimination
row 4 : 1958 | 1 | Convention on the Prevention and Punishment of the Crime of Genocide
        """
    ],
    "question": "What year did Monaco ratify more international human rights treaties than they did in 1979?",
    "answer": "1993",
    "explanation": "This question requires calculating the delay between introduction and ratification, grouping by ratification year, counting treaties per year, and sorting to compare years. The final table shows that Monaco ratified 4 treaties in 1993, which is more than the 2 treaties ratified in 1979."
},
    "EXAMPLE_7": {
    "table_info": """
col : Place | Code | Area (km2) | Population | Most spoken language
row 1 : Beatrix Mine | 40701 | 0.17 | 2,492 | Sotho
row 2 : Boipatong | 40702 | 0.31 | 1,501 | Sotho
row 3 : Brandfort | 40703 | 3.20 | 1,516 | Afrikaans
row 4 : Fora | 40704 | 0.05 | 530 | Sotho
row 5 : Ikgomotseng | 40705 | 1.07 | 2,254 | Tswana
row 6 : Joel Mine | 40706 | 0.11 | 728 | Sotho
row 7 : Lusaka | 40707 | 1.40 | 6,110 | Sotho
row 8 : Majwemasweu | 40708 | 2.50 | 10,328 | Sotho
row 9 : Makeleketla | 40709 | 1.35 | 6,629 | Sotho
row 10 : Masilo | 40710 | 3.02 | 14,903 | Sotho
    """,
    "chain": [
        "f_select_column()",
        "f_group_column()",
        "f_sort_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Place, Most spoken language, Population)",
        "f_group_column(Most spoken language)",
        "f_sort_column(total_population)",
        "f_add_inferred_column(population_percentage)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for language analysis",
        "Grouping by language to count places and population per language",
        "Sorting by total population to find most populous language groups",
        "Adding percentage column to show language distribution"
    ],
    "intermediate_tables": [
        """
col : Place | Most spoken language | Population
row 1 : Beatrix Mine | Sotho | 2,492
row 2 : Boipatong | Sotho | 1,501
row 3 : Brandfort | Afrikaans | 1,516
row 4 : Fora | Sotho | 530
row 5 : Ikgomotseng | Tswana | 2,254
row 6 : Joel Mine | Sotho | 728
row 7 : Lusaka | Sotho | 6,110
row 8 : Majwemasweu | Sotho | 10,328
row 9 : Makeleketla | Sotho | 6,629
row 10 : Masilo | Sotho | 14,903
        """,
        """
col : Most spoken language | count | total_population
row 1 : Sotho | 8 | 43,221
row 2 : Afrikaans | 1 | 1,516
row 3 : Tswana | 1 | 2,254
        """,
        """
col : Most spoken language | count | total_population
row 1 : Sotho | 8 | 43,221
row 2 : Tswana | 1 | 2,254
row 3 : Afrikaans | 1 | 1,516
        """,
        """
col : Most spoken language | count | total_population | population_percentage
row 1 : Sotho | 8 | 43,221 | 91.99%
row 2 : Tswana | 1 | 2,254 | 4.80%
row 3 : Afrikaans | 1 | 1,516 | 3.21%
        """
    ],
    "question": "How many different languages are listed?",
    "answer": "3",
    "explanation": "This question requires selecting relevant columns, grouping by language, and counting distinct languages. The final table shows three different languages listed in the region: Sotho, Tswana, and Afrikaans, with Sotho being the most common language spoken by 91.99% of the population."
},
    "EXAMPLE_8": {
    "table_info": """
col : Title | Platform | Developer | Publisher | Release Date | Genre
row 1 : ABZÛ | PlayStation 4, Windows, Xbox One, Nintendo Switch | Giant Squid | 505 Games | August 2, 2016 | Adventure
row 2 : The Unfinished Swan | PlayStation 3, PlayStation 4, PlayStation Vita | Giant Squid | Sony Computer Entertainment | October 15, 2012 | Puzzle
row 3 : Rime | PlayStation 4, Nintendo Switch, Windows, Xbox One | Tequila Works | Grey Box | May 26, 2017 | Puzzle, Adventure
row 4 : Flower | PlayStation 3, PlayStation 4, PlayStation Vita, iOS | Thatgamecompany | Sony Computer Entertainment | February 12, 2009 | Adventure
row 5 : Journey | PlayStation 3, PlayStation 4, Windows, iOS | Thatgamecompany | Sony Computer Entertainment | March 13, 2012 | Adventure
row 6 : The Pathless | PlayStation 4, PlayStation 5, Windows, iOS | Giant Squid | Annapurna Interactive | November 12, 2020 | Action-adventure
row 7 : Sky: Children of the Light | iOS, Android, Nintendo Switch | Thatgamecompany | Thatgamecompany | July 18, 2019 | Adventure, Social
row 8 : Adr1ft | Windows, PlayStation 4, Xbox One | Three One Zero | 505 Games | March 28, 2016 | Adventure, Simulation
    """,
    "chain": [
        "f_select_column()",
        "f_add_inferred_column()",
        "f_select_row()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Title, Platform, Developer, Release Date)",
        "f_add_inferred_column(platforms_count)",
        "f_select_row(row 1, row 3, row 4, row 5, row 6)",
        "f_group_column(Developer)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for platform analysis",
        "Adding a column to count number of platforms per game",
        "Filtering for games available on more than 3 platforms",
        "Grouping by developer to analyze their multi-platform strategy"
    ],
    "intermediate_tables": [
        """
col : Title | Platform | Developer | Release Date
row 1 : ABZÛ | PlayStation 4, Windows, Xbox One, Nintendo Switch | Giant Squid | August 2, 2016
row 2 : The Unfinished Swan | PlayStation 3, PlayStation 4, PlayStation Vita | Giant Squid | October 15, 2012
row 3 : Rime | PlayStation 4, Nintendo Switch, Windows, Xbox One | Tequila Works | May 26, 2017
row 4 : Flower | PlayStation 3, PlayStation 4, PlayStation Vita, iOS | Thatgamecompany | February 12, 2009
row 5 : Journey | PlayStation 3, PlayStation 4, Windows, iOS | Thatgamecompany | March 13, 2012
row 6 : The Pathless | PlayStation 4, PlayStation 5, Windows, iOS | Giant Squid | November 12, 2020
row 7 : Sky: Children of the Light | iOS, Android, Nintendo Switch | Thatgamecompany | July 18, 2019
row 8 : Adr1ft | Windows, PlayStation 4, Xbox One | Three One Zero | March 28, 2016 |
        """,
        """
col : Title | Platform | Developer | Release Date | platforms_count
row 1 : ABZÛ | PlayStation 4, Windows, Xbox One, Nintendo Switch | Giant Squid | August 2, 2016 | 4
row 2 : The Unfinished Swan | PlayStation 3, PlayStation 4, PlayStation Vita | Giant Squid | October 15, 2012 | 3
row 3 : Rime | PlayStation 4, Nintendo Switch, Windows, Xbox One | Tequila Works | May 26, 2017 | 4
row 4 : Flower | PlayStation 3, PlayStation 4, PlayStation Vita, iOS | Thatgamecompany | February 12, 2009 | 4
row 5 : Journey | PlayStation 3, PlayStation 4, Windows, iOS | Thatgamecompany | March 13, 2012 | 4
row 6 : The Pathless | PlayStation 4, PlayStation 5, Windows, iOS | Giant Squid | November 12, 2020 | 4
row 7 : Sky: Children of the Light | iOS, Android, Nintendo Switch | Thatgamecompany | July 18, 2019 | 3
row 8 : Adr1ft | Windows, PlayStation 4, Xbox One | Three One Zero | March 28, 2016 | 3
        """,
        """
col : Title | Platform | Developer | Release Date | platforms_count
row 1 : ABZÛ | PlayStation 4, Windows, Xbox One, Nintendo Switch | Giant Squid | August 2, 2016 | 4
row 3 : Rime | PlayStation 4, Nintendo Switch, Windows, Xbox One | Tequila Works | May 26, 2017 | 4
row 4 : Flower | PlayStation 3, PlayStation 4, PlayStation Vita, iOS | Thatgamecompany | February 12, 2009 | 4
row 5 : Journey | PlayStation 3, PlayStation 4, Windows, iOS | Thatgamecompany | March 13, 2012 | 4
row 6 : The Pathless | PlayStation 4, PlayStation 5, Windows, iOS | Giant Squid | November 12, 2020 | 4
        """,
        """
col : Developer | count | games | avg_platforms
row 1 : Giant Squid | 2 | ABZÛ, The Pathless | 4.0
row 2 : Tequila Works | 1 | Rime | 4.0
row 3 : Thatgamecompany | 2 | Flower, Journey | 4.0
        """
    ],
    "question": "Which platforms is 'The Pathless' available on?",
    "answer": "PlayStation 4, PlayStation 5, Windows, iOS",
    "explanation": "This question requires selecting relevant columns, counting platforms per game, filtering for games with more than 3 platforms, and analyzing developers' platform strategies. Looking at the intermediate tables, 'The Pathless' is available on PlayStation 4, PlayStation 5, Windows, and iOS platforms."
},
    "EXAMPLE_9": {
    "table_info": """
col : Position | Driver | Team | Score | Gap
row 1 : 1 | Lewis Hamilton | Mercedes | 384 | —
row 2 : 2 | Valtteri Bottas | Mercedes | 326 | 58
row 3 : 3 | Max Verstappen | Red Bull | 278 | 106
row 4 : 4 | Charles Leclerc | Ferrari | 264 | 120
row 5 : 5 | Sebastian Vettel | Ferrari | 240 | 144
row 6 : 6 | Carlos Sainz | McLaren | 96 | 288
row 7 : 7 | Pierre Gasly | Red Bull/Toro Rosso | 95 | 289
row 8 : 8 | Alexander Albon | Toro Rosso/Red Bull | 92 | 292
row 9 : 9 | Daniel Ricciardo | Renault | 54 | 330
row 10 : 10 | Sergio Pérez | Racing Point | 52 | 332
    """,
    "chain": [
        "f_select_column()",
        "f_select_row()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Driver, Team, Score)",
        "f_select_row(row 1, row 2, row 3, row 4, row 5)",
        "f_add_inferred_column(performance_rating)",
        "f_sort_column(performance_rating)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for driver performance analysis",
        "Select the drivers which have score greater than 100",
        "Adding a performance rating column based on score",
        "Sorting by performance rating to rank drivers"
    ],
    "intermediate_tables": [
        """
col : Driver | Team | Score
row 1 : Lewis Hamilton | Mercedes | 384
row 2 : Valtteri Bottas | Mercedes | 326
row 3 : Max Verstappen | Red Bull | 278
row 4 : Charles Leclerc | Ferrari | 264
row 5 : Sebastian Vettel | Ferrari | 240
row 6 : Carlos Sainz | McLaren | 96
row 7 : Pierre Gasly | Red Bull/Toro Rosso | 95
row 8 : Alexander Albon | Toro Rosso/Red Bull | 92
row 9 : Daniel Ricciardo | Renault | 54
row 10 : Sergio Pérez | Racing Point | 52
        """,
        """
col : Driver | Team | Score
row 1 : Lewis Hamilton | Mercedes | 384
row 2 : Valtteri Bottas | Mercedes | 326
row 3 : Max Verstappen | Red Bull | 278
row 4 : Charles Leclerc | Ferrari | 264
row 5 : Sebastian Vettel | Ferrari | 240
        """,
        """
col : Driver | Team | Score | performance_rating
row 1 : Lewis Hamilton | Mercedes | 384 | Exceptional
row 2 : Valtteri Bottas | Mercedes | 326 | Excellent
row 3 : Max Verstappen | Red Bull | 278 | Very Good
row 4 : Charles Leclerc | Ferrari | 264 | Very Good
row 5 : Sebastian Vettel | Ferrari | 240 | Good
        """,
        """
col : Driver | Team | Score | performance_rating
row 1 : Lewis Hamilton | Mercedes | 384 | Exceptional
row 2 : Valtteri Bottas | Mercedes | 326 | Excellent
row 3 : Max Verstappen | Red Bull | 278 | Very Good
row 4 : Charles Leclerc | Ferrari | 264 | Very Good
row 5 : Sebastian Vettel | Ferrari | 240 | Good
        """
    ],
    "question": "Which drivers scored more than 250 points?",
    "answer": "Lewis Hamilton, Valtteri Bottas, Max Verstappen, Charles Leclerc",
    "explanation": "This question requires selecting relevant columns, filtering for high-scoring drivers, adding performance ratings, and sorting for analysis. The final table shows four drivers scored more than 250 points: Lewis Hamilton (384), Valtteri Bottas (326), Max Verstappen (278), and Charles Leclerc (264)."
},
    "EXAMPLE_10": {
    "table_info": """
col : Team | Wins | Pole Positions | Fastest Laps | Points | Rank
row 1 : Ferrari | 9 | 12 | 5 | 655 | 1
row 2 : McLaren | 2 | 1 | 3 | 218 | 3
row 3 : Williams | 1 | 0 | 1 | 120 | 5
row 4 : Renault | 0 | 0 | 0 | 38 | 7
row 5 : Mercedes | 3 | 3 | 2 | 413 | 2
row 6 : Red Bull | 4 | 2 | 7 | 290 | 4
row 7 : Alpha Tauri | 1 | 0 | 0 | 107 | 6
row 8 : Haas | 0 | 0 | 0 | 28 | 8
row 9 : Alfa Romeo | 0 | 0 | 0 | 8 | 9
row 10 : Racing Point | 0 | 0 | 0 | 0 | 10
    """,
    "chain": [
        "f_sort_column()",
        "f_select_row()",
        "f_select_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_sort_column(Wins)",
        "f_select_row(row 1, row 2, row 3, row 4, row 5, row 6)",
        "f_select_column(Team, Wins, Points, Rank)",
        "f_add_inferred_column(performance_index)",
        "END"
    ],
    "explanations": [
        "Sorting teams by number of wins in ascending order",
        "Select the teams which have at most 1 win",
        "Selecting relevant columns for performance analysis",
        "Adding a performance index based on points and rank"
    ],
    "intermediate_tables": [
        """
col : Team | Wins | Pole Positions | Fastest Laps | Points | Rank
row 1 : Racing Point | 0 | 0 | 0 | 0 | 10
row 2 : Alfa Romeo | 0 | 0 | 0 | 8 | 9
row 3 : Haas | 0 | 0 | 0 | 28 | 8
row 4 : Renault | 0 | 0 | 0 | 38 | 7
row 5 : Williams | 1 | 0 | 1 | 120 | 5
row 6 : Alpha Tauri | 1 | 0 | 0 | 107 | 6
row 7 : McLaren | 2 | 1 | 3 | 218 | 3
row 8 : Mercedes | 3 | 3 | 2 | 413 | 2
row 9 : Red Bull | 4 | 2 | 7 | 290 | 4
row 10 : Ferrari | 9 | 12 | 5 | 655 | 1
        """,
        """
col : Team | Wins | Pole Positions | Fastest Laps | Points | Rank
row 1 : Racing Point | 0 | 0 | 0 | 0 | 10
row 2 : Alfa Romeo | 0 | 0 | 0 | 8 | 9
row 3 : Haas | 0 | 0 | 0 | 28 | 8
row 4 : Renault | 0 | 0 | 0 | 38 | 7
row 5 : Williams | 1 | 0 | 1 | 120 | 5
row 6 : Alpha Tauri | 1 | 0 | 0 | 107 | 6
        """,
        """
col : Team | Wins | Points | Rank
row 1 : Racing Point | 0 | 0 | 10
row 2 : Alfa Romeo | 0 | 8 | 9
row 3 : Haas | 0 | 28 | 8
row 4 : Renault | 0 | 38 | 7
row 5 : Williams | 1 | 120 | 5
row 6 : Alpha Tauri | 1 | 107 | 6
        """,
        """
col : Team | Wins | Points | Rank | performance_index
row 1 : Racing Point | 0 | 0 | 10 | 0.0
row 2 : Alfa Romeo | 0 | 8 | 9 | 0.9
row 3 : Haas | 0 | 28 | 8 | 3.5
row 4 : Renault | 0 | 38 | 7 | 5.4
row 5 : Williams | 1 | 120 | 5 | 24.0
row 6 : Alpha Tauri | 1 | 107 | 6 | 17.8
        """
    ],
    "question": "Which team has the fewest wins?",
    "answer": "Racing Point, Alfa Romeo, Haas, Renault",
    "explanation": "This question requires sorting teams by wins, filtering for teams with at most 1 win, selecting relevant columns, and calculating performance indices. The final table shows four teams tied with 0 wins: Racing Point, Alfa Romeo, Haas, and Renault, with Racing Point having the lowest performance index overall."
},
    "EXAMPLE_11": {
    "table_info": """
col : Player | Position | Games | Tackles | Sacks | Interceptions | Touchdowns
row 1 : Marcus Peters | CB | 16 | 63 | 0 | 9 | 3
row 2 : Minkah Fitzpatrick | FS | 16 | 69 | 0 | 5 | 2
row 3 : Tre'Davious White | CB | 15 | 58 | 0 | 6 | 0
row 4 : Stephon Gilmore | CB | 16 | 53 | 0 | 6 | 2
row 5 : Devin McCourty | FS | 16 | 58 | 0 | 5 | 1
row 6 : Anthony Harris | FS | 14 | 60 | 0 | 6 | 0
row 7 : Logan Ryan | CB | 16 | 113 | 4.5 | 4 | 0
row 8 : Quandre Diggs | FS | 10 | 44 | 0 | 3 | 1
row 9 : Justin Simmons | FS | 16 | 93 | 0 | 4 | 0
row 10 : Earl Thomas | FS | 15 | 49 | 0 | 2 | 0
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_group_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(int_per_game)",
        "f_select_column(Player, Position, Interceptions, Touchdowns, int_per_game)",
        "f_group_column(Position)",
        "f_sort_column(total_interceptions)",
        "END"
    ],
    "explanations": [
        "Adding a column to calculate interceptions per game",
        "Selecting relevant columns for defensive back analysis",
        "Grouping by position to compare cornerbacks and safeties",
        "Sorting by total interceptions to identify best positions"
    ],
    "intermediate_tables": [
        """
col : Player | Position | Games | Tackles | Sacks | Interceptions | Touchdowns | int_per_game
row 1 : Marcus Peters | CB | 16 | 63 | 0 | 9 | 3 | 0.56
row 2 : Minkah Fitzpatrick | FS | 16 | 69 | 0 | 5 | 2 | 0.31
row 3 : Tre'Davious White | CB | 15 | 58 | 0 | 6 | 0 | 0.40
row 4 : Stephon Gilmore | CB | 16 | 53 | 0 | 6 | 2 | 0.38
row 5 : Devin McCourty | FS | 16 | 58 | 0 | 5 | 1 | 0.31
row 6 : Anthony Harris | FS | 14 | 60 | 0 | 6 | 0 | 0.43
row 7 : Logan Ryan | CB | 16 | 113 | 4.5 | 4 | 0 | 0.25
row 8 : Quandre Diggs | FS | 10 | 44 | 0 | 3 | 1 | 0.30
row 9 : Justin Simmons | FS | 16 | 93 | 0 | 4 | 0 | 0.25
row 10 : Earl Thomas | FS | 15 | 49 | 0 | 2 | 0 | 0.13
        """,
        """
col : Player | Position | Interceptions | Touchdowns | int_per_game
row 1 : Marcus Peters | CB | 9 | 3 | 0.56
row 2 : Minkah Fitzpatrick | FS | 5 | 2 | 0.31
row 3 : Tre'Davious White | CB | 6 | 0 | 0.40
row 4 : Stephon Gilmore | CB | 6 | 2 | 0.38
row 5 : Devin McCourty | FS | 5 | 1 | 0.31
row 6 : Anthony Harris | FS | 6 | 0 | 0.43
row 7 : Logan Ryan | CB | 4 | 0 | 0.25
row 8 : Quandre Diggs | FS | 3 | 1 | 0.30
row 9 : Justin Simmons | FS | 4 | 0 | 0.25
row 10 : Earl Thomas | FS | 2 | 0 | 0.13
        """,
        """
col : Position | count | total_interceptions | total_touchdowns | avg_int_per_game
row 1 : CB | 4 | 25 | 5 | 0.40
row 2 : FS | 6 | 25 | 4 | 0.29
        """,
        """
col : Position | count | total_interceptions | total_touchdowns | avg_int_per_game
row 1 : CB | 4 | 25 | 5 | 0.40
row 2 : FS | 6 | 25 | 4 | 0.29
        """
    ],
    "question": "What is the total number of interceptions made by all players?",
    "answer": "50",
    "explanation": "This question requires calculating interceptions per game, selecting relevant columns, grouping by position, and summing the interceptions. From the group results, cornerbacks (CB) made 25 interceptions and free safeties (FS) made 25 interceptions, for a total of 50 interceptions across all players."
},
    "EXAMPLE_12": {
    "table_info": """
col : Court Name | Court Location | Year Established | Number of Courtrooms | Number of Judges
row 1 : Queens County Supreme Court | 88-11 Sutphin Boulevard, Jamaica, NY | 1872 | 47 | 52
row 2 : Kings County Supreme Court | 360 Adams Street, Brooklyn, NY | 1865 | 82 | 75
row 3 : New York County Supreme Court | 60 Centre Street, New York, NY | 1821 | 95 | 98
row 4 : Bronx County Supreme Court | 851 Grand Concourse, Bronx, NY | 1914 | 38 | 43
row 5 : Richmond County Supreme Court | 26 Central Avenue, Staten Island, NY | 1898 | 12 | 14
row 6 : Nassau County Supreme Court | 100 Supreme Court Drive, Mineola, NY | 1899 | 31 | 34
row 7 : Suffolk County Supreme Court | 400 Carleton Avenue, Central Islip, NY | 1911 | 27 | 30
row 8 : Westchester County Supreme Court | 111 Dr. Martin Luther King Jr. Boulevard, White Plains, NY | 1846 | 25 | 29
    """,
    "chain": [
        "f_select_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(Court Name, Year Established, Number of Courtrooms, Number of Judges)",
        "f_add_inferred_column(judge_to_courtroom_ratio)",
        "f_sort_column(Year Established)",
        "f_select_row(row 2, row 4, row 5, row 7, row 8)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for court analysis",
        "Adding a column to calculate the ratio of judges to courtrooms",
        "Sorting by establishment year to see historical development",
        "Select the courts which have ratio of judges to courtrooms greater than 1.1"
    ],
    "intermediate_tables": [
        """
col : Court Name | Year Established | Number of Courtrooms | Number of Judges
row 1 : Queens County Supreme Court | 1872 | 47 | 52
row 2 : Kings County Supreme Court | 1865 | 82 | 75
row 3 : New York County Supreme Court | 1821 | 95 | 98
row 4 : Bronx County Supreme Court | 1914 | 38 | 43
row 5 : Richmond County Supreme Court | 1898 | 12 | 14
row 6 : Nassau County Supreme Court | 1899 | 31 | 34
row 7 : Suffolk County Supreme Court | 1911 | 27 | 30
row 8 : Westchester County Supreme Court | 1846 | 25 | 29
        """,
        """
col : Court Name | Year Established | Number of Courtrooms | Number of Judges | judge_to_courtroom_ratio
row 1 : Queens County Supreme Court | 1872 | 47 | 52 | 1.11
row 2 : Kings County Supreme Court | 1865 | 82 | 75 | 0.91
row 3 : New York County Supreme Court | 1821 | 95 | 98 | 1.03
row 4 : Bronx County Supreme Court | 1914 | 38 | 43 | 1.13
row 5 : Richmond County Supreme Court | 1898 | 12 | 14 | 1.17
row 6 : Nassau County Supreme Court | 1899 | 31 | 34 | 1.10
row 7 : Suffolk County Supreme Court | 1911 | 27 | 30 | 1.11
row 8 : Westchester County Supreme Court | 1846 | 25 | 29 | 1.16
        """,
        """
col : Court Name | Year Established | Number of Courtrooms | Number of Judges | judge_to_courtroom_ratio
row 1 : New York County Supreme Court | 1821 | 95 | 98 | 1.03
row 2 : Westchester County Supreme Court | 1846 | 25 | 29 | 1.16
row 3 : Kings County Supreme Court | 1865 | 82 | 75 | 0.91
row 4 : Queens County Supreme Court | 1872 | 47 | 52 | 1.11
row 5 : Richmond County Supreme Court | 1898 | 12 | 14 | 1.17
row 6 : Nassau County Supreme Court | 1899 | 31 | 34 | 1.10
row 7 : Suffolk County Supreme Court | 1911 | 27 | 30 | 1.11
row 8 : Bronx County Supreme Court | 1914 | 38 | 43 | 1.13
        """,
        """
col : Court Name | Year Established | Number of Courtrooms | Number of Judges | judge_to_courtroom_ratio
row 2 : Westchester County Supreme Court | 1846 | 25 | 29 | 1.16
row 4 : Queens County Supreme Court | 1872 | 47 | 52 | 1.11
row 5 : Richmond County Supreme Court | 1898 | 12 | 14 | 1.17
row 7 : Suffolk County Supreme Court | 1911 | 27 | 30 | 1.11
row 8 : Bronx County Supreme Court | 1914 | 38 | 43 | 1.13
        """
    ],
    "question": "Which court has the highest ratio of judges to courtrooms?",
    "answer": "Richmond County Supreme Court",
    "explanation": "This question requires selecting relevant columns, calculating the judge-to-courtroom ratio, sorting by establishment year, and identifying courts with more judges than courtrooms. The final table shows that Richmond County Supreme Court has the highest ratio at 1.17 judges per courtroom."
},
    "EXAMPLE_13": {
    "table_info": """
col : Single | Artist | Album | Release date | Peak chart positions UK | Peak chart positions US
row 1 : "Waterloo" | ABBA | Waterloo | 4 March 1974 | 1 | 6
row 2 : "SOS" | ABBA | ABBA | 20 August 1975 | 6 | 15
row 3 : "Mamma Mia" | ABBA | ABBA | 12 December 1975 | 1 | 32
row 4 : "Fernando" | ABBA | Greatest Hits | 18 March 1976 | 1 | 13
row 5 : "Dancing Queen" | ABBA | Arrival | 15 August 1976 | 1 | 1
row 6 : "Money, Money, Money" | ABBA | Arrival | 1 November 1976 | 3 | 56
row 7 : "Knowing Me, Knowing You" | ABBA | Arrival | 14 February 1977 | 1 | 14
row 8 : "The Name of the Game" | ABBA | ABBA: The Album | 17 October 1977 | 1 | 12
row 9 : "Take a Chance on Me" | ABBA | ABBA: The Album | 17 January 1978 | 1 | 3
row 10 : "Summer Night City" | ABBA | Voulez-Vous | 6 September 1978 | 5 | 76
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_group_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(release_year)",
        "f_select_column(Single, release_year, Peak chart positions UK, Peak chart positions US)",
        "f_group_column(release_year)",
        "f_select_row(count > 2)",
        "END"
    ],
    "explanations": [
        "Adding a column to extract the release year from the date",
        "Selecting relevant columns for chart performance analysis",
        "Grouping by release year to count singles per year",
        "Filtering for years with more than 2 singles released"
    ],
    "intermediate_tables": [
        """
col : Single | Artist | Album | Release date | Peak chart positions UK | Peak chart positions US | release_year
row 1 : "Waterloo" | ABBA | Waterloo | 4 March 1974 | 1 | 6 | 1974
row 2 : "SOS" | ABBA | ABBA | 20 August 1975 | 6 | 15 | 1975
row 3 : "Mamma Mia" | ABBA | ABBA | 12 December 1975 | 1 | 32 | 1975
row 4 : "Fernando" | ABBA | Greatest Hits | 18 March 1976 | 1 | 13 | 1976
row 5 : "Dancing Queen" | ABBA | Arrival | 15 August 1976 | 1 | 1 | 1976
row 6 : "Money, Money, Money" | ABBA | Arrival | 1 November 1976 | 3 | 56 | 1976
row 7 : "Knowing Me, Knowing You" | ABBA | Arrival | 14 February 1977 | 1 | 14 | 1977
row 8 : "The Name of the Game" | ABBA | ABBA: The Album | 17 October 1977 | 1 | 12 | 1977
row 9 : "Take a Chance on Me" | ABBA | ABBA: The Album | 17 January 1978 | 1 | 3 | 1978
row 10 : "Summer Night City" | ABBA | Voulez-Vous | 6 September 1978 | 5 | 76 | 1978
        """,
        """
col : Single | release_year | Peak chart positions UK | Peak chart positions US
row 1 : "Waterloo" | 1974 | 1 | 6
row 2 : "SOS" | 1975 | 6 | 15
row 3 : "Mamma Mia" | 1975 | 1 | 32
row 4 : "Fernando" | 1976 | 1 | 13
row 5 : "Dancing Queen" | 1976 | 1 | 1
row 6 : "Money, Money, Money" | 1976 | 3 | 56
row 7 : "Knowing Me, Knowing You" | 1977 | 1 | 14
row 8 : "The Name of the Game" | 1977 | 1 | 12
row 9 : "Take a Chance on Me" | 1978 | 1 | 3
row 10 : "Summer Night City" | 1978 | 5 | 76
        """,
        """
col : release_year | count | singles | avg_UK_position | avg_US_position
row 1 : 1974 | 1 | "Waterloo" | 1.0 | 6.0
row 2 : 1975 | 2 | "SOS", "Mamma Mia" | 3.5 | 23.5
row 3 : 1976 | 3 | "Fernando", "Dancing Queen", "Money, Money, Money" | 1.67 | 23.33
row 4 : 1977 | 2 | "Knowing Me, Knowing You", "The Name of the Game" | 1.0 | 13.0
row 5 : 1978 | 2 | "Take a Chance on Me", "Summer Night City" | 3.0 | 39.5
        """,
        """
col : release_year | count | singles | avg_UK_position | avg_US_position
row 1 : 1976 | 3 | "Fernando", "Dancing Queen", "Money, Money, Money" | 1.67 | 23.33
        """
    ],
    "question": "In which year did ABBA release three singles?",
    "answer": "1976",
    "explanation": "This question requires extracting the release year from dates, selecting relevant columns, grouping by year to count singles, and filtering for years with more than 2 singles. The final table shows that 1976 was the only year in which ABBA released three singles: 'Fernando', 'Dancing Queen', and 'Money, Money, Money'."
}
}

task_4_EXAMPLES_multi = {
    "EXAMPLE_0": {
            "table_info": """
table_name: Treaty Info
col : Treaty | Organization | Introduced | Signed | Ratified
row 1 : Convention on the Prevention and Punishment of the Crime of Genocide | United Nations | 1948 | - | 1958
row 2 : International Convention on the Elimination of All Forms of Racial Discrimination | United Nations | 1966 | 1967 | 1970
row 3 : International Covenant on Economic, Social and Cultural Rights | United Nations | 1966 | 1977 | 1979
row 4 : International Covenant on Civil and Political Rights | United Nations | 1966 | 1977 | 1979
row 5 : Convention on the Elimination of All Forms of Discrimination against Women | United Nations | 1979 | - | 1993
row 6 : Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment | United Nations | 1984 | 1986 | 1993
row 7 : Convention on the Rights of the Child | United Nations | 1989 | 1990 | 1993
row 8 : Second Optional Protocol to the International Covenant on Civil and Political Rights, aiming at the abolition of the death penalty | United Nations | 1989 | - | -
row 9 : International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families | United Nations | 1990 | 1991 | 1993

table_name: Treaty Status
col : Treaty | Status | Implementation Level | Reporting Requirement | Reservations
row 1 : Convention on the Prevention and Punishment of the Crime of Genocide | Active | High | Annual | No
row 2 : International Convention on the Elimination of All Forms of Racial Discrimination | Active | Medium | Biennial | Yes
row 3 : International Covenant on Economic, Social and Cultural Rights | Active | Medium | Biennial | Yes
row 4 : International Covenant on Civil and Political Rights | Active | High | Annual | No
row 5 : Convention on the Elimination of All Forms of Discrimination against Women | Active | High | Annual | No
row 6 : Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment | Active | High | Annual | No
row 7 : Convention on the Rights of the Child | Active | High | Annual | No
row 8 : Second Optional Protocol to the International Covenant on Civil and Political Rights, aiming at the abolition of the death penalty | Pending | Low | None | N/A
row 9 : International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families | Active | Medium | Biennial | Yes

foreign_key: Treaty
""",
"question": "what year did monaco ratify more international human rights treaties than they did in 1979?",
"answer": "1993",
"explanation": "To answer this question, I need to select the Treaty Info table which contains ratification years, group by Ratified year to count treaties ratified in each year, sort by count to identify years with more ratifications than 1979, and select the first row to get the year with more ratifications than 1979. The data shows that in 1979, Monaco ratified 2 treaties, while in 1993, they ratified 4 treaties, which is more than in 1979.",
"chain": [
    "f_select_table()",
    "f_group_column()",
    "f_sort_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_select_table(Treaty Info)",
    "f_group_column(Ratified)",
    "f_sort_column(count)",
    "f_select_row(row 1)",
    "END"
],
"explanations": [
    "Selecting the Treaty Info table which contains ratification years",
    "Grouping by Ratified year to count treaties ratified in each year",
    "Sorting by count to identify years with more ratifications than 1979",
    "Selecting the first row to get the year with more ratifications than 1979"
],
"intermediate_tables": [
    """
col : Treaty | Organization | Introduced | Signed | Ratified
row 1 : Convention on the Prevention and Punishment of the Crime of Genocide | United Nations | 1948 | - | 1958
row 2 : International Convention on the Elimination of All Forms of Racial Discrimination | United Nations | 1966 | 1967 | 1970
row 3 : International Covenant on Economic, Social and Cultural Rights | United Nations | 1966 | 1977 | 1979
row 4 : International Covenant on Civil and Political Rights | United Nations | 1966 | 1977 | 1979
row 5 : Convention on the Elimination of All Forms of Discrimination against Women | United Nations | 1979 | - | 1993
row 6 : Convention against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment | United Nations | 1984 | 1986 | 1993
row 7 : Convention on the Rights of the Child | United Nations | 1989 | 1990 | 1993
row 8 : Second Optional Protocol to the International Covenant on Civil and Political Rights, aiming at the abolition of the death penalty | United Nations | 1989 | - | -
row 9 : International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families | United Nations | 1990 | 1991 | 1993
    """,
    """
col : Ratified | count
row 1 : 1958 | 1
row 2 : 1970 | 1
row 3 : 1979 | 2
row 4 : 1993 | 4
row 5 : - | 1
    """,
    """
col : Ratified | count
row 1 : 1993 | 4
row 2 : 1979 | 2
row 3 : 1958 | 1
row 4 : 1970 | 1
row 5 : - | 1
    """,
        """
col : Ratified | count
row 1 : 1993 | 4
    """
]
},
"EXAMPLE_1": {
            "table_info": """
table_name: Contestants
col : Represent | Contestant | Age | Height | Hometown
row 1 : 1 | Mildred Kincaid Adames | 20 | 1.65 mts | Panama City
row 2 : 2 | Catherine Henderson Tudisco | 20 | 1.66 mts | Panama City
row 3 : 3 | Giovanna Alida Loaiza | 21 | 1.67 mts | Panama City
row 4 : 4 | Reyna Royo | 24 | 1.69 mts | Panama City
row 5 : 5 | Ivonne Ileana Correa Turney | 23 | 1.70 mts | Panama City
row 6 : 6 | Karol Guevara | 22 | 1.70 mts | Panama City
row 7 : 7 | Betzy Janette Achurra Castillo | 20 | 1.70 mts | Panama City
row 8 : 8 | Marisela Moreno Montero | 24 | 1.73 mts | Panama City
row 9 : 15 | Swany Cisney Castillo | 23 | 1.78 mts | Panama City
row 10 : 16 | Michelle Krisko Sugasti | 20 | 1.80mts | Panama City

table_name: Performance Scores
col : ID | Participant Name | Swimsuit Score | Evening Gown Score | Interview Score | Total Points
row 1 : 1 | Mildred Kincaid Adames | 8.5 | 8.7 | 8.2 | 25.4
row 2 : 2 | Catherine Henderson Tudisco | 8.6 | 8.9 | 8.4 | 25.9
row 3 : 3 | Giovanna Alida Loaiza | 9.1 | 9.2 | 8.8 | 27.1
row 4 : 4 | Reyna Royo | 9.4 | 9.3 | 9.2 | 27.9
row 5 : 5 | Ivonne Ileana Correa Turney | 9.3 | 9.1 | 8.9 | 27.3
row 6 : 6 | Karol Guevara | 8.9 | 9.0 | 8.5 | 26.4
row 7 : 7 | Betzy Janette Achurra Castillo | 8.7 | 8.6 | 8.3 | 25.6
row 8 : 8 | Marisela Moreno Montero | 9.5 | 9.4 | 9.3 | 28.2
row 9 : 15 | Swany Cisney Castillo | 9.2 | 9.3 | 9.0 | 27.5
row 10 : 16 | Michelle Krisko Sugasti | 9.3 | 9.4 | 9.1 | 27.8

foreign_key: Contestant, Participant Name
""",
"question": "which contestant over 21 years old achieved the highest total points?",
"answer": "Marisela Moreno Montero",
"explanation": "To find the contestant over 21 years old with the highest total points, I need to combine information from both tables. First, I'll stitch the Contestants and Performance Scores tables using the contestant name as the foreign key. Then I'll select only rows where the contestant's age is greater than 21 years old, select only the relevant columns needed to identify the contestant with highest points, and sort by Total Points in descending order to identify the contestant with the highest score.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_select_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Contestants.Contestant, Performance Scores.Participant Name, inner)",
    "f_select_row(row 4, row 5, row 6, row 8, row 9)",
    "f_select_column(Contestant, Age, Total Points)",
    "f_sort_column(Total Points)",
    "END"
],
"explanations": [
    "Stitching the Contestants and Performance Scores tables using contestant name as the foreign key to combine demographic and performance data",
    "Selecting only rows where the contestant's age is greater than 21 years old, which are rows 4, 5, 6, 8, 15",
    "Selecting only the relevant columns needed to identify the contestant with highest points",
    "Sorting by Total Points in descending order to identify the contestant with the highest score"
],
"intermediate_tables": [
    """
col : Represent | Contestant | Age | Height | Hometown | ID | Participant Name | Swimsuit Score | Evening Gown Score | Interview Score | Total Points
row 1 : 1 | Mildred Kincaid Adames | 20 | 1.65 mts | Panama City | 1 | Mildred Kincaid Adames | 8.5 | 8.7 | 8.2 | 25.4
row 2 : 2 | Catherine Henderson Tudisco | 20 | 1.66 mts | Panama City | 2 | Catherine Henderson Tudisco | 8.6 | 8.9 | 8.4 | 25.9
row 3 : 3 | Giovanna Alida Loaiza | 21 | 1.67 mts | Panama City | 3 | Giovanna Alida Loaiza | 9.1 | 9.2 | 8.8 | 27.1
row 4 : 4 | Reyna Royo | 24 | 1.69 mts | Panama City | 4 | Reyna Royo | 9.4 | 9.3 | 9.2 | 27.9
row 5 : 5 | Ivonne Ileana Correa Turney | 23 | 1.70 mts | Panama City | 5 | Ivonne Ileana Correa Turney | 9.3 | 9.1 | 8.9 | 27.3
row 6 : 6 | Karol Guevara | 22 | 1.70 mts | Panama City | 6 | Karol Guevara | 8.9 | 9.0 | 8.5 | 26.4
row 7 : 7 | Betzy Janette Achurra Castillo | 20 | 1.70 mts | Panama City | 7 | Betzy Janette Achurra Castillo | 8.7 | 8.6 | 8.3 | 25.6
row 8 : 8 | Marisela Moreno Montero | 24 | 1.73 mts | Panama City | 8 | Marisela Moreno Montero | 9.5 | 9.4 | 9.3 | 28.2
row 9 : 15 | Swany Cisney Castillo | 23 | 1.78 mts | Panama City | 15 | Swany Cisney Castillo | 9.2 | 9.3 | 9.0 | 27.5
row 10 : 16 | Michelle Krisko Sugasti | 20 | 1.80mts | Panama City | 16 | Michelle Krisko Sugasti | 9.3 | 9.4 | 9.1 | 27.8
    """,
    """
col : Represent | Contestant | Age | Height | Hometown | ID | Participant Name | Swimsuit Score | Evening Gown Score | Interview Score | Total Points
row 4 : 4 | Reyna Royo | 24 | 1.69 mts | Panama City | 4 | Reyna Royo | 9.4 | 9.3 | 9.2 | 27.9
row 5 : 5 | Ivonne Ileana Correa Turney | 23 | 1.70 mts | Panama City | 5 | Ivonne Ileana Correa Turney | 9.3 | 9.1 | 8.9 | 27.3
row 6 : 6 | Karol Guevara | 22 | 1.70 mts | Panama City | 6 | Karol Guevara | 8.9 | 9.0 | 8.5 | 26.4
row 8 : 8 | Marisela Moreno Montero | 24 | 1.73 mts | Panama City | 8 | Marisela Moreno Montero | 9.5 | 9.4 | 9.3 | 28.2
row 9 : 15 | Swany Cisney Castillo | 23 | 1.78 mts | Panama City | 15 | Swany Cisney Castillo | 9.2 | 9.3 | 9.0 | 27.5
    """,
    """
col : Contestant | Age | Total Points
row 1 : Reyna Royo | 24 | 27.9
row 2 : Ivonne Ileana Correa Turney | 23 | 27.3
row 3 : Karol Guevara | 22 | 26.4
row 4 : Marisela Moreno Montero | 24 | 28.2
row 5 : Swany Cisney Castillo | 23 | 27.5
    """,
    """
col : Contestant | Age | Total Points
row 1 : Marisela Moreno Montero | 24 | 28.2
row 2 : Reyna Royo | 24 | 27.9
row 3 : Swany Cisney Castillo | 23 | 27.5
row 4 : Ivonne Ileana Correa Turney | 23 | 27.3
row 5 : Karol Guevara | 22 | 26.4
    """
]
},
    "EXAMPLE_2": {
            "table_info": """
table_name: Competitions
col : Year | Competition | Venue | Position | Event | Notes
row 1 : 1982 | African Championships | Cairo, Egypt | 1st | Marathon | 2:21:05
row 2 : 1982 | Commonwealth Games | Brisbane, Australia | 2nd | Marathon | 2:09:30
row 3 : 1983 | World Championships | Helsinki, Finland | 15th | Marathon | 2:13:11
row 4 : 1984 | Olympic Games | Los Angeles, United States | 6th | Marathon | 2:11:10
row 5 : 1986 | Fukuoka Marathon | Fukuoka, Japan | 1st | Marathon | 2:10:06
row 6 : 1988 | Olympic Games | Seoul, South Korea | 7th | Marathon | 2:13:06
row 7 : 1992 | Olympic Games | Barcelona, Spain | 34th | Marathon | 2:19:34
row 8 : 1993 | World Championships | Stuttgart, Germany | 21st | Marathon | 2:24:23
row 9 : 1995 | World Championships | Gothenburg, Sweden | 43rd | Marathon | 2:30:53

table_name: Competition Details
col : Event Name | Prestige Level | Prize Money | Participants | Weather Conditions
row 1 : African Championships | Regional | $50,000 | 82 | Hot, Dry
row 2 : Commonwealth Games | International | $100,000 | 124 | Warm, Humid
row 3 : World Championships | Global | $250,000 | 156 | Moderate
row 4 : Melbourne Marathon | Major | $75,000 | 12,345 | Cool, Cloudy
row 5 : Tokyo Marathon | Major | $150,000 | 35,600 | Cold, Rainy
row 6 : Olympic Games | Global | $0 | 92 | Warm, Clear
row 7 : Fukuoka Marathon | Major | $100,000 | 15,780 | Cool, Clear
row 8 : Beijing Marathon | Major | $80,000 | 28,900 | Moderate, Smoggy
row 9 : Boston Marathon | Major | $175,000 | 26,800 | Cool, Rainy
row 10 : New York City Marathon | Major | $200,000 | 42,600 | Cool, Windy

foreign_key: Competition, Event Name
""",
"question": "which global competition with the highest prize money appears most frequently in the chart?",
"answer": "World Championships",
"explanation": "To answer this question, I need to identify global competitions, determine their prize money, and count how many times each appears in the chart. First, I'll stitch the two tables to combine competition details with appearance data. Then I'll filter for global competitions, check their prize money, and count occurrences to find the one that appears most frequently.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_sort_column()",
    "f_select_row()",
    "f_group_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Competitions.Competition, Competition Details.Event Name, inner)",
    "f_select_row(row 3, row 4, row 5, row 6, row 7, row 8, row 9)",
    "f_sort_column(Prize Money)",
    "f_select_row(row 1, row 2, row 3, row 4)",
    "f_group_column(Competition)",
    "f_sort_column(count)",
    "END"
],
"explanations": [
    "Stitching the Competitions and Competition Details tables using competition name as the foreign key to combine appearance data with competition details",
    "Selecting only rows where the prestige level is 'Global' to focus on global competitions",
    "Sorting by Prize Money in descending order to identify the global competition with the highest prize money",
    "Selecting only the rows with the highest prize money to focus on the global competition with the highest prize money",
    "Grouping by Competition name to prepare for counting occurrences",
    "Sorting by count in descending order to identify which global competition appears most often"
],
"intermediate_tables": [
    """
col : Year | Competition | Venue | Position | Event | Notes | Event Name | Prestige Level | Prize Money | Participants | Weather Conditions
row 1 : 1982 | African Championships | Cairo, Egypt | 1st | Marathon | 2:21:05 | African Championships | Regional | $50,000 | 82 | Hot, Dry
row 2 : 1982 | Commonwealth Games | Brisbane, Australia | 2nd | Marathon | 2:09:30 | Commonwealth Games | International | $100,000 | 124 | Warm, Humid
row 3 : 1983 | World Championships | Helsinki, Finland | 15th | Marathon | 2:13:11 | World Championships | Global | $250,000 | 156 | Moderate
row 4 : 1984 | Olympic Games | Los Angeles, United States | 6th | Marathon | 2:11:10 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 5 : 1986 | Fukuoka Marathon | Fukuoka, Japan | 1st | Marathon | 2:10:06 | Fukuoka Marathon | Major | $100,000 | 15,780 | Cool, Clear
row 6 : 1988 | Olympic Games | Seoul, South Korea | 7th | Marathon | 2:13:06 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 7 : 1992 | Olympic Games | Barcelona, Spain | 34th | Marathon | 2:19:34 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 8 : 1993 | World Championships | Stuttgart, Germany | 21st | Marathon | 2:24:23 | World Championships | Global | $250,000 | 156 | Moderate
row 9 : 1995 | World Championships | Gothenburg, Sweden | 43rd | Marathon | 2:30:53 | World Championships | Global | $250,000 | 156 | Moderate
    """,
    """
col : Year | Competition | Venue | Position | Event | Notes | Event Name | Prestige Level | Prize Money | Participants | Weather Conditions
row 3 : 1983 | World Championships | Helsinki, Finland | 15th | Marathon | 2:13:11 | World Championships | Global | $250,000 | 156 | Moderate
row 4 : 1984 | Olympic Games | Los Angeles, United States | 6th | Marathon | 2:11:10 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 5 : 1987 | World Championships | Rome, Italy | 6th | Marathon | 2:13:43 | World Championships | Global | $250,000 | 156 | Moderate
row 6 : 1988 | Olympic Games | Seoul, South Korea | 7th | Marathon | 2:13:06 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 7 : 1992 | Olympic Games | Barcelona, Spain | 34th | Marathon | 2:19:34 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 8 : 1993 | World Championships | Stuttgart, Germany | 21st | Marathon | 2:24:23 | World Championships | Global | $250,000 | 156 | Moderate
row 9 : 1995 | World Championships | Gothenburg, Sweden | 43rd | Marathon | 2:30:53 | World Championships | Global | $250,000 | 156 | Moderate
    """,
        """
col : Year | Competition | Venue | Position | Event | Notes | Event Name | Prestige Level | Prize Money | Participants | Weather Conditions
row 1 : 1983 | World Championships | Helsinki, Finland | 15th | Marathon | 2:13:11 | World Championships | Global | $250,000 | 156 | Moderate
row 2 : 1987 | World Championships | Rome, Italy | 6th | Marathon | 2:13:43 | World Championships | Global | $250,000 | 156 | Moderate
row 3 : 1993 | World Championships | Stuttgart, Germany | 21st | Marathon | 2:24:23 | World Championships | Global | $250,000 | 156 | Moderate
row 4 : 1995 | World Championships | Gothenburg, Sweden | 43rd | Marathon | 2:30:53 | World Championships | Global | $250,000 | 156 | Moderate
row 5 : 1984 | Olympic Games | Los Angeles, United States | 6th | Marathon | 2:11:10 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 6 : 1988 | Olympic Games | Seoul, South Korea | 7th | Marathon | 2:13:06 | Olympic Games | Global | $0 | 92 | Warm, Clear
row 7 : 1992 | Olympic Games | Barcelona, Spain | 34th | Marathon | 2:19:34 | Olympic Games | Global | $0 | 92 | Warm, Clear
    """,
    """
col : Year | Competition | Venue | Position | Event | Notes | Event Name | Prestige Level | Prize Money | Participants | Weather Conditions
row 1 : 1983 | World Championships | Helsinki, Finland | 15th | Marathon | 2:13:11 | World Championships | Global | $250,000 | 156 | Moderate
row 2 : 1987 | World Championships | Rome, Italy | 6th | Marathon | 2:13:43 | World Championships | Global | $250,000 | 156 | Moderate
row 3 : 1993 | World Championships | Stuttgart, Germany | 21st | Marathon | 2:24:23 | World Championships | Global | $250,000 | 156 | Moderate
row 4 : 1995 | World Championships | Gothenburg, Sweden | 43rd | Marathon | 2:30:53 | World Championships | Global | $250,000 | 156 | Moderate
    """,
    """
col : Competition | count
row 1 : World Championships | 4
    """,
    """
col : Competition | count
row 1 : World Championships | 4
    """
]
},
"EXAMPLE_3": {
            "table_info": """
table_name: Hands
col : Hand | 1 credit | 2 credits | 3 credits | 4 credits | 5 credits
row 1 : Royal flush | 250 | 500 | 750 | 1000 | 4000*
row 2 : Straight flush | 60 | 120 | 180 | 240 | 400
row 3 : Four aces | 400 | 800 | 1200 | 1600 | 2000
row 4 : Four of a kind, 2-4 | 100 | 200 | 300 | 400 | 500
row 5 : Four of a kind, 5-K | 50 | 100 | 150 | 200 | 250

table_name: Hand Probabilities
col : Poker Combination | Probability | Frequency | Difficulty Level | Average Return
row 1 : Royal flush | 0.000154% | 1 in 649,740 | Extremely Rare | 0.0200
row 2 : Straight flush | 0.00139% | 1 in 72,193 | Very Rare | 0.0050
row 3 : Four aces | 0.0118% | 1 in 8,485 | Very Rare | 0.0236
row 4 : Four of a kind, 2-4 | 0.0235% | 1 in 4,245 | Rare | 0.0118
row 5 : Four of a kind, 5-K | 0.0705% | 1 in 1,418 | Rare | 0.0177

foreign_key: Hand, Poker Combination
""",
"question": "which hand is the top hand in the card game super aces?",
"answer": "Royal flush",
"explanation": "To identify the top hand in the Super Aces card game, I need to analyze the payout structure and hand rankings. I'll stitch the Hands and Hand Probabilities tables using the hand name as the foreign key to combine payout and rarity information, select columns for hand name, maximum credit payout (5 credits), and difficulty level to focus on identifying the top hand, sort by the 5 credits column in descending order to identify the hand with the highest payout, and select the first row which contains the top hand with the highest payout.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_sort_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Hands.Hand, Hand Probabilities.Poker Combination, inner)",
    "f_select_column(Hand, 5 credits, Difficulty Level)",
    "f_sort_column(5 credits)",
    "f_select_row(row 1)",
    "END"
],
"explanations": [
    "Stitching the Hands and Hand Probabilities tables using the hand name as the foreign key to combine payout and rarity information",
    "Selecting columns for hand name, maximum credit payout (5 credits), and difficulty level to focus on identifying the top hand",
    "Sorting by the 5 credits column in descending order to identify the hand with the highest payout",
    "Selecting the first row which contains the top hand with the highest payout"
],
"intermediate_tables": [
    """
col : Hand | 1 credit | 2 credits | 3 credits | 4 credits | 5 credits | Poker Combination | Probability | Frequency | Difficulty Level | Average Return
row 1 : Royal flush | 250 | 500 | 750 | 1000 | 4000* | Royal flush | 0.000154% | 1 in 649,740 | Extremely Rare | 0.0200
row 2 : Straight flush | 60 | 120 | 180 | 240 | 400 | Straight flush | 0.00139% | 1 in 72,193 | Very Rare | 0.0050
row 3 : Four aces | 400 | 800 | 1200 | 1600 | 2000 | Four aces | 0.0118% | 1 in 8,485 | Very Rare | 0.0236
row 4 : Four of a kind, 2-4 | 100 | 200 | 300 | 400 | 500 | Four of a kind, 2-4 | 0.0235% | 1 in 4,245 | Rare | 0.0118
row 5 : Four of a kind, 5-K | 50 | 100 | 150 | 200 | 250 | Four of a kind, 5-K | 0.0705% | 1 in 1,418 | Rare | 0.0177
    """,
    """
col : Hand | 5 credits | Difficulty Level
row 1 : Royal flush | 4000* | Extremely Rare
row 2 : Straight flush | 400 | Very Rare
row 3 : Four aces | 2000 | Very Rare
row 4 : Four of a kind, 2-4 | 500 | Rare
row 5 : Four of a kind, 5-K | 250 | Rare
    """,
    """
col : Hand | 5 credits | Difficulty Level
row 1 : Royal flush | 4000* | Extremely Rare
row 2 : Four aces | 2000 | Very Rare
row 3 : Four of a kind, 2-4 | 500 | Rare
row 4 : Straight flush | 400 | Very Rare
row 5 : Four of a kind, 5-K | 250 | Rare
    """,
    """
col : Hand | 5 credits | Difficulty Level
row 1 : Royal flush | 4000* | Extremely Rare
    """
]
},
"EXAMPLE_5": {
            "table_info": """
table_name: Coaching Records
col : Season | Head Coach | Overall Record | Conference Record
row 1 : 1931 | Tom Conley | 4-4 | 
row 2 : 1932 | Tom Conley | 4-2-2 | 
row 3 : 1933 | Marty Brill | 3-3-2 | 
row 4 : 1934 | Marty Brill | 7-0-1 | 
row 5 : 1935 | Marty Brill | 4-4-1 | 
row 6 : 1936 | Marty Brill | 6-4-1 | 
row 7 : 1937 | Marty Brill | 2-7 | 
row 8 : 1938 | Marty Brill | 4-4 | 
row 9 : 1939 | Marty Brill | 6-1-1 | 
row 10 : 1940 | Jim Henry | 6-2 | 
row 11 : 1941 | Jim Henry | 5-3 | 
row 12 : 1997 | Bill Manlove | 1-8 | 

table_name: Coach Profiles
col : Coach Name | Years Active | Win Percentage | Previous Experience | Playing Career
row 1 : Tom Conley | 1931-1932 | .500 | Notre Dame Assistant | All-American End
row 2 : Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 3 : Jim Henry | 1940-1941 | .688 | Georgetown Assistant | Georgetown Tackle
row 4 : Bill Manlove | 1997-2001 | .333 | Widener Head Coach | Temple Lineman

foreign_key: Head Coach, Coach Name
""",
"question": "who was the next head coach after marty brill?",
"answer": "Jim Henry",
"explanation": "To determine who was the next head coach after Marty Brill, I need to analyze the coaching timeline. I'll stitch the Coaching Records and Coach Profiles tables using coach name as the foreign key to combine coaching records with profile information, select columns for season, head coach name, and active years to focus on coaching timeline, sort by season to establish chronological order of coaches, select rows starting from 1939 (Marty Brill's last year) to see who came next, and select only the Head Coach column to clearly identify the next coach after Marty Brill.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_sort_column()",
    "f_select_row()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Coaching Records.Head Coach, Coach Profiles.Coach Name, inner)",
    "f_select_column(Season, Head Coach, Years Active)",
    "f_sort_column(Season)",
    "f_select_row(row 9, row 10, row 11, row 12)",
    "f_select_column(Head Coach)",
    "END"
],
"explanations": [
    "Stitching the Coaching Records and Coach Profiles tables using coach name as the foreign key to combine coaching records with profile information",
    "Selecting columns for season, head coach name, and active years to focus on coaching timeline",
    "Sorting by season to establish chronological order of coaches",
    "Selecting rows starting from 1939 (Marty Brill's last year) to see who came next",
    "Selecting only the Head Coach column to clearly identify the next coach after Marty Brill"
],
"intermediate_tables": [
    """
col : Season | Head Coach | Overall Record | Conference Record | Coach Name | Years Active | Win Percentage | Previous Experience | Playing Career
row 1 : 1931 | Tom Conley | 4-4 |  | Tom Conley | 1931-1932 | .500 | Notre Dame Assistant | All-American End
row 2 : 1932 | Tom Conley | 4-2-2 |  | Tom Conley | 1931-1932 | .500 | Notre Dame Assistant | All-American End
row 3 : 1933 | Marty Brill | 3-3-2 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 4 : 1934 | Marty Brill | 7-0-1 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 5 : 1935 | Marty Brill | 4-4-1 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 6 : 1936 | Marty Brill | 6-4-1 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 7 : 1937 | Marty Brill | 2-7 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 8 : 1938 | Marty Brill | 4-4 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 9 : 1939 | Marty Brill | 6-1-1 |  | Marty Brill | 1933-1939 | .562 | Notre Dame Assistant | All-American Halfback
row 10 : 1940 | Jim Henry | 6-2 |  | Jim Henry | 1940-1941 | .688 | Georgetown Assistant | Georgetown Tackle
row 11 : 1941 | Jim Henry | 5-3 |  | Jim Henry | 1940-1941 | .688 | Georgetown Assistant | Georgetown Tackle
row 12 : 1997 | Bill Manlove | 1-8 |  | Bill Manlove | 1997-2001 | .333 | Widener Head Coach | Temple Lineman
    """,
    """
col : Season | Head Coach | Years Active
row 1 : 1931 | Tom Conley | 1931-1932
row 2 : 1932 | Tom Conley | 1931-1932
row 3 : 1933 | Marty Brill | 1933-1939
row 4 : 1934 | Marty Brill | 1933-1939
row 5 : 1935 | Marty Brill | 1933-1939
row 6 : 1936 | Marty Brill | 1933-1939
row 7 : 1937 | Marty Brill | 1933-1939
row 8 : 1938 | Marty Brill | 1933-1939
row 9 : 1939 | Marty Brill | 1933-1939
row 10 : 1940 | Jim Henry | 1940-1941
row 11 : 1941 | Jim Henry | 1940-1941
row 12 : 1997 | Bill Manlove | 1997-2001
    """,
    """
col : Season | Head Coach | Years Active
row 1 : 1931 | Tom Conley | 1931-1932
row 2 : 1932 | Tom Conley | 1931-1932
row 3 : 1933 | Marty Brill | 1933-1939
row 4 : 1934 | Marty Brill | 1933-1939
row 5 : 1935 | Marty Brill | 1933-1939
row 6 : 1936 | Marty Brill | 1933-1939
row 7 : 1937 | Marty Brill | 1933-1939
row 8 : 1938 | Marty Brill | 1933-1939
row 9 : 1939 | Marty Brill | 1933-1939
row 10 : 1940 | Jim Henry | 1940-1941
row 11 : 1941 | Jim Henry | 1940-1941
row 12 : 1997 | Bill Manlove | 1997-2001
    """,
    """
col : Season | Head Coach | Years Active
row 9 : 1939 | Marty Brill | 1933-1939
row 10 : 1940 | Jim Henry | 1940-1941
row 11 : 1941 | Jim Henry | 1940-1941
row 12 : 1997 | Bill Manlove | 1997-2001
    """,
    """
col : Head Coach
row 9 : Marty Brill
row 10 : Jim Henry
row 11 : Jim Henry
row 12 : Bill Manlove
    """
]
},
    "EXAMPLE_6": {
            "table_info": """
table_name: Players
col : Player | Position | Team | Games | Tackles | Sacks | Interceptions
row 1 : Marcus Peters | CB | Ravens | 16 | 63 | 0 | 9
row 2 : Minkah Fitzpatrick | FS | Steelers | 16 | 69 | 0 | 5
row 3 : Tre'Davious White | CB | Bills | 15 | 58 | 0 | 6
row 4 : Stephon Gilmore | CB | Patriots | 16 | 53 | 0 | 6
row 5 : Devin McCourty | FS | Patriots | 16 | 58 | 0 | 5
row 6 : Anthony Harris | FS | Vikings | 14 | 60 | 0 | 6
row 7 : Logan Ryan | CB | Titans | 16 | 113 | 4.5 | 4
row 8 : Quandre Diggs | FS | Seahawks | 10 | 44 | 0 | 3

table_name: Team Stats
col : Team | Wins | Losses | Playoff Team | Points For | Points Against
row 1 : Ravens | 14 | 2 | Yes | 531 | 282
row 2 : Steelers | 8 | 8 | No | 289 | 303
row 3 : Bills | 10 | 6 | Yes | 314 | 259
row 4 : Patriots | 12 | 4 | Yes | 420 | 225
row 5 : Vikings | 10 | 6 | Yes | 407 | 303
row 6 : Titans | 9 | 7 | Yes | 402 | 331
row 7 : Seahawks | 11 | 5 | Yes | 405 | 398

foreign_key: Team
""",
"question": "which defensive position has the most interceptions on playoff teams?",
"answer": "CB",
"explanation": "To determine which defensive position has the most interceptions on playoff teams, I need to combine player statistics with team playoff status. First, I'll stitch the Players and Team Stats tables to identify players on playoff teams. Then I'll group by position and sum the interceptions to find which position has the most interceptions.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(Players.Team, Team Stats.Team, inner)",
    "f_select_row(row 1, row 3, row 4, row 5, row 6, row 7, row 8)",
    "f_select_column(Position, Interceptions)",
    "f_add_inferred_column(total_interceptions)",
    "f_sort_column(total_interceptions)",
    "END"
],
"explanations": [
    "Stitching the Players and Team Stats tables using team name as the foreign key to combine player stats with team playoff status",
    "Selecting only rows where the team made the playoffs",
    "Selecting only the position and interceptions columns needed for the analysis",
    "Adding an inferred column to sum the interceptions for each position group",
    "Sorting by total interceptions in descending order to identify which position has the most"
],
"intermediate_tables": [
    """
col : Player | Position | Team | Games | Tackles | Sacks | Interceptions | Wins | Losses | Playoff Team | Points For | Points Against
row 1 : Marcus Peters | CB | Ravens | 16 | 63 | 0 | 9 | 14 | 2 | Yes | 531 | 282
row 2 : Minkah Fitzpatrick | FS | Steelers | 16 | 69 | 0 | 5 | 8 | 8 | No | 289 | 303
row 3 : Tre'Davious White | CB | Bills | 15 | 58 | 0 | 6 | 10 | 6 | Yes | 314 | 259
row 4 : Stephon Gilmore | CB | Patriots | 16 | 53 | 0 | 6 | 12 | 4 | Yes | 420 | 225
row 5 : Devin McCourty | FS | Patriots | 16 | 58 | 0 | 5 | 12 | 4 | Yes | 420 | 225
row 6 : Anthony Harris | FS | Vikings | 14 | 60 | 0 | 6 | 10 | 6 | Yes | 407 | 303
row 7 : Logan Ryan | CB | Titans | 16 | 113 | 4.5 | 4 | 9 | 7 | Yes | 402 | 331
row 8 : Quandre Diggs | FS | Seahawks | 10 | 44 | 0 | 3 | 11 | 5 | Yes | 405 | 398
    """,
    """
col : Player | Position | Team | Games | Tackles | Sacks | Interceptions | Wins | Losses | Playoff Team | Points For | Points Against
row 1 : Marcus Peters | CB | Ravens | 16 | 63 | 0 | 9 | 14 | 2 | Yes | 531 | 282
row 3 : Tre'Davious White | CB | Bills | 15 | 58 | 0 | 6 | 10 | 6 | Yes | 314 | 259
row 4 : Stephon Gilmore | CB | Patriots | 16 | 53 | 0 | 6 | 12 | 4 | Yes | 420 | 225
row 5 : Devin McCourty | FS | Patriots | 16 | 58 | 0 | 5 | 12 | 4 | Yes | 420 | 225
row 6 : Anthony Harris | FS | Vikings | 14 | 60 | 0 | 6 | 10 | 6 | Yes | 407 | 303
row 7 : Logan Ryan | CB | Titans | 16 | 113 | 4.5 | 4 | 9 | 7 | Yes | 402 | 331
row 8 : Quandre Diggs | FS | Seahawks | 10 | 44 | 0 | 3 | 11 | 5 | Yes | 405 | 398
    """,
    """
col : Position | Interceptions
row 1 : CB | 9
row 3 : CB | 6
row 4 : CB | 6
row 5 : FS | 5
row 6 : FS | 6
row 7 : CB | 4
row 8 : FS | 3
    """,
    """
col : Position | Interceptions | total_interceptions
row 1 : CB | 9 | 25
row 3 : CB | 6 | 25
row 4 : CB | 6 | 25
row 5 : FS | 5 | 14
row 6 : FS | 6 | 14
row 7 : CB | 4 | 25
row 8 : FS | 3 | 14
    """,
    """
col : Position | Interceptions | total_interceptions
row 1 : CB | 9 | 25
row 3 : CB | 6 | 25
row 4 : CB | 6 | 25
row 7 : CB | 4 | 25
row 5 : FS | 5 | 14
row 6 : FS | 6 | 14
row 8 : FS | 3 | 14
    """,
]
},
    "EXAMPLE_7": {
            "table_info": """
table_name: Season Records
col : year | team | games | wins | losses | points
row 1 : 2015 | Lakers | 82 | 17 | 65 | 34
row 2 : 2016 | Lakers | 82 | 26 | 56 | 52
row 3 : 2017 | Lakers | 82 | 35 | 47 | 70
row 4 : 2018 | Lakers | 82 | 37 | 45 | 74
row 5 : 2019 | Lakers | 82 | 52 | 30 | 104
row 6 : 2020 | Lakers | 72 | 52 | 20 | 104

table_name: Player Stats
col : year | player | games | points | rebounds | assists
row 1 : 2015 | Kobe Bryant | 66 | 17.6 | 3.7 | 2.8
row 2 : 2016 | D'Angelo Russell | 80 | 15.6 | 3.5 | 4.8
row 3 : 2017 | Brandon Ingram | 79 | 16.1 | 5.3 | 3.9
row 4 : 2018 | LeBron James | 55 | 27.4 | 8.5 | 8.3
row 5 : 2019 | Anthony Davis | 62 | 26.1 | 9.3 | 3.2
row 6 : 2020 | LeBron James | 45 | 25.0 | 7.8 | 7.8

foreign_key: year
""",
"question": "in which year did the lakers see the biggest increase in win percentage?",
"answer": "2019",
"explanation": "To determine the year with the biggest increase in win percentage, I need to calculate the win percentage for each season and then find the year-over-year changes. First, I'll stitch the Season Records and Player Stats tables to have all information in one place. Then I'll calculate win percentages for each year and compare consecutive seasons to find the largest increase.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_add_inferred_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_select_table(Season Records)",
    "f_select_column(year, team, games, wins, losses)",
    "f_add_inferred_column(win_percentage)",
    "f_add_inferred_column(win_percentage_increase)",
    "f_sort_column(win_percentage_increase)",
    "END"
],
"explanations": [
    "Selecting the Season Records table to calculate win percentage changes",
    "Selecting only the columns needed for calculating win percentage changes",
    "Adding a win_percentage column to calculate the percentage of games won each season",
    "Adding a win_percentage_increase column to calculate the change in win percentage from the previous season",
    "Sorting by win_percentage_increase in descending order to identify the year with the largest increase"
],
"intermediate_tables": [
    """
col : year | team | games | wins | losses | points
row 1 : 2015 | Lakers | 82 | 17 | 65 | 34
row 2 : 2016 | Lakers | 82 | 26 | 56 | 52
row 3 : 2017 | Lakers | 82 | 35 | 47 | 70
row 4 : 2018 | Lakers | 82 | 37 | 45 | 74
row 5 : 2019 | Lakers | 82 | 52 | 30 | 104
row 6 : 2020 | Lakers | 72 | 52 | 20 | 104
    """,
    """
col : year | team | games | wins | losses
row 1 : 2015 | Lakers | 82 | 17 | 65
row 2 : 2016 | Lakers | 82 | 26 | 56
row 3 : 2017 | Lakers | 82 | 35 | 47
row 4 : 2018 | Lakers | 82 | 37 | 45
row 5 : 2019 | Lakers | 82 | 52 | 30
row 6 : 2020 | Lakers | 72 | 52 | 20
    """,
    """
col : year | team | games | wins | losses | win_percentage
row 1 : 2015 | Lakers | 82 | 17 | 65 | 20.7%
row 2 : 2016 | Lakers | 82 | 26 | 56 | 31.7%
row 3 : 2017 | Lakers | 82 | 35 | 47 | 42.7%
row 4 : 2018 | Lakers | 82 | 37 | 45 | 45.1%
row 5 : 2019 | Lakers | 82 | 52 | 30 | 63.4%
row 6 : 2020 | Lakers | 72 | 52 | 20 | 72.2%
    """,
    """
col : year | team | games | wins | losses | win_percentage | win_percentage_increase
row 1 : 2015 | Lakers | 82 | 17 | 65 | 20.7% | N/A
row 2 : 2016 | Lakers | 82 | 26 | 56 | 31.7% | 11.0%
row 3 : 2017 | Lakers | 82 | 35 | 47 | 42.7% | 11.0%
row 4 : 2018 | Lakers | 82 | 37 | 45 | 45.1% | 2.4%
row 5 : 2019 | Lakers | 82 | 52 | 30 | 63.4% | 18.3%
row 6 : 2020 | Lakers | 72 | 52 | 20 | 72.2% | 8.8%
    """,
    """
col : year | team | games | wins | losses | win_percentage | win_percentage_increase
row 5 : 2019 | Lakers | 82 | 52 | 30 | 63.4% | 18.3%
row 2 : 2016 | Lakers | 82 | 26 | 56 | 31.7% | 11.0%
row 3 : 2017 | Lakers | 82 | 35 | 47 | 42.7% | 11.0%
row 6 : 2020 | Lakers | 72 | 52 | 20 | 72.2% | 8.8%
row 4 : 2018 | Lakers | 82 | 37 | 45 | 45.1% | 2.4%
row 1 : 2015 | Lakers | 82 | 17 | 65 | 20.7% | N/A
    """
]
}
}