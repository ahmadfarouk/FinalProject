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

function getMonthlyData() {

    var queryUrl = `https://www.quandl.com/api/v3/datasets/WIKI/AMZN.json?start_date=2016-10-01&end_date=2017-10-01&collapse=monthly&api_key=${apiKey}`;
    d3.json(queryUrl).then(function(data) {
      // @TODO: Unpack the dates, open, high, low, close, and volume
      var dates = unpack(data.dataset.data, 0)
      var openPrices = unpack(data.dataset.data, 1)
      var highPrices = unpack(data.dataset.data,2)
      var lowPrices =unpack(data.dataset.data,3)
      var closingPrices= unpack(data.dataset.data, 4)
      var volume = unpack(data.dataset.data,5)