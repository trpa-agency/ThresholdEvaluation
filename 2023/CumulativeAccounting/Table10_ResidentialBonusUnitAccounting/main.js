// Grid API and options
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
{ field: "category", headerName: "Category", cellDataType: 'text', flex: 1},
{ field: "TRPAPools", headerName: "TRPA Pools", cellDataType: 'numeric',type: 'rightAligned', flex: 1, valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
{ field: "LocalJurisdictionPools", headerName: "Local Jurisdiction Pools", cellDataType: 'numeric', wrapHeaderText:true, type: 'rightAligned', flex: 1, valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
{ field: "Total", headerName: "Total", cellDataType: 'numeric', type: 'rightAligned', cellClass: 'total-column', flex: 1, valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
];

// Row Data
const rowData = [
{ category: "Remaining Residential Bonus Units", TRPAPools: 1108, LocalJurisdictionPools: 337, Total: 1445 },
{ category: "Permitted Projects Under Construction", TRPAPools: -126, LocalJurisdictionPools: -20, Total: -146 },
{ category: "Permitted Projects Not Yet Started", TRPAPools: -141, LocalJurisdictionPools: -4, Total: -145 },
{ category: "Reserved Units", TRPAPools: -262, LocalJurisdictionPools: 0, Total: -262 },
{ category: "Remaining, Unreserved Units", TRPAPools: 579, LocalJurisdictionPools: 313, Total: 892 },
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
    const params = {
      fileName: 'Table10_ResidentialBonusUnitAccounting.csv' 
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