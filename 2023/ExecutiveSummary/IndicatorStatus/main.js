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

document.addEventListener('DOMContentLoaded', () => {
    // Grid Options configuration
    const gridOptions = {
        columnDefs: columnDefs,
        rowData: [], 
        suppressExcelExport: true,
        popupParent: document.body,
        components: {
            'statusIconRenderer': StatusIconRenderer
        },
        defaultColDef: {
            resizable: true,
            sortable: true
        }
    };

    // Initialize the grid
    const gridDiv = document.querySelector("#myGrid");
    gridDiv.style.height = '500px';
    gridDiv.style.width = '100%';

    // Apply custom styles
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .ag-theme-alpine {
            --ag-font-family: "Calibri", sans-serif;
            --ag-font-size: 14px;
            --ag-header-height: 36px;
            --ag-header-foreground-color: white;
            --ag-header-background-color: #337ab7;
            --ag-header-cell-hover-background-color: #279bdc;
            --ag-header-cell-moving-background-color: #279bdc;
            --ag-row-height: 36px;
            --ag-borders: solid 1px;
            --ag-border-color: #dde2eb;
            --ag-cell-horizontal-border: solid 1px #dde2eb;
            --ag-row-border-color: #dde2eb;
            --ag-grid-size: 10px;
        }

        .status-icon {
            width: 24px;
            height: 24px;
            display: block;
            margin: auto;
        }

        .imgSpanLogo {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
        }

        .ag-cell {
            display: flex;
            align-items: center;
        }

        .ag-header-cell-label {
            justify-content: center;
        }
    `;
    document.head.appendChild(styleElement);

    try {
        // Create the grid using the Grid constructor
        new agGrid.Grid(gridDiv, gridOptions);
        
        // Fetch data
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
                
                // Use the gridOptions API
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
