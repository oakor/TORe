# Task 1 Examples - SQL/Table Analysis
task_1_EXAMPLES = {
    "EXAMPLE_1": {
    "table_info": """
col : rank | airport | total passengers | % change 2008 / 2009 | international passengers | domestic passengers | transit passengers | aircraft movements | freight ( metric tonnes )
row 1 : 1 | london heathrow | 66036957 | 1.5% | 60652036 | 5254605 | 130316 | 466393 | 1277650
row 2 : 2 | london gatwick | 32392520 | 5.3% | 28698660 | 3662113 | 31747 | 251879 | 74680
row 3 : 3 | london stansted | 19957077 | 10.7% | 18054748 | 1894941 | 7388 | 167817 | 182810
row 4 : 4 | manchester | 18724889 | 11.8% | 16063891 | 2566503 | 94495 | 172515 | 102543
row 5 : 5 | london luton | 9120546 | 10.4% | 7937319 | 1178008 | 5219 | 98736 | 28643
row 6 : 6 | birmingham | 9102899 | 5.4% | 7773643 | 1319558 | 9698 | 101221 | 13070
row 7 : 7 | edinburgh | 9049355 | 0.5% | 4136677 | 4906775 | 5903 | 115969 | 23791
row 8 : 8 | glasgow international | 7225021 | 11.7% | 3423174 | 3790223 | 11624 | 85281 | 2334
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_select_row()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(international_percentage)",
        "f_sort_column(international_percentage)",
        "f_select_row(row 1, row 2, row 3)",
        "END"
    ],
    "explanations": [
        "Adding international_percentage to analyze the proportion of international to total passengers",
        "Sorting by international_percentage to identify airports with highest international traffic ratio",
        "Selecting top 3 airports with the highest international passenger percentage"
    ],
    "intermediate_tables": [
        """
col : rank | airport | total passengers | % change 2008 / 2009 | international passengers | domestic passengers | transit passengers | aircraft movements | freight ( metric tonnes ) | international_percentage
row 1 : 1 | london heathrow | 66036957 | 1.5% | 60652036 | 5254605 | 130316 | 466393 | 1277650 | 91.85%
row 2 : 2 | london gatwick | 32392520 | 5.3% | 28698660 | 3662113 | 31747 | 251879 | 74680 | 88.60%
row 3 : 3 | london stansted | 19957077 | 10.7% | 18054748 | 1894941 | 7388 | 167817 | 182810 | 90.47%
row 4 : 4 | manchester | 18724889 | 11.8% | 16063891 | 2566503 | 94495 | 172515 | 102543 | 85.79%
row 5 : 5 | london luton | 9120546 | 10.4% | 7937319 | 1178008 | 5219 | 98736 | 28643 | 87.03%
row 6 : 6 | birmingham | 9102899 | 5.4% | 7773643 | 1319558 | 9698 | 101221 | 13070 | 85.40%
row 7 : 7 | edinburgh | 9049355 | 0.5% | 4136677 | 4906775 | 5903 | 115969 | 23791 | 45.71%
row 8 : 8 | glasgow international | 7225021 | 11.7% | 3423174 | 3790223 | 11624 | 85281 | 2334 | 47.38%
        """,
        """
col : rank | airport | total passengers | % change 2008 / 2009 | international passengers | domestic passengers | transit passengers | aircraft movements | freight ( metric tonnes ) | international_percentage
row 1 : 1 | london heathrow | 66036957 | 1.5% | 60652036 | 5254605 | 130316 | 466393 | 1277650 | 91.85%
row 2 : 3 | london stansted | 19957077 | 10.7% | 18054748 | 1894941 | 7388 | 167817 | 182810 | 90.47%
row 3 : 2 | london gatwick | 32392520 | 5.3% | 28698660 | 3662113 | 31747 | 251879 | 74680 | 88.60%
row 4 : 5 | london luton | 9120546 | 10.4% | 7937319 | 1178008 | 5219 | 98736 | 28643 | 87.03%
row 5 : 4 | manchester | 18724889 | 11.8% | 16063891 | 2566503 | 94495 | 172515 | 102543 | 85.79%
row 6 : 6 | birmingham | 9102899 | 5.4% | 7773643 | 1319558 | 9698 | 101221 | 13070 | 85.40%
row 7 : 8 | glasgow international | 7225021 | 11.7% | 3423174 | 3790223 | 11624 | 85281 | 2334 | 47.38%
row 8 : 7 | edinburgh | 9049355 | 0.5% | 4136677 | 4906775 | 5903 | 115969 | 23791 | 45.71%
        """,
        """
col : rank | airport | total passengers | % change 2008 / 2009 | international passengers | domestic passengers | transit passengers | aircraft movements | freight ( metric tonnes ) | international_percentage
row 1 : 1 | london heathrow | 66036957 | 1.5% | 60652036 | 5254605 | 130316 | 466393 | 1277650 | 91.85%
row 2 : 3 | london stansted | 19957077 | 10.7% | 18054748 | 1894941 | 7388 | 167817 | 182810 | 90.47%
row 3 : 2 | london gatwick | 32392520 | 5.3% | 28698660 | 3662113 | 31747 | 251879 | 74680 | 88.60%
        """
    ],
    "question": "Which airport has the highest percentage of international passengers relative to its total passenger traffic?",
    "answer": "London Heathrow",
    "explanation": "This question requires calculating the percentage of international passengers for each airport, sorting by this percentage to identify the airport with the highest international traffic share. London Heathrow has the highest percentage at 91.85%."
    },
    "EXAMPLE_2": {
    "table_info": """
col : name | games played | minutes played | minutes played per game | rebounds | rebounds per game | assists | assists per game | field goal % | free throw % | points | points per game
row 1 : allan houston | 78 | 2858 | 36.6 | 283 | 3.6 | 173 | 2.2 | 449 | 909 | 1459 | 18.7
row 2 : latrell sprewell | 77 | 3017 | 39.2 | 347 | 4.5 | 269 | 3.5 | 430 | 783 | 1364 | 17.7
row 3 : glen rice | 75 | 2212 | 29.5 | 307 | 4.1 | 89 | 1.2 | 440 | 852 | 899 | 12.0
row 4 : marcus camby | 63 | 2127 | 33.8 | 515 | 11.5 | 52 | 0.8 | 524 | 667 | 759 | 12.0
row 5 : kurt thomas | 77 | 2125 | 27.6 | 723 | 6.7 | 63 | 0.8 | 511 | 814 | 800 | 10.4
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(efficiency_rating)",
        "f_sort_column(efficiency_rating)",
        "f_add_inferred_column(performance_rank)",
        "END"
    ],
    "explanations": [
        "Adding efficiency_rating based on points, rebounds, and assists per game",
        "Sorting players by efficiency_rating to identify most efficient players",
        "Adding performance_rank to numerically rank players based on efficiency"
    ],
    "intermediate_tables": [
        """
col : name | games played | minutes played | minutes played per game | rebounds | rebounds per game | assists | assists per game | field goal % | free throw % | points | points per game | efficiency_rating
row 1 : allan houston | 78 | 2858 | 36.6 | 283 | 3.6 | 173 | 2.2 | 449 | 909 | 1459 | 18.7 | 24.5
row 2 : latrell sprewell | 77 | 3017 | 39.2 | 347 | 4.5 | 269 | 3.5 | 430 | 783 | 1364 | 17.7 | 25.7
row 3 : glen rice | 75 | 2212 | 29.5 | 307 | 4.1 | 89 | 1.2 | 440 | 852 | 899 | 12.0 | 17.3
row 4 : marcus camby | 63 | 2127 | 33.8 | 515 | 11.5 | 52 | 0.8 | 524 | 667 | 759 | 12.0 | 24.3
row 5 : kurt thomas | 77 | 2125 | 27.6 | 723 | 6.7 | 63 | 0.8 | 511 | 814 | 800 | 10.4 | 17.9
        """,
        """
col : name | games played | minutes played | minutes played per game | rebounds | rebounds per game | assists | assists per game | field goal % | free throw % | points | points per game | efficiency_rating
row 1 : latrell sprewell | 77 | 3017 | 39.2 | 347 | 4.5 | 269 | 3.5 | 430 | 783 | 1364 | 17.7 | 25.7
row 2 : allan houston | 78 | 2858 | 36.6 | 283 | 3.6 | 173 | 2.2 | 449 | 909 | 1459 | 18.7 | 24.5
row 3 : marcus camby | 63 | 2127 | 33.8 | 515 | 11.5 | 52 | 0.8 | 524 | 667 | 759 | 12.0 | 24.3
row 4 : kurt thomas | 77 | 2125 | 27.6 | 723 | 6.7 | 63 | 0.8 | 511 | 814 | 800 | 10.4 | 17.9
row 5 : glen rice | 75 | 2212 | 29.5 | 307 | 4.1 | 89 | 1.2 | 440 | 852 | 899 | 12.0 | 17.3
        """,
        """
col : name | games played | minutes played | minutes played per game | rebounds | rebounds per game | assists | assists per game | field goal % | free throw % | points | points per game | efficiency_rating | performance_rank
row 1 : latrell sprewell | 77 | 3017 | 39.2 | 347 | 4.5 | 269 | 3.5 | 430 | 783 | 1364 | 17.7 | 25.7 | 1
row 2 : allan houston | 78 | 2858 | 36.6 | 283 | 3.6 | 173 | 2.2 | 449 | 909 | 1459 | 18.7 | 24.5 | 2
row 3 : marcus camby | 63 | 2127 | 33.8 | 515 | 11.5 | 52 | 0.8 | 524 | 667 | 759 | 12.0 | 24.3 | 3
row 4 : kurt thomas | 77 | 2125 | 27.6 | 723 | 6.7 | 63 | 0.8 | 511 | 814 | 800 | 10.4 | 17.9 | 4
row 5 : glen rice | 75 | 2212 | 29.5 | 307 | 4.1 | 89 | 1.2 | 440 | 852 | 899 | 12.0 | 17.3 | 5
        """
    ],
    "question": "Who is the most efficient player when considering points, rebounds, and assists per game?",
    "answer": "Latrell Sprewell",
    "explanation": "This question requires calculating an efficiency rating that combines points, rebounds, and assists per game, then sorting players by this metric to determine the most efficient player. Latrell Sprewell has the highest efficiency rating at 25.7."
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
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_select_column(name, city, salary, department)",
        "f_add_inferred_column(salary_level)",
        "f_sort_column(salary)",
        "f_group_column(city)",
        "END"
    ],
    "explanations": [
        "Selecting relevant columns for salary analysis",
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
    "explanation": "This question requires selecting Sales employees, adding salary level information, sorting by salary, and grouping by city to calculate average salaries. The final table shows that Chicago has the highest average salary ($95,000) for Sales employees."
    },
    "EXAMPLE_13": {
    "table_info": """
col : rank | nation | gold | silver | bronze | total
row 1 : brazil | 6 | 2 | 3 | 11
row 2 : venezuela | 3 | 3 | 1 | 7
row 3 : ecuador | 3 | 1 | 1 | 5
row 4 : argentina | 0 | 3 | 5 | 8
row 5 : peru | 0 | 1 | 1 | 2
row 6 : aruba | 0 | 1 | 0 | 1
row 7 : guyana | 0 | 0 | 5 | 5
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(medal_points)",
        "f_select_column(nation, gold, silver, bronze, total, medal_points)",
        "f_sort_column(medal_points)",
        "f_group_column(has_gold)",
        "END"
    ],
    "explanations": [
        "Adding medal_points column to weight medals (gold=3, silver=2, bronze=1)",
        "Selecting relevant columns for medal analysis",
        "Sorting by medal_points to rank nations by weighted medal count",
        "Grouping nations by whether they have gold medals"
    ],
    "intermediate_tables": [
        """
col : rank | nation | gold | silver | bronze | total | medal_points
row 1 : brazil | 6 | 2 | 3 | 11 | 25
row 2 : venezuela | 3 | 3 | 1 | 7 | 16
row 3 : ecuador | 3 | 1 | 1 | 5 | 12
row 4 : argentina | 0 | 3 | 5 | 8 | 11
row 5 : peru | 0 | 1 | 1 | 2 | 3
row 6 : aruba | 0 | 1 | 0 | 1 | 2
row 7 : guyana | 0 | 0 | 5 | 5 | 5
        """,
        """
col : nation | gold | silver | bronze | total | medal_points
row 1 : brazil | 6 | 2 | 3 | 11 | 25
row 2 : venezuela | 3 | 3 | 1 | 7 | 16
row 3 : ecuador | 3 | 1 | 1 | 5 | 12
row 4 : argentina | 0 | 3 | 5 | 8 | 11
row 5 : guyana | 0 | 0 | 5 | 5 | 5
row 6 : peru | 0 | 1 | 1 | 2 | 3
row 7 : aruba | 0 | 1 | 0 | 1 | 2
        """,
        """
col : nation | gold | silver | bronze | total | medal_points
row 1 : brazil | 6 | 2 | 3 | 11 | 25
row 2 : venezuela | 3 | 3 | 1 | 7 | 16
row 3 : ecuador | 3 | 1 | 1 | 5 | 12
row 4 : argentina | 0 | 3 | 5 | 8 | 11
row 5 : guyana | 0 | 0 | 5 | 5 | 5
row 6 : peru | 0 | 1 | 1 | 2 | 3
row 7 : aruba | 0 | 1 | 0 | 1 | 2
        """,
        """
col : has_gold | nations | total_gold | total_silver | total_bronze | total_medals | avg_medal_points
row 1 : Yes | 3 | 12 | 6 | 5 | 23 | 17.67
row 2 : No | 4 | 0 | 5 | 11 | 16 | 5.25
        """
    ],
    "question": "What is the difference between the total number of medals won by the top 3 nations and the total number of medals won by the bottom 3 nations?",
    "answer": "15",
    "explanation": "This question requires comparing the total medal counts between two groups of nations. First, I need to identify the top 3 nations (Brazil, Venezuela, Ecuador) with 11+7+5=23 total medals, and the bottom 3 nations (Peru, Aruba, Guyana) with 2+1+5=8 total medals. The difference is 23-8=15, which is 15 medals."
    },
    "EXAMPLE_14": {
    "table_info": """
col : episode no | airdate | total viewers | share | bbc one weekly ranking
row 1 : 1 | 2 september 2011 | 6114000 | 24.2% | 9
row 2 : 2 | 9 september 2011 | 5370000 | 20.2% | 14
row 3 : 3 | 16 september 2011 | 5450000 | 21.7% | 11
row 4 : 4 | 23 september 2011 | 5210000 | 19.5% | 10
row 5 : 5 | 29 september 2011 | 5020000 | 18.8% | 16
row 6 : 6 | 7 october 2011 | 4780000 | 16.9% | 17
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(viewers_change)",
        "f_select_column(episode no, airdate, total viewers, viewers_change, share)",
        "f_sort_column(total viewers)",
        "f_group_column(above_5M_viewers)",
        "END"
    ],
    "explanations": [
        "Adding viewers_change column to track episode-to-episode viewership trends",
        "Selecting relevant columns for viewership analysis",
        "Sorting by total viewers to identify most popular episodes",
        "Grouping episodes by whether they exceeded 5 million viewers"
    ],
    "intermediate_tables": [
        """
col : episode no | airdate | total viewers | share | bbc one weekly ranking | viewers_change
row 1 : 1 | 2 september 2011 | 6114000 | 24.2% | 9 | N/A
row 2 : 2 | 9 september 2011 | 5370000 | 20.2% | 14 | -744000
row 3 : 3 | 16 september 2011 | 5450000 | 21.7% | 11 | +80000
row 4 : 4 | 23 september 2011 | 5210000 | 19.5% | 10 | -240000
row 5 : 5 | 29 september 2011 | 5020000 | 18.8% | 16 | -190000
row 6 : 6 | 7 october 2011 | 4780000 | 16.9% | 17 | -240000
        """,
        """
col : episode no | airdate | total viewers | viewers_change | share
row 1 : 1 | 2 september 2011 | 6114000 | N/A | 24.2%
row 2 : 2 | 9 september 2011 | 5370000 | -744000 | 20.2%
row 3 : 3 | 16 september 2011 | 5450000 | +80000 | 21.7%
row 4 : 4 | 23 september 2011 | 5210000 | -240000 | 19.5%
row 5 : 5 | 29 september 2011 | 5020000 | -190000 | 18.8%
row 6 : 6 | 7 october 2011 | 4780000 | -240000 | 16.9%
        """,
        """
col : episode no | airdate | total viewers | viewers_change | share
row 1 : 1 | 2 september 2011 | 6114000 | N/A | 24.2%
row 2 : 3 | 16 september 2011 | 5450000 | +80000 | 21.7%
row 3 : 2 | 9 september 2011 | 5370000 | -744000 | 20.2%
row 4 : 4 | 23 september 2011 | 5210000 | -240000 | 19.5%
row 5 : 5 | 29 september 2011 | 5020000 | -190000 | 18.8%
row 6 : 6 | 7 october 2011 | 4780000 | -240000 | 16.9%
        """,
        """
col : above_5M_viewers | episode_count | avg_viewers | avg_share | total_viewers
row 1 : Yes | 4 | 5536000 | 21.4% | 22144000
row 2 : No | 2 | 4900000 | 17.85% | 9800000
        """
    ],
    "question": "Which episode had the highest total viewers, and which episode had the lowest total viewers?",
    "answer": "1, 6",
    "explanation": "This question requires identifying the episodes with the maximum and minimum viewership. Looking at the total viewers column, Episode 1 had the highest viewership with 6,114,000 viewers, while Episode 6 had the lowest with 4,780,000 viewers."
    },
    "EXAMPLE_15": {
    "table_info": """
col : Finish | Driver | Races | Wins | Poles | Points | Earnings
row 1 : 1 | Buck Baker | 40 | 10 | 6 | 10,716 | $30,763
row 2 : 2 | Marvin Panch | 42 | 6 | 4 | 9956 | $24,307
row 3 : 3 | Speedy Thompson | 38 | 2 | 4 | 8580 | $26,841
row 4 : 4 | Lee Petty | 38 | 2 | 4 | 8528 | $18,325
row 5 : 5 | Jack Smith | 40 | 4 | 2 | 8464 | $14,561
row 6 : 6 | Fireball Roberts | 42 | 8 | 4 | 8268 | $19,828
row 7 : 7 | Johnny Allen | 42 | 0 | 1 | 7068 | $9,814
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(points_per_race)",
        "f_select_column(Driver, Races, Wins, Points, points_per_race, Earnings)",
        "f_sort_column(points_per_race)",
        "f_group_column(win_category)",
        "END"
    ],
    "explanations": [
        "Adding points_per_race to evaluate driver efficiency",
        "Selecting relevant columns for driver performance analysis",
        "Sorting by points_per_race to identify most consistent drivers",
        "Grouping drivers by win category (high: 5+, medium: 1-4, low: 0)"
    ],
    "intermediate_tables": [
        """
col : Finish | Driver | Races | Wins | Poles | Points | Earnings | points_per_race
row 1 : 1 | Buck Baker | 40 | 10 | 6 | 10,716 | $30,763 | 267.9
row 2 : 2 | Marvin Panch | 42 | 6 | 4 | 9956 | $24,307 | 237.0
row 3 : 3 | Speedy Thompson | 38 | 2 | 4 | 8580 | $26,841 | 225.8
row 4 : 4 | Lee Petty | 38 | 2 | 4 | 8528 | $18,325 | 224.4
row 5 : 5 | Jack Smith | 40 | 4 | 2 | 8464 | $14,561 | 211.6
row 6 : 6 | Fireball Roberts | 42 | 8 | 4 | 8268 | $19,828 | 196.9
row 7 : 7 | Johnny Allen | 42 | 0 | 1 | 7068 | $9,814 | 168.3
        """,
        """
col : Driver | Races | Wins | Points | points_per_race | Earnings
row 1 : Buck Baker | 40 | 10 | 10,716 | 267.9 | $30,763
row 2 : Marvin Panch | 42 | 6 | 9956 | 237.0 | $24,307
row 3 : Speedy Thompson | 38 | 2 | 8580 | 225.8 | $26,841
row 4 : Lee Petty | 38 | 2 | 8528 | 224.4 | $18,325
row 5 : Jack Smith | 40 | 4 | 8464 | 211.6 | $14,561
row 6 : Fireball Roberts | 42 | 8 | 8268 | 196.9 | $19,828
row 7 : Johnny Allen | 42 | 0 | 7068 | 168.3 | $9,814
        """,
        """
col : Driver | Races | Wins | Points | points_per_race | Earnings
row 1 : Buck Baker | 40 | 10 | 10,716 | 267.9 | $30,763
row 2 : Marvin Panch | 42 | 6 | 9956 | 237.0 | $24,307
row 3 : Speedy Thompson | 38 | 2 | 8580 | 225.8 | $26,841
row 4 : Lee Petty | 38 | 2 | 8528 | 224.4 | $18,325
row 5 : Jack Smith | 40 | 4 | 8464 | 211.6 | $14,561
row 6 : Fireball Roberts | 42 | 8 | 8268 | 196.9 | $19,828
row 7 : Johnny Allen | 42 | 0 | 7068 | 168.3 | $9,814
        """,
        """
col : win_category | drivers | total_wins | avg_points | avg_earnings | avg_points_per_race
row 1 : high | 3 | 24 | 9647 | $24,966 | 233.9
row 2 : medium | 3 | 8 | 8524 | $19,909 | 220.6
row 3 : low | 1 | 0 | 7068 | $9,814 | 168.3
        """
    ],
    "question": "How many more points does the driver with the highest points have compared to the driver with the lowest points?",
    "answer": "3648",
    "explanation": "This question requires finding the difference between the highest and lowest point totals. From the data, Buck Baker has the highest points at 10,716, while Johnny Allen has the lowest at 7,068. The difference is 10,716 - 7,068 = 3,648 points."
    },
    "EXAMPLE_17": {
    "table_info": """
col : gun class (pdr) | shot diameter (cm) | shot volume (cm 3 ) | approx service bore (cm) | mass of projectile (kg)
row 1 : 2 | 6.04 | 172.76 | 6.64 | 0.90846
row 2 : 3 | 6.91 | 172.76 | 7.6 | 1.36028
row 3 : 4 | 7.6 | 230.3 | 8.37 | 1.81339
row 4 : 6 | 8.71 | 345.39 | 9.58 | 2.71957
row 5 : 9 | 10.0 | 518.28 | 11.0 | 4.08091
row 6 : 12 | 10.97 | 691.22 | 12.07 | 5.44269
row 7 : 18 | 12.56 | 1036.96 | 13.81 | 8.16499
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(mass_to_volume_ratio)",
        "f_select_column(gun class (pdr), shot diameter (cm), mass of projectile (kg), mass_to_volume_ratio)",
        "f_sort_column(mass_to_volume_ratio)",
        "f_group_column(size_category)",
        "END"
    ],
    "explanations": [
        "Adding mass_to_volume_ratio to analyze projectile density",
        "Selecting relevant columns for projectile analysis",
        "Sorting by mass_to_volume_ratio to identify most dense projectiles",
        "Grouping by size category (small: ≤4, medium: 6-12, large: ≥18)"
    ],
    "intermediate_tables": [
        """
col : gun class (pdr) | shot diameter (cm) | shot volume (cm 3 ) | approx service bore (cm) | mass of projectile (kg) | mass_to_volume_ratio
row 1 : 2 | 6.04 | 172.76 | 6.64 | 0.90846 | 0.0053
row 2 : 3 | 6.91 | 172.76 | 7.6 | 1.36028 | 0.0079
row 3 : 4 | 7.6 | 230.3 | 8.37 | 1.81339 | 0.0079
row 4 : 6 | 8.71 | 345.39 | 9.58 | 2.71957 | 0.0079
row 5 : 9 | 10.0 | 518.28 | 11.0 | 4.08091 | 0.0079
row 6 : 12 | 10.97 | 691.22 | 12.07 | 5.44269 | 0.0079
row 7 : 18 | 12.56 | 1036.96 | 13.81 | 8.16499 | 0.0079
        """,
        """
col : gun class (pdr) | shot diameter (cm) | mass of projectile (kg) | mass_to_volume_ratio
row 1 : 2 | 6.04 | 0.90846 | 0.0053
row 2 : 3 | 6.91 | 1.36028 | 0.0079
row 3 : 4 | 7.6 | 1.81339 | 0.0079
row 4 : 6 | 8.71 | 2.71957 | 0.0079
row 5 : 9 | 10.0 | 4.08091 | 0.0079
row 6 : 12 | 10.97 | 5.44269 | 0.0079
row 7 : 18 | 12.56 | 8.16499 | 0.0079
        """,
        """
col : gun class (pdr) | shot diameter (cm) | mass of projectile (kg) | mass_to_volume_ratio
row 1 : 3 | 6.91 | 1.36028 | 0.0079
row 2 : 4 | 7.6 | 1.81339 | 0.0079
row 3 : 6 | 8.71 | 2.71957 | 0.0079
row 4 : 9 | 10.0 | 4.08091 | 0.0079
row 5 : 12 | 10.97 | 5.44269 | 0.0079
row 6 : 18 | 12.56 | 8.16499 | 0.0079
row 7 : 2 | 6.04 | 0.90846 | 0.0053
        """,
        """
col : size_category | count | avg_diameter | avg_mass | avg_ratio
row 1 : small | 3 | 6.85 | 1.36 | 0.0070
row 2 : medium | 3 | 9.89 | 4.08 | 0.0079
row 3 : large | 1 | 12.56 | 8.16 | 0.0079
        """
    ],
    "question": "How much more is the mass of the projectile (kg) for a 24-pounder gun compared to a 12-pounder gun?",
    "answer": "5.44427",
    "explanation": "This question requires comparing the mass of projectiles for different gun classes. However, the table doesn't include a 24-pounder gun. From the data, a 12-pounder gun has a projectile mass of 5.44269 kg. Based on the pattern, a 24-pounder gun would have approximately twice the mass, but without exact data in the table, we cannot provide a precise answer."
    },
    "EXAMPLE_18": {
    "table_info": """
col : Rank | City | Population | Area (km2) | Density (inhabitants/km2) | Altitude (mslm)
row 1 : 1st | Alessandria | 94191 | 203.97 | 461.8 | 95
row 2 : 2nd | Casale Monferrato | 36039 | 86.32 | 417.5 | 116
row 3 : 3rd | Novi Ligure | 28581 | 54.22 | 527.1 | 197
row 4 : 4th | Tortona | 27476 | 99.29 | 276.7 | 122
row 5 : 5th | Acqui Terme | 20426 | 33.42 | 611.2 | 156
row 6 : 6th | Valenza | 20282 | 50.05 | 405.2 | 125
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(population_altitude_ratio)",
        "f_select_column(City, Population, Density, Altitude, population_altitude_ratio)",
        "f_sort_column(Density)",
        "f_group_column(density_category)",
        "END"
    ],
    "explanations": [
        "Adding population_altitude_ratio to analyze relationship between elevation and population size",
        "Selecting relevant columns for urban geography analysis",
        "Sorting by population density to identify most densely populated cities",
        "Grouping by density category (high: >500, medium: 300-500, low: <300)"
    ],
    "intermediate_tables": [
        """
col : Rank | City | Population | Area (km2) | Density (inhabitants/km2) | Altitude (mslm) | population_altitude_ratio
row 1 : 1st | Alessandria | 94191 | 203.97 | 461.8 | 95 | 991.5
row 2 : 2nd | Casale Monferrato | 36039 | 86.32 | 417.5 | 116 | 310.7
row 3 : 3rd | Novi Ligure | 28581 | 54.22 | 527.1 | 197 | 145.1
row 4 : 4th | Tortona | 27476 | 99.29 | 276.7 | 122 | 225.2
row 5 : 5th | Acqui Terme | 20426 | 33.42 | 611.2 | 156 | 130.9
row 6 : 6th | Valenza | 20282 | 50.05 | 405.2 | 125 | 162.3
        """,
        """
col : City | Population | Density | Altitude | population_altitude_ratio
row 1 : Alessandria | 94191 | 461.8 | 95 | 991.5
row 2 : Casale Monferrato | 36039 | 417.5 | 116 | 310.7
row 3 : Novi Ligure | 28581 | 527.1 | 197 | 145.1
row 4 : Tortona | 27476 | 276.7 | 122 | 225.2
row 5 : Acqui Terme | 20426 | 611.2 | 156 | 130.9
row 6 : Valenza | 20282 | 405.2 | 125 | 162.3
        """,
        """
col : City | Population | Density | Altitude | population_altitude_ratio
row 1 : Acqui Terme | 20426 | 611.2 | 156 | 130.9
row 2 : Novi Ligure | 28581 | 527.1 | 197 | 145.1
row 3 : Alessandria | 94191 | 461.8 | 95 | 991.5
row 4 : Valenza | 20282 | 405.2 | 125 | 162.3
row 5 : Casale Monferrato | 36039 | 417.5 | 116 | 310.7
row 6 : Tortona | 27476 | 276.7 | 122 | 225.2
        """,
        """
col : density_category | count | avg_population | avg_altitude | total_population
row 1 : high | 2 | 24504 | 177 | 49007
row 2 : medium | 3 | 50171 | 112 | 150512
row 3 : low | 1 | 27476 | 122 | 27476
        """
    ],
    "question": "Which city has the highest population density, and which city has the lowest population density?",
    "answer": "Acqui Terme, Tortona",
    "explanation": "This question requires comparing the population density values across cities. From the data, Acqui Terme has the highest population density at 611.2 inhabitants/km², while Tortona has the lowest at 276.7 inhabitants/km²."
    },
    "EXAMPLE_19": {
    "table_info": """
col : Binary | Octal | Decimal | Hexadecimal | Glyph
row 1 : 0011 0000 | 60 | 48 | 30 | 0
row 2 : 0011 0001 | 61 | 49 | 31 | 1
row 3 : 0011 0010 | 62 | 50 | 32 | 2
row 4 : 0011 0011 | 63 | 51 | 33 | 3
row 5 : 0011 0100 | 64 | 52 | 34 | 4
row 6 : 0011 0111 | 67 | 55 | 37 | 7
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(binary_digit_sum)",
        "f_select_column(Glyph, Binary, Decimal, Hexadecimal, binary_digit_sum)",
        "f_sort_column(binary_digit_sum)",
        "f_select_row(row 5, row 6)",
        "END"
    ],
    "explanations": [
        "Adding binary_digit_sum to count the number of 1s in each binary representation",
        "Selecting relevant columns for numerical representation analysis",
        "Sorting by binary_digit_sum to identify patterns in binary representations",
        "Select the glyphs which have binary_digit_sum greater than 3"
    ],
    "intermediate_tables": [
        """
col : Binary | Octal | Decimal | Hexadecimal | Glyph | binary_digit_sum
row 1 : 0011 0000 | 60 | 48 | 30 | 0 | 2
row 2 : 0011 0001 | 61 | 49 | 31 | 1 | 3
row 3 : 0011 0010 | 62 | 50 | 32 | 2 | 3
row 4 : 0011 0011 | 63 | 51 | 33 | 3 | 4
row 5 : 0011 0100 | 64 | 52 | 34 | 4 | 3
row 6 : 0011 0111 | 67 | 55 | 37 | 7 | 5
        """,
        """
col : Glyph | Binary | Decimal | Hexadecimal | binary_digit_sum
row 1 : 0 | 0011 0000 | 48 | 30 | 2
row 2 : 1 | 0011 0001 | 49 | 31 | 3
row 3 : 2 | 0011 0010 | 50 | 32 | 3
row 4 : 3 | 0011 0011 | 51 | 33 | 4
row 5 : 4 | 0011 0100 | 52 | 34 | 3
row 6 : 7 | 0011 0111 | 55 | 37 | 5
        """,
        """
col : Glyph | Binary | Decimal | Hexadecimal | binary_digit_sum
row 1 : 0 | 0011 0000 | 48 | 30 | 2
row 2 : 1 | 0011 0001 | 49 | 31 | 3
row 3 : 2 | 0011 0010 | 50 | 32 | 3
row 4 : 4 | 0011 0100 | 52 | 34 | 3
row 5 : 3 | 0011 0011 | 51 | 33 | 4
row 6 : 7 | 0011 0111 | 55 | 37 | 5
        """,
        """
col : Glyph | Binary | Decimal | Hexadecimal | binary_digit_sum
row 5 : 3 | 0011 0011 | 51 | 33 | 4
row 6 : 7 | 0011 0111 | 55 | 37 | 5
        """
    ],
    "question": "What is the sum of the decimal values for the glyphs 3 and 7, and what is the total of the binary digit sum for the glyphs 3 and 7?",
    "answer": "106, 9",
    "explanation": "This question requires adding the decimal values for glyphs 3 and 7, then converting the result to hexadecimal. From the table, glyph 3 has decimal value 51 and glyph 7 has decimal value 55. The sum is 51 + 55 = 106. Converting 106 to hexadecimal gives 6A. The total of the binary digit sum for the glyphs 3 and 7 is 4 + 5 = 9."
    },
    "EXAMPLE_20": {
    "table_info": """
col : Country | Gold | Silver | Bronze | Total | Rank
row 1 : United States | 39 | 41 | 33 | 113 | 1
row 2 : China | 38 | 32 | 18 | 88 | 2
row 3 : Japan | 27 | 14 | 17 | 58 | 3
row 4 : Great Britain | 22 | 21 | 22 | 65 | 4
row 5 : ROC | 20 | 28 | 23 | 71 | 5
row 6 : Australia | 17 | 7 | 22 | 46 | 6
row 7 : Netherlands | 10 | 12 | 14 | 36 | 7
row 8 : France | 10 | 12 | 11 | 33 | 8
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(weighted_score)",
        "f_sort_column(weighted_score)",
        "f_group_column(medal_tier)",
        "END"
    ],
    "explanations": [
        "Adding weighted_score to calculate medal points (gold=3, silver=2, bronze=1)",
        "Sorting countries by weighted_score to identify strongest performers",
        "Grouping countries by medal tier (high: >150, medium: 100-150, low: <100)"
    ],
    "intermediate_tables": [
        """
col : Country | Gold | Silver | Bronze | Total | Rank | weighted_score
row 1 : United States | 39 | 41 | 33 | 113 | 1 | 191
row 2 : China | 38 | 32 | 18 | 88 | 2 | 164
row 3 : Japan | 27 | 14 | 17 | 58 | 3 | 109
row 4 : Great Britain | 22 | 21 | 22 | 65 | 4 | 108
row 5 : ROC | 20 | 28 | 23 | 71 | 5 | 111
row 6 : Australia | 17 | 7 | 22 | 46 | 6 | 70
row 7 : Netherlands | 10 | 12 | 14 | 36 | 7 | 56
row 8 : France | 10 | 12 | 11 | 33 | 8 | 54
        """,
        """
col : Country | Gold | Silver | Bronze | Total | Rank | weighted_score
row 1 : United States | 39 | 41 | 33 | 113 | 1 | 191
row 2 : China | 38 | 32 | 18 | 88 | 2 | 164
row 3 : ROC | 20 | 28 | 23 | 71 | 5 | 111
row 4 : Japan | 27 | 14 | 17 | 58 | 3 | 109
row 5 : Great Britain | 22 | 21 | 22 | 65 | 4 | 108
row 6 : Australia | 17 | 7 | 22 | 46 | 6 | 70
row 7 : Netherlands | 10 | 12 | 14 | 36 | 7 | 56
row 8 : France | 10 | 12 | 11 | 33 | 8 | 54
        """,
        """
col : medal_tier | countries | total_gold | total_silver | total_bronze | avg_weighted_score
row 1 : high | 2 | 77 | 73 | 51 | 177.5
row 2 : medium | 3 | 69 | 63 | 62 | 109.3
row 3 : low | 3 | 37 | 31 | 47 | 60.0
        """
    ],
    "question": "What is the difference in weighted score between the country with the most gold medals and the country with the most silver medals?",
    "answer": "27",
    "explanation": "This question requires identifying which country has the most gold medals (United States with 39) and which has the most silver medals (United States with 41). Since it's the same country, we need to look at the second-highest in silver medals, which is China with 32. The weighted scores are 191 for United States and 164 for China, with a difference of 191 - 164 = 27 points."
    },
    "EXAMPLE_21": {
    "table_info": """
col : University | Country | World Rank | Research Quality | Teaching Quality | Student-Faculty Ratio | International Students (%)
row 1 : Harvard University | USA | 1 | 98.7 | 95.2 | 8:1 | 24
row 2 : Stanford University | USA | 2 | 97.5 | 94.8 | 7:1 | 22
row 3 : University of Cambridge | UK | 3 | 96.8 | 95.6 | 11:1 | 37
row 4 : MIT | USA | 4 | 97.9 | 93.4 | 6:1 | 33
row 5 : University of Oxford | UK | 5 | 96.4 | 95.3 | 10:1 | 41
row 6 : ETH Zurich | Switzerland | 9 | 93.2 | 90.1 | 15:1 | 38
row 7 : University of Tokyo | Japan | 23 | 89.5 | 88.7 | 13:1 | 15
row 8 : Peking University | China | 18 | 90.8 | 89.2 | 17:1 | 19
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(overall_score)",
        "f_select_column(University, Country, World Rank, Research Quality, Teaching Quality, overall_score)",
        "f_sort_column(overall_score)",
        "f_group_column(Country)",
        "END"
    ],
    "explanations": [
        "Adding overall_score as a weighted average of research and teaching quality",
        "Selecting relevant columns for university performance analysis",
        "Sorting by overall_score to identify top-performing universities",
        "Grouping by country to analyze performance across different nations"
    ],
    "intermediate_tables": [
        """
col : University | Country | World Rank | Research Quality | Teaching Quality | Student-Faculty Ratio | International Students (%) | overall_score
row 1 : Harvard University | USA | 1 | 98.7 | 95.2 | 8:1 | 24 | 97.4
row 2 : Stanford University | USA | 2 | 97.5 | 94.8 | 7:1 | 22 | 96.5
row 3 : University of Cambridge | UK | 3 | 96.8 | 95.6 | 11:1 | 37 | 96.4
row 4 : MIT | USA | 4 | 97.9 | 93.4 | 6:1 | 33 | 96.2
row 5 : University of Oxford | UK | 5 | 96.4 | 95.3 | 10:1 | 41 | 96.0
row 6 : ETH Zurich | Switzerland | 9 | 93.2 | 90.1 | 15:1 | 38 | 92.0
row 7 : University of Tokyo | Japan | 23 | 89.5 | 88.7 | 13:1 | 15 | 89.2
row 8 : Peking University | China | 18 | 90.8 | 89.2 | 17:1 | 19 | 90.2
        """,
        """
col : University | Country | World Rank | Research Quality | Teaching Quality | overall_score
row 1 : Harvard University | USA | 1 | 98.7 | 95.2 | 97.4
row 2 : Stanford University | USA | 2 | 97.5 | 94.8 | 96.5
row 3 : University of Cambridge | UK | 3 | 96.8 | 95.6 | 96.4
row 4 : MIT | USA | 4 | 97.9 | 93.4 | 96.2
row 5 : University of Oxford | UK | 5 | 96.4 | 95.3 | 96.0
row 6 : ETH Zurich | Switzerland | 9 | 93.2 | 90.1 | 92.0
row 7 : Peking University | China | 18 | 90.8 | 89.2 | 90.2
row 8 : University of Tokyo | Japan | 23 | 89.5 | 88.7 | 89.2
        """,
        """
col : University | Country | World Rank | Research Quality | Teaching Quality | overall_score
row 1 : Harvard University | USA | 1 | 98.7 | 95.2 | 97.4
row 2 : Stanford University | USA | 2 | 97.5 | 94.8 | 96.5
row 3 : University of Cambridge | UK | 3 | 96.8 | 95.6 | 96.4
row 4 : MIT | USA | 4 | 97.9 | 93.4 | 96.2
row 5 : University of Oxford | UK | 5 | 96.4 | 95.3 | 96.0
row 6 : ETH Zurich | Switzerland | 9 | 93.2 | 90.1 | 92.0
row 7 : Peking University | China | 18 | 90.8 | 89.2 | 90.2
row 8 : University of Tokyo | Japan | 23 | 89.5 | 88.7 | 89.2
        """,
        """
col : Country | universities | avg_rank | avg_research | avg_teaching | avg_overall
row 1 : USA | 3 | 2.3 | 98.0 | 94.5 | 96.7
row 2 : UK | 2 | 4.0 | 96.6 | 95.5 | 96.2
row 3 : Switzerland | 1 | 9.0 | 93.2 | 90.1 | 92.0
row 4 : China | 1 | 18.0 | 90.8 | 89.2 | 90.2
row 5 : Japan | 1 | 23.0 | 89.5 | 88.7 | 89.2
        """
    ],
    "question": "Which country has the highest average teaching quality score among its universities, and what is that score?",
    "answer": "UK, 95.5",
    "explanation": "This question requires calculating the average teaching quality for universities grouped by country. The UK has the highest average teaching quality at 95.5, derived from the University of Cambridge (95.6) and the University of Oxford (95.3)."
    },
    "EXAMPLE_22": {
    "table_info": """
col : Model | Manufacturer | Type | Engine (L) | Horsepower | MPG City | MPG Highway | Price ($) | Safety Rating
row 1 : Civic | Honda | Sedan | 1.5 | 174 | 32 | 42 | 21700 | 5
row 2 : Accord | Honda | Sedan | 1.5 | 192 | 30 | 38 | 24970 | 5
row 3 : Camry | Toyota | Sedan | 2.5 | 203 | 28 | 39 | 25945 | 5
row 4 : RAV4 | Toyota | SUV | 2.5 | 203 | 27 | 35 | 26975 | 5
row 5 : F-150 | Ford | Truck | 3.5 | 400 | 18 | 24 | 30635 | 4
row 6 : Mustang | Ford | Sports | 5.0 | 460 | 15 | 24 | 37075 | 4
row 7 : Model 3 | Tesla | Electric | N/A | 283 | 138 | 126 | 46990 | 5
row 8 : Wrangler | Jeep | SUV | 3.6 | 285 | 17 | 23 | 29995 | 3
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "f_group_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(efficiency_score)",
        "f_select_column(Model, Manufacturer, Type, Horsepower, MPG Highway, efficiency_score)",
        "f_sort_column(efficiency_score)",
        "f_group_column(Type)",
        "END"
    ],
    "explanations": [
        "Adding efficiency_score to balance power and fuel economy (Horsepower × MPG Highway / 100)",
        "Selecting relevant columns for vehicle performance analysis",
        "Sorting by efficiency_score to identify most efficient vehicles",
        "Grouping by vehicle type to compare efficiency across different categories"
    ],
    "intermediate_tables": [
        """
col : Model | Manufacturer | Type | Engine (L) | Horsepower | MPG City | MPG Highway | Price ($) | Safety Rating | efficiency_score
row 1 : Civic | Honda | Sedan | 1.5 | 174 | 32 | 42 | 21700 | 5 | 73.1
row 2 : Accord | Honda | Sedan | 1.5 | 192 | 30 | 38 | 24970 | 5 | 73.0
row 3 : Camry | Toyota | Sedan | 2.5 | 203 | 28 | 39 | 25945 | 5 | 79.2
row 4 : RAV4 | Toyota | SUV | 2.5 | 203 | 27 | 35 | 26975 | 5 | 71.1
row 5 : F-150 | Ford | Truck | 3.5 | 400 | 18 | 24 | 30635 | 4 | 96.0
row 6 : Mustang | Ford | Sports | 5.0 | 460 | 15 | 24 | 37075 | 4 | 110.4
row 7 : Model 3 | Tesla | Electric | N/A | 283 | 138 | 126 | 46990 | 5 | 356.6
row 8 : Wrangler | Jeep | SUV | 3.6 | 285 | 17 | 23 | 29995 | 3 | 65.6
        """,
        """
col : Model | Manufacturer | Type | Horsepower | MPG Highway | efficiency_score
row 1 : Civic | Honda | Sedan | 174 | 42 | 73.1
row 2 : Accord | Honda | Sedan | 192 | 38 | 73.0
row 3 : Camry | Toyota | Sedan | 203 | 39 | 79.2
row 4 : RAV4 | Toyota | SUV | 203 | 35 | 71.1
row 5 : F-150 | Ford | Truck | 400 | 24 | 96.0
row 6 : Mustang | Ford | Sports | 460 | 24 | 110.4
row 7 : Model 3 | Tesla | Electric | 283 | 126 | 356.6
row 8 : Wrangler | Jeep | SUV | 285 | 23 | 65.6
        """,
        """
col : Model | Manufacturer | Type | Horsepower | MPG Highway | efficiency_score
row 1 : Model 3 | Tesla | Electric | 283 | 126 | 356.6
row 2 : Mustang | Ford | Sports | 460 | 24 | 110.4
row 3 : F-150 | Ford | Truck | 400 | 24 | 96.0
row 4 : Camry | Toyota | Sedan | 203 | 39 | 79.2
row 5 : Civic | Honda | Sedan | 174 | 42 | 73.1
row 6 : Accord | Honda | Sedan | 192 | 38 | 73.0
row 7 : RAV4 | Toyota | SUV | 203 | 35 | 71.1
row 8 : Wrangler | Jeep | SUV | 285 | 23 | 65.6
        """,
        """
col : Type | models | avg_horsepower | avg_mpg | avg_efficiency
row 1 : Electric | 1 | 283.0 | 126.0 | 356.6
row 2 : Sports | 1 | 460.0 | 24.0 | 110.4
row 3 : Truck | 1 | 400.0 | 24.0 | 96.0
row 4 : Sedan | 3 | 189.7 | 39.7 | 75.1
row 5 : SUV | 2 | 244.0 | 29.0 | 68.3
        """
    ],
    "question": "Which vehicle type has the best balance of power and fuel economy based on the efficiency score?",
    "answer": "Electric",
    "explanation": "This question requires analyzing the efficiency score (Horsepower × MPG Highway / 100) across different vehicle types. Electric vehicles, represented by the Tesla Model 3, have by far the highest efficiency score at 356.6, due to their combination of good horsepower (283) and exceptional fuel economy equivalent (126 MPG Highway)."
    }
}
