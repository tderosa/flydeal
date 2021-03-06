var weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

var flights = {};
var flight_array = [];

var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var color = d3.scale.category10();

var y = d3.scale.linear()
    .range([height, 0]);

var x = d3.time.scale()
  .range([0, width]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var chart = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class", "chart");
    
var svg = chart
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Setup datasets of (feature, price) point pairs
var duration_set = [];
var day_set = [];
var depart_time_set = [];
var on_time_set = [];

// Open CSV of  airline flight routes, each with a unique (Flight #, Airline) pair
d3.csv('../../data/outputs/price_averages.csv', function(error, data){
  data.forEach(function(d) {
    var i, flight_info;

    // Unique identifier made up of Flight # and Airline
    var fid = d["flight_no"]+"_"+d["airline"];

    // Store feature set and parse applicable feature values
    flight_info = d;
    flight_info["duration"] = parseFloat(d.duration);
    flight_info["price"] = parseFloat(d.price);
    flight_info["avg_on_time"] = parseFloat(d.avg_on_time);
    
    // Set weekday index in range 0-6, when 0 represents Monday and 6 represents Sunday
    flight_info["day_index"] = weekday_names.indexOf(flight_info["most_common_depart_day"])

    var date = new Date();
    var time = d.most_common_depart_time.split(":");
    date.setHours(time[0]);
    date.setMinutes(time[1]);
    flight_info["most_common_depart_time"] = new Date("January 1, 2016 " + date.getHours() + ":" + date.getMinutes() + ":00");

    flights[fid] = flight_info;
    flight_array.push(flight_info);

    // Add each coordinate pair to the appropriate dataset
    duration_set.push([flight_info["duration"], flight_info["price"]]);
    day_set.push([flight_info["day_index"], flight_info["price"]]);
    depart_time_set.push([flight_info["most_common_depart_time"], flight_info["price"]]);
    on_time_set.push([flight_info["avg_on_time"], flight_info["price"]]);
  });

  // Begin with Departure Time vs. Price graph
  var start = d3.min(flight_array, function(d) {return d["most_common_depart_time"]});
  var end = d3.max(flight_array, function(d) {return d["most_common_depart_time"]});
  x.domain([start, end]);

  // Ignore outlier prices to make the most relevant visualization
  y.domain([100, 500])


  // Add points
  svg.selectAll("circle")
      .data(flight_array)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 2.5)
      .attr("cx", function(d) { 
        return x(d["most_common_depart_time"]);
      })
      .attr("cy", function(d) { 
        return y(d["price"]);
      });

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "xaxis label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Departure Time");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Price")


  // Point animations from: http://bl.ocks.org/WilliamQLiu/bd12f73d0b79d70bfbae
  function updatePoints(dataset) {
    xAxis = d3.svg.axis().scale(x).orient("bottom");

    svg.selectAll("circle")
      .data(dataset)  // Update with new data
      .transition()  // Transition from old to new
      .duration(1000)  // Length of animation
      .each("start", function() {  // Start animation
          d3.select(this)  // 'this' means the current element
              .attr("fill", "red")  // Change color
              .attr("r", 5);  // Change size
      })
      .delay(function(d, i) {
          return i / dataset.length * 500;  // Dynamic delay (i.e. each item delays a little longer)
      })
      //.ease("linear")  // Transition easing - default 'variable' (i.e. has acceleration), also: 'circle', 'elastic', 'bounce', 'linear'
      .attr("cx", function(d) {
          return x(d[0]);  // Circle's X
      })
      .attr("cy", function(d) {
          return y(d[1]);  // Circle's Y
      })
      .each("end", function() {  // End animation
          d3.select(this)  // 'this' means the current element
              .transition()
              .duration(500)
              .attr("fill", "black")  // Change color
              .attr("r", 2);  // Change radius
      });

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
  }

  // Change x-axis and update points to new dataset when feature is changed
  function changeFeature(feature) {
    start = d3.min(flight_array, function(d) {return d[feature]});
    end = d3.max(flight_array, function(d) {return d[feature]});
    
    // Depending on what feature is selected, choose the appropriate 
    // dataset, domain, and scale, then update all the points
    switch(feature) {
      case "duration":
        x = d3.scale.linear().range([0, width]);
        x.domain([start,end]);
        d3.select(".xaxis.label").text("Duration");
        updatePoints(duration_set);
        break;
      case "most_common_depart_day":
        x = d3.scale.linear().range([0, width]);
        x.domain([0,6]);
        d3.select(".xaxis.label").text("Day of Week");
        updatePoints(day_set);
        break;      
      case "avg_on_time":
        x = d3.scale.linear().range([0, width]);
        x.domain([start,end]);
        d3.select(".xaxis.label").text("On Time Percentage");
        updatePoints(on_time_set);
        break;
      case "most_common_depart_time":
        x = d3.time.scale().range([0, width]);
        x.domain([start,end]);
        d3.select(".xaxis.label").text("Departure Time");
        updatePoints(depart_time_set);
        break;
      default:
    }
  }

  // When new dropdown value selected call changeFeature with new feature
  $("#feature").change(function(event) {
    changeFeature($("#feature").val());
  });
});