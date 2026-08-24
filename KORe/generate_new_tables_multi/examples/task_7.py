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


task_7_EXAMPLES_multi = {
"EXAMPLE_0": {
            "table_info": """
table_name: texture_types
col : texture_type_id | texture_name | texture_description
row 1 : 0 | diffuse | Diffuse texture maps
row 2 : 1 | normal | Normal maps

table_name: texture_format_usage
col : usage_id | texture_type_id | format_id | project_id | usage_date
row 1 : 0 | 1 | 1 | 1001 | 2023-05-01
row 2 : 1 | 0 | 2 | 1002 | 2023-05-02

foreign_key: texture_type_id
""",
"question": "What are the names of the texture types that have the earliest or latest usage dates across all projects, listed in alphabetical order?",
"answer": "diffuse, normal",
"explanation": "To find texture types with earliest or latest usage dates, I need to join the texture_types and texture_format_usage tables to connect texture names with their usage dates. Then I'll select only the relevant columns (texture_name and usage_date), add a column to identify whether each date is the earliest or latest, filter to keep only rows with the earliest or latest dates, and finally sort the texture names alphabetically to get the answer: 'diffuse, normal'.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(texture_types.texture_type_id, texture_format_usage.texture_type_id, inner)",
    "f_select_column(texture_name, usage_date)",
    "f_add_inferred_column(date_extremity)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(texture_name)",
    "END"
],
"explanations": [
    "Joining texture_types and texture_format_usage tables to connect texture names with their usage dates",
    "Selecting only the relevant columns needed for analysis: texture_name and usage_date",
    "Adding a column to identify whether each date is the earliest (min) or latest (max) usage date",
    "Filtering to keep only rows with the earliest or latest usage dates, which are row 1 and row 2 respectively",
    "Sorting the texture names alphabetically as requested in the question"
],
"intermediate_tables": [
    """
col : texture_type_id | texture_name | texture_description | usage_id | texture_format_usage.texture_type_id | format_id | project_id | usage_date
row 1 : 0 | diffuse | Diffuse texture maps | 1 | 1 | 1 | 1001 | 2023-05-01
row 2 : 1 | normal | Normal maps | 0 | 0 | 2 | 1002 | 2023-05-02
    """,
    """
col : texture_name | usage_date
row 1 : diffuse | 2023-05-02
row 2 : normal | 2023-05-01
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : diffuse | 2023-05-02 | max
row 2 : normal | 2023-05-01 | min
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : diffuse | 2023-05-02 | max
row 2 : normal | 2023-05-01 | min
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : diffuse | 2023-05-02 | max
row 2 : normal | 2023-05-01 | min
    """
]
},
"EXAMPLE_1": {
            "table_info": """
table_name: issue_quality_metrics
col : metric_id | issue_id | readability_score | clarity_score | conciseness_score

table_name: issue_tagging
col : tag_id | issue_id | tag_name

foreign_key: 
""",
"question": "What is the maximum cumulative average readability score for issues tagged with 'specific_tag', grouped by clarity and conciseness scores?",
"answer": "None",
"explanation": "To find the maximum cumulative average readability score for issues tagged with 'specific_tag', I need to join the issue_quality_metrics and issue_tagging tables to connect issues with their tags. I'll then filter for issues with the 'specific_tag' tag. Since the tables don't contain any issues with 'specific_tag' (only 'bug' and 'feature' tags exist), the result is 'None'.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(issue_quality_metrics.issue_id, issue_tagging.issue_id, inner)",
    "f_select_row(row 1)",
    "END"
],
"explanations": [
    "Joining issue_quality_metrics with issue_tagging to connect issues with their tags",
    "Filtering to include only issues tagged with 'specific_tag'",
],
"intermediate_tables": [
    """
col : metric_id | issue_id | readability_score | clarity_score | conciseness_score | tag_id | issue_tagging.issue_id | tag_name
    """,
    """
col : metric_id | issue_id | readability_score | clarity_score | conciseness_score | tag_id | issue_tagging.issue_id | tag_name
    """
]
},
"EXAMPLE_2": {
            "table_info": """
table_name: players
col : player_id | player_name | position | team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration
row 1 : 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31
row 2 : 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31

table_name: pitchers
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage
row 1 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5
row 2 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0

foreign_keys: 
""",
"question": "What are the names of the top three pitchers for each team who are still active and will be playing beyond 2024?",
"answer": "Chris Bassitt, Max Scherzer",
"explanation": "To identify the top three pitchers per team who are active and have contracts beyond 2024, I need to join the players and pitchers tables. First, I'll select the pitchers table to get performance metrics. Then I'll join with the players table to get contract and status information. Next, I'll filter for active players with contracts extending beyond 2024, rank pitchers within each team based on ERA, WHIP, and BAA, and select the top three per team. The result includes Chris Bassitt and Max Scherzer.",
"chain": [
    "f_stitch_tables()",
    "f_select_row()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(pitchers.pitcher_name, players.player_name, inner)",
    "f_select_row(row 1, row 2)",
    "f_add_inferred_column(pitcher_rank)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(pitcher_name)",
    "END"
],
"explanations": [
    "Joining pitchers with players table to connect performance metrics with contract and status information",
    "Filtering to include only active players with contracts extending beyond 2024, which are row 1 and row 2",
    "Adding a column to rank pitchers within each team based on performance metrics",
    "Selecting only the top three pitchers from each team based on their rank, which are row 1 and row 2",
    "Sorting the results by pitcher name for clear presentation"
],
"intermediate_tables": [
    """
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage | player_id | players.player_name | position | players.team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration
row 1 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5 | 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31
row 2 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0 | 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31
    """,
    """
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage | player_id | players.player_name | position | players.team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration
row 1 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5 | 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31
row 2 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0 | 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31
    """,
    """
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage | player_id | players.player_name | position | players.team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration | pitcher_rank
row 1 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5 | 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31 | 1
row 2 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0 | 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31 | 2
    """,
    """
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage | player_id | players.player_name | position | players.team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration | pitcher_rank
row 1 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5 | 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31 | 1
row 2 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0 | 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31 | 2
    """,
    """
col : pitcher_id | pitcher_name | team | ERA | WHIP | BAA | pitching_hand | pitch_types | strikeouts_per_9_innings | walks_per_9_innings | hits_per_9_innings | home_runs_per_9_innings | ground_ball_percentage | fly_ball_percentage | strikeout_percentage | walk_percentage | player_id | players.player_name | position | players.team | date_joined | status | player_number | date_of_birth | height | weight | batting_hand | throwing_hand | salary | contract_expiration | pitcher_rank
row 1 : 1 | Chris Bassitt | Athletics | 3.5 | 1.25 | 0.23 | right | fastball,changeup,slider | 9.0 | 3.0 | 8.2 | 1.0 | 50.0 | 30.0 | 25.0 | 8.0 | 1 | Kodai Senga | Pitcher | Mariners | 2023-02-15 | active | 46 | 1992-09-20 | 6'2" | 190 lbs | right | right | 1200000 | 2026-12-31 | 1
row 2 : 0 | Max Scherzer | Mets | 3.2 | 1.1 | 0.22 | right | fastball,curveball,slider | 10.5 | 2.5 | 7.8 | 0.8 | 45.0 | 35.0 | 28.0 | 7.5 | 0 | Tylor Megill | Pitcher | Mets | 2022-03-01 | active | 45 | 1993-06-15 | 6'4" | 200 lbs | right | right | 1000000 | 2025-12-31 | 2
    """
]
},
"EXAMPLE_3": {
            "table_info": """
table_name: gacha_rewards
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha

foreign_key: 
""",
"question": "How many users have obtained more than 10 rewards, have a player level greater than 20, have more than 1000 experience points, and have spent more than 500 units of in-game currency?",
"answer": "0",
"explanation": "To find users who meet all the specified criteria, I need to analyze the gacha_rewards table. First, I'll select the relevant columns: user_id, player_level, player_experience, and currency_spent. Then I'll filter to use distinct user IDs, and add columns to count the number of rewards per user and calculate total currency spent. The result is 0 users because while there is one user with player level 20 and experience points over 1000, they only have 2 rewards and spent only 100 currency units in total, which doesn't meet the criteria of having more than 10 rewards and spending more than 500 units of currency.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_select_row()",
    "f_add_inferred_column()",
    "END"
],
"filled_chain": [
    "f_select_table(gacha_rewards)",
    "f_select_column(user_id, player_level, player_experience, currency_spent)",
    "f_select_row(row 1)",
    "f_add_inferred_column(reward_count, total_currency_spent)",
    "END"
],
"explanations": [
    "Selecting the gacha_rewards table to analyze user reward data",
    "Selecting the relevant columns needed to evaluate the criteria: user_id, player_level, player_experience, and currency_spent",
    "Filtering to use distinct user_id",
    "Adding columns to count rewards per user and calculate total currency spent per user"
],
"intermediate_tables": [
    """
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha
    """,
    """
col : user_id | player_level | player_experience | currency_spent
row 1 : 1001 | 20 | 1500.0 | 50.0
row 2 : 1001 | 20 | 1500.0 | 50.0
    """,
    """
col : user_id | player_level | player_experience | currency_spent
row 1 : 1001 | 20 | 1500.0 | 50.0
    """,
    """
col : user_id | max_player_level | max_player_experience | sum_currency_spent | count | reward_count | total_currency_spent
row 1 : 1001 | 20 | 1500.0 | 100.0 | 2 | 2 | 100.0
    """
]
},
"EXAMPLE_4": {
            "table_info": """
table_name: algorithm_tags
col : tag_id | algorithm_id | tag_name
row 1 : 0 | 1 | super-resolution
row 2 : 1 | 1 | image-processing

table_name: algorithm_ratings
col : rating_id | algorithm_id | user_id | rating | rating_date
row 1 : 0 | 1 | 1 | 4 | 2023-05-01
row 2 : 1 | 2 | 2 | 3 | 2023-05-02

foreign_key: 
""",
"question": "Gather the unique identifiers of the algorithms that have blossomed with high praise, along with the bouquet of tags that adorn them, and arrange these by the intensity of their acclaim, descending.",
"answer": "1, image-processing,super-resolution, 4.0",
"explanation": "To find algorithms with high praise and their tags, I need to join the algorithm_ratings and algorithm_tags tables. After joining these tables, I'll add a column to calculate the average rating per algorithm, filter to include only algorithms with high ratings (above 3), and sort by average rating in descending order. The result shows algorithm 1 has an average rating of 4.0 and is tagged with 'image-processing' and 'super-resolution'.",
"chain": [
    "f_stitch_tables()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(algorithm_ratings.algorithm_id, algorithm_tags.algorithm_id, inner)",
    "f_add_inferred_column(avg_rating)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(avg_rating)",
    "END"
],
"explanations": [
    "Joining algorithm_ratings with algorithm_tags to connect ratings with tag information",
    "Adding columns for average rating and a concatenated list of tags per algorithm",
    "Filtering to include only algorithms with high ratings (above 3), which are row 1 and row 2",
    "Sorting by average rating in descending order to show highest rated algorithms first"
],
"intermediate_tables": [
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing
    """,
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """,
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """,
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """
]
},
"EXAMPLE_5": {
            "table_info": """
table_name: gacha_rewards
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha

foreign_key: 
""",
"question": "**User**: I want to find out the average amount of in-game currency spent by users to obtain rewards.**Assistant**: Sure, I can help with that. Do you want to know the average for each user, or the overall average across all users?**User**: I want the overall average.**Assistant**: Got it. Is there any other specific information you need related to this query?**User**: No, that's all I need.**Assistant**: OK, I will help you translate your request into an SQL query.",
"answer": "50.0",
"explanation": "To calculate the overall average amount of in-game currency spent by users to obtain rewards, I need to analyze the currency_spent column in the gacha_rewards table. First, I'll select the gacha_rewards table to access the data, then select only the currency_spent column for analysis, and finally calculate the average of these values. The result is 50.0, which represents the overall average amount of in-game currency spent per reward.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_add_inferred_column()",
    "END"
],
"filled_chain": [
    "f_select_table(gacha_rewards)",
    "f_select_column(currency_spent)",
    "f_add_inferred_column(average_currency_spent)",
    "END"
],
"explanations": [
    "Selecting the gacha_rewards table to analyze reward data",
    "Selecting only the currency_spent column for analysis",
    "Calculating the average currency spent across all rewards"
],
"intermediate_tables": [
    """
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha
    """,
    """
col : currency_spent
row 1 : 50.0
row 2 : 50.0
    """,
    """
col : currency_spent | average_currency_spent
row 1 : 50.0 | 50.0
row 2 : 50.0 | 50.0
    """
]
}
}


task_7_EXAMPLES_single = {
"EXAMPLE_0": {
            "table_info": """
col : texture_type_id | texture_name | texture_description | usage_id | format_id | project_id | usage_date
row 1 : 1 | normal | Normal maps | 0 | 1 | 1001 | 2023-05-01
row 2 : 0 | diffuse | Diffuse texture maps | 1 | 2 | 1002 | 2023-05-02
""",
"question": "What are the names of the texture types that have the earliest or latest usage dates across all projects, listed in alphabetical order?",
"answer": "diffuse, normal",
"explanation": "To find texture types with earliest or latest usage dates, I need to analyze the data. First, I'll select the relevant columns (texture_name and usage_date), add a column to identify the earliest and latest dates, select rows with these extreme dates, and sort the results alphabetically. The earliest date is 2023-05-01 (associated with 'normal') and the latest is 2023-05-02 (associated with 'diffuse'), so the alphabetically sorted result is 'diffuse, normal'.",
"chain": [
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_select_column(texture_name, usage_date)",
    "f_add_inferred_column(date_extremity)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(texture_name)",
    "END"
],
"explanations": [
    "Selecting only the relevant columns needed for analysis: texture_name and usage_date",
    "Adding a column to identify whether each date is the earliest (min) or latest (max) usage date",
    "Filtering to keep only rows with the earliest or latest usage dates, which are row 1 and row 2",
    "Sorting the texture names alphabetically as requested in the question"
],
"intermediate_tables": [
    """
col : texture_name | usage_date
row 1 : normal | 2023-05-01
row 2 : diffuse | 2023-05-02
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : normal | 2023-05-01 | min
row 2 : diffuse | 2023-05-02 | max
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : normal | 2023-05-01 | min
row 2 : diffuse | 2023-05-02 | max
    """,
    """
col : texture_name | usage_date | date_extremity
row 1 : diffuse | 2023-05-02 | max
row 2 : normal | 2023-05-01 | min
    """
]
},
"EXAMPLE_1": {
            "table_info": """
table_name: issue_metrics_with_tags
col : metric_id | issue_id | readability_score | clarity_score | conciseness_score | tag_id | tag_name
row 1 : 1 | 101 | 8.5 | 7.0 | 9.0 | 201 | bug
row 2 : 2 | 102 | 7.5 | 8.0 | 6.5 | 202 | feature

foreign_key: 
""",
"question": "What is the maximum cumulative average readability score for issues tagged with 'specific_tag', grouped by clarity and conciseness scores?",
"answer": "None",
"explanation": "To find the maximum cumulative average readability score for issues with 'specific_tag', I need to analyze the issue_metrics_with_tags table. By grouping by tag_name, I can identify if the 'specific_tag' exists and what issues are associated with it. Since there are no issues tagged with 'specific_tag' in the table (only 'bug' and 'feature' tags exist), the result is 'None'.",
"chain": [
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_group_column(tag_name)",
    "END"
],
"explanations": [
    "Grouping by tag_name to analyze issues with 'specific_tag'",
],
"intermediate_tables": [
    """
col : tag_name | count
row 1 : bug | 1
row 2 : feature | 1
    """
]
},
"EXAMPLE_3": {
            "table_info": """
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha
""",
"question": "How many users have obtained more than 10 rewards, have a player level greater than 20, have more than 1000 experience points, and have spent more than 500 units of in-game currency?",
"answer": "0",
"explanation": "To find users who meet all the specified criteria, I need to analyze the gacha_rewards table. I'll select the relevant columns (user_id, player_level, player_experience, currency_spent), then add columns to count rewards per user and calculate total currency spent. The result is 0 users because while there is one user with player level 20 and experience points over 1000, they only have 2 rewards and spent only 100 currency units in total, which doesn't meet the criteria of having more than 10 rewards and spending more than 500 units of currency.",
"chain": [
    "f_select_column()",
    "f_add_inferred_column()",
    "f_add_inferred_column()",
    "END"
],
"filled_chain": [
    "f_select_column(user_id, player_level, player_experience, currency_spent)",
    "f_add_inferred_column(reward_count)",
    "f_add_inferred_column(total_currency_spent)",
    "END"
],
"explanations": [
    "Selecting the relevant columns needed to evaluate the criteria: user_id, player_level, player_experience, and currency_spent",
    "Adding columns to count rewards per user",
    "Adding columns to calculate total currency spent per user",
],
"intermediate_tables": [
    """
col : user_id | player_level | player_experience | currency_spent
row 1 : 1001 | 20 | 1500.0 | 50.0
row 2 : 1001 | 20 | 1500.0 | 50.0
    """,
    """
col : user_id | player_level | player_experience | currency_spent | reward_count 
row 1 : 1001 | 20 | 1500.0 | 50.0 | 2 
row 2 : 1001 | 20 | 1500.0 | 50.0 | 2 
    """,
    """
col : user_id | player_level | player_experience | currency_spent | reward_count | total_currency_spent
row 1 : 1001 | 20 | 1500.0 | 50.0 | 2 | 100.0
row 2 : 1001 | 20 | 1500.0 | 50.0 | 2 | 100.0
    """
]
},
"EXAMPLE_4": {
            "table_info": """
col : algorithm_id | tag_name | rating_id | user_id | rating | rating_date
row 1 : 1 | super-resolution | 0 | 1 | 4 | 2023-05-01
row 2 : 1 | image-processing | 0 | 1 | 4 | 2023-05-01
row 3 : 2 | null | 1 | 2 | 3 | 2023-05-02
""",
"question": "Gather the unique identifiers of the algorithms that have blossomed with high praise, along with the bouquet of tags that adorn them, and arrange these by the intensity of their acclaim, descending.",
"answer": "1, image-processing, super-resolution, 4.0",
"explanation": "To find algorithms with high praise and their associated tags, I need to analyze the algorithm_performance_data table. First, I'll group the data by algorithm_id to calculate average ratings and collect tags. Then I'll filter for algorithms with high ratings (above 3) and sort by rating in descending order. The result shows algorithm 1 has an average rating of 4.0 and is tagged with 'image-processing' and 'super-resolution'.",
"chain": [
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_add_inferred_column(avg_rating)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(avg_rating)",
    "END"
],
"explanations": [
    "Adding columns for average rating and a concatenated list of tags per algorithm",
    "Filtering to include only algorithms with high ratings (above 3), which are row 1 and row 2",
    "Sorting by average rating in descending order to show highest rated algorithms first"
],
"intermediate_tables": [
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """,
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """,
    """
col : rating_id | algorithm_id | user_id | rating | rating_date | tag_id | algorithm_tags.algorithm_id | tag_name | avg_rating 
row 1 : 0 | 1 | 1 | 4 | 2023-05-01 | 0 | 1 | super-resolution | 4.0
row 2 : 0 | 1 | 1 | 4 | 2023-05-01 | 1 | 1 | image-processing | 4.0
    """
]
},
"EXAMPLE_5": {
            "table_info": """
table_name: gacha_rewards
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha

foreign_key: 
""",
"question": "**User**: I want to find out the average amount of in-game currency spent by users to obtain rewards.**Assistant**: Sure, I can help with that. Do you want to know the average for each user, or the overall average across all users?**User**: I want the overall average.**Assistant**: Got it. Is there any other specific information you need related to this query?**User**: No, that's all I need.**Assistant**: OK, I will help you translate your request into an SQL query.",
"answer": "50.0",
"explanation": "To calculate the overall average amount of in-game currency spent by users to obtain rewards, I need to analyze the currency_spent column in the gacha_rewards table. I'll calculate the average of the currency_spent values across all rewards. The result is 50.0, which represents the overall average amount of in-game currency spent per reward.",
"chain": [
    "f_add_inferred_column()",
    "f_select_column()",
    "END"
],
"filled_chain": [
    "f_add_inferred_column(average_currency_spent)",
    "f_select_column(average_currency_spent)",
    "END"
],
"explanations": [
    "Adding a column to calculate the average currency spent across all rewards",
    "Selecting only the average_currency_spent column for the final result"
],
"intermediate_tables": [
    """
col : reward_id | timestamp | reward_name | reward_type | rarity | wish_count | pity_count | user_id | game_session_id | platform | device_id | location | ip_address | currency_spent | reward_details | is_first_wish | is_last_wish | is_pity_reward | is_event_reward | event_id | event_name | event_start_date | event_end_date | event_description | reward_source | reward_quantity | reward_quality | reward_effectiveness | reward_rarity_modifier | reward_type_modifier | reward_pity_modifier | reward_event_modifier | reward_user_modifier | server_id | player_level | player_experience | reward_usage_count | reward_expiration_date | transaction_id | payment_method | reward_image_url | reward_description | is_featured_reward | reward_obtained_from | average_currency_spent
row 1 : 0 | 2020-10-06 10:48:37 | Magic Guide | Weapon | 3 | 1 | 1 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans123 | In-app Purchase | http://example.com/reward1.jpg | A basic magic weapon for beginners. | 0 | Standard Gacha | 50.0
row 2 : 1 | 2020-10-06 10:48:37 | Thrilling Tales of Dragon Slayers | Weapon | 3 | 2 | 2 | 1001 | session123 | iOS | device123 | New York, NY, USA | 192.168.1.1 | 50.0 | None | 0 | 0 | 0 | 0 | null | null | null | null | null | Standard | 1 | Good | Average | None | None | None | None | None | 101 | 20 | 1500.0 | 0 | 2021-12-31 | trans124 | Earned Currency | http://example.com/reward2.jpg | A book that enhances your combat skills. | 0 | Standard Gacha | 50.0
    """,
    """
col : average_currency_spent
row 1 : 50.0
row 2 : 50.0
    """
]
}
}