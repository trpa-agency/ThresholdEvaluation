// Grid API and options
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
{ field: "category", headerName: "Category", cellDataType: 'text', flex: 1},
{ field: "ResidentialBonusUnitAccounting", headerName: "Residential Bonus Unit Accounting", cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
{ field: "TRPAPools", headerName: "TRPA Pools", cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
{ field: "LocalJurisdictionPools", headerName: "Local Jurisdiction Pools", cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
{ field: "Total", headerName: "Total", cellDataType: 'numeric', valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
];

// Row Data
const rowData = [
{ category: "Remaining Residential Bonus Units", ResidentialBonusUnitAccounting: 1108, TRPAPools: 337, LocalJurisdictionPools: 1445, Total: 1445 },
{ category: "Permitted Projects Under Construction", ResidentialBonusUnitAccounting: -126, TRPAPools: -20, LocalJurisdictionPools: -146, Total: -146 },
{ category: "Permitted Projects Not Yet Started", ResidentialBonusUnitAccounting: -141, TRPAPools: -4, LocalJurisdictionPools: -145, Total: -145 },
{ category: "Reserved Units", ResidentialBonusUnitAccounting: -262, TRPAPools: 0, LocalJurisdictionPools: -262, Total: -262 },
{ category: "Remaining, Unreserved Units", ResidentialBonusUnitAccounting: 579, TRPAPools: 313, LocalJurisdictionPools: 892, Total: 892 },
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