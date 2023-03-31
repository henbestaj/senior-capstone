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


// <script>
//             var hatchlings = ['3-1', '3-2', '3-3','3-4',"6-1","6-2","6-3","6-4","6-5","6-6","6-7",
//             "6-8","6-9","6-10","6-11","6-12","6-13","6-14","6-15","6-16","6-17","6-18","6-19","7-1","7-2","7-3","7-4",
//             "7-5","8-1","8-2","8-3","8-4","8-5","9-1","9-2","9-3","9-4","9-5","10-1","10-2","10-3","10-4","10-5","11-1",
//             "11-2","11-3","11-4","11-5","12-1","12-2","12-3","12-4","12-5","13-1","13-2","13-3","13-4","13-5","13-6",
//             "13-7","13-8","13-9","13-10","13-11","14-1","14-2"];
//             function remake() {
//             var count = 0;
//             for (var i =0; i<hatchlings.length; i++) {
//                 if (i==0) {
//                     document.getElementById("rows").createElement('tr');
//                 }
//                 if (count<=6) {
//                     var newCell = document.createElement("td");
//                     newCell.innerHTML = hatchlings[i];
//                     newRow.append(newCell)
//                     count+=1;
//                 }
//                 else {
//                     var newRow = document.createElement("tr");
//                     var newCell = document.createElement("td");
//                     newCell.innerHTML = hatchlings[i];
//                     newRow.append(newCell);
//                     document.getElementById("rows").appendChild(newRow);
//                     count = 0;
//                 }   
//             }
//         }
//         </script>

