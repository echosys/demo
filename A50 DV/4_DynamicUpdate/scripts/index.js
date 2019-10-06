// This is what you could consider the "central control" file 

// global variables for our visualizations
var flowDiagram = undefined;
var scatterPlot = undefined;

// only called once, to instantiate your charts
function initCharts(data) {
    // instantiate the flow diagram, and send it the container it should exist in (.flow)
    flowDiagram = new FlowDiagram(d3.select('.flow'), data);
     
    // instantiate the scatter plot, and send it the container it should exist in (.scatter)
    scatterPlot = new ScatterPlot(d3.select('.scatter'), data);
}

// called every time the data updates
function tickDataFlow(newData) {
    console.log("Data updated:", newData);
    
    // you'll probably want to implement these functions and call them :) 
    //scatterPlot.draw(newData);
    //flowDiagram.draw(newData);
}
