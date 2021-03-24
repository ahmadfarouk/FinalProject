var apiKey = "eys9Qowq7xsT5zdCr6-m";

function unpack(rows, index) {
  
  return rows.map(function(row) {
    return row[index];
  });
}
// Submit Button handler
function handleSubmit() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Select the input value from the form
  var stock = d3.select("#stockInput").node().value;
  // console.log(stock);
   // clear the input value
   d3.select("#stockInput").node().value = "";
   buildPlot(stock);  
}

// var ticker= "AMZN"
function buildTable(dates, openPrices, highPrices, lowPrices, closingPrices, volume) {
var table = d3.select("#summary-table");
var tbody = table.select("tbody");
var trow;
for (var i = 0; i < 12; i++) {
  trow = tbody.append("tr");
  trow.append("td").text(dates[i]);
  trow.append("td").text(openPrices[i]);
  trow.append("td").text(highPrices[i]);
  trow.append("td").text(lowPrices[i]);
  trow.append("td").text(closingPrices[i]);
  trow.append("td").text(volume[i]);
}
}

function buildPlot(stock) {
    // var url=  ` https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${ticker}&apikey=${apiKey}`;
    var url = `https://www.quandl.com/api/v3/datasets/WIKI/${stock}.json?start_date=2017-01-01&end_date=2018-11-22&api_key=${apiKey}`;
  
    d3.json(url).then(function(data) {
    console.log(data)
  
      // @TODO: Grab Name, Stock, Start Date, and End Date from the response json object to build the plots
      var name = data.dataset.name;
      var stock = data.dataset.dataset_code;
      var startDate = data.dataset.start_date;
      var endDate = data.dataset.end_date;
      // @TODO: Unpack the dates, open, high, low, and close prices
      
      var dates = unpack(data.dataset.data, 0)
      var open = unpack(data.dataset.data, 1)
      var high = unpack(data.dataset.data,2)
      var low =unpack(data.dataset.data,3)
      var close = unpack(data.dataset.data, 4)
      var volume = unpack(data.dataset.data,5)
  

      var comp_div =d3.select(".company");
      comp_div.text(" ")
      comp_div.append("p").html(data.dataset.description);
      
      // Closing Scatter Line Trace
      var trace1 = {
        type: "scatter",
        mode: "lines",
        name: name,
        x: dates,
        y: close,
        line: {
          color: "#17BECF"}
        
      };
  
      // Candlestick Trace
      var trace2 = {
       
        type: "candlestick",
        name:"Candlestick Data",
        x: data.dataset.data.map(row =>row[0]),
        high:data.dataset.data.map(row =>row[2]),
        low:data.dataset.data.map(row =>row[3]),
        open:data.dataset.data.map(row =>row[1]),
        close:data.dataset.data.map(row =>row[4]),
        
      };
  
      var data = [trace1, trace2];
  
      var layout = {
        title: `${stock} closing prices`,
        xaxis: {
          range: [startDate, endDate],
          type: "date"
        },
        yaxis: {
          autorange: true,
          type: "linear"
        },
        showlegend: false
      };
  
      Plotly.newPlot("plot", data, layout);
      buildTable(dates, open, high, low, close, volume);
  
    });
  }
  
// Add event listener for submit button
d3.select("#submit").on("click", handleSubmit);
 