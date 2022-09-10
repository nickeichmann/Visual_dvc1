##import of all the packages
import pandas as pd
import numpy as np
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS

##Task 1
output_file("dvc_ex1.html")
url = "https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/demographics_switzerland_bag.csv"
df = pd.read_csv(url,index_col=0)
print(df)

## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting:
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped


# Filter out rows containing 'CH'
df = df[df["canton"] != "CH"]
##print(df.head())

# Extract unique value lists of canton, age_group and sex
canton = np.unique(df["canton"].tolist())
##print(canton)

age_group = np.unique(df["age_group"].tolist())
##print(age_group)

sex = np.unique(df["sex"].tolist())
##print(sex)


# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = []
for x in canton:
    for y in age_group:
        t = (x, y)
        factors.append(t)
##print(factors)

# Use genders as stack names
stacks = ['male', 'female']

# Calculate total population size as the value for each stack identified by canton,age_group and sex
stack_val = []

for c in canton:
    for a in age_group:
        for s in sex:
            v = df[(df["canton"] == c) & (df["age_group"] == a) & (df["sex"] == s)]
            summe = v["pop_size"].sum()
            stack_val.append(summe)
##print(stack_val)


# Build a ColumnDataSource using above information
male_list = []
female_list = []
counter = 0
for num in stack_val:
    counter += 1
    if counter % 2 == 0:
        male_list.append(num)
    else:
        female_list.append(num)

source = ColumnDataSource(data=dict(
    x=factors,
    male = male_list,
    female = female_list,
))

### Task 2: Data Visualization


## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None


p.vbar_stack(stacks, x='x', width=0.9, alpha=0.5, color=["wheat", "lightseagreen"], source=source,
             legend_label=stacks)

##adjust the sublabels so they don't squeeze
p.xaxis.major_label_orientation = 1.5
##p.xaxis.major_label_text_font_size = "4px"

##adjust the legend
p.legend.label_text_font = "times"
p.legend.location = "top_left"

## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart


hover = HoverTool(
tooltips=[
    ("gender", "$name"),
    ("(canton, age group)", "@x"),
    ("population", "@$name"),
    ],
)
p.add_tools(hover)

output_file("dvc_ex1.html")

show(p)


