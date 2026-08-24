import re
from typing import List, Tuple, Optional
import pandas as pd

def extract_stitch_tables_params(llm_output: str) -> Optional[Tuple[str, str]]:
    """LLMf_stitch_tables"""
    match = re.search(r"f_stitch_tables\(([^,]+),\s*([^)]+)\)", llm_output)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None

def process_stitch_tables(
    tables: List[List[List[str]]], 
    table_names: List[str], 
    params: Tuple[str, str],
    join_method: str = "inner"
) -> Optional[List[List[str]]]:
    """
    pandas
    
    Args:
        tables: 
        table_names: 
        params:  (e.g., ('table1.colA', 'table2.colB'))
        
    Returns:
        
    """
    try:
        # 
        t1_name_str, t1_col_str = params[0].split('.')
        t2_name_str, t2_col_str = params[1].split('.')
        
        # 
        t1_idx = table_names.index(t1_name_str)
        t2_idx = table_names.index(t2_name_str)

        # DataFrame
        df1 = pd.DataFrame(tables[t1_idx][1:], columns=tables[t1_idx][0])
        df2 = pd.DataFrame(tables[t2_idx][1:], columns=tables[t2_idx][0])

        # 
        merged_df = pd.merge(df1, df2, left_on=t1_col_str, right_on=t2_col_str, how=join_method)

        # list of lists
        new_table_header = merged_df.columns.tolist()
        new_table_rows = merged_df.values.tolist()
        return [new_table_header] + new_table_rows
        
    except (ValueError, IndexError, KeyError) as e:
        print(f"Error processing stitch_tables: {e}")
        return None 

if __name__ == "__main__":
    # ，
    table1_col = "book_club.book_club_id"
    table2_col = "culture_company.book_club_id"
    join_method = "inner"
    table_names = [
      "book_club",
      "culture_company"
    ]
    # ：table_names 
    tables = [
        [
            ['book_club_id', 'Year', 'Author_or_Editor', 'Book_Title', 'Publisher', 'Category', 'Result'],
            [1, 1989, 'Michael Nava', 'Goldenboy', 'Alyson', 'Gay M/SF', 'Won [A ]'],
            [2, 1989, 'Donald Ward', 'Death Takes the Stage', "St. Martin's Press", 'Gay M/SF', 'Nom'],
            [3, 1989, 'Michael Bishop', 'Unicorn Mountain', 'William Morrow', 'Gay M/SF', 'Nom'],
            [4, 1989, 'Joseph Hansen', 'Obedience', 'Mysterious Press', 'Gay M/SF', 'Nom'],
            [5, 1989, 'George Baxt', 'WhoÓ³ Next', 'International Polygonics', 'Gay M/SF', 'Nom'],
            [6, 1989, 'Antoinette Azolakov', 'Skiptrace', 'Banned Books', 'Lesb. M/SF', 'Won'],
            [7, 1989, 'Claire McNab', 'Lessons In Murder', 'Naiad Press', 'Lesb. M/SF', 'Nom'],
            [8, 1989, 'Judy Grahn', 'MundaneÓ³ World', 'Crossing Press', 'Lesb. M/SF', 'Nom'],
            [9, 1989, 'Dolores Klaich', 'Heavy Gilt', 'Naiad Press', 'Lesb. M/SF', 'Nom'],
            [10, 1989, 'Sandy Bayer', 'The Crystal Curtain', 'Alyson', 'Lesb. M/SF', 'Nom'],
            [11, 1990, 'Jeffrey N. McMahan', 'Somewhere in the Night', 'Alyson', 'Gay SF/F', 'Won [B ]'],
            [12, 1990, 'Thom Nickels', 'Walking Water / After All This', 'Banned Books', 'Gay SF/F', 'Nom']
        ],
        [
            ['Company_name', 'Type', 'Incorporated_in', 'Group_Equity_Shareholding', 'book_club_id', 'movie_id'],
            ['Culture China', 'Corporate', 'China', 18.77, '1', '2'],
            ['Culture China Cargo', 'Joint Venture', 'China', 49.0, '2', '3'],
            ['Culture Hong Kong', 'Joint Venture', 'Hong Kong', 60.0, '3', '4'],
            ['Dragonair', 'Subsidiary', 'Hong Kong', 100.0, '5', '7'],
            ['Cathay Pacific Culture', 'Subsidiary', 'Hong Kong', 100.0, '5', '5'],
            ['Cathay Pacific Culture Services (HK) Limited', 'Subsidiary', 'Hong Kong', 100.0, '6', '6']
        ]
    ]

    result = process_stitch_tables(tables, table_names, (table1_col, table2_col), join_method)
    print(result)