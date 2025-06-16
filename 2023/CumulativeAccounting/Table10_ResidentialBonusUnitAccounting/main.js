// Grid API and options
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
{ field: "category", headerName: "Category", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 180,
  cellDataType: 'text', flex: 2, 
  valueFormatter: (params) => {return params.value.toLocaleString();}
},
{ field: "TRPAPools", headerName: "TRPA Pools", 
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();}
},
{ field: "LocalJurisdictionPools", headerName: "Local Jurisdiction Pools",
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();}
},
{ field: "Total", headerName: "Total", cellClass: 'total-column',
  wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
  cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
  valueFormatter: (params) => {return params.value.toLocaleString();}
}
];

// Row Data
const rowData = [
{ category: "Remaining Residential Bonus Units", TRPAPools: 1109, LocalJurisdictionPools: 341, Total: 1450 },
{ category: "Permitted Projects Under Construction", TRPAPools: -126, LocalJurisdictionPools: -24, Total: -150 },
{ category: "Permitted Projects Not Yet Started", TRPAPools: -146, LocalJurisdictionPools: -10, Total: -156 },
{ category: "Reserved Units", TRPAPools: -256, LocalJurisdictionPools: 0, Total: -256 },
{ category: "Remaining, Unreserved Units", TRPAPools: 581, LocalJurisdictionPools: 307, Total: 888 },
];

// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  domLayout: 'autoHeight',
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