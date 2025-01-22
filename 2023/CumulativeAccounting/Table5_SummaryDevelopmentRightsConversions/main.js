let gridAppi;

// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight", flex: 1 },
    { headerName: "Commercial Floor Area (sq. ft.)", field: "commercialFloorArea", type: 'rightAligned',flex: 2 },
    { headerName: "Tourist Accommodation Units", field: "touristAccommodationUnits",type: 'rightAligned', flex: 2 },
    { headerName: "Residential Units", field: "residentialUnits",type: 'rightAligned', flex: 2 }
  ];
  
  // Row data for the AG Grid
  const rowData = [
    {
      developmentRight: "Net Change from Conversions",
      commercialFloorArea: "-30,583",
      touristAccommodationUnits: "-65",
      residentialUnits: "+157"
    }
  ];
   // Grid Options with the fetched data as rowData
   gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData,
    theme:"legacy",
    suppressExcelExport: true,
    popupParent: document.body,
    onGridReady: (params) => {
      // Save the grid API reference for later use
      window.gridAPI = params.api; // Make API globally available
    },
  };

// setup the grid after the page has finished loading
document.addEventListener("DOMContentLoaded", function () {
  var gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);
});
function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table5_SummaryDevelopmentRightsConversions.csv' 
    };
    window.gridAPI.exportDataAsCsv(params);
  } else {
    console.error("Grid API is not initialized.");
  }
}