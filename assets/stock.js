var apiKey = "eys9Qowq7xsT5zdCr6-m";

/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Close
 * index 5 - Volume
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}
var ticker= "AMZN"


function getMonthlyData() {
  
    var queryUrl = `https://www.quandl.com/api/v3/datasets/WIKI/${ticker}.json?start_date=2016-10-01&end_date=2020-10-01&collapse=monthly&api_key=${apiKey}`;
    d3.json(queryUrl).then(function(data) {
      // @TODO: Unpack the dates, open, high, low, close, and volume
      var dates = unpack(data.dataset.data, 0)
      var openPrices = unpack(data.dataset.data, 1)
      var highPrices = unpack(data.dataset.data,2)
      var lowPrices =unpack(data.dataset.data,3)
      var closingPrices= unpack(data.dataset.data, 4)
      var volume = unpack(data.dataset.data,5)
        
    buildTable(dates, openPrices, highPrices, lowPrices, closingPrices, volume);
});
}

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

function buildPlot() {
  
    var url = `https://www.quandl.com/api/v3/datasets/WIKI/${ticker}.json?start_date=2017-01-01&end_date=2018-11-22&api_key=${apiKey}`;
  
    d3.json(url).then(function(data) {
  
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
  
      getMonthlyData();
      var comp_div =d3.select(".company");
      comp_div.text(" ")
      comp_div.append("p").text(data.dataset.description);
  
      // Closing Scatter Line Trace
      var trace1 = {
        type: "scatter",
        mode: "lines",
        name: name,
        x: dates,
        y: close,
        line: {
          color: "#17BECF"}
        // @TODO: YOUR CODE HERE
      };
  
      // Candlestick Trace
      var trace2 = {
        // @TODO: YOUR CODE HERE
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
  
    });
  }
  
  buildPlot();  