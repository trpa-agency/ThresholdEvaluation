// Define the columns for the AG Grid
const columnDefs = [
    { headerName: 'Indicator', field: 'IndicatorName', width: 250 },
    { headerName: '2011', field: 'Combined2011', width: 150, cellRenderer: 'statusIconRenderer' },
    { headerName: '2015', field: 'Combined2015', width: 150, cellRenderer: 'statusIconRenderer' },
    { headerName: '2019', field: 'Combined2019', width: 150, cellRenderer: 'statusIconRenderer' },
    { headerName: '2023', field: 'Combined2023', width: 150, cellRenderer: 'statusIconRenderer' }
];

// Function to combine status and trend values for each year
function combineStatusTrend(status, trend) {
    if (status === null || trend === null) {
        return 'nan';
    }
    return `${status}-${trend}`;
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Grid Options configuration
    const gridOptions = {
        columnDefs: columnDefs,
        rowData: [], 
        theme: 'legacy',
        suppressExcelExport: true,
        popupParent: document.body,
        components: {
            'statusIconRenderer': StatusIconRenderer
        }
    };

    // Initialize the grid
    const gridDiv = document.querySelector("#myGrid");
    try {
        // Create the grid
        new agGrid.Grid(gridDiv, gridOptions);
        
        // After grid is created, fetch the data
        fetch('https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/116/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=&f=json')
            .then(response => response.json())
            .then(data => {
                const transformedData = data.features.map(item => ({
                    IndicatorName: item.attributes.IndicatorName,
                    Combined2011: combineStatusTrend(item.attributes.Status2011, item.attributes.Trend2011),
                    Combined2015: combineStatusTrend(item.attributes.Status2015, item.attributes.Trend2015),
                    Combined2019: combineStatusTrend(item.attributes.Status2019, item.attributes.Trend2019),
                    Combined2023: combineStatusTrend(item.attributes.Status2023, item.attributes.Trend2023)
                }));
                console.log("Data fetched:", transformedData);
                
                // Update the grid with the new data
                gridOptions.api.setRowData(transformedData);
                gridOptions.api.sizeColumnsToFit();
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                gridDiv.innerHTML = 'Error loading data. Please refresh the page.';
            });
    } catch (error) {
        console.error('Failed to initialize AG Grid:', error);
        gridDiv.innerHTML = 'Failed to load the grid. Please refresh the page.';
    }
});
