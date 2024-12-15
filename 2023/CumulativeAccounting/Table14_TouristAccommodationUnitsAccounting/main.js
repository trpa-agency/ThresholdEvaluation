// Get the grid to put the data into
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text'},
  { field: "TotalExistingTAUs", headerName: "Total Existing TAUs", cellDataType: 'numeric', 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "BankedReceivedTAUs", headerName: "Banked/Received TAUs", cellDataType: 'numeric', 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "RemainingFrom1987PlanAnd2012Allocation", headerName: "Remaining from 1987 Plan and 2012 Allocation", 
    cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "TotalDevelopmentPotential", headerName: "Total Development Potential", cellDataType: 'numeric', 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
];

// Row Data
const rowData = [
  { Jurisdiction: "City of South Lake Tahoe", TotalExistingTAUs: 5909, BankedReceivedTAUs: 602, RemainingFrom1987PlanAnd2012Allocation: 25, TotalDevelopmentPotential: 6536 },
  { Jurisdiction: "Douglas County", TotalExistingTAUs: 2792, BankedReceivedTAUs: 40, RemainingFrom1987PlanAnd2012Allocation: 25, TotalDevelopmentPotential: 2857 },
  { Jurisdiction: "El Dorado County", TotalExistingTAUs: 112, BankedReceivedTAUs: 211, RemainingFrom1987PlanAnd2012Allocation: 10, TotalDevelopmentPotential: 333 },
  { Jurisdiction: "Placer County", TotalExistingTAUs: 1224, BankedReceivedTAUs: 253, RemainingFrom1987PlanAnd2012Allocation: 37, TotalDevelopmentPotential: 1514 },
  { Jurisdiction: "Washoe County", TotalExistingTAUs: 1002, BankedReceivedTAUs: 64, RemainingFrom1987PlanAnd2012Allocation: 33, TotalDevelopmentPotential: 1099 },
  { Jurisdiction: "TRPA Incentive Pool", TotalExistingTAUs: "-", BankedReceivedTAUs: "-", RemainingFrom1987PlanAnd2012Allocation: 212, TotalDevelopmentPotential: 212 },
  { Jurisdiction: "Total", TotalExistingTAUs: 11039, BankedReceivedTAUs: 1170, RemainingFrom1987PlanAnd2012Allocation: 342, TotalDevelopmentPotential: 12551 },
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
    window.gridAPI.exportDataAsCsv();
  } else {
    console.error("Grid API is not initialized.");
  }
}

// setup the grid after the page has finished loading
document.addEventListener("DOMContentLoaded", function () {
  var gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);
});