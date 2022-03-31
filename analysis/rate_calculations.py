from utilities import *
from pathlib import Path
import pandas as pd
import os
from cohortextractor import Measure
from config import demographics, codelist_path, qof_measure_marker, vertical_lines
from ebmdatalab import charts

from study_definition import measures

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

# Add demographics measures

for d in demographics:

    m = Measure(
        id=f"{d}_rate", numerator="event", denominator="population", group_by=[d]
    )

    measures.append(m)

measures_dict = {}

for m in measures:
    measures_dict[m.id] = m

for key, value in measures_dict.items():

    df = pd.read_csv(
        os.path.join(OUTPUT_DIR, f"measure_{value.id}.csv"), parse_dates=["date"]
    ).sort_values(by="date")
    df = drop_missing_demographics(df, value.group_by[0])

    if key == "ethnicity_rate":
        df = convert_ethnicity(df)

    df = calculate_rate(
        df, numerator=value.numerator, denominator=value.denominator, rate_per=1
    )

    if key == "imd_rate":
        df = calculate_imd_group(df, value.numerator, "rate")
        df = redact_small_numbers(df, 5, value.numerator, value.denominator, "rate")

    elif key == "care_home_status_rate":
        df = convert_binary(
            df,
            "care_home_status",
            "Record of positive care home status",
            "No record of positive care home status",
        )

    elif key == "learning_disability_rate":
        df = convert_binary(
            df,
            "learning_disability",
            "Record of learning disability",
            "No record of learning disability",
        )

    elif key == "age_band_rate":
        df = df[df["age_band"] != "missing"]
        df = redact_small_numbers(df, 5, value.numerator, value.denominator, "rate")
        df.to_csv(
            os.path.join(OUTPUT_DIR, f"rate_table_{value.group_by[0]}.csv"), index=False
        )

    # get total population rate
    if value.id == "practice_rate":
        df = calculate_rate(
            df, numerator=value.numerator, denominator=value.denominator, rate_per=1
        )
        df = drop_irrelevant_practices(df, "practice")
        df.to_csv(
            os.path.join(OUTPUT_DIR, f"rate_table_{value.group_by[0]}.csv"), index=False
        )

        bp002_decile_chart = charts.deciles_chart(
            df,
            period_column="date",
            column="rate",
            title=None,
            ylabel=None,
            show_outer_percentiles=False,
            show_legend=True,
        )

        add_date_lines(bp002_decile_chart, vertical_lines)
        bp002_decile_chart.gcf().set_size_inches(15, 8)
        bp002_decile_chart.gca().set_yticklabels(
            ["{:.0f}%".format(x * 100) for x in bp002_decile_chart.gca().get_yticks()]
        )
        # bp002_decile_chart.gca().set_xticklabels(bp002_decile_chart.gca().get_yticks(), rotation='horizontal')
        # bp002_decile_chart.gca().xaxis.set_major_formatter(
        #     mdates.ConciseDateFormatter(bp002_decile_chart.gca().xaxis.get_major_locator()))

        bp002_decile_chart.rc("font", size=16)
        bp002_decile_chart.rc("axes", titlesize=16)
        bp002_decile_chart.rc("axes", labelsize=16)
        bp002_decile_chart.rc("xtick", labelsize=16)
        bp002_decile_chart.rc("ytick", labelsize=16)
        bp002_decile_chart.rc("legend", fontsize=16)
        bp002_decile_chart.rc("figure", titlesize=16)

        bp002_decile_chart.savefig("output/decile_chart.png", bbox_inches="tight")

        df_total = (
            df.groupby(by="date")[[value.numerator, value.denominator]]
            .sum()
            .reset_index()
        )
        df_total = calculate_rate(
            df_total,
            numerator=value.numerator,
            denominator=value.denominator,
            rate_per=1,
        )

        plot_measures(
            df_total,
            filename="plot_total.png",
            title=None,
            column_to_plot="rate",
            category=None,
            y_label=None,
            autoscale=False,
            vlines=vertical_lines
        )

        df_total.to_csv(os.path.join(OUTPUT_DIR, "rate_table_total.csv"), index=False)

    elif value.id == "event_code_rate":
        df.to_csv(
            os.path.join(OUTPUT_DIR, f"rate_table_{value.group_by[0]}.csv"), index=False
        )
        codelist = pd.read_csv(codelist_path)
        child_code_table = create_child_table(
            df=df, code_df=codelist, code_column="code", term_column="term"
        )
        child_code_table.to_csv("output/child_code_table.csv", index=False)

    else:
        plot_measures(
            df,
            filename=f"plot_{value.group_by[0]}.png",
            title=None,
            # title=f'Breakdown of {qof_measure_marker} by {value.group_by[0]}',
            column_to_plot="rate",
            category=value.group_by[0],
            y_label=None,
            vlines=vertical_lines
        )

        df.to_csv(
            os.path.join(OUTPUT_DIR, f"rate_table_{value.group_by[0]}.csv"), index=False
        )
