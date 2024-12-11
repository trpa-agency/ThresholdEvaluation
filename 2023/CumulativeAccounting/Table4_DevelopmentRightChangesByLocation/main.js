// main.js

// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight" },
    { headerName: "Remote Areas", field: "remoteAreas" },
    { headerName: "Areas within 1/4 mile of a Town Center", field: "areasWithinQuarterMile" },
    { headerName: "Town Centers", field: "townCenters" }
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
    // pagination: true,
    domLayout: 'autoHeight',
    defaultColDef: {
      sortable: true,
      // filter: true,
      resizable: true
    }
  };
  
  // Once the document is fully loaded, initialize the grid
  document.addEventListener('DOMContentLoaded', function() {
    const gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);
  });
  
  