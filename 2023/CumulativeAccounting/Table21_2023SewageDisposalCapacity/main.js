// get the grid to put the data into
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
  { headerName: "Sewer District", field: "sewerDistrict", flex: 1 
  },
  { headerName: "Peak Sewer Flow (MGD)", field: "peakSewerFlow", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1
  },
  { headerName: "Average 2023 Peak Sewer Flow (MGD)", field: "average2023PeakFlow", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
   },
  { headerName: "Capacity (MGD)", field: "capacity", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
   },
  { headerName: "Reserve from Peak Flow (MGD)", field: "reserveFromPeakFlow", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
  }
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
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  },
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