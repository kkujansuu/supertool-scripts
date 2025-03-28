Charts
------

Author: kari.kujansuu@gmail.com<br>
2025

Here are some sample scripts that can generate charts using the Google chart tools (e.g. https://developers.google.com/chart/interactive/docs/gallery/barchart). These can be used to display some statistics of a Gramps family tree.

Load a script into SuperTool, possibly adjust some parameters in the "Initialization statements" section and press Execute. The script generates a temporary HTML file with Javascript code that draws the chart. The script then invokes a web browser to display the chart. 

### Implementation details

The scripts use the auxiliary code in <code>chart.py</code> which contains the function <code>drawgraph</code>. The function should be called with the arguments:

    1. Header for the page. The examples use the database name.
    2. Title of the graph
    3. List of column names.
    4. The data to be displayed. A list of tuples (or lists). The tuples are (itemlabel, colvalue1, colvalue2, ...).
    5. The type of the chart. Default "ColumnChart". Possible values are at least "ColumnChart", "BarChart", "PieChart" and "LineChart".

***
Examples below:


1. Place Types
2. Event Types
3. Event Places
4. Age statistics
5. Birth Years
6. Occupation statistics

***

### Place Types

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/placetype-statistics-graph.script

Simple column chart that shows which place types are used. This should be run in the Places category. The result could be like:

![Charts](images/placetype-statistics-graph.png)

***

### Event Types

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/eventtype-statistics-graph.script

A pie chart that shows which event types are used. This should be run in the Events category. The result could be like:

![Charts](images/eventtype-statistics-graph.png)

***

### Event Places

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/event-place-statistics-graph.script

Simple chart that shows the most common places used in events. This should be run in the Events category.

Note that the parameter MIN_COUNT excludes places
that appear in fewer than 20 events. The result could be like:

![Charts](images/event-place-statistics-graph.png)

Apparently Ottawa is the most common place. You might be interested to see the types of events. Here is a slightly
enhanced script:

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/event-place-statistics-graph2.script

which gives:

![Charts](images/event-place-statistics-graph2.png)

***

### Age statistics

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/age-statistics-graph.script

Number of deaths by age and by gender. This should be run in the People category.

![Charts](images/age-statistics.png)


***

### Birth years

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/birth-year-statistics-graph.script

Number of people by birth decade. This should be run in the People category.

![Charts](images/birth-year-statistics.png)

***

### Occupation statistics

https://github.com/kkujansuu/supertool-scripts/blob/main/charts/occupation-statistics-graph.script

Number of people with the most common occupations by birth year. This should be run in the Events category.

The script uses these constants defined in a the beginning of the script:

	START_YEAR = 1800
	END_YEAR = 1900
	SPAN = 25 # years
	NUM_OCCUPS = 6

The script assumes that occupations are events of type Occupation and the occupation (e.g. "farmer") is stored in the description field of the event.

The script finds NUM_OCCUPS most common occupations within the years START_YEAR - END_YEAR. Then it divides the year range in spans of SPAN years and displays the number of the occupations within each year span. Example: 
 
![Charts](images/occupation-statistics.png)



