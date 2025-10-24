import pandas as pd
from prettytable import PrettyTable

def printTableBy(df:pd.DataFrame, col_name:str, how_many:int, title:str) -> None:
    df_select = df[['state', 'county', 'PCI', 'poverty_rate', 'avg_unemployment']]
    if col_name=='PCI':
        my_bool=True
    else:
        my_bool=False
    df_sorted = df_select.sort_values(col_name, ascending=my_bool)
    table = PrettyTable()
    table.title = title
    table.field_names = ['State', 'County', 'PCI', 'Poverty Rate', 'Avg Unemployment']
    for i in range (how_many):
        table.add_row(df_sorted.iloc[i])
    print(table)

def main() -> None:
    df = pd.read_csv('county_economic_status_2024.csv', 
                     skiprows = 6,
                     index_col=False,
                     names = ['fips',
                  'state', 
                  'county', 
                  'arc_county', 
                  'county_economic_status', 
                  'avg_unemployment', 
                  'PCI', 
                  'poverty_rate', 
                  'avg_unemployment_percent_US', 
                  'PCMI_percent_US', 
                  'PCMI_percent_US_inverse', 
                  'poverty_rate_percent_US', 
                  'composite_index', 
                  'quartile'])
    df['PCI'] = df['PCI'].replace(',', '', regex=True).astype(float)

    printTableBy(df, 'poverty_rate', 5, 'COUNTIES BY POVERTY RATE')
    printTableBy(df, 'PCI', 5, 'COUNTIES BY PER CAPITA INCOME')
    printTableBy(df, 'avg_unemployment', 5, 'COUNTIES BY AVERAGE UNEMPLOYMENT')

if __name__ == '__main__':
    main()