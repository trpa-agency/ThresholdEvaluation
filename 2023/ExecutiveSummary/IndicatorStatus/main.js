// Define the columns for the AG Grid
const columnDefs = [
    { headerName: 'Indicator', field: 'IndicatorName', width: 250 },
    { headerName: '2011', field: 'Combined2011', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2015', field: 'Combined2015', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2019', field: 'Combined2019', width: 150, cellRenderer: StatusIconRenderer },
    { headerName: '2023', field: 'Combined2023', width: 150, cellRenderer: StatusIconRenderer }
];

// Map status/trend combinations to image paths
const statusTrendImageMap = {
    'Implemented': 'images/Implemented.png',
    'nan': 'images/nan.png', // Placeholder for NaN, adjust the path if necessary
    'At or Somewhat Better Than Target-Moderate Decline': 'images/at_or_somewhat_better_than_target-moderate_decline.png',
    'At or Somewhat Better Than Target-Insufficient Data to Determine Trend': 'images/at_or_somewhat_better_than_target-insufficient_data_to_determine_trend.png',
    'Considerably Worse Than Target-Little or No Change': 'images/considerably_worse_than_target-little_or_no_change.png',
    'Insufficient Data to Determine Status or No Target Established-Rapid Improvement': 'images/insufficient_data_to_determine_status_or_no_target_established-rapid_improvement.png',
    'Considerably Better Than Target-Insufficient Data to Determine Trend': 'images/considerably_better_than_target-insufficient_data_to_determine_trend.png',
    'Insufficient Data to Determine Status or No Target Established-Little or No Change': 'images/insufficient_data_to_determine_status_or_no_target_established-little_or_no_change.png',
    'Somewhat Worse Than Target-Rapid Decline': 'images/somewhat_worse_than_target-rapid_decline.png',
    'Considerably Worse Than Target-Rapid Decline': 'images/considerably_worse_than_target-rapid_decline.png',
    'At or Somewhat Better Than Target-Little or No Change': 'images/at_or_somewhat_better_than_target-little_or_no_change.png',
    'Considerably Better Than Target-Moderate Decline': 'images/considerably_better_than_target-moderate_decline.png',
    'Insufficient Data to Determine Status or No Target Established-Moderate Improvement': 'images/insufficient_data_to_determine_status_or_no_target_established-moderate_improvement.png',
    'Somewhat Worse Than Target-Little or No Change': 'images/somewhat_worse_than_target-little_or_no_change.png',
    'Somewhat Worse Than Target-Moderate Improvement': 'images/somewhat_worse_than_target-moderate_improvement.png',
    'Considerably Worse Than Target-Moderate Decline': 'images/considerably_worse_than_target-moderate_decline.png',
    'Somewhat Worse Than Target-Moderate Decline': 'images/somewhat_worse_than_target-moderate_decline.png',
    'At or Somewhat Better Than Target-Moderate Improvement': 'images/at_or_somewhat_better_than_target-moderate_improvement.png',
    'Considerably Better Than Target-Little or No Change': 'images/considerably_better_than_target-little_or_no_change.png',
    'Considerably Worse Than Target-Insufficient Data to Determine Trend': 'images/considerably_worse_than_target-insufficient_data_to_determine_trend.png',
    'Considerably Better Than Target-Moderate Improvement': 'images/considerably_better_than_target-moderate_improvement.png',
    'Considerably Better Than Target-Rapid Improvement': 'images/considerably_better_than_target-rapid_improvement.png',
    'Somewhat Worse Than Target-Insufficient Data to Determine Trend': 'images/somewhat_worse_than_target-insufficient_data_to_determine_trend.png',
    'Considerably Worse Than Target-Moderate Improvement': 'images/considerably_worse_than_target-moderate_improvement.png',
    'Insufficient Data to Determine Status or No Target Established-Insufficient Data to Determine Trend': 'images/insufficient_data_to_determine_status_or_no_target_established-insufficient_data_to_determine_trend.png',
};

// Function to combine status and trend values for each year
function combineStatusTrend(status, trend) {
    if (status === null || trend === null) {
        return 'No Data'; // Handle missing data gracefully
    }
    return `${status}-${trend}`;
}

// Fetch data from the new service URL
fetch('https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/118/query?where=1%3D1&outFields=*&outSR=4326&f=json')
    .then(response => response.json())
    .then(data => {
        // Transform the data to combine status and trend for each year
        const transformedData = data.features.map(item => ({
            IndicatorName: item.attributes.IndicatorName,
            Combined2011: statusTrendImageMap[combineStatusTrend(item.attributes.Status2011, item.attributes.Trend2011)] || combineStatusTrend(item.attributes.Status2011, item.attributes.Trend2011),
            Combined2015: statusTrendImageMap[combineStatusTrend(item.attributes.Status2015, item.attributes.Trend2015)] || combineStatusTrend(item.attributes.Status2015, item.attributes.Trend2015),
            Combined2019: statusTrendImageMap[combineStatusTrend(item.attributes.Status2019, item.attributes.Trend2019)] || combineStatusTrend(item.attributes.Status2019, item.attributes.Trend2019),
            Combined2023: statusTrendImageMap[combineStatusTrend(item.attributes.Status2023, item.attributes.Trend2023)] || combineStatusTrend(item.attributes.Status2023, item.attributes.Trend2023)
        }));
        console.log("Data fetched:", transformedData); // Log the data to ensure it is correct
        
        // Grid Options with the fetched data as rowData
        const gridOptions = {
            columnDefs: columnDefs,
            rowData: transformedData, 
            theme: "legacy",
            suppressExcelExport: true,
            popupParent: document.body,
            onGridReady: (params) => {
                window.gridAPI = params.api; // Make API globally available if needed
            },
        };
        // Initialize the grid
        const gridDiv = document.querySelector("#myGrid");
        agGrid.createGrid(gridDiv, gridOptions); // This initializes the grid with the data
        })
.catch((error) => {
    console.error("Error fetching data:", error);
});