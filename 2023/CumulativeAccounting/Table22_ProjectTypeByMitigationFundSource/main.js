// get the grid to put the data into
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
  { headerName: "Project Type", field: "projectType", flex: 2 },
  { headerName: "Air Quality Mitigation", field: "airQualityMitigation", 
    type: 'rightAligned', flex: 1
   },
  { headerName: "Water Quality Mitigation", field: "waterQualityMitigation", 
    type: 'rightAligned', flex: 1
  },
  { headerName: "Stream Environment Zone Restoration", field: "streamEnvironmentZoneRestoration", 
    type: 'rightAligned', flex: 1
   },
  { headerName: "Operations Maintenance", field: "operationsMaintenance", 
    type: 'rightAligned', flex: 1
  },
  { headerName: "Excess Offsite Land Coverage Mitigation", field: "excessOffsiteLandCoverageMitigation", 
    type: 'rightAligned', flex: 1
  }
];

// Row Data
const rowData = [
  { projectType: "SEZ Restoration and Erosion Control Projects", airQualityMitigation: "28%", waterQualityMitigation: "29%", streamEnvironmentZoneRestoration: "59%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Street Sweeper Equipment Purchase", airQualityMitigation: "10%", waterQualityMitigation: "3%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "84%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Stormwater Improvement Projects", airQualityMitigation: "0%", waterQualityMitigation: "11%", streamEnvironmentZoneRestoration: "41%", operationsMaintenance: "6%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Recreation Improvement Projects", airQualityMitigation: "7%", waterQualityMitigation: "0%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Bike and Pedestrian Lane Improvement Projects", airQualityMitigation: "32%", waterQualityMitigation: "12%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Air Quality Improvement Projects", airQualityMitigation: "19%", waterQualityMitigation: "0%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Transit Services", airQualityMitigation: "5%", waterQualityMitigation: "0%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Water Quality Improvement Projects", airQualityMitigation: "0%", waterQualityMitigation: "44%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "9%", excessOffsiteLandCoverageMitigation: "0%" },
  { projectType: "Land Bank and Operational Support", airQualityMitigation: "0%", waterQualityMitigation: "0%", streamEnvironmentZoneRestoration: "0%", operationsMaintenance: "0%", excessOffsiteLandCoverageMitigation: "100%" },
  { projectType: "Total", airQualityMitigation: "100%", waterQualityMitigation: "100%", streamEnvironmentZoneRestoration: "100%", operationsMaintenance: "100%", excessOffsiteLandCoverageMitigation: "100%" }
];


// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  defaultColDef: {
    flex: 1,
    minWidth: 5,
    resizable: true
  },
  popupParent: document.body,
  getRowClass: (params) => {
    // Apply a custom class to the row containing the "Total" account
    if (params.data && params.data.projectType === "Total") {
      return "total-row-highlight"; // Custom CSS class for highlighting
    }
  },
  onGridReady: (params) => {
    // Save the grid API reference for later use
    window.gridAPI = params.api; // Make API globally available if needed
  },
};

function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table22_ProjectTypeByMitigationFundSource.csv' 
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
  
  