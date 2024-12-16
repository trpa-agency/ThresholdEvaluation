// Column Definitions
const columnDefs = [
  { headerName: "Improvement Districts", field: "jurisdictions", flex: 1 }
];

// Row Data
const rowData = [
  { jurisdictions: "Cave Rock Estates GID" },
  { jurisdictions: "Oliver Park GID" },
  { jurisdictions: "Incline Village GID" },
  { jurisdictions: "Round Hill GID" },
  { jurisdictions: "Kingsbury GID" },
  { jurisdictions: "South Tahoe PUD" },
  { jurisdictions: "Lakeridge GID" },
  { jurisdictions: "Tahoe City PUD" },
  { jurisdictions: "Logan Creek Estates GID" },
  { jurisdictions: "Zephyr Cove GID" },
  { jurisdictions: "Marla Bay GID" },
  { jurisdictions: "Zephyr Heights GID" },
  { jurisdictions: "North Tahoe PUD" },
  { jurisdictions: "Zephyr Knolls GID" }
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