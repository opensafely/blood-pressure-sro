from utilities import *
from pathlib import Path
import pandas as pd
import os
from cohortextractor import Measure
from config import demographics, codelist_path
from ebmdatalab import charts

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

# Create default measures
measures = [

    Measure(
        id="event_code_rate",
        numerator="event",
        denominator="population",
        group_by=["event_code"]
    ),

    Measure(
        id="practice_rate",
        numerator="event",
        denominator="population",
        group_by=["practice"]
    ),



]

#Add demographics measures

for d in demographics:
 
    m = Measure(
        id=f'{d}_rate',
        numerator="event",
        denominator="population",
        group_by=[d]
    )
    
    measures.append(m)



measures_dict = {}

for m in measures:
    measures_dict[m.id] = m


for key, value in measures_dict.items():
    
    df = pd.read_csv(os.path.join(OUTPUT_DIR, f'measure_{value.id}.csv'), parse_dates=['date']).sort_values(by='date')
    df = drop_missing_demographics(df, value.group_by[0])

    if key == "ethnicity_rate":
        df = convert_ethnicity(df)
        
    df = calculate_rate(df, numerator=value.numerator, denominator=value.denominator, rate_per=1000)
    
    if key == "imd_rate":
        df = calculate_imd_group(df, value.numerator, 'rate')
        df = redact_small_numbers(df, 5, value.numerator, value.denominator, 'rate')
    
    elif key == "care_home_status_rate":
        df = convert_binary(df, 'care_home_status', 'Record of positive care home status', 'No record of positive care home status')

    elif key =='learning_disability_rate':
        df = convert_binary(df, 'learning_disability', 'Record of learning disability', 'No record of learning disability')


    # get total population rate
    if value.id=='practice_rate':
        
        df = drop_irrelevant_practices(df, 'practice')
        df.to_csv(os.path.join(OUTPUT_DIR, f'rate_table_{value.group_by[0]}.csv'), index=False)

        charts.deciles_chart(
        df,
        period_column='date',
        column='event',
        title='Decile Chart',
        ylabel='rate per 1000',
        show_outer_percentiles=False,
        show_legend=True,
        ).savefig('output/decile_chart.png', bbox_inches='tight')  
        
        df_total = df.groupby(by='date')[[value.numerator, value.denominator]].sum().reset_index()
        df_total = calculate_rate(df_total, numerator=value.numerator, denominator=value.denominator, rate_per=1000)
        plot_measures(df_total, filename='plot_total.png', title='Population Rate', column_to_plot='rate', category=None, y_label='Rate per 1000')
        df_total.to_csv(os.path.join(OUTPUT_DIR, 'rate_table_total.csv'), index=False)

    elif value.id=='event_code_rate':
        df.to_csv(os.path.join(OUTPUT_DIR, f'rate_table_{value.group_by[0]}.csv'), index=False)
        codelist = pd.read_csv(codelist_path)
        child_code_table = create_child_table(df=df, code_df=codelist, code_column='code', term_column='term')
        child_code_table.to_csv('output/child_code_table.csv', index=False)

    else:
        plot_measures(df, filename=f'plot_{value.group_by[0]}.png', title=f'Breakdown by {value.group_by[0]}', column_to_plot='rate', category=value.group_by[0], y_label='Rate per 1000')
        df.to_csv(os.path.join(OUTPUT_DIR, f'rate_table_{value.group_by[0]}.csv'), index=False)