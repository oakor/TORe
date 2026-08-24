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

task_5_EXAMPLES_multi = {
    "EXAMPLE_0": {
            "table_info": """
table_name: locations
col : location_id | location_name | address | city | state | zip | created_at | updated_at | latitude | longitude | phone | website
row 1 : 0 | Fair Oaks Adult Activity Center | 2600 Middlefield Rd | Palo Alto | CA | 94306 | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 37.4419 | -122.1430 | (650) 321-8020 | https://www.foaac.org
row 2 : 1 | Second Career Employment Program | 123 Main St | Redwood City | CA | 94063 | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 37.5047 | -122.2580 | (650) 123-4567 | https://www.scep.org

table_name: providers
col : provider_id | provider_name | email | phone | website | created_at | updated_at | address | city | state | zip | description | services_offered
row 1 : 0 | Fair Oaks Adult Activity Center | info@foaac.org | (650) 321-8020 | https://www.foaac.org | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 2600 Middlefield Rd | Palo Alto | CA | 94306 | A community center offering a variety of programs for older adults. | ['Fair Oaks Adult Activity Center']
row 2 : 1 | Second Career Employment Program | info@scep.org | (650) 123-4567 | https://www.scep.org | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 123 Main St | Redwood City | CA | 94063 | A program providing job training and placement for older adults. | ['Second Career Employment Program']

table_name: service_areas
col : service_area_id | service_id | area_name | city | state | zip | created_at | updated_at | latitude | longitude
row 1 : 0 | 1 | Colma | Colma | CA | 94014 | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 37.6990 | -122.4780
row 2 : 1 | 2 | San Mateo County | Redwood City | CA | 94063 | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 37.5047 | -122.2580

foreign_key: 
""",
"question": "Hey, could you help me find the average number of service areas per provider in each city? I'd love to know the city names along with these averages.",
"answer": "Redwood City, 1.0",
"explanation": "To solve this problem, I need to find the average number of service areas per provider in each city. First, I need to join the providers and service_areas tables to connect providers with their service areas. Then I need to group by city, count the service areas, count the providers, and calculate the average service areas per provider for each city. The result shows that Redwood City has an average of 1.0 service areas per provider.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(providers.city, service_areas.city, left)",
    "f_select_column(provider_name, city, service_area_id)",
    "f_add_inferred_column(has_service_area)",
    "f_group_column(providers.city)",
    "END"
],
"explanations": [
    "Joining providers and service_areas tables on city to connect providers with service areas in the same city",
    "Selecting relevant columns to identify providers, their cities, and associated service areas",
    "Adding a column to indicate whether a provider has a service area (1 if yes, 0 if no)",
    "Grouping by city to calculate the average number of service areas per provider in each city"
],
"intermediate_tables": [
    """
col : provider_id | provider_name | email | phone | website | created_at | updated_at | address | city | state | zip | description | services_offered | service_area_id | service_id | area_name | service_areas.city | service_areas.state | service_areas.zip | service_areas.created_at | service_areas.updated_at | service_areas.latitude | service_areas.longitude
row 1 : 0 | Fair Oaks Adult Activity Center | info@foaac.org | (650) 321-8020 | https://www.foaac.org | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 2600 Middlefield Rd | Palo Alto | CA | 94306 | A community center offering a variety of programs for older adults. | ['Fair Oaks Adult Activity Center'] | null | null | null | null | null | null | null | null | null | null
row 2 : 1 | Second Career Employment Program | info@scep.org | (650) 123-4567 | https://www.scep.org | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 123 Main St | Redwood City | CA | 94063 | A program providing job training and placement for older adults. | ['Second Career Employment Program'] | 1 | 2 | San Mateo County | Redwood City | CA | 94063 | 2023-01-01 00:00:00 | 2023-01-01 00:00:00 | 37.5047 | -122.2580
    """,
    """
col : provider_name | city | service_area_id
row 1 : Fair Oaks Adult Activity Center | Palo Alto | null
row 2 : Second Career Employment Program | Redwood City | 1
    """,
    """
col : provider_name | city | service_area_id | has_service_area
row 1 : Fair Oaks Adult Activity Center | Palo Alto | null | 0
row 2 : Second Career Employment Program | Redwood City | 1 | 1
    """,
    """
col : city | provider_count | service_area_count | avg_service_areas_per_provider
row 1 : Palo Alto | 1 | 0 | 0.0
row 2 : Redwood City | 1 | 1 | 1.0
    """
]
},
"EXAMPLE_2": {
            "table_info": """
table_name: members
col : individual_id | first_last_name | primary_email_address | secondary_email_address | last_membership_year | frequency | recency | membership_product_group | primary_member_type | country | membership_year | date_of_birth | gender | address_line_1 | address_line_2 | city | state | zip_code | phone_number | date_joined | status | renewal_date | renewal_reminder_sent | last_interacted | total_interactions | member_category | benefits_claimed
row 1 : 0 | A Bromfield, Hine | drbh165@hotmail.com | drbh165@gmail.com | 2020 | 5 | 1 | Lifetime Membership | Emeritus | United States | 2016 | 1950-01-01 | Male | 123 Main St | Apt 4B | Anytown | Anystate | 12345 | 123-456-7890 | 2016-01-01 | Active | 2023-12-31 | 1 | 2023-05-15 | 30 | Emeritus | Discounted Conferences, Free Webinars
row 2 : 1 | A Claudio, Cuello | claudio.cuello@mcgill.ca | claudio.cuello@gmail.com | 2021 | 6 | 0 | 1 Year Membership | Regular | Canada | 2016 | 1970-05-22 | Female | 456 Maple Ave | None | Ottawa | Ontario | K1A 0A1 | 555-123-4567 | 2016-05-22 | Active | 2024-06-15 | 0 | 2023-10-01 | 15 | Regular | Access to Online Resources, Priority Registration

foreign_key: 
""",
"question": "How many high-frequency members, who have not renewed their membership since before 2023 and have not yet received a renewal reminder, need to be sent a renewal reminder?",
"answer": "1",
"explanation": "To find high-frequency members who need renewal reminders, I need to identify members with high interaction frequency (5 or higher) who haven't renewed since before 2023 and haven't received a reminder. First, I'll select the relevant columns for analysis. Then I'll add a column to identify high-frequency members. Next, I'll filter to include only those who haven't renewed since before 2023 and haven't received a reminder. The result shows that 1 member meets all these criteria.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_select_table(members)",
    "f_select_column(individual_id, first_last_name, frequency, last_membership_year, renewal_reminder_sent, status)",
    "f_add_inferred_column(needs_reminder)",
    "f_select_row(row 1)",
    "f_group_column(needs_reminder)",
    "END"
],
"explanations": [
    "Selecting the members table to focus on identifying members who need renewal reminders",
    "Selecting relevant columns to identify members who need renewal reminders",
    "Adding a column to flag members who need reminders (high frequency, old membership, no reminder sent)",
    "Selecting only rows where members need reminders, which is row 1",
    "Grouping by reminder status to count members needing reminders"
],
"intermediate_tables": [
    """
col : individual_id | first_last_name | primary_email_address | secondary_email_address | last_membership_year | frequency | recency | membership_product_group | primary_member_type | country | membership_year | date_of_birth | gender | address_line_1 | address_line_2 | city | state | zip_code | phone_number | date_joined | status | renewal_date | renewal_reminder_sent | last_interacted | total_interactions | member_category | benefits_claimed
row 1 : 0 | A Bromfield, Hine | drbh165@hotmail.com | drbh165@gmail.com | 2020 | 5 | 1 | Lifetime Membership | Emeritus | United States | 2016 | 1950-01-01 | Male | 123 Main St | Apt 4B | Anytown | Anystate | 12345 | 123-456-7890 | 2016-01-01 | Active | 2023-12-31 | 1 | 2023-05-15 | 30 | Emeritus | Discounted Conferences, Free Webinars
row 2 : 1 | A Claudio, Cuello | claudio.cuello@mcgill.ca | claudio.cuello@gmail.com | 2021 | 6 | 0 | 1 Year Membership | Regular | Canada | 2016 | 1970-05-22 | Female | 456 Maple Ave | None | Ottawa | Ontario | K1A 0A1 | 555-123-4567 | 2016-05-22 | Active | 2024-06-15 | 0 | 2023-10-01 | 15 | Regular | Access to Online Resources, Priority Registration
    """,
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status
row 1 : 0 | A Bromfield, Hine | 5 | 2020 | 1 | Active
row 2 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active
    """,
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status | needs_reminder
row 1 : 0 | A Bromfield, Hine | 5 | 2020 | 1 | Active | 0
row 2 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active | 1
    """,
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status | needs_reminder
row 1 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active | 1
    """,
    """
col : needs_reminder | count
row 1 : 1 | 1
    """
]
},
"EXAMPLE_3": {
            "table_info": """
table_name: prediction_results
col : prediction_id | model_id | scenario_id | prediction | confidence
row 1 : 0 | 1 | 1 | High demand | 0.8
row 2 : 1 | 2 | 1 | Low demand | 0.6

foreign_key: 
""",
"question": "Find the most confident predictions for each scenario, uncovering the 'jewels' of certainty within a sea of uncertainty, where 'certainty' refers to the highest confidence level in each scenario.",
"answer": "1, High demand, 0.8",
"explanation": "To find the most confident predictions for each scenario, I need to identify predictions with the highest confidence level per scenario. First, I'll select the relevant columns for analysis. Then I'll sort the data by confidence in descending order to bring the most confident predictions to the top. Next, I'll group by scenario_id to find the top prediction for each scenario. The result shows that for scenario 1, the most confident prediction is 'High demand' with a confidence of 0.8.",
"chain": [
    "f_select_table()",
    "f_select_column()",
    "f_sort_column()",
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_select_table(prediction_results)",
    "f_select_column(scenario_id, prediction, confidence, model_id)",
    "f_sort_column(confidence)",
    "f_group_column(scenario_id)",
    "END"
],
"explanations": [
    "Selecting the prediction_results table to analyze prediction confidence",
    "Selecting relevant columns to identify scenarios, predictions, and their confidence levels",
    "Sorting by confidence in descending order to identify the most confident predictions",
    "Grouping by scenario_id to find the top prediction for each unique scenario"
],
"intermediate_tables": [
    """
col : prediction_id | model_id | scenario_id | prediction | confidence
row 1 : 0 | 1 | 1 | High demand | 0.8
row 2 : 1 | 2 | 1 | Low demand | 0.6
    """,
    """
col : scenario_id | prediction | confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
row 2 : 1 | Low demand | 0.6 | 2
    """,
    """
col : scenario_id | prediction | confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
row 2 : 1 | Low demand | 0.6 | 2
    """,
    """
col : scenario_id | top_prediction | highest_confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
    """
]
},
"EXAMPLE_4": {
            "table_info": """
table_name: tags
col : tag_id | tag_name | created_at | updated_at
row 1 : 0 | decimal | 2023-01-01 12:00:00 | 2023-01-01 12:00:00
row 2 : 1 | binary | 2023-01-02 12:00:00 | 2023-01-02 12:00:00

table_name: conversion_tags
col : conversion_id | tag_id | created_at | updated_at
row 1 : 0 | 0 | 2023-01-01 12:00:00 | 2023-01-01 12:00:00
row 2 : 1 | 1 | 2023-01-02 12:00:00 | 2023-01-02 12:00:00

table_name: notifications
col : notification_id | user_id | notification_message | created_at | updated_at
row 1 : 0 | 1 | You have a new conversion request. | 2023-01-01 12:00:00 | 2023-01-01 12:00:00
row 2 : 1 | 2 | Your conversion is complete. | 2023-01-02 12:00:00 | 2023-01-02 12:00:00

foreign_key: 
""",
"question": "Could you please list all the users who received notifications for conversions tagged as 'binary', and provide the count of notifications each user received, sorted by user ID in ascending order?",
"answer": "1, 1",
"explanation": "To find users who received notifications for conversions tagged as 'binary', I need to connect the tags, conversion_tags, and notifications tables. First, I'll join the tags and conversion_tags tables to identify conversions tagged as 'binary'. Then I'll join this result with the notifications table to find users who received notifications for these conversions. Finally, I'll filter for the 'binary' tag, count notifications per user, and sort by user ID. The result shows that user ID 2 received 1 notification for a conversion tagged as 'binary'.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_select_row()",
    "f_group_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(conversion_tags.created_at, notifications.created_at, inner)",
    "f_select_column(user_id, notification_id)",
    "f_select_row(row 2)",
    "f_group_column(user_id)",
    "f_sort_column(user_id)",
    "END"
],
"explanations": [
    "Joining the result with notifications based on creation time to find notifications related to conversions",
    "Selecting relevant columns to identify users and their notifications for specific tags",
    "Filtering to include only rows where the tag is 'binary' which is row 2",
    "Grouping by user_id to count notifications per user",
    "Sorting by user_id in ascending order as requested"
],
"intermediate_tables": [
    """
col : conversion_id | tag_id | created_at | updated_at | notification_id | user_id | notification_message | created_at | updated_at
row 1 : 0 | 0 | 2023-01-01 12:00:00 | 2023-01-01 12:00:00 | 0 | 1 | You have a new conversion request. | 2023-01-01 12:00:00 | 2023-01-01 12:00:00
row 2 : 1 | 1 | 2023-01-02 12:00:00 | 2023-01-02 12:00:00 | 1 | 2 | Your conversion is complete. | 2023-01-02 12:00:00 | 2023-01-02 12:00:00
    """,
    """
col : user_id | notification_id
row 1 : 1 | 0
row 2 : 2 | 1
    """,
    """
col : user_id | notification_id
row 1 : 2 | 1
    """,
    """
col : user_id | count
row 1 : 2 | 1
    """,
    """
col : user_id | count
row 1 : 2 | 1
    """
]
},
"EXAMPLE_5": {
            "table_info": """
table_name: properties
col : property_id | address | price | avg_area_income | avg_area_house_age | avg_area_number_of_rooms | avg_area_number_of_bedrooms | area_population | property_type | year_built | square_footage | number_of_bathrooms | garage_type | lot_size | property_condition | last_sold_date | last_sold_price | zillow_id | google_maps_link
row 1 : 0 | 208 Michael Ferry Apt. 674 | 1059030.0 | 79545.5 | 5.68286 | 7.00919 | 4.09 | 23086.8 | single-family home | 2000 | 2500.0 | 3 | attached | 8000.0 | excellent | 2022-01-01 | 1000000.0 | Z1234567 | https://www.google.com/maps/place/208+Michael+Ferry+Apt.+674
row 2 : 1 | 188 Johnson Views Suite 079 | 1505890.0 | 79248.6 | 6.0029 | 6.73082 | 3.09 | 40173.1 | apartment | 1995 | 1500.0 | 2 | none | 1000.0 | good | 2021-05-01 | 1450000.0 | Z7654321 | https://www.google.com/maps/place/188+Johnson+Views+Suite+079

table_name: locations
col : location_id | city | state | zip_code | latitude | longitude | median_income | median_age | median_house_age | school_rating | crime_rate | proximity_to_public_transport | proximity_to_commercial_areas
row 1 : 0 | Laurabury | NE | 37010-5101 | 41.2345 | -96.789 | 80000.0 | 35.0 | 10.0 | 8 | 2.5 | 0.5 miles | 1 mile
row 2 : 1 | Lake Kathleen | CA | 48958 | 37.1234 | -122.4567 | 100000.0 | 40.0 | 15.0 | 7 | 1.8 | 0.3 miles | 0.8 miles

table_name: property_locations
col : property_id | location_id | date_added | source
row 1 : 0 | 0 | 2023-01-01 | Zillow
row 2 : 1 | 1 | 2023-02-01 | MLS

foreign_key: 
""",
"question": "Could you please gather the addresses of the most expensive properties in each city with high median income, specifically those that rank highest in terms of price and have a median income ranking of 5 or better, and list them in order of highest median income and then highest price?",
"answer": "188 Johnson Views Suite 079, 208 Michael Ferry Apt. 674",
"explanation": "To find the most expensive properties in cities with high median income, I need to connect property information with location data. First, I'll join the properties, property_locations, and locations tables to link properties with their cities and income data. Then I'll add a column to rank cities by median income and filter for high-income cities (rank 5 or better). Next, I'll sort by median income (descending) and then by property price (descending) to get the desired order. The result shows the addresses in order: '188 Johnson Views Suite 079' followed by '208 Michael Ferry Apt. 674'.",
"chain": [
    "f_stitch_tables()",
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_stitch_tables(properties.property_id, locations.location_id, inner)",
    "f_select_column(address, price, city, median_income)",
    "f_add_inferred_column(income_rank)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(median_income)",
    "END"
],
"explanations": [
    "Joining properties and locations tables to connect property_id and location_id with each other, according to the table property_locations in which property_id and location_id are the same in one row",
    "Selecting relevant columns for property address, price, city, and median income",
    "Adding income_rank column to rank cities by their median income",
    "Filtering to include only properties in cities with high median income (rank 5 or better)",
    "Sorting first by median income (descending) and then by price (descending) to get the desired order"
],
"intermediate_tables": [
    """
col : property_id | address | price | avg_area_income | avg_area_house_age | avg_area_number_of_rooms | avg_area_number_of_bedrooms | area_population | property_type | year_built | square_footage | number_of_bathrooms | garage_type | lot_size | property_condition | last_sold_date | last_sold_price | zillow_id | google_maps_link | location_id | city | state | zip_code | latitude | longitude | median_income | median_age | median_house_age | school_rating | crime_rate | proximity_to_public_transport | proximity_to_commercial_areas
row 1 : 0 | 208 Michael Ferry Apt. 674 | 1059030.0 | 79545.5 | 5.68286 | 7.00919 | 4.09 | 23086.8 | single-family home | 2000 | 2500.0 | 3 | attached | 8000.0 | excellent | 2022-01-01 | 1000000.0 | Z1234567 | https://www.google.com/maps/place/208+Michael+Ferry+Apt.+674 | 0 | Laurabury | NE | 37010-5101 | 41.2345 | -96.789 | 80000.0 | 35.0 | 10.0 | 8 | 2.5 | 0.5 miles | 1 mile
row 2 : 1 | 188 Johnson Views Suite 079 | 1505890.0 | 79248.6 | 6.0029 | 6.73082 | 3.09 | 40173.1 | apartment | 1995 | 1500.0 | 2 | none | 1000.0 | good | 2021-05-01 | 1450000.0 | Z7654321 | https://www.google.com/maps/place/188+Johnson+Views+Suite+079 | 1 | Lake Kathleen | CA | 48958 | 37.1234 | -122.4567 | 100000.0 | 40.0 | 15.0 | 7 | 1.8 | 0.3 miles | 0.8 miles
    """,
    """
col : address | price | city | median_income
row 1 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0
row 2 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
row 2 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
row 2 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
row 2 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
    """
]
}
}

task_5_EXAMPLES_single = {
    "EXAMPLE_0": {
            "table_info": """
col : provider_id | provider_name | email | phone | website | address | city | state | zip | description | services_offered | service_area_id | service_id | area_name | service_city | latitude | longitude
row 1 : 0 | Fair Oaks Adult Activity Center | info@foaac.org | (650) 321-8020 | https://www.foaac.org | 2600 Middlefield Rd | Palo Alto | CA | 94306 | A community center offering a variety of programs for older adults. | ['Fair Oaks Adult Activity Center'] | null | null | null | null | 37.4419 | -122.1430
row 2 : 1 | Second Career Employment Program | info@scep.org | (650) 123-4567 | https://www.scep.org | 123 Main St | Redwood City | CA | 94063 | A program providing job training and placement for older adults. | ['Second Career Employment Program'] | 1 | 2 | San Mateo County | Redwood City | 37.5047 | -122.2580
""",
"question": "Can you tell me the average number of service areas per provider in each city?",
"answer": "Redwood City, 1.0; Palo Alto, 0.0",
"explanation": "To find the average number of service areas per provider in each city, I need to analyze the relationship between providers and service areas. First, I'll select relevant columns to identify providers, their cities, and associated service areas. Then I'll add a column to indicate whether a provider has a service area (1 if yes, 0 if no). Next, I'll group by city to calculate the average number of service areas per provider in each city. Finally, I'll sort by average service areas in descending order to show cities with highest averages first. The results show that Redwood City has an average of 1.0 service areas per provider, while Palo Alto has 0.0.",
"chain": [
    "f_select_column()",
    "f_add_inferred_column()",
    "f_group_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_select_column(provider_name, city, service_area_id)",
    "f_add_inferred_column(has_service_area)",
    "f_group_column(city)",
    "f_sort_column(avg_service_areas)",
    "END"
],
"explanations": [
    "Selecting relevant columns to identify providers, their cities, and associated service areas",
    "Adding a column to indicate whether a provider has a service area (1 if yes, 0 if no)",
    "Grouping by city to calculate the average number of service areas per provider in each city",
    "Sorting by average service areas in descending order to show cities with highest averages first"
],
"intermediate_tables": [
    """
col : provider_name | city | service_area_id
row 1 : Fair Oaks Adult Activity Center | Palo Alto | null
row 2 : Second Career Employment Program | Redwood City | 1
    """,
    """
col : provider_name | city | service_area_id | has_service_area
row 1 : Fair Oaks Adult Activity Center | Palo Alto | null | 0
row 2 : Second Career Employment Program | Redwood City | 1 | 1
    """,
    """
col : city | provider_count | service_area_count | avg_service_areas
row 1 : Palo Alto | 1 | 0 | 0.0
row 2 : Redwood City | 1 | 1 | 1.0
    """,
    """
col : city | provider_count | service_area_count | avg_service_areas
row 1 : Redwood City | 1 | 1 | 1.0
row 2 : Palo Alto | 1 | 0 | 0.0
    """
]
},
"EXAMPLE_1": {
            "table_info": """
col : notification_id | user_id | notification_message | created_at | conversion_id | tag_id | tag_name
row 1 : 0 | 1 | You have a new conversion request. | 2023-01-01 12:00:00 | 0 | 0 | decimal
row 2 : 1 | 2 | Your conversion is complete. | 2023-01-02 12:00:00 | 1 | 1 | binary
""",
"question": "What is the total number of unique users who have received at least one notification that is associated with a conversion?",
"answer": "2",
"explanation": "To find the total number of unique users who have received notifications associated with conversions, I need to connect notifications with conversions through their tags. First, I'll select the user_id, conversion_id, and tag_name to identify which users received notifications for which conversions. Then I'll group by user_id to count unique users who received notifications associated with conversions. The result shows there are 2 unique users who received notifications associated with conversions.",
"chain": [
    "f_select_column()",
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_select_column(user_id, conversion_id, tag_name)",
    "f_group_column(user_id)",
    "END"
],
"explanations": [
    "Selecting the user_id, conversion_id, and tag_name to identify which users received notifications for which conversions",
    "Grouping by user_id to count unique users who received notifications associated with conversions"
],
"intermediate_tables": [
    """
col : user_id | conversion_id | tag_name
row 1 : 1 | 0 | decimal
row 2 : 2 | 1 | binary
    """,
    """
col : user_id | count
row 1 : 1 | 1
row 2 : 2 | 1
    """
]
},
"EXAMPLE_2": {
            "table_info": """
col : individual_id | first_last_name | primary_email_address | secondary_email_address | last_membership_year | frequency | recency | membership_product_group | primary_member_type | country | membership_year | date_of_birth | gender | address_line_1 | address_line_2 | city | state | zip_code | phone_number | date_joined | status | renewal_date | renewal_reminder_sent | last_interacted | total_interactions | member_category | benefits_claimed
row 1 : 0 | A Bromfield, Hine | drbh165@hotmail.com | drbh165@gmail.com | 2020 | 5 | 1 | Lifetime Membership | Emeritus | United States | 2016 | 1950-01-01 | Male | 123 Main St | Apt 4B | Anytown | Anystate | 12345 | 123-456-7890 | 2016-01-01 | Active | 2023-12-31 | 1 | 2023-05-15 | 30 | Emeritus | Discounted Conferences, Free Webinars
row 2 : 1 | A Claudio, Cuello | claudio.cuello@mcgill.ca | claudio.cuello@gmail.com | 2021 | 6 | 0 | 1 Year Membership | Regular | Canada | 2016 | 1970-05-22 | Female | 456 Maple Ave | None | Ottawa | Ontario | K1A 0A1 | 555-123-4567 | 2016-05-22 | Active | 2024-06-15 | 0 | 2023-10-01 | 15 | Regular | Access to Online Resources, Priority Registration
""",
"question": "How many high-frequency members, who have not renewed their membership since before 2023 and have not yet received a renewal reminder, need to be sent a renewal reminder?",
"answer": "1",
"explanation": "To find high-frequency members who need renewal reminders, I need to identify members with high interaction frequency (5 or higher) who haven't renewed since before 2023 and haven't received a reminder. First, I'll select the relevant columns for analysis. Then I'll add a column to identify high-frequency members. Next, I'll filter to include only those who haven't renewed since before 2023 and haven't received a reminder. The result shows that 1 member meets all these criteria.",
"chain": [
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_group_column()",
    "END"
],
"filled_chain": [
    "f_select_column(individual_id, first_last_name, frequency, last_membership_year, renewal_reminder_sent, status)",
    "f_add_inferred_column(needs_reminder)",
    "f_select_row(row 1)",
    "f_group_column(needs_reminder)",
    "END"
],
"explanations": [
    "Selecting relevant columns to identify members who need renewal reminders",
    "Adding a column to flag members who need reminders (high frequency, old membership, no reminder sent)",
    "Selecting only rows where members need reminders which is row 1",
    "Grouping by reminder status to count members needing reminders"
],
"intermediate_tables": [
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status
row 1 : 0 | A Bromfield, Hine | 5 | 2020 | 1 | Active
row 2 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active
    """,
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status | needs_reminder
row 1 : 0 | A Bromfield, Hine | 5 | 2020 | 1 | Active | 0
row 2 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active | 1
    """,
    """
col : individual_id | first_last_name | frequency | last_membership_year | renewal_reminder_sent | status | needs_reminder
row 1 : 1 | A Claudio, Cuello | 6 | 2021 | 0 | Active | 1
    """,
    """
col : needs_reminder | count
row 1 : 1 | 1
    """
]
},
"EXAMPLE_3": {
            "table_info": """
col : prediction_id | model_id | scenario_id | prediction | confidence
row 1 : 0 | 1 | 1 | High demand | 0.8
row 2 : 1 | 2 | 1 | Low demand | 0.6
""",
"question": "Find the most confident predictions for each scenario, uncovering the 'jewels' of certainty within a sea of uncertainty, where 'certainty' refers to the highest confidence level in each scenario.",
"answer": "1, High demand, 0.8",
"explanation": "To find the most confident predictions for each scenario, I need to identify predictions with the highest confidence level per scenario. First, I'll select the relevant columns for analysis. Then I'll sort the data by confidence in descending order to bring the most confident predictions to the top. Next, I'll group by scenario_id to find the top prediction for each scenario. The result shows that for scenario 1, the most confident prediction is 'High demand' with a confidence of 0.8.",
"chain": [
    "f_select_column()",
    "f_sort_column()",
    "f_select_row()",
    "END"
],
"filled_chain": [
    "f_select_column(scenario_id, prediction, confidence, model_id)",
    "f_sort_column(confidence)",
    "f_select_row(row 1)",
    "END"
],
"explanations": [
    "Selecting relevant columns to identify scenarios, predictions, and their confidence levels",
    "Sorting by confidence to identify the most confident predictions",
    "Selecting only the most confident prediction for each scenario which is row 1"
],
"intermediate_tables": [
    """
col : scenario_id | prediction | confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
row 2 : 1 | Low demand | 0.6 | 2
    """,
    """
col : scenario_id | prediction | confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
row 2 : 1 | Low demand | 0.6 | 2
    """,
    """
col : scenario_id | top_prediction | highest_confidence | model_id
row 1 : 1 | High demand | 0.8 | 1
    """
]
},
"EXAMPLE_4": {
            "table_info": """
col : notification_id | user_id | notification_message | created_at | conversion_id | tag_id | tag_name
row 1 : 0 | 1 | You have a new conversion request. | 2023-01-01 12:00:00 | 0 | 0 | decimal
row 2 : 1 | 2 | Your conversion is complete. | 2023-01-02 12:00:00 | 1 | 1 | binary
""",
"question": "Could you please list all the users who received notifications for conversions tagged as 'binary', and provide the count of notifications each user received, sorted by user ID in ascending order?",
"answer": "2, 1",
"explanation": "To find users who received notifications for conversions tagged as 'binary', I need to connect the tags, conversion_tags, and notifications tables. First, I'll join the tags and conversion_tags tables to identify conversions tagged as 'binary'. Then I'll join this result with the notifications table to find users who received notifications for these conversions. Finally, I'll filter for the 'binary' tag, count notifications per user, and sort by user ID. The result shows that user ID 2 received 1 notification for a conversion tagged as 'binary'.",
"chain": [
    "f_select_column()",
    "f_select_row()",
    "f_group_column()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_select_column(user_id, tag_name, notification_id)",
    "f_select_row(row 2)",
    "f_group_column(user_id)",
    "f_sort_column(user_id)",
    "END"
],
"explanations": [
    "Selecting relevant columns to identify users and their notifications for specific tags",
    "Filtering to include only rows where the tag is 'binary' which is row 2",
    "Grouping by user_id to count notifications per user",
    "Sorting by user_id in ascending order as requested"
],
"intermediate_tables": [
    """
col : user_id | tag_name | notification_id
row 1 : 1 | decimal | 0
row 2 : 2 | binary | 1
    """,
    """
col : user_id | tag_name | notification_id
row 2 : 2 | binary | 1
    """,
    """
col : user_id | count
row 1 : 2 | 1
    """,
    """
col : user_id | count
row 1 : 2 | 1
    """
]
},
"EXAMPLE_5": {
            "table_info": """
col : property_id | address | price | property_type | year_built | square_footage | number_of_bathrooms | garage_type | lot_size | property_condition | last_sold_date | last_sold_price | city | state | zip_code | latitude | longitude | median_income | median_age | median_house_age | school_rating | crime_rate
row 1 : 0 | 208 Michael Ferry Apt. 674 | 1059030.0 | single-family home | 2000 | 2500.0 | 3 | attached | 8000.0 | excellent | 2022-01-01 | 1000000.0 | Laurabury | NE | 37010-5101 | 41.2345 | -96.789 | 80000.0 | 35.0 | 10.0 | 8 | 2.5
row 2 : 1 | 188 Johnson Views Suite 079 | 1505890.0 | apartment | 1995 | 1500.0 | 2 | none | 1000.0 | good | 2021-05-01 | 1450000.0 | Lake Kathleen | CA | 48958 | 37.1234 | -122.4567 | 100000.0 | 40.0 | 15.0 | 7 | 1.8
""",
"question": "Could you please gather the addresses of the most expensive properties in each city with high median income, specifically those that rank highest in terms of price and have a median income ranking of 5 or better, and list them in order of highest median income and then highest price?",
"answer": "188 Johnson Views Suite 079, 208 Michael Ferry Apt. 674",
"explanation": "To find the most expensive properties in cities with high median income, I need to connect property information with location data. First, I'll join the properties, property_locations, and locations tables to link properties with their cities and income data. Then I'll add a column to rank cities by median income and filter for high-income cities (rank 5 or better). Next, I'll sort by median income (descending) and then by property price (descending) to get the desired order. The result shows the addresses in order: '188 Johnson Views Suite 079' followed by '208 Michael Ferry Apt. 674'.",
"chain": [
    "f_select_column()",
    "f_add_inferred_column()",
    "f_select_row()",
    "f_sort_column()",
    "END"
],
"filled_chain": [
    "f_select_column(address, price, city, median_income)",
    "f_add_inferred_column(income_rank)",
    "f_select_row(row 1, row 2)",
    "f_sort_column(median_income)",
    "END"
],
"explanations": [
    "Selecting relevant columns for property address, price, city, and median income",
    "Adding income_rank column to rank cities by their median income",
    "Filtering to include only properties in cities with high median income (rank 5 or better)",
    "Sorting first by median income (descending) and then by price (descending) to get the desired order"
],
"intermediate_tables": [
    """
col : address | price | city | median_income
row 1 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0
row 2 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
row 2 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
row 2 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
    """,
    """
col : address | price | city | median_income | income_rank
row 1 : 188 Johnson Views Suite 079 | 1505890.0 | Lake Kathleen | 100000.0 | 1
row 2 : 208 Michael Ferry Apt. 674 | 1059030.0 | Laurabury | 80000.0 | 2
    """
]
}
}