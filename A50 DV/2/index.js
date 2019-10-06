// Set the dimensions of the canvas / graph

const color = d3.scaleOrdinal(d3.schemeCategory10);
var a = color(3)
var b = color(4)

var margin = {top: 10, right: 20, bottom: 50, left: 50},
    width = 800 - margin.left - margin.right,
    height = 470 - margin.top - margin.bottom;

// parse the date / time
// var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var x = d3.scaleLog().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);
var z = d3.scaleQuantile().domain(0, 100000000).range([4, 5, 6, 7, ,8, 9, 10])

// define the line
// var valueline = d3.line()
//     .x(function(d) { return x(d.gdpPercap); })
//     .y(function(d) { return y(d.lifeExp); });

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("body").select("div").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.tsv("data/gapminderDataFiveYear.tsv", function(error, data) {
    if (error) throw error;

    // format the data (i.e., process it such that strings are converted to their appropriate types)
    data.forEach(function(d) {
        d.gdpPercap = +d.gdpPercap;
        d.lifeExp = +d.lifeExp;
        d.pop = +d.pop
    });

    // Scale the range of the data
    // x.domain(d3.extent(data, function(d) { return d.gdpPercap; }));
    x.domain([d3.min(data, function(d) { return d.gdpPercap; }), d3.max(data, function(d) { return d.gdpPercap; })]);
    y.domain([d3.min(data, function(d) { return d.lifeExp; }), d3.max(data, function(d) { return d.lifeExp; })]);
    z.domain([d3.min(data, function(d) { return d.pop; }), d3.max(data, function(d) { return d.pop; })])
    // z.domain(0, 100000000).range([4, 10])
    // Add the valueline path.
    // svg.append("path")
    //     .data([data])
    //     .attr("class", "line")
    //     .attr("d", valueline);

    // Add the scatterplot
    svg.selectAll("dot")
        .data(data)
        .enter().append("circle")
        .filter(function(d) { return d.year == "1952"})
        .style("fill", a)
        .style("opacity", 0.8)
        .attr("r", function(d) { return z(d.pop); })
        .attr("cx", function(d) { return x(d.gdpPercap); })
        .attr("cy", function(d) { return y(d.lifeExp); });

    svg.selectAll("dot")
        .data(data)
        .enter().append("circle")
        .filter(function(d) { return d.year == "2007"})
        .style("fill", b)
        .style("opacity", 0.8)
        .attr("r", function(d) { return z(d.pop); })
        .attr("cx", function(d) { return x(d.gdpPercap); })
        .attr("cy", function(d) { return y(d.lifeExp); });

    // Add the X Axis
    // var xaxis = d3.axisBottom(x)
        // .ticks(11)
        // .tickValues([300, 400, 1000, 2000, 3000, 4000, 10000, 20000, 30000, 40000, 100000])
        // .tickFormat(d3.format(".0s"));
        // .tickArguments([10])
    // svg.append("g")
        // .attr("transform", "translate(0," + height + ")")
        // .style("font-family", "Lato")
        // .call(d3.axisBottom(x).tickFormat(d3.format(".0s")).ticks(11));

//     svg.append("g")
//         .attr("transform", "translate(0," + height + ")")
//         .call(d3.axisBottom(x).ticks(11, '.0s') )

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(11).tickFormat(d3.format('.0s')) )

        //.call(d3.axisBottom(x).ticks(11).tickFormat(d3.format('.0s')) )

        //.call(d3.axisBottom(x).ticks(11) )
        //.call(d3.axisBottom(x).tickFormat(d3.format('.0s')) ); //.tickFormat(d3.format(".0s")));

    svg.append("text")
        .text("GDP per Capita")
        .attr("transform","translate(0,"+ (height+38) +")")
        .attr("x", width/2-50)
        .style("font-family", "sans-serif")
        .style("font-size", 14)
        .style("font-weight", 700)
        // .style("text-anchor", "middle")
        

    // Add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y))
    svg.append("text")
        .text("Life Expectancy")
        .attr("transform", "rotate(-90)")
        .attr("dx", -250)
        // .style("text-anchor", "middle")
        .attr("dy", -35)
        .style("font-family", "sans-serif")
        .style("font-size", 14)
        .style("font-weight", 700);


    // Add the title and the legend
    svg.append("text")
        .text("GDP vs Life Expectancy (1952, 2007)")
        .attr("dx", 200)
        .attr("dy", 10)
        .style("font-family", "sans-serif")
        .style("font-size", 16)
        .style("font-weight", 700)
        .style("text-decoration", "underline");

    var legend = svg.append("g")
      .attr("class", "legend")
      .attr("x", width)
      .attr("y", 20)
      .attr("height", 100)
      .attr("width", 100);

    legend.append("rect")
      .attr("x", width-40)
      .attr("y", 20)
      .attr("width", 15)
      .attr("height", 15)
      .style("fill", a);

    legend.append("text")
      .attr("x", width-25)
      .attr("y", 30)
      .text("1952")
      .style("font-size", 10);

    legend.append("rect")
      .attr("x", width-40)
      .attr("y", 40)
      .attr("width", 15)
      .attr("height", 15)
      .style("fill", b);

    legend.append("text")
      .attr("x", width-25)
      .attr("y", 50)
      .text("2007")
      .style("font-size", 10);
});
