//typically the chart creation would happen in a callback, like the commented out line below,
//but is not needed here if the chart is draw well after  the page loads

google.load("visualization", "1", {packages:["corechart"]});
//google.setOnLoadCallback(drawChart);

console.log("draw chart present")

// mode: 0 = all data, 1 = elapsed data, 2 = zoom to most recent data
function drawChart(data, progress, mode) {
      console.log(progress)

/*      let zoomData = {}
      if(mode == 1){
        for (let d = 10; d >= 0; d--){
          zoomData[Object.keys(data)[Object.keys(data).length-d]] = data[Object.keys(data)[Object.keys(data).length-d]]
        }
      }

      data = zoomData*/

      //console.log(zoomData)

      let cData = new google.visualization.DataTable();
      //console.log(data)
      dKeys = Object.keys(data)

      //console.log(progress)
      //needs to be a date type if the issue is fixed
      cData.addColumn('date', 'X');
      cData.addColumn('number', 'PWM Val');
      cData.addColumn('number', 'progress');//this draws a different color line over the primary one
/*      cData.addColumn('number', 'Cats');*/

      //progress bar data
      for (let d=0;d<dKeys.length;d++){
        //console.log(data[dKeys[d]])
        //cData.addRow([d,data[dKeys[d]]])

        if(mode == 0){
          if( d <= (dKeys.length*progress*.01)){
            cData.addRow([new Date(dKeys[d]),data[dKeys[d]],data[dKeys[d]]])
          } else {
            cData.addRow([new Date(dKeys[d]),data[dKeys[d]],null])
            }
        } else if (mode == 1){
          if( d <= (dKeys.length*progress*.01)){
            cData.addRow([new Date(dKeys[d]),data[dKeys[d]],data[dKeys[d]]])
          } 
        } else if (mode == 2){
          if( d > (dKeys.length*progress*.01)-10 && d <= (dKeys.length*progress*.01)){
            cData.addRow([new Date(dKeys[d]),data[dKeys[d]],data[dKeys[d]]])
          } 
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
        lineWidth: [3],
        colors: ['black', 'yellow']
      };

      //var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));

      chart.draw(cData, options);
    }