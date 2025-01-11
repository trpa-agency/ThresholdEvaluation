// Define the columns for the AG Grid
const columnDefs = [
    { headerName: 'Indicator', field: 'IndicatorName', width: 250 },
    { headerName: '2011', field: 'Combined2011', width: 150, cellRenderer: imageCellRenderer },
    { headerName: '2015', field: 'Combined2015', width: 150, cellRenderer: imageCellRenderer },
    { headerName: '2019', field: 'Combined2019', width: 150, cellRenderer: imageCellRenderer },
    { headerName: '2023', field: 'Combined2023', width: 150, cellRenderer: imageCellRenderer }
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

// Cell renderer for AG Grid to display images based on the status/trend combination
function imageCellRenderer(params) {
    const combinedValue = params.value;
    const imageUrl = statusTrendImageMap[combinedValue];
    if (imageUrl) {
        return `<img src="${imageUrl}" alt="${combinedValue}" style="width: 30px; height: 30px;">`;
    }
    return ''; // Return empty if no image is found for the combination
}

// Function to combine status and trend values for each year
function combineStatusTrend(status, trend) {
    if (!status || !trend) {
        return 'No Data'; // Handle missing data gracefully
    }
    return `${status}-${trend}`;
}

// Fetch data from the API and populate the grid
function fetchDataAndPopulateGrid() {
    const corsProxy = 'https://cors-anywhere.herokuapp.com/'; // CORS proxy
    const apiUrl = 'https://www.laketahoeinfo.org/WebServices/GetThresholdEvaluations/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476';

    fetch(corsProxy + apiUrl)
        .then(response => response.json())
        .then(data => {
            // Transform the data to combine status and trend for each year
            const transformedData = data.map(item => ({
                IndicatorName: item.IndicatorName,
                Combined2011: combineStatusTrend(item.Status2011, item.Trend2011),
                Combined2015: combineStatusTrend(item.Status2015, item.Trend2015),
                Combined2019: combineStatusTrend(item.Status2019, item.Trend2019),
                Combined2023: combineStatusTrend(item.Status2023, item.Trend2023)
            }));

            // Set up the grid options
            const gridOptions = {
                columnDefs: columnDefs,
                rowData: transformedData,
                domLayout: 'autoHeight'
            };

            // Initialize the grid
            const gridDiv = document.querySelector('#myGrid');
            new agGrid.Grid(gridDiv, gridOptions);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Run the function once the page is loaded
document.addEventListener('DOMContentLoaded', fetchDataAndPopulateGrid);
