// Grid API and options
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text'},
  { field: "TotalExistingCFA", headerName: "Total Existing CFA", cellDataType: 'numeric', 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "BankedCFA", headerName: "Banked CFA", cellDataType: 'numeric', 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "RemainingFrom1987PlanAnd2012Allocation", headerName: "Remaining from 1987 Plan and 2012 Allocation", 
    cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "TotalExistingAndPotentialDevelopment", headerName: "Total Existing and Potential Development", 
    cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
];

// Row Data
const rowData = [
  { Jurisdiction: "City of South Lake Tahoe", TotalExistingCFA: 2992830, BankedCFA: 110308, RemainingFrom1987PlanAnd2012Allocation: 28889, TotalExistingAndPotentialDevelopment: 3132027 },
  { Jurisdiction: "Douglas County", TotalExistingCFA: 670802, BankedCFA: 85756, RemainingFrom1987PlanAnd2012Allocation: 33520, TotalExistingAndPotentialDevelopment: 790078 },
  { Jurisdiction: "El Dorado County", TotalExistingCFA: 335706, BankedCFA: 8245, RemainingFrom1987PlanAnd2012Allocation: 33395, TotalExistingAndPotentialDevelopment: 377346 },
  { Jurisdiction: "Placer County", TotalExistingCFA: 1294248, BankedCFA: 56776, RemainingFrom1987PlanAnd2012Allocation: 63648, TotalExistingAndPotentialDevelopment: 1414672 },
  { Jurisdiction: "Washoe County", TotalExistingCFA: 1184357, BankedCFA: 83337, RemainingFrom1987PlanAnd2012Allocation: 10000, TotalExistingAndPotentialDevelopment: 1277694 },
  { Jurisdiction: "TRPA Incentive Pool", TotalExistingCFA: 0, BankedCFA: 0, RemainingFrom1987PlanAnd2012Allocation: 360428, TotalExistingAndPotentialDevelopment: 360428 },
  { Jurisdiction: "Total", TotalExistingCFA: 6477943, BankedCFA: 344422, RemainingFrom1987PlanAnd2012Allocation: 529880, TotalExistingAndPotentialDevelopment: 7352245 },
];

// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
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