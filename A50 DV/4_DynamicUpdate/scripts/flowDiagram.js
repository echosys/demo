// this is where your implementation for your flow diagram should go 
function FlowDiagram(svg, data) {
    this.svg = svg;
    
    // grab the bounding box of the container
    var boundingBox = svg.node().getBoundingClientRect();

    //  grab the width and height of our containing SVG
    var svgHeight = boundingBox.height;
    var svgWidth = boundingBox.width;

    //var svg = d3.select("svg"),
    //width = +svg.attr("width"),
    //height = +svg.attr("height"),
    g = svg.append("g")//.attr("transform", "translate(32," + (svgHeight / 2) + ")");

    // this is where your code should go to generate the flow diagram from the random data
    var lastExit;
    this.update = function (data) {
        if (lastExit != undefined){
            lastExit.remove()}

        var t = d3.transition()
        .duration(750)
        
        // DATA JOIN
        // Join new data with old elements, if any.
        var text = g.selectAll("text")
          .data(data, d => d['name'])

        lastExit = text.exit();

        var exitList = lastExit._groups[0]
        delList = exitList.filter(function (el) {
            return el != null;
          });

        lastExit
            .attr("class", "update")
        .transition(t)
            .attr("x", "400")
            .attr("y", function(d, i) {
                if (delList.includes(exitList[i]) ){
                    return (delList.indexOf(exitList[i])+1) * 15
                }else{
                    return (delList.length+1) * 15 }
            })
            //.attr("dy", ".35em")
            //.merge(text)
            .text(function(d) { return d.name; })
            .attr("fill", "red");
        // EXIT
        // Remove old elements as needed.
        //text.exit().remove();


        // UPDATE
        // Update old elements as needed.
        text
            .transition(t)
            .attr("x", "200") 
            .attr("y", function(d, i) { 
                return (i+1) * 15; })
            .attr("fill", "orange");
      
        // ENTER
        // Create new elements as needed.
        //
        // ENTER + UPDATE
        // After merging the entered elements with the update selection,
        // apply operations to both.

        //text.enter()._groups[0][28].__data__.name
        var newList = text.enter()._groups[0],
        newIndex = newList.length;
        for (i = 0; i < newList.length; i++) {
            if (newList[i] != undefined && i < newIndex){
                newIndex = i
            }
        } 
        text.enter()
            .append("text")
            .attr("class", "enter")
        .transition(t)
            .attr("x", "0")
            //.attr("x", function(d, i) { return i * 0; })
            .attr("y", function(d, i) {
                if (i<newIndex){
                    return 0
                }else{
                    return (i - newIndex+1) * 15}
            })
            //.attr("dy", ".35em")
            //.merge(text)
            .text(function(d) { return d.name; })
            .attr("fill", "green");
        

        

      }
      
      // The initial display.
      this.update(data);
}
