import nbformat as nbf
from config import demographics


nb = nbf.v4.new_notebook()


imports = """\
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from IPython.display import HTML
from IPython.display import Markdown as md
from IPython.core.display import HTML as Center
from config import marker, start_date, end_date, demographics, codelist_path
from IPython.display import Image, display
from utilities import *
%matplotlib inline

"""

header = """\
display(
md("# Service Restoration Observatory"),
md(f"## Changes in {marker} between {start_date} and {end_date}"),
md(f"Below are various time-series graphs showing changes in {marker} code use."),
)
"""

methods = """\
display(
md("### Methods"),
md(f"Using OpenSAFELY-TPP, covering 40% of England's population, we have assessed coding activity related to {marker} between {start_date} and {end_date}. The codelist used can be found here at [OpenSAFELY Codelists](https://codelists.opensafely.org/).  For each month within the study period, we have calculated the rate at which the code was recorded per 1000 registered patients."),
md(f"All analytical code and output is available for inspection at the [OpenSAFELY GitHub repository](https://github.com/opensafely)")
)
"""

get_data = """\
codelist = pd.read_csv(f'../{codelist_path}')

image_paths = {d: f'../output/plot_{d}.png' for d in demographics}
image_paths['total'] = '../output/plot_total.png'
"""

output_total_title = """\
display(
md(f"## Total {marker} Number")
)
"""

output_total_plot = """\
display(Image(filename=image_paths['total']))
"""

output_event_codes = """\
display(
md("### Sub totals by sub codes"),
md("Events for the top 5 subcodes across the study period"))

child_table = pd.read_csv('../output/child_code_table.csv')
child_table
    """

output_practice_title = """\
display(
md("## Total Number by GP Practice")
)
"""

output_practice_plot = """\

practice_table = pd.read_csv('../output/rate_table_practice.csv', parse_dates=['date']).sort_values(by='date')
percentage_practices = get_percentage_practices(practice_table)
md(f"Percentage of practices with a recording of a code within the codelist during the study period: {percentage_practices}%")
display(Image(filename='../output/decile_chart.png'))
"""

nb['cells'] = [
    nbf.v4.new_code_cell(imports),
    nbf.v4.new_code_cell(header),
    nbf.v4.new_code_cell(methods),
    nbf.v4.new_code_cell(get_data),
    nbf.v4.new_code_cell(output_total_title),
    nbf.v4.new_code_cell(output_total_plot),
    nbf.v4.new_code_cell(output_event_codes),
    nbf.v4.new_code_cell(output_practice_title),
    nbf.v4.new_code_cell(output_practice_plot),
    ]

counter = """\
i=0
"""

nb['cells'].append(nbf.v4.new_code_cell(counter))

for d in range(len(demographics)):
    cell_counts = """\
    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    """
    nb['cells'].append(nbf.v4.new_code_cell(cell_counts))
    
    cell_plot = """\
    display(Image(filename=image_paths[demographics[i]]))
    i+=1
    """
    nb['cells'].append(nbf.v4.new_code_cell(cell_plot))


nbf.write(nb, 'analysis/SRO_Notebook.ipynb')