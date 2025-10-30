import pandas as pd
from prettytable import PrettyTable
import matplotlib.pyplot as plt

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

def createByStateBarPlot(df: pd.DataFrame, field: str, filename: str, title: str, ylabel: str) -> None:
    '''
    Function to create a per-state bar plot

    Parameters:
        df : pd.DataFrame
            Dataframe of ARC county level data.
        field : str
            Column name to select and plot by
        filename : str
            Output filename
        title : str
            Title of the generated plot
        ylabel : str
            The y-axis label for the plot

    Returns: None
    '''
    group = df.groupby('state')[field].mean().sort_values(ascending=True)

    us_state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
        'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }

    group.index = [us_state_abbrev.get(state, state) for state in group.index]

    plt.figure(figsize=(12, 6))
    plt.bar(group.index, group.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()


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

    createByStateBarPlot(df, 'poverty_rate', 'pov_rate.png', 'States by Poverty Rate', 'Poverty Rate (%)')
    createByStateBarPlot(df, 'avg_unemployment', 'unemployment.png', 'States by Average Unemployment', 'Unemployment Rate (%)')
    createByStateBarPlot(df, 'PCI', 'income.png', 'States by Per Capita Income', 'Per Capita Income ($)')


if __name__ == '__main__':
    main()