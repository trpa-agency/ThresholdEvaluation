// Import ag-Grid library
// get the grid to put the data into
let gridOptions;
let gridAPI;

const columnDefs = [
  { headerName: "Development Right", field: "Development Right" },
  { headerName: "Stream Environment Zones", field: "Stream Environment Zones" },
  { headerName: "Other Sensitive Areas", field: "Other Sensitive Areas" },
  { headerName: "Non-Sensitive Areas", field: "Non-Sensitive Areas" }
];

const rowData = [
  {
    "Development Right": "Coverage (sq. ft.)",
    "Stream Environment Zones": -137193,
    "Other Sensitive Areas": 25472,
    "Non-Sensitive Areas": 111721
  },
  {
    "Development Right": "Commercial Floor Area (CFA) (sq. ft.)",
    "Stream Environment Zones": 0,
    "Other Sensitive Areas": -10492,
    "Non-Sensitive Areas": 10492
  },
  {
    "Development Right": "Residential Units (SFRRU/MFRUU/RDR)",
    "Stream Environment Zones": -89,
    "Other Sensitive Areas": -13,
    "Non-Sensitive Areas": 102
  },
  {
    "Development Right": "Tourist Accommodation Units (TAU)",
    "Stream Environment Zones": -109,
    "Other Sensitive Areas": 0,
    "Non-Sensitive Areas": 109
  }
];

  // Grid Options with the fetched data as rowData
  gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData, // Use the fetched data
    suppressExcelExport: true,
    popupParent: document.body,
    onGridReady: (params) => {
      // Save the grid API reference for later use
      window.gridAPI = params.api; // Make API globally available if needed
    },
  };
  // Initialize the grid
  const gridDiv = document.querySelector("#myGrid");
  agGrid.createGrid(gridDiv, gridOptions); // This initializes the grid with the data
  
  function onBtnExport() {
    if (window.gridAPI) {
      window.gridAPI.exportDataAsCsv();
    } else {
      console.error("Grid API is not initialized.");
    }
  }


  
  