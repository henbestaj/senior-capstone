// creates a bar graph using d3 of 5 turtles, each with a different height. The line that represents the average height
// is also included. The bar graph is interactive, and the user can hover over the bars to see the height of each turtle.
let clutch = [ {height:1, width: 5}, {height:2, width:4}, {height:3, width:3}, {height:4, width:3}, {height:5, width:2}];


let divSelection = d3.select("body") 
    .selectAll("div")    
    .attr("style", "width:90%; background-color:blue; height: 150px");

 divSelection
    .data(clutch)
    .enter()
  .append('div')
    .text(function(d) { 
       return d.height;
	  })
    .attr("class", "bar")
    .style("width", function(d) { return d.width * 50 + "px"; });

