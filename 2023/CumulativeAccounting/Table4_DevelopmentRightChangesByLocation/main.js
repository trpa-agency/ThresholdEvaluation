// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight", flex: 1 },
    { headerName: "Remote Areas", field: "remoteAreas", cellDataType: 'numeric', type: 'rightAligned',flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
    { headerName: "Areas within 1/4 mile of a Town Center", 
      field: "areasWithinQuarterMile", cellDataType: 'numeric',type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
    { headerName: "Town Centers", field: "townCenters", cellDataType: 'numeric',type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
        }},
  ];
  
  // Row data for the AG Grid
  const rowData = [
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

    // setup the grid after the page has finished loading
    document.addEventListener("DOMContentLoaded", function () {
      var gridDiv = document.querySelector("#myGrid");
      gridApi = agGrid.createGrid(gridDiv, gridOptions);
    });

    function onBtnExport() {
      if (window.gridAPI) {
        const params = {
          fileName: 'Table4_DevelopmentRightChangesByLocation.csv' // Replace 'GridTitle' with the actual title of your grid
        };
        window.gridAPI.exportDataAsCsv(params);
      } else {
        console.error("Grid API is not initialized.");
      }
    }