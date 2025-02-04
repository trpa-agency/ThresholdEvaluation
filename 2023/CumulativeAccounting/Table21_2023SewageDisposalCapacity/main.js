// get the grid to put the data into
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
  { headerName: "Sewer District", field: "sewerDistrict", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150, 
    cellDataType: 'text', flex: 2
  },
  { headerName: "Peak Sewer Flow (MGD)", field: "peakSewerFlow", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { headerName: "Average 2023 Peak Sewer Flow (MGD)", field: "average2023PeakFlow", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { headerName: "Capacity (MGD)", field: "capacity", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { headerName: "Reserve from Peak Flow (MGD)", field: "reserveFromPeakFlow", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
];

// Row Data
const rowData = [
  { sewerDistrict: "North Tahoe PUD", peakSewerFlow: 1.7, average2023PeakFlow: 1.6, capacity: 6.0, reserveFromPeakFlow: 4.3 },
  { sewerDistrict: "Tahoe City PUD", peakSewerFlow: 2.3, average2023PeakFlow: 2.0, capacity: 7.8, reserveFromPeakFlow: 5.5 },
  { sewerDistrict: "South Tahoe PUD", peakSewerFlow: 3.5, average2023PeakFlow: 3.5, capacity: 7.7, reserveFromPeakFlow: 4.2 },
  { sewerDistrict: "Incline Village GID", peakSewerFlow: 1.4, average2023PeakFlow: 1.0, capacity: 3.0, reserveFromPeakFlow: 1.7 },
  { sewerDistrict: "Douglas County Lake Tahoe Sewer Authority*", peakSewerFlow: 1.7, average2023PeakFlow: 1.2, capacity: 3.8, reserveFromPeakFlow: 2.1 },
];
// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  domLayout: 'autoHeight',
  popupParent: document.body,
  onGridReady: (params) => {
    // Save the grid API reference for later use
    window.gridAPI = params.api; // Make API globally available if needed
  },
};

function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table21_2023SewageDisposalCapacity.csv' 
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