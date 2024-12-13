// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight", flex: 1 },
    { headerName: "Remote Areas", field: "remoteAreas", cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
    { headerName: "Areas within 1/4 mile of a Town Center", 
      field: "areasWithinQuarterMile", cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
    { headerName: "Town Centers", field: "townCenters", cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
  ];
  
  // Row data for the AG Grid
  const rowData = [
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
  
  // Grid options for AG Grid
  const gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData,
    theme: 'legacy',
    domLayout: 'autoHeight',
    defaultColDef: {
      sortable: true,
      // filter: true,
      resizable: true},
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