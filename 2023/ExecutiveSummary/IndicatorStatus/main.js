// Define the columns for the AG Grid
const columnDefs = [
    { headerName: 'Indicator', field: 'IndicatorName', width: 250 },
    { headerName: '2011', field: 'Combined2011', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2015', field: 'Combined2015', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2019', field: 'Combined2019', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2023', field: 'Combined2023', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2023', field: 'Combined2023', width: 150, cellRenderer: StatusIconRenderer }
];

// Map status/trend combinations to image paths
const statusTrendImageMap = {
    'Considerably Better Than Target-Rapid Improvement': 'images/considerably_better_than_target-rapid_improvement.png',
    'Considerably Better Than Target-Moderate Improvement': 'images/considerably_better_than_target-moderate_improvement.png',
    'Considerably Better Than Target-Moderate Decline': 'images/considerably_better_than_target-moderate_decline.png',
    'At or Somewhat Better Than Target-Moderate Improvement': 'images/at_or_somewhat_better_than_target-moderate_improvement.png',
    'At or Somewhat Better Than Target-Little or No Change': 'images/at_or_somewhat_better_than_target-little_or_no_change.png',
    'Somewhat Worse Than Target-Moderate Improvement': 'images/somewhat_worse_than_target-moderate_improvement.png',
    'Somewhat Worse Than Target-Moderate Decline': 'images/somewhat_worse_than_target-moderate_decline.png',
    'Considerably Worse Than Target-Moderate Decline': 'images/considerably_worse_than_target-moderate_decline.png',
    'Considerably Worse Than Target-Little or No Change': 'images/considerably_worse_than_target-little_or_no_change.png',
    // Add more combinations as needed
};
// Function to combine status and trend values for each year
function combineStatusTrend(status, trend) {
    if (status === null || trend === null) {
        return 'No Data'; // Handle missing data gracefully
    }
    return `${status}-${trend}`;
}

// Fetch data from the Lake Tahoe Info API for threshold evaluations using a different proxy server
// URL: https://www.laketahoeinfo.org/WebServices/GetThresholdEvaluatio
fetch('https://www.laketahoeinfo.org/WebServices/GetThresholdEvaluations/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476', { 
        method: "GET", mode: 'no-cors', 
        headers: { 'Content-Type': 'application/json',}})
        .then(response => response.json())
        .then(data => {
    // Transform the data to combine status and trend for each year
    const transformedData = data.map(item => ({
        IndicatorName: item.IndicatorName,
        Combined2011: statusTrendImageMap[combineStatusTrend(item.Status2011, item.Trend2011)] || combineStatusTrend(item.Status2011, item.Trend2011),
        Combined2015: statusTrendImageMap[combineStatusTrend(item.Status2015, item.Trend2015)] || combineStatusTrend(item.Status2015, item.Trend2015),
        Combined2019: statusTrendImageMap[combineStatusTrend(item.Status2019, item.Trend2019)] || combineStatusTrend(item.Status2019, item.Trend2019),
        Combined2023: statusTrendImageMap[combineStatusTrend(item.Status2023, item.Trend2023)] || combineStatusTrend(item.Status2023, item.Trend2023)
    }));

    logger.info("Data fetched:", { data: transformedData }); // Log the data to ensure it is correct
    console.log("Data fetched:", transformedData); // Log the data to ensure it is correct
    
    // Grid Options with the fetched data as rowData
})
.catch(error => {
    console.error('Error fetching data:', error);
});