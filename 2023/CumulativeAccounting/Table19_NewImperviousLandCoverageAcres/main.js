// Define the formatNumber function
function formatNumber(value) {
  return value.toFixed(1);
}

// get the grid to put the data into
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
{ headerName: "Jurisdiction", field: "jurisdiction",
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
  cellDataType: 'rext', flex: 2, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "1991-1995 Acres", field: "acres1991_1995",
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "1996-2000 Acres", field: "acres1996_2000", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "2001-2005 Acres", field: "acres2001_2005", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "2006-2010 Acres", field: "acres2006_2010", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "2011-2015 Acres", field: "acres2011_2015", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "2016-2019 Acres", field: "acres2016_2019", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
{ headerName: "2020-2023 Acres", field: "acres2020_2023", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();
}},
  {
    headerName: "Total", field: "total", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'text', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => formatNumber(params.value),
    cellClass: 'total-column'
  }
];

// Row Data
const rowData = [
  { jurisdiction: "Douglas County", acres1991_1995: 7.0, acres1996_2000: 6.0, acres2001_2005: 6.5, acres2006_2010: 3.4, acres2011_2015: 0.5, acres2016_2019: 1.4, acres2020_2023: 3.6, total: 28.4 },
  { jurisdiction: "El Dorado County", acres1991_1995: 32.1, acres1996_2000: 40.4, acres2001_2005: 46.1, acres2006_2010: 28.1, acres2011_2015: 4.2, acres2016_2019: 13.7, acres2020_2023: 22.8, total: 187.4 },
  { jurisdiction: "Placer County", acres1991_1995: 25.5, acres1996_2000: 28.7, acres2001_2005: 35.1, acres2006_2010: 15.3, acres2011_2015: 3.3, acres2016_2019: 6.0, acres2020_2023: 4.8, total: 118.7 },
  { jurisdiction: "Washoe County", acres1991_1995: 29.7, acres1996_2000: 17.0, acres2001_2005: 15.7, acres2006_2010: 5.6, acres2011_2015: 10.9, acres2016_2019: 3.2, acres2020_2023: 2.6, total: 84.7 },
];

// Calculate totals
const totalRow = rowData.reduce((acc, row) => {
  Object.keys(row).forEach((key) => {
    if (key !== "jurisdiction") {
      acc[key] = (acc[key] || 0) + (row[key] || 0);
    }
  });
  return acc;

}, { jurisdiction: "Total" });  
// Grid Options with the fetched data as rowData
gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData, // Use the fetched data
    pinnedBottomRowData: [totalRow],
    theme:"legacy",
    domLayout: "autoHeight",
    suppressExcelExport: true,
    popupParent: document.body,
    getRowClass: (params) => {
    // Apply a custom class to the row containing the "Total" account
    if (params.data && params.data.jurisdiction === "Total") {
      return "total-row-highlight"; // Custom CSS class for highlighting
    }
  },
  onGridReady: (params) => {
    // Save the grid API reference for later use
    window.gridAPI = params.api; // Make API globally available if needed
  },
};

function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table19_NewImperviousLandCoverageAcres.csv' 
    };
    window.gridAPI.exportDataAsCsv(params);
  } else {
    console.error("Grid API is not initialized.");
  }
}

// setup the grid after the page has finished loading
document.addEventListener("DOMContentLoaded", function () {
  var gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);
});
  