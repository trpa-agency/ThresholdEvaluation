// Get the grid to put the data into
let gridAPIDevLan, gridAPIDevLoc;

// Column Definitions for Dev Lan
const columnDefsDevLan = [
  { headerName: "Development Right", field: "Development Right", flex: 1},
  { headerName: "Stream Environment Zones", field: "Stream Environment Zones", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); 
      }},
  { headerName: "Other Sensitive Areas", field: "Other Sensitive Areas", cellDataType: 'numeric',type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); 
      }},
  { headerName: "Non-Sensitive Areas", field: "Non-Sensitive Areas", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); 
      }}
];

const rowDataDevLan = [
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

// Column Definitions for Dev Loc
const columnDefsDevLoc = [
  { headerName: "Development Right", field: "developmentRight", flex: 1 },
  { headerName: "Remote Areas", field: "remoteAreas", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); 
      }},
  { headerName: "Areas within 1/4 mile of a Town Center", 
    field: "areasWithinQuarterMile", cellDataType: 'numeric',type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString(); 
      }},
  { headerName: "Town Centers", field: "townCenters", cellDataType: 'numeric',type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {
    return params.value.toLocaleString();
      }},
];

// Row Data
const rowDataDevLoc = [
  {
    developmentRight: "Coverage (sq. ft.)",
    remoteAreas: "-169,079",
    areasWithinQuarterMile: "+19,697",
    townCenters: "+149,382"
  },
  {
    developmentRight: "Commercial Floor Area (CFA) (sq. ft.)",
    remoteAreas: "+0",
    areasWithinQuarterMile: "-16,791",
    townCenters: "+16,791"
  },
  {
    developmentRight: "Residential Units (SFRRU/MFRUU/RDR)",
    remoteAreas: "-47",
    areasWithinQuarterMile: "+23",
    townCenters: "+24"
  },
  {
    developmentRight: "Tourist Accommodation Units (TAU)",
    remoteAreas: "-12",
    areasWithinQuarterMile: "-21",
    townCenters: "+33"
  }
];

// Grid Options for DVTE
const gridOptionsDevLan = {
  columnDefs: columnDefsDevLan,
  rowData: rowDataDevLan,
  suppressExcelExport: true,
  popupParent: document.body,
  theme: "legacy",
  onGridReady: (params) => {
    gridAPIDevLan = params.api; 
  },
};

// Grid Options for VMT
const gridOptionsDevLoc = {
  columnDefs: columnDefsDevLoc,
  rowData: rowDataDevLoc,
  suppressExcelExport: true,
  theme: "legacy",
  popupParent: document.body,
  onGridReady: (params) => {
    gridAPIDevLoc = params.api; 
  },
};

// Initialize the DVTE Grid
const gridDivDevLan = document.querySelector("#myGridDevLan");
agGrid.createGrid(gridDivDevLan, gridOptionsDevLan); 

// Initialize the VMT Grid
const gridDivDevLoc = document.querySelector("#myGridDevLoc");
agGrid.createGrid(gridDivDevLoc, gridOptionsDevLoc); 

// Export Data as CSV
function onBtnExport() {
  if (gridAPIDevLan) {
    gridAPIDevLan.exportDataAsCsv({fileName: 'Table3_DevelopmentRightChangesByLandSensitivity.csv'});
  }
  if (gridAPIDevLoc) {
    gridAPIDevLoc.exportDataAsCsv({fileName: 'Table4_DevelopmentRightChangesByLocation.csv'});
  }
}
