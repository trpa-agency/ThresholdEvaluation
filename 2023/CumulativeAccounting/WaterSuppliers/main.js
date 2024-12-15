
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { headerName: "Tahoe Water Purveyors", field: "waterSystem", flex: 1 }
];

// Row Data
const rowData = [
  { waterSystem: "Cave Rock Water System (Cave Rock; Douglas County)" },
  { waterSystem: "Edgewood Water Company (Edgewood)" },
  { waterSystem: "Glenbrook Water Cooperative (Glenbrook)" },
  { waterSystem: "Incline Village General Improvement District (IVGID)" },
  { waterSystem: "Kingsbury General Improvement District (KGID)" },
  { waterSystem: "Lakeside Park Association (LPA)" },
  { waterSystem: "North Tahoe Public Utility District (NTPUD)" },
  { waterSystem: "Round Hill General Improvement District (RHGID)" },
  { waterSystem: "Skyland Water Company (Skyland; Douglas County)" },
  { waterSystem: "South Tahoe Public Utility District (STPUD)" },
  { waterSystem: "Tahoe City Public Utility District (TCPUD)" },
  { waterSystem: "Zephyr Water Utility (Zephyr; Douglas County)" }
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

  
  