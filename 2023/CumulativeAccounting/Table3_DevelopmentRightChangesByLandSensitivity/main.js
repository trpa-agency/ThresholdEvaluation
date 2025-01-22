// Import ag-Grid library
// get the grid to put the data into
let gridOptions;
let gridAPI;

const columnDefs = [
  { headerName: "Development Right", field: "Development Right", flex: 1},
  { headerName: "Stream Environment Zones", field: "Stream Environment Zones", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); // Format with commas
      }},
  { headerName: "Other Sensitive Areas", field: "Other Sensitive Areas", cellDataType: 'numeric',type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); // Format with commas
      }},
  { headerName: "Non-Sensitive Areas", field: "Non-Sensitive Areas", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); // Format with commas
      }}
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
          fileName: 'Table3_DevelopmentRightChangesByLandSensitivity.csv' 
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