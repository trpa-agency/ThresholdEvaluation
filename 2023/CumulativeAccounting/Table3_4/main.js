// Get the grid to put the data into
let gridAPIDevLan, gridAPIDevLoc;

// Column Definitions for Dev Lan
const columnDefsDevLan = [
  { headerName: "Development Right", field: "Development Right", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'text', flex: 2, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Stream Environment Zones", field: "Stream Environment Zones", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Other Sensitive Areas", field: "Other Sensitive Areas", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Non-Sensitive Areas", field: "Non-Sensitive Areas",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  }
];

const rowDataDevLan = [
  {
    "Development Right": "Coverage (sq. ft.)",
    "Stream Environment Zones": -165394,
    "Other Sensitive Areas": 24502,
    "Non-Sensitive Areas": 140892
  },
  {
    "Development Right": "Commercial Floor Area (CFA) (sq. ft.)",
    "Stream Environment Zones": 0,
    "Other Sensitive Areas": -10492,
    "Non-Sensitive Areas": 10492
  },
  {
    "Development Right": "Residential Units (SFRRU/MFRUU/RDR)",
    "Stream Environment Zones": -30,
    "Other Sensitive Areas": -28,
    "Non-Sensitive Areas": 58
  },
  {
    "Development Right": "Tourist Accommodation Units (TAU)",
    "Stream Environment Zones": -145,
    "Other Sensitive Areas": 1,
    "Non-Sensitive Areas": 144
  }
];

// Column Definitions for Dev Loc
const columnDefsDevLoc = [
  { headerName: "Development Right", field: "developmentRight", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'text',  flex: 2, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Remote Areas", field: "remoteAreas", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Within 1/4 mile of Town Center", 
    field: "areasWithinQuarterMile", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { headerName: "Town Centers", field: "townCenters", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
];

// Row Data
const rowDataDevLoc = [
  {
    developmentRight: "Coverage (sq. ft.)",
    remoteAreas: "-141,364",
    areasWithinQuarterMile: "+15,123",
    townCenters: "+136,241"
  },
  {
    developmentRight: "Commercial Floor Area (CFA) (sq. ft.)",
    remoteAreas: "+21,565",
    areasWithinQuarterMile: "-14,811",
    townCenters: "+16,754"
  },
  {
    developmentRight: "Residential Units (SFRRU/MFRUU/RDR)",
    remoteAreas: "+30",
    areasWithinQuarterMile: "-2",
    townCenters: "-28"
  },
  {
    developmentRight: "Tourist Accommodation Units (TAU)",
    remoteAreas: "+209",
    areasWithinQuarterMile: "-60",
    townCenters: "-149"
  }
];

// Grid Options for DVTE
const gridOptionsDevLan = {
  columnDefs: columnDefsDevLan,
  rowData: rowDataDevLan,
  suppressExcelExport: true,
  popupParent: document.body,
  theme: "legacy",
  domLayout: 'autoHeight',
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
  domLayout: 'autoHeight',
  popupParent: document.body,
  onGridReady: (params) => {
    gridAPIDevLoc = params.api; 
  },
};

// Initialize the DVTE Grid
const gridDivDevLan = document.querySelector("#myGridDevLan");
agGrid.createGrid(gridDivDevLan, gridOptionsDevLan); // This initializes the grid with DVTE data

// Initialize the VMT Grid
const gridDivDevLoc = document.querySelector("#myGridDevLoc");
agGrid.createGrid(gridDivDevLoc, gridOptionsDevLoc); // This initializes the grid with VMT data

// Export Data as CSV
function onBtnExport() {
  if (gridAPIDevLan) {
    gridAPIDevLan.exportDataAsCsv({fileName: 'Table3_DevelopmentRightChangesByLandSensitivity.csv'});
  }
  if (gridAPIDevLoc) {
    gridAPIDevLoc.exportDataAsCsv({fileName: 'Table4_DevelopmentRightChangesByLocation.csv'});
  }
}
