var width = 900,
    height = 500,
    centered;


// MAP PROJECTION -- using standard TopoJSON code
var projection = d3.geo.albersUsa()
    .scale(1070)
    .translate([width / 2, height / 2]);

var path = d3.geo.path()
    .projection(projection);

var graticule = d3.geo.graticule();


// SVG -- attach svg to doc and append groups for viz elements
var svg = d3.select("#viz").append("svg")
    .attr("width", width)
    .attr("height", height);

var g = svg.append("g");
var colors = ["#f0f9e8","#bae4bc","#7bccc4","#43a2ca","#0868ac"];
var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
var stateGroup = g.append('g');
var routesGroup = g.append('g');
var airportGroup = g.append('g');

// COLOR SCALING -- set threshold values for delay times
var scale = d3.scale.threshold()
  .domain([15,30,60,90])
  .range(colors); 

d3.json("../lib/us.json", function(error, us) {
  // DRAW MAP -- Mike Bostock's TopoJSON code
  stateGroup.append("g")
    .attr("id", "states")
  .selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
  .enter().append("path")
    .attr("d", path);

  stateGroup.append("path")
    .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
    .attr("id", "state-borders")
    .attr("d", path);


  d3.csv("../../data/outputs/mon_year_delays.csv", function(error, mon_data) {
    // cast data to proper types
    for (var i=0;i<mon_data.length;i++) {
      d = mon_data[i];
      d.Avg_Delay = +d.Avg_Delay < 0.0 ? d.Avg_Delay = 0.0 : d.Avg_Delay = +d.Avg_Delay;
      d.Org_Lat = +d.Org_Lat;
      d.Org_Lon = +d.Org_Lon;
      d.Dest_Lat = +d.Dest_Lat;
      d.Dest_Lon = +d.Dest_Lon;
      d.Fl_date = new Date(d.Year + "-" + d.Month);
      d.Month = +d.Month;
    }

    // Nest data by flight date
    var by_date = d3.nest()
      .key(function(d) { return d.Fl_date; })
      .sortValues(function(a,b) { return a.Avg_Delay - b.Avg_Delay; } )
      .entries(mon_data);

    // Sorts entries by date
    function sortByDateAscending(a, b) {return new Date(a.key) - new Date(b.key);}
    by_date = by_date.sort(sortByDateAscending);

    // Nest data by airports
    var by_airport = d3.nest()
      .key(function(d) { return d.Origin; })
      .map(mon_data);

    // Axis formatting -- axis labels by Mon Year
    var dateFormat = d3.time.format("%b %Y");
    var tickFormat = function(d) {
      var date = new Date(by_date[d].key);
      return dateFormat(date);
    }

    // Instantiate d3 slider
    var slider = d3.select('#axis').call(d3.slider()
      .axis(d3.svg.axis().ticks(12).tickFormat(tickFormat))
      .min(0).max(35)
      .step(1)
      // Slide event -- update route colors
      .on("slide", function(evt, value) {
        updateRoutes(by_date[value]);
      })
    );

    // Updates route colors based on delay time
    function updateRoutes(routeData) {
      d3.select("#current_time").text(dateFormat(new Date(routeData.key)));

      svg.selectAll("line")
        .data(routeData.values)
        .attr("stroke",function(d) {
          var pt = d.values;
          return scale(d.Avg_Delay);
      });
    } 

    // Draws routes  
    function draw(routeData) {

      d3.selectAll("line").remove();
      routesGroup.selectAll("line")
        .data(routeData.values)
        .enter().append('line')
        .attr("x1", function(d) {
            return projection([ d.Org_Lon, d.Org_Lat ])[0];
        })
        .attr("y1", function(d) {
            return projection([ d.Org_Lon, d.Org_Lat])[1];
        })
        .attr("x2", function(d) {
            return projection([ d.Dest_Lon, d.Dest_Lat ])[0];
        })
        .attr("y2", function(d) {
            return projection([ d.Dest_Lon, d.Dest_Lat ])[1];
        })
        .attr("class",function(d) {
          return d.Origin; 
        })
        .attr("stroke-width", 1.5)
        .attr("stroke", function(d) {
            return scale(d.Avg_Delay);
        })
      } 

      draw(by_date[0]);

    d3.csv("../../data/domestic_airports.csv", function(error, airport_data) {
      // Draw airports
      airportGroup.selectAll("circle")
         .data(airport_data)
         .enter()
         .append("circle")
          .attr("class","airport-loc")
          .attr("r", "4")
          .attr("cx", function(d) {
              // console.log([parseFloat(d.LNG), parseFloat(d.LAT)])
              return projection([ d.LNG, d.LAT ])[0];
          })
          .attr("cy", function(d) {
              return projection([ d.LNG, d.LAT ])[1];
          })
          .on("click", function(d) {
            selectAirport(d);
            d3.select("#current_airport").text(d.AIRPORT);
          });

      // Show routes for selected airports
      var selectAirport = function(point) {
          console.log(point);
          var airport = "line." + point.AIRPORT;
          svg.selectAll("line").attr("stroke-width",0.0);
          svg.selectAll(airport).attr("stroke-width",1.5);
      }
    });
  });
});