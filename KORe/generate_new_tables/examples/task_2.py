# Task 2 Examples - SQL/Table Analysis (Trend Analysis)
task_2_EXAMPLES = {
    "EXAMPLE_1": {
    "table_info": """
col : rank | name | height ft ( m ) | floors | year
row 1 : 1 | wells fargo plaza | 296 (90) | 21 | 1972
row 2 : 2 | chase tower | 250 (76) | 20 | 1971
row 3 : 3 | plaza hotel | 239 (72) | 19 | 1930
row 4 : 4 | kayser building | 232 (70) | 20 | 1983
row 5 : 5 | bassett tower | 216 (66) | 15 | 1930
row 6 : 6 | el paso natural gas company building | 208 (63) | 18 | 1954
row 7 : 7 | camino real paso del norte hotel | 205 (62) | 17 | 1986
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(height_to_floor_ratio)",
        "f_sort_column(year)",
        "f_add_inferred_column(building_era)",
        "END"
    ],
    "explanations": [
        "Adding height_to_floor_ratio to analyze efficiency of building designs",
        "Sorting by year to observe building height trends over time",
        "Adding building_era to categorize buildings by construction periods"
    ],
    "intermediate_tables": [
        """
col : rank | name | height ft ( m ) | floors | year | height_to_floor_ratio
row 1 : 1 | wells fargo plaza | 296 (90) | 21 | 1972 | 14.10
row 2 : 2 | chase tower | 250 (76) | 20 | 1971 | 12.50
row 3 : 3 | plaza hotel | 239 (72) | 19 | 1930 | 12.58
row 4 : 4 | kayser building | 232 (70) | 20 | 1983 | 11.60
row 5 : 5 | bassett tower | 216 (66) | 15 | 1930 | 14.40
row 6 : 6 | el paso natural gas company building | 208 (63) | 18 | 1954 | 11.56
row 7 : 7 | camino real paso del norte hotel | 205 (62) | 17 | 1986 | 12.06
        """,
        """
col : rank | name | height ft ( m ) | floors | year | height_to_floor_ratio
row 1 : 3 | plaza hotel | 239 (72) | 19 | 1930 | 12.58
row 2 : 5 | bassett tower | 216 (66) | 15 | 1930 | 14.40
row 3 : 6 | el paso natural gas company building | 208 (63) | 18 | 1954 | 11.56
row 4 : 2 | chase tower | 250 (76) | 20 | 1971 | 12.50
row 5 : 1 | wells fargo plaza | 296 (90) | 21 | 1972 | 14.10
row 6 : 4 | kayser building | 232 (70) | 20 | 1983 | 11.60
row 7 : 7 | camino real paso del norte hotel | 205 (62) | 17 | 1986 | 12.06
        """,
        """
col : rank | name | height ft ( m ) | floors | year | height_to_floor_ratio | building_era
row 1 : 3 | plaza hotel | 239 (72) | 19 | 1930 | 12.58 | Pre-Modern
row 2 : 5 | bassett tower | 216 (66) | 15 | 1930 | 14.40 | Pre-Modern
row 3 : 6 | el paso natural gas company building | 208 (63) | 18 | 1954 | 11.56 | Mid-Century
row 4 : 2 | chase tower | 250 (76) | 20 | 1971 | 12.50 | Modern
row 5 : 1 | wells fargo plaza | 296 (90) | 21 | 1972 | 14.10 | Modern
row 6 : 4 | kayser building | 232 (70) | 20 | 1983 | 11.60 | Contemporary
row 7 : 7 | camino real paso del norte hotel | 205 (62) | 17 | 1986 | 12.06 | Contemporary
        """
    ],
    "question": "What trend can be observed in building heights from the 1930s to the 1980s?",
    "answer": "No clear trend",
    "explanation": "This question requires analyzing building heights across different time periods. The final table shows that heights from the 1930s to 1970s (from 239ft to 296ft) has no clear trend."
    },
    "EXAMPLE_2": {
    "table_info": """
col : episode number | title | original airing | timeslot | viewers | top 50 ranking | scripted show ranking
row 1 : 112 | nice is different than good | february 15 , 2010 | 8:35 pm - 9:30 pm | 479100 | 12 | 3
row 2 : 113 | being alive) | february 22 , 2010 | 8:30 pm - 9:30 pm | 477080 | 8 | 1
row 3 : 114 | never judge a lady by her lover | march 1 , 2010 | 8:30 pm - 9:30 pm | 447990 | 9 | 1
row 4 : 115 | the god - why - don't - you - love - me blues | march 8 , 2010 | 8:30 pm - 9:30 pm | 471200 | 14 | 4
row 5 : 116 | everybody ought to have a maid | march 15 , 2010 | 8:30 pm - 9:30 pm | 448490 | 15 | 5
row 6 : 117 | don't walk on the grass | march 22 , 2010 | 8:30 pm - 9:30 pm | 452490 | 12 | 4
row 7 : 118 | careful the things you say | march 29 , 2010 | 8:30 pm - 9:30 pm | 413820 | 13 | 5
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_sort_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(viewer_trend)",
        "f_sort_column(original airing)",
        "f_add_inferred_column(season_segment)",
        "END"
    ],
    "explanations": [
        "Adding viewer_trend to track changes in viewership compared to previous episode",
        "Sorting by air date to analyze the chronological trend in viewership",
        "Adding season_segment to identify different parts of the season"
    ],
    "intermediate_tables": [
        """
col : episode number | title | original airing | timeslot | viewers | top 50 ranking | scripted show ranking | viewer_trend
row 1 : 112 | nice is different than good | february 15 , 2010 | 8:35 pm - 9:30 pm | 479100 | 12 | 3 | N/A
row 2 : 113 | being alive) | february 22 , 2010 | 8:30 pm - 9:30 pm | 477080 | 8 | 1 | -2020
row 3 : 114 | never judge a lady by her lover | march 1 , 2010 | 8:30 pm - 9:30 pm | 447990 | 9 | 1 | -29090
row 4 : 115 | the god - why - don't - you - love - me blues | march 8 , 2010 | 8:30 pm - 9:30 pm | 471200 | 14 | 4 | +23210
row 5 : 116 | everybody ought to have a maid | march 15 , 2010 | 8:30 pm - 9:30 pm | 448490 | 15 | 5 | -22710
row 6 : 117 | don't walk on the grass | march 22 , 2010 | 8:30 pm - 9:30 pm | 452490 | 12 | 4 | +4000
row 7 : 118 | careful the things you say | march 29 , 2010 | 8:30 pm - 9:30 pm | 413820 | 13 | 5 | -38670
        """,
        """
col : episode number | title | original airing | timeslot | viewers | top 50 ranking | scripted show ranking | viewer_trend
row 1 : 112 | nice is different than good | february 15 , 2010 | 8:35 pm - 9:30 pm | 479100 | 12 | 3 | N/A
row 2 : 113 | being alive) | february 22 , 2010 | 8:30 pm - 9:30 pm | 477080 | 8 | 1 | -2020
row 3 : 114 | never judge a lady by her lover | march 1 , 2010 | 8:30 pm - 9:30 pm | 447990 | 9 | 1 | -29090
row 4 : 115 | the god - why - don't - you - love - me blues | march 8 , 2010 | 8:30 pm - 9:30 pm | 471200 | 14 | 4 | +23210
row 5 : 116 | everybody ought to have a maid | march 15 , 2010 | 8:30 pm - 9:30 pm | 448490 | 15 | 5 | -22710
row 6 : 117 | don't walk on the grass | march 22 , 2010 | 8:30 pm - 9:30 pm | 452490 | 12 | 4 | +4000
row 7 : 118 | careful the things you say | march 29 , 2010 | 8:30 pm - 9:30 pm | 413820 | 13 | 5 | -38670
        """,
        """
col : episode number | title | original airing | timeslot | viewers | top 50 ranking | scripted show ranking | viewer_trend | season_segment
row 1 : 112 | nice is different than good | february 15 , 2010 | 8:35 pm - 9:30 pm | 479100 | 12 | 3 | N/A | Early
row 2 : 113 | being alive) | february 22 , 2010 | 8:30 pm - 9:30 pm | 477080 | 8 | 1 | -2020 | Early
row 3 : 114 | never judge a lady by her lover | march 1 , 2010 | 8:30 pm - 9:30 pm | 447990 | 9 | 1 | -29090 | Mid
row 4 : 115 | the god - why - don't - you - love - me blues | march 8 , 2010 | 8:30 pm - 9:30 pm | 471200 | 14 | 4 | +23210 | Mid
row 5 : 116 | everybody ought to have a maid | march 15 , 2010 | 8:30 pm - 9:30 pm | 448490 | 15 | 5 | -22710 | Mid
row 6 : 117 | don't walk on the grass | march 22 , 2010 | 8:30 pm - 9:30 pm | 452490 | 12 | 4 | +4000 | Late
row 7 : 118 | careful the things you say | march 29 , 2010 | 8:30 pm - 9:30 pm | 413820 | 13 | 5 | -38670 | Late
        """
    ],
    "question": "Based on the viewership data, what is the overall trend for the show from February to March 2010?",
    "answer": "Decreasing trend",
    "explanation": "This question requires analyzing the viewership numbers over time. The final table shows that viewership started at 479,100 in February and declined to 413,820 by late March, with some fluctuations but an overall downward trend."
    },
    "EXAMPLE_3": {
    "table_info": """
col : season | series | team | races | wins | poles | f / laps | podiums | points | position
row 1 : 2005 | formula renault 2.0 germany | novorace oy | 16 | 1 | 1 | 2 | 2 | 156 | 9th
row 2 : 2005 | eurocup formula renault 2.0 | korainen bros motorsport | 10 | 0 | 0 | 0 | 0 | 13 | 20th
row 3 : 2005 | formula renault 2.0 italia winter series | korainen bros motorsport | 4 | 1 | 0 | 0 | 3 | 44 | 1st
row 4 : 2006 | formula renault 2.0 nec | korainen bros motorsport | 12 | 0 | 0 | 1 | 2 | 149 | 11th
row 5 : 2006 | eurocup formula renault 2.0 | korainen bros motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th
row 6 : 2006 | eurocup formula renault 2.0 | jenzer motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(performance_index)",
        "f_add_inferred_column(season_avg_performance)",
        "f_sort_column(season)",
        "END"
    ],
    "explanations": [
        "Adding performance_index based on wins, poles, and podiums to measure overall performance",
        "Adding season_avg_performance to calculate average performance for each season",
        "Sorting by season to analyze chronological trends"
    ],
    "intermediate_tables": [
        """
col : season | series | team | races | wins | poles | f / laps | podiums | points | position | performance_index
row 1 : 2005 | formula renault 2.0 germany | novorace oy | 16 | 1 | 1 | 2 | 2 | 156 | 9th | 3.75
row 2 : 2005 | eurocup formula renault 2.0 | korainen bros motorsport | 10 | 0 | 0 | 0 | 0 | 13 | 20th | 0.00
row 3 : 2005 | formula renault 2.0 italia winter series | korainen bros motorsport | 4 | 1 | 0 | 0 | 3 | 44 | 1st | 4.00
row 4 : 2006 | formula renault 2.0 nec | korainen bros motorsport | 12 | 0 | 0 | 1 | 2 | 149 | 11th | 1.50
row 5 : 2006 | eurocup formula renault 2.0 | korainen bros motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43
row 6 : 2006 | eurocup formula renault 2.0 | jenzer motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43
        """,
        """
col : season | series | team | races | wins | poles | f / laps | podiums | points | position | performance_index | season_avg_performance
row 1 : 2005 | formula renault 2.0 germany | novorace oy | 16 | 1 | 1 | 2 | 2 | 156 | 9th | 3.75 | 2.58
row 2 : 2005 | eurocup formula renault 2.0 | korainen bros motorsport | 10 | 0 | 0 | 0 | 0 | 13 | 20th | 0.00 | 2.58
row 3 : 2005 | formula renault 2.0 italia winter series | korainen bros motorsport | 4 | 1 | 0 | 0 | 3 | 44 | 1st | 4.00 | 2.58
row 4 : 2006 | formula renault 2.0 nec | korainen bros motorsport | 12 | 0 | 0 | 1 | 2 | 149 | 11th | 1.50 | 1.45
row 5 : 2006 | eurocup formula renault 2.0 | korainen bros motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43 | 1.45
row 6 : 2006 | eurocup formula renault 2.0 | jenzer motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43 | 1.45
        """,
        """
col : season | series | team | races | wins | poles | f / laps | podiums | points | position | performance_index | season_avg_performance
row 1 : 2005 | formula renault 2.0 germany | novorace oy | 16 | 1 | 1 | 2 | 2 | 156 | 9th | 3.75 | 2.58
row 2 : 2005 | eurocup formula renault 2.0 | korainen bros motorsport | 10 | 0 | 0 | 0 | 0 | 13 | 20th | 0.00 | 2.58
row 3 : 2005 | formula renault 2.0 italia winter series | korainen bros motorsport | 4 | 1 | 0 | 0 | 3 | 44 | 1st | 4.00 | 2.58
row 4 : 2006 | formula renault 2.0 nec | korainen bros motorsport | 12 | 0 | 0 | 1 | 2 | 149 | 11th | 1.50 | 1.45
row 5 : 2006 | eurocup formula renault 2.0 | korainen bros motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43 | 1.45
row 6 : 2006 | eurocup formula renault 2.0 | jenzer motorsport | 14 | 0 | 0 | 1 | 2 | 54 | 9th | 1.43 | 1.45
        """
    ],
    "question": "How did the driver's performance trend change from 2005 to 2006?",
    "answer": "Decreasing trend",
    "explanation": "This question requires analyzing performance metrics across seasons. The final table shows that the season_avg_performance decreased from 2.58 in 2005 to 1.45 in 2006, indicating a downward trend in the driver's performance."
    },
    "EXAMPLE_4": {
    "table_info": """
col : Rank | Bank name | Country | Total assets (US$ billion)
row 1 : 1 | DBS Bank | Singapore | 404.1
row 2 : 2 | OCBC Bank | Singapore | 351.2
row 3 : 3 | United Overseas Bank | Singapore | 277.99
row 4 : 4 | Maybank | Malaysia | 189.1
row 5 : 5 | CIMB | Malaysia | 125.3
row 6 : 6 | Public Bank Berhad | Malaysia | 102.9
row 7 : 7 | Bangkok Bank | Thailand | 101.5
row 8 : 8 | Siam Commercial Bank | Thailand | 97.7
row 9 : 9 | Kasikornbank | Thailand | 95.8
row 10 : 10 | Krung Thai Bank | Thailand | 92.3
    """,
    "chain": [
        "f_add_knowledge_column()",
        "f_group_column()",
        "f_add_inferred_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_knowledge_column(economic_zone)",
        "f_group_column(Country)",
        "f_add_inferred_column(avg_assets)",
        "END"
    ],
    "explanations": [
        "Adding economic_zone to categorize banks by their regional economic affiliations",
        "Grouping by Country to analyze banking assets by nation",
        "Adding avg_assets to calculate the average assets per bank in each country"
    ],
    "intermediate_tables": [
        """
col : Rank | Bank name | Country | Total assets (US$ billion) | economic_zone
row 1 : 1 | DBS Bank | Singapore | 404.1 | ASEAN
row 2 : 2 | OCBC Bank | Singapore | 351.2 | ASEAN
row 3 : 3 | United Overseas Bank | Singapore | 277.99 | ASEAN
row 4 : 4 | Maybank | Malaysia | 189.1 | ASEAN
row 5 : 5 | CIMB | Malaysia | 125.3 | ASEAN
row 6 : 6 | Public Bank Berhad | Malaysia | 102.9 | ASEAN
row 7 : 7 | Bangkok Bank | Thailand | 101.5 | ASEAN
row 8 : 8 | Siam Commercial Bank | Thailand | 97.7 | ASEAN
row 9 : 9 | Kasikornbank | Thailand | 95.8 | ASEAN
row 10 : 10 | Krung Thai Bank | Thailand | 92.3 | ASEAN
        """,
        """
col : Country | count
row 1 : Singapore | 3
row 2 : Malaysia | 3
row 3 : Thailand | 4
        """,
        """
col : Country | count | avg_assets
row 1 : Singapore | 3 | 344.43
row 2 : Malaysia | 3 | 139.10
row 3 : Thailand | 4 | 96.83
        """
    ],
    "question": "Based on the data, which country shows the strongest banking sector in terms of average assets per bank?",
    "answer": "Singapore",
    "explanation": "This question requires analyzing the average assets per bank across different countries. The final table shows that Singapore has the highest average assets per bank at $344.43 billion, significantly higher than Malaysia ($139.10 billion) and Thailand ($96.83 billion)."
    },
    "EXAMPLE_5": {
    "table_info": """
col : no | title | original air date | viewers | top 50 ranking | scripted show ranking
row 1 : 112 | nice is different than good | february 15, 2010 | 479100 | 12 | 3
row 2 : 113 | being alive | february 22, 2010 | 477080 | 8 | 1
row 3 : 114 | never judge a lady by her lover | march 1, 2010 | 447990 | 9 | 1
row 4 : 115 | the god-why-don't-you-love-me blues | march 8, 2010 | 471200 | 14 | 4
row 5 : 116 | everybody ought to have a maid | march 15, 2010 | 448490 | 15 | 5
row 6 : 117 | don't walk on the grass | march 22, 2010 | 452490 | 12 | 4
row 7 : 118 | careful the things you say | march 29, 2010 | 413820 | 13 | 5
row 8 : 119 | the coffee cup | april 12, 2010 | 397830 | 23 | 8
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_select_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(viewer_change)",
        "f_select_column(no, title, original air date, viewers, viewer_change)",
        "f_sort_column(viewers)",
        "END"
    ],
    "explanations": [
        "Adding viewer_change to track episode-to-episode changes in viewership",
        "Selecting only the relevant columns for viewership analysis",
        "Sorting by viewers to identify highest and lowest performing episodes"
    ],
    "intermediate_tables": [
        """
col : no | title | original air date | viewers | top 50 ranking | scripted show ranking | viewer_change
row 1 : 112 | nice is different than good | february 15, 2010 | 479100 | 12 | 3 | N/A
row 2 : 113 | being alive | february 22, 2010 | 477080 | 8 | 1 | -2020
row 3 : 114 | never judge a lady by her lover | march 1, 2010 | 447990 | 9 | 1 | -29090
row 4 : 115 | the god-why-don't-you-love-me blues | march 8, 2010 | 471200 | 14 | 4 | +23210
row 5 : 116 | everybody ought to have a maid | march 15, 2010 | 448490 | 15 | 5 | -22710
row 6 : 117 | don't walk on the grass | march 22, 2010 | 452490 | 12 | 4 | +4000
row 7 : 118 | careful the things you say | march 29, 2010 | 413820 | 13 | 5 | -38670
row 8 : 119 | the coffee cup | april 12, 2010 | 397830 | 23 | 8 | -15990
        """,
        """
col : no | title | original air date | viewers | viewer_change
row 1 : 112 | nice is different than good | february 15, 2010 | 479100 | N/A
row 2 : 113 | being alive | february 22, 2010 | 477080 | -2020
row 3 : 114 | never judge a lady by her lover | march 1, 2010 | 447990 | -29090
row 4 : 115 | the god-why-don't-you-love-me blues | march 8, 2010 | 471200 | +23210
row 5 : 116 | everybody ought to have a maid | march 15, 2010 | 448490 | -22710
row 6 : 117 | don't walk on the grass | march 22, 2010 | 452490 | +4000
row 7 : 118 | careful the things you say | march 29, 2010 | 413820 | -38670
row 8 : 119 | the coffee cup | april 12, 2010 | 397830 | -15990
        """,
        """
col : no | title | original air date | viewers | viewer_change
row 1 : 119 | the coffee cup | april 12, 2010 | 397830 | -15990
row 2 : 118 | careful the things you say | march 29, 2010 | 413820 | -38670
row 3 : 114 | never judge a lady by her lover | march 1, 2010 | 447990 | -29090
row 4 : 116 | everybody ought to have a maid | march 15, 2010 | 448490 | -22710
row 5 : 117 | don't walk on the grass | march 22, 2010 | 452490 | +4000
row 6 : 115 | the god-why-don't-you-love-me blues | march 8, 2010 | 471200 | +23210
row 7 : 113 | being alive | february 22, 2010 | 477080 | -2020
row 8 : 112 | nice is different than good | february 15, 2010 | 479100 | N/A
        """
    ],
    "question": "Based on the viewership data from February to April 2010, what is the overall trend in the show's popularity?",
    "answer": "Decreasing trend",
    "explanation": "This question requires analyzing the viewership numbers over time. The table shows a clear declining trend from the first episode (479,100 viewers) to the last episode (397,830 viewers), with some fluctuations in between but an overall decrease of 81,270 viewers over the period."
    },
    "EXAMPLE_6": {
    "table_info": """
col : season | team | races | wins | poles | podiums | points | position
row 1 : 2005 | Formula One | 19 | 7 | 9 | 13 | 136 | 3rd
row 2 : 2006 | Formula One | 18 | 5 | 6 | 11 | 121 | 2nd
row 3 : 2007 | Formula One | 17 | 4 | 3 | 12 | 109 | 1st
row 4 : 2008 | Formula One | 18 | 5 | 2 | 10 | 98 | 2nd
row 5 : 2009 | Formula One | 17 | 2 | 1 | 5 | 76 | 5th
row 6 : 2010 | Formula One | 19 | 3 | 0 | 7 | 84 | 4th
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_group_column()",
        "f_add_knowledge_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(win_rate)",
        "f_group_column(season)",
        "f_add_knowledge_column(career_stage)",
        "END"
    ],
    "explanations": [
        "Adding win_rate to measure performance efficiency in each season",
        "Grouping by season to analyze performance changes over time",
        "Adding career_stage to categorize different periods of the driver's career"
    ],
    "intermediate_tables": [
        """
col : season | team | races | wins | poles | podiums | points | position | win_rate
row 1 : 2005 | Formula One | 19 | 7 | 9 | 13 | 136 | 3rd | 0.37
row 2 : 2006 | Formula One | 18 | 5 | 6 | 11 | 121 | 2nd | 0.28
row 3 : 2007 | Formula One | 17 | 4 | 3 | 12 | 109 | 1st | 0.24
row 4 : 2008 | Formula One | 18 | 5 | 2 | 10 | 98 | 2nd | 0.28
row 5 : 2009 | Formula One | 17 | 2 | 1 | 5 | 76 | 5th | 0.12
row 6 : 2010 | Formula One | 19 | 3 | 0 | 7 | 84 | 4th | 0.16
        """,
        """
col : season | count
row 1 : 2005 | 1
row 2 : 2006 | 1
row 3 : 2007 | 1
row 4 : 2008 | 1
row 5 : 2009 | 1
row 6 : 2010 | 1
        """,
        """
col : season | team | races | wins | poles | podiums | points | position | win_rate | career_stage
row 1 : 2005 | Formula One | 19 | 7 | 9 | 13 | 136 | 3rd | 0.37 | Early
row 2 : 2006 | Formula One | 18 | 5 | 6 | 11 | 121 | 2nd | 0.28 | Mid
row 3 : 2007 | Formula One | 17 | 4 | 3 | 12 | 109 | 1st | 0.24 | Mid
row 4 : 2008 | Formula One | 18 | 5 | 2 | 10 | 98 | 2nd | 0.28 | Mid
row 5 : 2009 | Formula One | 17 | 2 | 1 | 5 | 76 | 5th | 0.12 | Late
row 6 : 2010 | Formula One | 19 | 3 | 0 | 7 | 84 | 4th | 0.16 | Late
        """
    ],
    "question": "What is the trend of the win rate for the driver's career stage?",
    "answer": "Decreasing trend",
    "explanation": "This question requires analyzing the trend of the win rate for the driver's career stage. The final table shows that the win rate is decreasing from 0.37 to 0.16, indicating a decreasing trend."
    },
    "EXAMPLE_7": {
    "table_info": """
col : student_id | name | age | gender | math_score | reading_score | writing_score
row 1 : 1 | John | 15 | M | 85 | 92 | 78
row 2 : 2 | Jane | 16 | F | 90 | 88 | 85
row 3 : 3 | Mike | 14 | M | 78 | 85 | 82
row 4 : 4 | Emily | 15 | F | 88 | 90 | 87
row 5 : 5 | Chris | 16 | M | 92 | 89 | 90
row 6 : 6 | Sarah | 14 | F | 80 | 82 | 79
row 7 : 7 | David | 15 | M | 87 | 88 | 86
row 8 : 8 | Olivia | 16 | F | 91 | 87 | 89
row 9 : 9 | Daniel | 14 | M | 75 | 80 | 77
row 10 : 10 | Sophia | 15 | F | 86 | 89 | 88
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(average_score)",
        "f_add_inferred_column(grade)",
        "f_sort_column(average_score)",
        "END"
    ],
    "explanations": [
        "Adding average_score to calculate the overall performance of each student",
        "Adding grade to categorize students based on their average score",
        "Sorting by average_score to identify top-performing students"
    ],
    "intermediate_tables": [
        """
col : student_id | name | age | gender | math_score | reading_score | writing_score | average_score
row 1 : 1 | John | 15 | M | 85 | 92 | 78 | 85.00
row 2 : 2 | Jane | 16 | F | 90 | 88 | 85 | 87.67
row 3 : 3 | Mike | 14 | M | 78 | 85 | 82 | 81.67
row 4 : 4 | Emily | 15 | F | 88 | 90 | 87 | 88.33
row 5 : 5 | Chris | 16 | M | 92 | 89 | 90 | 90.33
row 6 : 6 | Sarah | 14 | F | 80 | 82 | 79 | 80.33
row 7 : 7 | David | 15 | M | 87 | 88 | 86 | 87.00
row 8 : 8 | Olivia | 16 | F | 91 | 87 | 89 | 89.00
row 9 : 9 | Daniel | 14 | M | 75 | 80 | 77 | 77.33
row 10 : 10 | Sophia | 15 | F | 86 | 89 | 88 | 87.67
        """,
        """
col : student_id | name | age | gender | math_score | reading_score | writing_score | average_score | grade
row 1 : 1 | John | 15 | M | 85 | 92 | 78 | 85.00 | B
row 2 : 2 | Jane | 16 | F | 90 | 88 | 85 | 87.67 | B
row 3 : 3 | Mike | 14 | M | 78 | 85 | 82 | 81.67 | C
row 4 : 4 | Emily | 15 | F | 88 | 90 | 87 | 88.33 | B
row 5 : 5 | Chris | 16 | M | 92 | 89 | 90 | 90.33 | A
row 6 : 6 | Sarah | 14 | F | 80 | 82 | 79 | 80.33 | B
row 7 : 7 | David | 15 | M | 87 | 88 | 86 | 87.00 | B
row 8 : 8 | Olivia | 16 | F | 91 | 87 | 89 | 89.00 | A
row 9 : 9 | Daniel | 14 | M | 75 | 80 | 77 | 77.33 | C
row 10 : 10 | Sophia | 15 | F | 86 | 89 | 88 | 87.67 | B
        """,
        """
col : student_id | name | age | gender | math_score | reading_score | writing_score | average_score | grade
row 1 : 9 | Daniel | 14 | M | 75 | 80 | 77 | 77.33 | C
row 2 : 6 | Sarah | 14 | F | 80 | 82 | 79 | 80.33 | B
row 3 : 3 | Mike | 14 | M | 78 | 85 | 82 | 81.67 | C
row 4 : 1 | John | 15 | M | 85 | 92 | 78 | 85.00 | B
row 5 : 7 | David | 15 | M | 87 | 88 | 86 | 87.00 | B
row 6 : 10 | Sophia | 15 | F | 86 | 89 | 88 | 87.67 | B
row 7 : 4 | Emily | 15 | F | 88 | 90 | 87 | 88.33 | B
row 8 : 2 | Jane | 16 | F | 90 | 88 | 85 | 87.67 | B
row 9 : 8 | Olivia | 16 | F | 91 | 87 | 89 | 89.00 | A
row 10 : 5 | Chris | 16 | M | 92 | 89 | 90 | 90.33 | A
        """
    ],
    "question": "What is the average score for the B grade students?",
    "answer": "81.67",
    "explanation": "This question requires analyzing the average score for the B grade students. The final table shows that the average score for the B grade students is 81.67."
    },
    "EXAMPLE_8": {
    "table_info": """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65%
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58%
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72%
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61%
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70%
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48%
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52%
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_knowledge_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(engagement_score)",
        "f_add_knowledge_column(page_type)",
        "f_sort_column(engagement_score)",
        "END"
    ],
    "explanations": [
        "Adding engagement_score to quantify user engagement based on time on page and bounce rate",
        "Adding page_type to categorize pages by their function in the user journey",
        "Sorting by engagement_score to identify highest engaging pages"
    ],
    "intermediate_tables": [
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0
        """,
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score | page_type
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6 | Navigational
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3 | Commercial
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2 | Informational
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6 | Informational
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0 | Transactional
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3 | Transactional
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0 | Transactional
        """,
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score | page_type
row 1 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6 | Informational
row 2 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0 | Transactional
row 3 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6 | Navigational
row 4 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2 | Informational
row 5 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3 | Commercial
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3 | Transactional
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0 | Transactional
        """
    ],
    "question": "What is the engagement score for the Commercial page?",
    "answer": "8.3",
    "explanation": "This question requires analyzing the engagement score for the Commercial page. The final table shows that the engagement score for the Commercial page is 8.3."
    },
    "EXAMPLE_9": {
    "table_info": """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65%
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58%
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72%
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61%
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70%
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48%
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52%
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_knowledge_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(engagement_score)",
        "f_add_knowledge_column(page_type)",
        "f_sort_column(engagement_score)",
        "END"
    ],
    "explanations": [
        "Adding engagement_score to quantify user engagement based on time on page and bounce rate",
        "Adding page_type to categorize pages by their function in the user journey",
        "Sorting by engagement_score to identify highest engaging pages"
    ],
    "intermediate_tables": [
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0
        """,
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score | page_type
row 1 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6 | Navigational
row 2 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3 | Commercial
row 3 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2 | Informational
row 4 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6 | Informational
row 5 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0 | Transactional
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3 | Transactional
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0 | Transactional
        """,
        """
col : page | visitors | bounce_rate | avg_time_on_page | conversion_rate | mobile_traffic | engagement_score | page_type
row 1 : About Us | 5630 | 51% | 1:48 | 1.5% | 61% | 2.6 | Informational
row 2 : Contact | 4280 | 38% | 2:10 | 3.2% | 70% | 4.0 | Transactional
row 3 : Homepage | 25420 | 32% | 2:45 | 4.2% | 65% | 5.6 | Navigational
row 4 : Blog | 12840 | 45% | 4:22 | 2.1% | 72% | 7.2 | Informational
row 5 : Products | 18750 | 28% | 3:50 | 5.8% | 58% | 8.3 | Commercial
row 6 : Support | 8960 | 22% | 5:15 | 6.5% | 48% | 12.3 | Transactional
row 7 : Checkout | 3850 | 18% | 6:30 | 72.5% | 52% | 16.0 | Transactional
        """
    ],
    "question": "What is the average literacy rate in districts with a population density greater than 300 persons per km²?",
    "answer": "82.7",
    "explanation": "This question requires calculating the average literacy rate for districts with population density greater than 300 persons per km². First, we need to identify these districts: Balasore (609), Bhadrak (601), and Cuttack (666). Then, we calculate the average literacy rate: (80.66 + 83.25 + 84.2) / 3 = 82.7."
    },
    "EXAMPLE_10": {
    "table_info": """
col : athlete | final | lane | semi | quart | heat
row 1 : marie - josé pérec ( fra ) | 48.25 | 3 | 49.19 | 51.0 | 51.82
row 2 : cathy freeman ( aus ) | 48.63 | 4 | 50.32 | 50.43 | 51.99
row 3 : falilat ogunkoya ( ngr ) | 49.1 | 5 | 49.57 | 50.65 | 52.65
row 4 : pauline davis ( bah ) | 49.28 | 2 | 49.85 | 51.08 | 51.0
row 5 : jearl miles ( usa ) | 49.55 | 8 | 50.21 | 50.84 | 51.96
row 6 : fatima yusuf ( ngr ) | 49.77 | 6 | 50.36 | 51.27 | 52.25
row 7 : sandie richards ( jam ) | 50.45 | 7 | 50.74 | 51.22 | 51.79
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(improvement_from_heat)",
        "f_add_inferred_column(consistency_score)",
        "f_sort_column(improvement_from_heat)",
        "END"
    ],
    "explanations": [
        "Adding improvement_from_heat to measure progression from first to final race",
        "Adding consistency_score to evaluate performance stability across races",
        "Sorting by improvement_from_heat to identify athletes with greatest progress"
    ],
    "intermediate_tables": [
        """
col : athlete | final | lane | semi | quart | heat | improvement_from_heat
row 1 : marie - josé pérec ( fra ) | 48.25 | 3 | 49.19 | 51.0 | 51.82 | 3.57
row 2 : cathy freeman ( aus ) | 48.63 | 4 | 50.32 | 50.43 | 51.99 | 3.36
row 3 : falilat ogunkoya ( ngr ) | 49.1 | 5 | 49.57 | 50.65 | 52.65 | 3.55
row 4 : pauline davis ( bah ) | 49.28 | 2 | 49.85 | 51.08 | 51.0 | 1.72
row 5 : jearl miles ( usa ) | 49.55 | 8 | 50.21 | 50.84 | 51.96 | 2.41
row 6 : fatima yusuf ( ngr ) | 49.77 | 6 | 50.36 | 51.27 | 52.25 | 2.48
row 7 : sandie richards ( jam ) | 50.45 | 7 | 50.74 | 51.22 | 51.79 | 1.34
        """,
        """
col : athlete | final | lane | semi | quart | heat | improvement_from_heat | consistency_score
row 1 : marie - josé pérec ( fra ) | 48.25 | 3 | 49.19 | 51.0 | 51.82 | 3.57 | 8.8
row 2 : cathy freeman ( aus ) | 48.63 | 4 | 50.32 | 50.43 | 51.99 | 3.36 | 7.6
row 3 : falilat ogunkoya ( ngr ) | 49.1 | 5 | 49.57 | 50.65 | 52.65 | 3.55 | 8.2
row 4 : pauline davis ( bah ) | 49.28 | 2 | 49.85 | 51.08 | 51.0 | 1.72 | 6.5
row 5 : jearl miles ( usa ) | 49.55 | 8 | 50.21 | 50.84 | 51.96 | 2.41 | 7.2
row 6 : fatima yusuf ( ngr ) | 49.77 | 6 | 50.36 | 51.27 | 52.25 | 2.48 | 7.0
row 7 : sandie richards ( jam ) | 50.45 | 7 | 50.74 | 51.22 | 51.79 | 1.34 | 6.2
        """,
        """
col : athlete | final | lane | semi | quart | heat | improvement_from_heat | consistency_score
row 1 : sandie richards ( jam ) | 50.45 | 7 | 50.74 | 51.22 | 51.79 | 1.34 | 6.2
row 2 : pauline davis ( bah ) | 49.28 | 2 | 49.85 | 51.08 | 51.0 | 1.72 | 6.5
row 3 : jearl miles ( usa ) | 49.55 | 8 | 50.21 | 50.84 | 51.96 | 2.41 | 7.2
row 4 : fatima yusuf ( ngr ) | 49.77 | 6 | 50.36 | 51.27 | 52.25 | 2.48 | 7.0
row 5 : cathy freeman ( aus ) | 48.63 | 4 | 50.32 | 50.43 | 51.99 | 3.36 | 7.6
row 6 : falilat ogunkoya ( ngr ) | 49.1 | 5 | 49.57 | 50.65 | 52.65 | 3.55 | 8.2
row 7 : marie - josé pérec ( fra ) | 48.25 | 3 | 49.19 | 51.0 | 51.82 | 3.57 | 8.8
        """
    ],
    "question": "What is the mean of the 'final' times for all athletes?",
    "answer": "49.29",
    "explanation": "This question requires calculating the average of the final race times for all athletes. Adding the final times (48.25 + 48.63 + 49.1 + 49.28 + 49.55 + 49.77 + 50.45) gives 345.03. Dividing by the number of athletes (7) results in a mean final time of 49.29 seconds."
    },
    "EXAMPLE_11": {
    "table_info": """
col : city | pm2.5_level | co2_emissions | air_quality_index | green_space_percent | population_density | industry_count
row 1 : Metropolis | 35.2 | 8.5 | 125 | 12.5 | 5280 | 42
row 2 : Riverside | 28.7 | 6.2 | 105 | 18.4 | 3150 | 28
row 3 : Oakville | 15.3 | 4.1 | 62 | 31.2 | 1980 | 12
row 4 : Steeltown | 42.6 | 9.8 | 145 | 8.3 | 4320 | 56
row 5 : Lakeside | 18.9 | 5.3 | 78 | 26.7 | 2420 | 18
row 6 : Harborview | 32.1 | 7.4 | 118 | 15.8 | 4680 | 35
row 7 : Greendale | 12.8 | 3.5 | 52 | 38.5 | 1540 | 8
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_group_column()",
        "f_add_knowledge_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(pollution_index)",
        "f_group_column(pollution_index)",
        "f_add_knowledge_column(region)",
        "END"
    ],
    "explanations": [
        "Adding pollution_index to create a composite score based on pm2.5, co2, and air quality",
        "Grouping by pollution_index to categorize cities by their pollution levels",
        "Adding region information to analyze geographic patterns in pollution"
    ],
    "intermediate_tables": [
        """
col : city | pm2.5_level | co2_emissions | air_quality_index | green_space_percent | population_density | industry_count | pollution_index
row 1 : Metropolis | 35.2 | 8.5 | 125 | 12.5 | 5280 | 42 | High
row 2 : Riverside | 28.7 | 6.2 | 105 | 18.4 | 3150 | 28 | Medium
row 3 : Oakville | 15.3 | 4.1 | 62 | 31.2 | 1980 | 12 | Low
row 4 : Steeltown | 42.6 | 9.8 | 145 | 8.3 | 4320 | 56 | High
row 5 : Lakeside | 18.9 | 5.3 | 78 | 26.7 | 2420 | 18 | Low
row 6 : Harborview | 32.1 | 7.4 | 118 | 15.8 | 4680 | 35 | Medium
row 7 : Greendale | 12.8 | 3.5 | 52 | 38.5 | 1540 | 8 | Low
        """,
        """
col : pollution_index | count
row 1 : High | 2
row 2 : Medium | 2
row 3 : Low | 3
        """,
        """
col : pollution_index | count | region
row 1 : High | 2 | Industrial Belt
row 2 : Medium | 2 | Urban Center
row 3 : Low | 3 | Green Zone
        """
    ],
    "question": "How many cities are in the Industrial Belt region?",
    "answer": "2",
    "explanation": "This question requires counting the number of cities in the Industrial Belt region. The final table shows that there are 2 cities in the Industrial Belt region: Metropolis and Steeltown."
    },
    "EXAMPLE_12": {
    "table_info": """
col : country | population | gdp_billions | energy_consumption | renewable_percent | co2_emissions | energy_efficiency_score
row 1 : Northland | 25.4 | 1250 | 325 | 42.5 | 180 | 7.8
row 2 : Eastonia | 68.2 | 2180 | 845 | 28.3 | 520 | 6.2
row 3 : Westeria | 42.1 | 1820 | 640 | 35.6 | 310 | 7.1
row 4 : Southbay | 94.5 | 3540 | 1260 | 18.9 | 860 | 5.5
row 5 : Centralius | 36.8 | 1640 | 520 | 31.2 | 280 | 6.9
row 6 : Islandia | 8.3 | 580 | 105 | 65.8 | 48 | 8.9
row 7 : Mountainia | 15.7 | 920 | 210 | 53.4 | 95 | 8.2
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_select_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(energy_per_capita)",
        "f_add_inferred_column(emissions_per_gdp)",
        "f_select_column(country, energy_per_capita, renewable_percent, emissions_per_gdp, energy_efficiency_score)",
        "END"
    ],
    "explanations": [
        "Adding energy_per_capita to normalize energy consumption by population",
        "Adding emissions_per_gdp to measure carbon intensity of economic output",
        "Selecting only the most relevant columns for energy efficiency analysis"
    ],
    "intermediate_tables": [
        """
col : country | population | gdp_billions | energy_consumption | renewable_percent | co2_emissions | energy_efficiency_score | energy_per_capita
row 1 : Northland | 25.4 | 1250 | 325 | 42.5 | 180 | 7.8 | 12.8
row 2 : Eastonia | 68.2 | 2180 | 845 | 28.3 | 520 | 6.2 | 12.4
row 3 : Westeria | 42.1 | 1820 | 640 | 35.6 | 310 | 7.1 | 15.2
row 4 : Southbay | 94.5 | 3540 | 1260 | 18.9 | 860 | 5.5 | 13.3
row 5 : Centralius | 36.8 | 1640 | 520 | 31.2 | 280 | 6.9 | 14.1
row 6 : Islandia | 8.3 | 580 | 105 | 65.8 | 48 | 8.9 | 12.7
row 7 : Mountainia | 15.7 | 920 | 210 | 53.4 | 95 | 8.2 | 13.4
        """,
        """
col : country | population | gdp_billions | energy_consumption | renewable_percent | co2_emissions | energy_efficiency_score | energy_per_capita | emissions_per_gdp
row 1 : Northland | 25.4 | 1250 | 325 | 42.5 | 180 | 7.8 | 12.8 | 0.144
row 2 : Eastonia | 68.2 | 2180 | 845 | 28.3 | 520 | 6.2 | 12.4 | 0.239
row 3 : Westeria | 42.1 | 1820 | 640 | 35.6 | 310 | 7.1 | 15.2 | 0.170
row 4 : Southbay | 94.5 | 3540 | 1260 | 18.9 | 860 | 5.5 | 13.3 | 0.243
row 5 : Centralius | 36.8 | 1640 | 520 | 31.2 | 280 | 6.9 | 14.1 | 0.171
row 6 : Islandia | 8.3 | 580 | 105 | 65.8 | 48 | 8.9 | 12.7 | 0.083
row 7 : Mountainia | 15.7 | 920 | 210 | 53.4 | 95 | 8.2 | 13.4 | 0.103
        """,
        """
col : country | energy_per_capita | renewable_percent | emissions_per_gdp | energy_efficiency_score
row 1 : Northland | 12.8 | 42.5 | 0.144 | 7.8
row 2 : Eastonia | 12.4 | 28.3 | 0.239 | 6.2
row 3 : Westeria | 15.2 | 35.6 | 0.170 | 7.1
row 4 : Southbay | 13.3 | 18.9 | 0.243 | 5.5
row 5 : Centralius | 14.1 | 31.2 | 0.171 | 6.9
row 6 : Islandia | 12.7 | 65.8 | 0.083 | 8.9
row 7 : Mountainia | 13.4 | 53.4 | 0.103 | 8.2
        """
    ],
    "question": "What is the average energy efficiency score for countries with renewable energy percentage above 40%?",
    "answer": "8.3",
    "explanation": "This question requires calculating the average energy efficiency score for countries with renewable energy percentage above 40%. First, we identify these countries: Northland (42.5%), Islandia (65.8%), and Mountainia (53.4%). Then, we calculate the average energy efficiency score: (7.8 + 8.9 + 8.2) / 3 = 8.3."
    },
    "EXAMPLE_13": {
    "table_info": """
col : year | company | revenue_millions | profit_millions | market_share | employees | r_and_d_budget_millions
row 1 : 2017 | TechInnovate | 425 | 32 | 5.2% | 1850 | 42
row 2 : 2018 | TechInnovate | 512 | 45 | 6.8% | 2100 | 58
row 3 : 2019 | TechInnovate | 645 | 78 | 8.5% | 2450 | 76
row 4 : 2020 | TechInnovate | 780 | 95 | 10.2% | 2780 | 92
row 5 : 2021 | TechInnovate | 968 | 124 | 12.6% | 3150 | 115
row 6 : 2022 | TechInnovate | 1240 | 168 | 15.8% | 3580 | 145
row 7 : 2023 | TechInnovate | 1580 | 225 | 19.5% | 4200 | 185
    """,
    "chain": [
        "f_add_inferred_column()",
        "f_add_inferred_column()",
        "f_sort_column()",
        "END"
    ],
    "filled_chain": [
        "f_add_inferred_column(profit_margin)",
        "f_add_inferred_column(annual_growth_rate)",
        "f_sort_column(year)",
        "END"
    ],
    "explanations": [
        "Adding profit_margin to calculate the percentage of revenue that translates to profit",
        "Adding annual_growth_rate to measure year-over-year revenue growth",
        "Sorting by year to analyze chronological trends in company performance"
    ],
    "intermediate_tables": [
        """
col : year | company | revenue_millions | profit_millions | market_share | employees | r_and_d_budget_millions | profit_margin
row 1 : 2017 | TechInnovate | 425 | 32 | 5.2% | 1850 | 42 | 7.5%
row 2 : 2018 | TechInnovate | 512 | 45 | 6.8% | 2100 | 58 | 8.8%
row 3 : 2019 | TechInnovate | 645 | 78 | 8.5% | 2450 | 76 | 12.1%
row 4 : 2020 | TechInnovate | 780 | 95 | 10.2% | 2780 | 92 | 12.2%
row 5 : 2021 | TechInnovate | 968 | 124 | 12.6% | 3150 | 115 | 12.8%
row 6 : 2022 | TechInnovate | 1240 | 168 | 15.8% | 3580 | 145 | 13.5%
row 7 : 2023 | TechInnovate | 1580 | 225 | 19.5% | 4200 | 185 | 14.2%
        """,
        """
col : year | company | revenue_millions | profit_millions | market_share | employees | r_and_d_budget_millions | profit_margin | annual_growth_rate
row 1 : 2017 | TechInnovate | 425 | 32 | 5.2% | 1850 | 42 | 7.5% | N/A
row 2 : 2018 | TechInnovate | 512 | 45 | 6.8% | 2100 | 58 | 8.8% | 20.5%
row 3 : 2019 | TechInnovate | 645 | 78 | 8.5% | 2450 | 76 | 12.1% | 26.0%
row 4 : 2020 | TechInnovate | 780 | 95 | 10.2% | 2780 | 92 | 12.2% | 20.9%
row 5 : 2021 | TechInnovate | 968 | 124 | 12.6% | 3150 | 115 | 12.8% | 24.1%
row 6 : 2022 | TechInnovate | 1240 | 168 | 15.8% | 3580 | 145 | 13.5% | 28.1%
row 7 : 2023 | TechInnovate | 1580 | 225 | 19.5% | 4200 | 185 | 14.2% | 27.4%
        """,
        """
col : year | company | revenue_millions | profit_millions | market_share | employees | r_and_d_budget_millions | profit_margin | annual_growth_rate
row 1 : 2017 | TechInnovate | 425 | 32 | 5.2% | 1850 | 42 | 7.5% | N/A
row 2 : 2018 | TechInnovate | 512 | 45 | 6.8% | 2100 | 58 | 8.8% | 20.5%
row 3 : 2019 | TechInnovate | 645 | 78 | 8.5% | 2450 | 76 | 12.1% | 26.0%
row 4 : 2020 | TechInnovate | 780 | 95 | 10.2% | 2780 | 92 | 12.2% | 20.9%
row 5 : 2021 | TechInnovate | 968 | 124 | 12.6% | 3150 | 115 | 12.8% | 24.1%
row 6 : 2022 | TechInnovate | 1240 | 168 | 15.8% | 3580 | 145 | 13.5% | 28.1%
row 7 : 2023 | TechInnovate | 1580 | 225 | 19.5% | 4200 | 185 | 14.2% | 27.4%
        """
    ],
    "question": "Based on the data from 2017 to 2023, what is the overall trend in TechInnovate's profit margin?",
    "answer": "Increasing trend",
    "explanation": "This question requires analyzing the profit margin trend over time. The final table shows that profit margin has consistently increased from 7.5% in 2017 to 14.2% in 2023, demonstrating a clear upward trend in the company's profitability."
    }
}