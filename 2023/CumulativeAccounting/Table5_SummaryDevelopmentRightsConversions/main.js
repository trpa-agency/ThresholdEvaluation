// main.js

// Column definitions for the AG Grid
const columnDefs = [
    { headerName: "Development Right", field: "developmentRight" },
    { headerName: "Commercial Floor Area (sq. ft.)", field: "commercialFloorArea" },
    { headerName: "Tourist Accommodation Units", field: "touristAccommodationUnits" },
    { headerName: "Residential Units", field: "residentialUnits" }
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
  
  // Grid options for AG Grid
  const gridOptions = {
    columnDefs: columnDefs,
    rowData: rowData,
    pagination: true,
    domLayout: 'autoHeight',
    defaultColDef: {
      sortable: true,
      filter: true,
      resizable: true
    }
  };
  
  // Once the document is fully loaded, initialize the grid
  document.addEventListener('DOMContentLoaded', function() {
    const gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);
  });
  