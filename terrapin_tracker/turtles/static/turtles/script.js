// function addData() {
//     var rNum = document.getElementById("hatchlings").value;
//     var newRow = document.createElement("tr");
//     var newCell = document.createElement("td");
//     newCell.innerHTML = personName;
//     newRow.append(newCell);
//     document.getElementById("rows").appendChild(newRow);
//     document.getElementById("hatchlings").value = '';
// }

// creates a bar graph using d3 of 5 turtles, each with a different height. The line that represents the average height
// is also included. The bar graph is interactive, and the user can hover over the bars to see the height of each turtle.
var clutch = [ {height:1, width:5}, {height:2, width:4}, {height:3, width:3}, {height:4, width:3}, {height:5, width:2}, {height:6, width:1}];

d3.select('div')
  .text('Select All')
  .style('color', 'red');    
// .selectAll("div");

// divSelection
//     .data(clutch)
//     .enter()
//   .append('div')
//     .text(function(d) { 
//         return d.height ;
//         })
//     .attr("class", "bar")
//     .style("width", function(d) { return d.height * 50 + "px"; });