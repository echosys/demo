// Set the dimensions of the canvas / graph

var margin = {top: 10, right: 20, bottom: 50, left: 50},
    width = 800 - margin.left - margin.right,
    height = 470 - margin.top - margin.bottom;

// parse the lifeExp / time
var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var x = d3.scaleLog().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// define the line
var valueline = d3.line()
    .x(function(d) { return x(d.lifeExp); })
    .y(function(d) { return y(d.close); });

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("body").select(".center")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Get the data
//d3.csv("data/dates.csv", function(error, data) {
d3.tsv("data/gapminderDataFiveYear.tsv", function(error, data) {
    if (error) throw error;

    // format the data (i.e., process it such that strings are converted to their appropriate types)
    data.forEach(function(d) {
        d.lifeExp = +d.lifeExp;
        d.gdpPercap = +d.gdpPercap;
        d.year = parseInt(d.year)
        d.pop = +d.pop
    });

    // Scale the range of the data
    //x.domain(d3.extent(data, function(d) { return d.lifeExp; }));
    //y.domain([0, d3.max(data, function(d) { return d.close; })]);
    x.domain(d3.extent(data, function(d) { 
        if (d.year == 2007 || d.year == 1952){
            return d.gdpPercap;}
        }));
    y.domain(d3.extent(data, function(d) {
        if (d.year == 2007 || d.year == 1952){
            return d.lifeExp;}
        }) );


    // Add the valueline path.
    // svg.append("path")
    //     .data([data])
    //     .attr("class", "line")
    //     .attr("d", valueline);

    var color = d3.scaleOrdinal(d3.schemeCategory10);
    // Add the scatterplot
    svg.selectAll("dot")
        .data(data)
        .enter().append("circle")

        .filter(function(d) {
            if(d.year == 2007 || d.year == 1952){
            //console.log(d.gdpPercap)   
            return d; }
        })

        //.attr("r", 5)
        .attr("r", function(d){ 
            maxValue = d3.max(data, function(d) { return d.pop; }) ;
            minValue = d3.min(data, function(d) { return d.pop; }) ;
            circleRadiusScale = d3.scaleLinear()
                .domain([minValue, maxValue])
                .range([4, 10]);
            //cr = circleRadiusScale(d.pop)
            return circleRadiusScale(d.pop); })

        //.attr("cx", function(d) { return x(d.lifeExp); })
        //.attr("cy", function(d) { return y(d.close); });
        .attr("cy", function(d) { return y(d.lifeExp); })
        .attr("cx", function(d) { return x(d.gdpPercap); })
        .style("fill", function(d){ return d.year == 2007 ? color(0) : color(1) })
        .attr("fill-opacity","0.8")
        .attr("data-legend",function(d) { return d.year})


    // Add the X Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(11, ".0s"));
    
    svg.select(".x.axis")
        .style("font", "14px Lato")
    
    svg.append("text")
        .attr("transform",
                "translate(" + (width/2) + " ," + 
                            (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .style("font", "14px sans-serif")
        .style("font-weight", "700")
        
        .text("GDP per Capita");

    // Add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));
        svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .style("text-anchor", "middle")
        .attr("dy", "1em")
        .style("font", "14px sans-serif")
        .style("font-weight", "700")
        .text("Life Expectancy"); 
    
    // Add title
    svg.append("text")
        .attr("x", (width / 2))    
        //.attr("y", 0 - (margin.top))         
        .attr("y", 0 + (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font", "16px sans-serif")
        //.style("font-size", "16px") 
        .style("font-weight", "700")
        .style("text-decoration", "underline")  
        .text("GDP vs Life Expectancy (1952, 2007)");

    // Add legend
    var legendRectSize = 18;                               
    var legendSpacing = 4;                                  

    var legend = svg.selectAll('.legend')                 
        //.data(color.domain())      if data then all year shown   
        .data(color.domain())                            
        .enter()                                              
        .append('g')                                          
        .attr('class', 'legend')                              
        .attr('transform', function(d, i) {                   
        var height = legendRectSize + legendSpacing;        
        var offset =  height * color.domain().length / 2;   
        var horz = -2 * legendRectSize + width;                     
        var vert = i * height + offset;                     
        return 'translate(' + horz + ',' + vert + ')';      
        });                                                   

    legend.append('rect')                                 
        .attr('width', legendRectSize)                        
        .attr('height', legendRectSize)                       
        .style('fill', color)                                 
        .style('stroke', color);                              
    
    legend.append('text')                                 
        .attr('x', legendRectSize + legendSpacing)            
        .attr('y', legendRectSize - legendSpacing)            
        .text(function(d) { return d == 0 ? 2007 : 1952 });  
});
