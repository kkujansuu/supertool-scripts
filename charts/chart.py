# See e.g.
# https://developers.google.com/chart/interactive/docs/gallery/barchart

import tempfile

from gramps.gui import utils

html = """
<html lang="fi">
  <head>
    <title>%(header)s - %(title)s</title>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <link type="text/css" rel="stylesheet" href="/css/style.css"/>
    
    <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawCharts);

      function drawCharts() {
        drawChart1();
      }

      function drawChart1() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'X');
        for (var name of %(colnames)s) {
            data.addColumn('number', name);
            data.addColumn({type:'number', role:'annotation'});
        }
        data.addRows(
        
            %(rows)s
        
        );

        var options = {
          width: 1000, height: 400,
          title: '%(title)s'
        };

        var chart = new google.visualization.%(charttype)s(document.getElementById('chart_div1'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <h1>%(header)s</h1>
    <p>
    <div id="chart_div1"></div>
  </body>
</html>
"""


def open_file(filename):
    utils.open_file_with_default_application(filename, uistate)

def drawgraph(header, title, colnames, rows, charttype="ColumnChart"):

    """
    rows = [
        [label, value1, value2, ...],
        ...
    ]
    """

    with tempfile.NamedTemporaryFile(suffix=".html") as fp:
        fname = fp.name
    
    # add annotations:
    rows2 = []
    for [label, *values] in rows:
        row = [label]
        for v in values:
            row.append(v)  # value
            row.append(v)  # annotation
        rows2.append(row)
    html2 = html % {
        "header": header,
        "title": title,
        "colnames": repr(colnames),
        "rows": rows2,
        "charttype": charttype}
    open(fname,"w").write(html2)
    open_file(fname)

