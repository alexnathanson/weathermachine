//typically the chart creation would happen in a callback, like the commented out line below,
//but is not needed here if the chart is draw well after  the page loads

google.load("visualization", "1", {packages:["corechart"]});
//google.setOnLoadCallback(drawChart);

console.log("draw chart present")

function drawChart(data, progress) {
      let cData = new google.visualization.DataTable();
      //console.log(data)
      dKeys = Object.keys(data)

      //console.log(progress)
      //needs to be a date type if the issue is fixed
      cData.addColumn('date', 'X');
      cData.addColumn('number', 'PWM Val');
      cData.addColumn('number', 'progress');//this draws a different color line over the primary one
/*      cData.addColumn('number', 'Cats');*/

      for (let d=0;d<dKeys.length;d++){
        //console.log(data[dKeys[d]])
        //cData.addRow([d,data[dKeys[d]]])
        if( d <= (dKeys.length*progress*.01)){
          cData.addRow([new Date(dKeys[d]),data[dKeys[d]],data[dKeys[d]]])
        } else {
          cData.addRow([new Date(dKeys[d]),data[dKeys[d]],null])
        }
      }

      //good annotation stuff here: https://stackoverflow.com/questions/17845607/google-charts-line-graph-points
      var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Light'
        },
        lineWidth: 3,
        colors: ['black', 'yellow']
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(cData, options);
    }