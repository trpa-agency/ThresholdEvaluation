let gridAppi;

// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
      // cellDataType: 'numeric', type: 'centerAligned', flex: 1 
    },
    { headerName: "Commercial Floor Area (sq. ft.)", field: "commercialFloorArea", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    },
    { headerName: "Tourist Accommodation Units", field: "touristAccommodationUnits",
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    },
    { headerName: "Residential Units", field: "residentialUnits",
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1,  
    }
  ];
  
  // Row data for the AG Grid
  const rowData = [
    {
      developmentRight: "Net Change from Conversions",
      commercialFloorArea: "-39,155",
      touristAccommodationUnits: "-105",
      residentialUnits: "+232"
    }
  ];
  
   // Grid Options with the fetched data as rowData
   gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData,
    theme:"legacy",
    domLayout: "autoHeight",
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