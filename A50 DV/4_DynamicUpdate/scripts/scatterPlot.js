// this is where your implementation for your scatter plot should go 
function ScatterPlot(svg, data){//, updateFlowDiagram) {

    var margins = {
        top: 30,
        bottom: 30,
        left: 30,
        right: 30
    };

    this.svg = svg;
    
    // grab the bounding box of the container
    var boundingBox = svg.node().getBoundingClientRect();

    //  grab the width and height of our containing SVG
    var svgHeight = boundingBox.height;
    var svgWidth = boundingBox.width;

    // this is where your code should go to generate the flow diagram from the random data
    var lastExit;
    this.drawReg = function(){};
    var myLine = 1;

    this.draw = function (data) {
        
        //scatter plot 
        var canvas_width = svgHeight;
        var canvas_height = svgWidth;
        var padding = 30;  // for chart edges

        // Create scale functions
        var xScale = d3.scaleLinear()  // xScale is width of graphic
            .domain(d3.extent(data, function(d) {
                return d.v0;  // input domain
            }))
            .range([padding, canvas_width - padding * 2]); 
            // output range

        var yScale = d3.scaleLinear()  // yScale is height of graphic
            .domain(d3.extent(data, function(d) {
                return d.v1;  // input domain
            }))
            .range([canvas_height - padding, padding]);  
            // remember y starts on top going down so we flip

        // Define X axis
        var xAxis = d3.axisBottom()
            .scale(xScale)
            .ticks(9);
            //.ticks(9, ".0s");

        // Define Y axis
        var yAxis = d3.axisLeft()
            .scale(yScale)
            .ticks(9);
            //.ticks(9, ".0s");

        // Create Circles
        var myCircle  = svg.selectAll("circle")
            .data(data)

        myCircle    
            .enter()
            .append("circle")  // Add circle svg
            .attr("cx", function(d) {
                return xScale(d.v0);  // Circle's X
            })
            .attr("cy", function(d) {  // Circle's Y
                return yScale(d.v1);
            })
            .attr("r", 5)  // radius
            .attr("fill", "green")
        

        
        // Add to X axis
        svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (canvas_height - padding) +")")
        .call(xAxis);

        // Add to Y axis
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + padding +",0)")
            .call(yAxis);

        //debug tooltip
        //var tooltip = svg.append("div")     //you can not append div to svg
        var tooltip = d3.select("body")
            .append("div") 
            .attr("class", "tooltip")
            .style("opacity", 0);

        var tipMouseout = function(d) {
            tooltip.transition()
                .duration(300) // ms
                .style("opacity", 0.5); // don't care about position!
        };

        var tipMouseover = function(d) {
            //var color = colorScale(d.manufacturer);
            var html  = d.name + "<br/>" +
                d.v0 + "<br/>" +
                d.v1 + "<br/>";

            tooltip.html(html)
                .style("left", (d3.event.pageX + 15) + "px")
                .style("top", (d3.event.pageY - 28) + "px")
                .transition()
                .duration(200) // ms
                .style("opacity", .9) // started as 0!
        };    

        svg.selectAll("circle")
            .on("mouseover", tipMouseover)
            .on("mouseout", tipMouseout);
        
    this.update = function (data) {
            // Update scale domains
            xScale.domain(d3.extent(data, function(d) {
                return d.v0; }));
            yScale.domain(d3.extent(data, function(d) {
                return d.v1; }));

        // Update circles
        myCircle = svg.selectAll("circle")
            .data(data, function(d){
                return d.id;
            })  // Update with new data
        myCircle
            .transition()  // Transition from old to new
            .duration(1000)  // Length of animation
            .on("start", function() {  // Start animation
                d3.select(this)  // 'this' means the current element
                    .attr("fill", "orange")  // Change color
                    .attr("r", 6);  // Change size
            })
            .delay(function(d, i) {
                return i / data.length * 500;  // Dynamic delay (i.e. each item delays a little longer)
            })
            //.ease("linear")  // Transition easing - default 'variable' (i.e. has acceleration), also: 'circle', 'elastic', 'bounce', 'linear'
            .attr("cx", function(d) {
                return xScale(d.v0);  // Circle's X
            })
            .attr("cy", function(d) {
                return yScale(d.v1);  // Circle's Y
            })
            .on("end", function() {  // End animation
                d3.select(this)  // 'this' means the current element
                    .transition()
                    .duration(500)
                    .attr("fill", "orange")  // Change color
                    .attr("r", 5);  // Change radius
            });
        
        myCircle.enter()    
            .append("circle")  // Add circle svg
            .attr("cx", function(d) {
                return xScale(d.v0);  // Circle's X
            })
            .attr("cy", function(d) {  // Circle's Y
                return yScale(d.v1);
            })
            .attr("r", 5)  // radius
            .attr("fill", "green")
            .on("mouseover", tipMouseover)
            .on("mouseout", tipMouseout);
        
        myCircle.exit()    
            //.append("circle")  // Add circle svg
            .attr("cx", function(d) {
                return xScale(d.v0);  // Circle's X
            })
            .attr("cy", function(d) {  // Circle's Y
                return yScale(d.v1);
            })
            .attr("r", 5)  // radius
            .attr("fill", "red")
            .remove()

        // Update X Axis
        svg.select(".x.axis")
            .transition()
            .duration(1000)
            .call(xAxis);

        // Update Y Axis
        svg.select(".y.axis")
            .transition()
            .duration(100)
            .call(yAxis);           
        
        this.drawReg()
        }//this.update
        this.drawReg = function (){
            if(myLine != 1){
                myLine.remove()}
            function linearRegression(y,x){

                var lr = {};
                var n = y.length;
                var sum_x = 0;
                var sum_y = 0;
                var sum_xy = 0;
                var sum_xx = 0;
                var sum_yy = 0;
        
                for (var i = 0; i < y.length; i++) {
        
                    sum_x += x[i];
                    sum_y += y[i];
                    sum_xy += (x[i]*y[i]);
                    sum_xx += (x[i]*x[i]);
                    sum_yy += (y[i]*y[i]);
                } 
        
                lr['slope'] = (n * sum_xy - sum_x * sum_y) / (n*sum_xx - sum_x * sum_x);
                lr['intercept'] = (sum_y - lr.slope * sum_x)/n;
                lr['r2'] = Math.pow((n*sum_xy - sum_x*sum_y)/Math.sqrt((n*sum_xx-sum_x*sum_x)*(n*sum_yy-sum_y*sum_y)),2);
        
                return lr;
        
            };//linearRegression
            
            var yval = data.map(function (d) { return parseFloat(d.v1); });
            var xval = data.map(function (d) { return parseFloat(d.v0); });
            
            
            var lr = linearRegression(yval,xval);

            var max = d3.max(data, function (d) { return d.v0; });
            myLine = svg.append("svg:line")
                        .attr("x1", xScale(0))
                        .attr("y1", yScale(lr.intercept))
                        .attr("x2", xScale(max))
                        .attr("y2", yScale( (max * lr.slope) + lr.intercept ))
                        .style("stroke-dasharray", ("3, 3"))
                        //.style("stroke", "black");
        }//drawReg
        this.drawReg()

      }//this.draw
      
      // The initial display.
      this.draw(data);
}
