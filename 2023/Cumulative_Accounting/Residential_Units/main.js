
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', flex: 1 },
  { field: "EstimatedExisting", headerName: "Residential Units",cellDataType: 'numeric', flex: 1, 
                                valueFormatter: (params) => {
                              return params.value.toLocaleString(); // Format with commas
                            }},
  { field: "BankedExisting", headerName: "Banked Residential Units", flex: 1},
];

// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/61/query?where=1%3D1&outFields=EstimatedExisting,BankedExisting,Jurisdiction&outSR=&f=json"
  )
  .then((response) => response.json())
  .then((data) => {
    // Map the results to the format needed for the grid
    const rowData = data.features.map((feature) => ({
                        Jurisdiction: feature.attributes.Jurisdiction,
                        EstimatedExisting: feature.attributes.EstimatedExisting,
                        BankedExisting: feature.attributes.BankedExisting,
    }));

    console.log("Data fetched:", rowData); // Log the data to ensure it is correct

    // Grid Options with the fetched data as rowData
  gridOptions = {
      columnDefs: columnDefs,
      rowData: rowData, // Use the fetched data
      suppressExcelExport: true,
      popupParent: document.body,
      onGridReady: (params) => {
        // Save the grid API reference for later use
        window.gridAPI = params.api; // Make API globally available if needed
      },
    };

    // Initialize the grid
    const gridDiv = document.querySelector("#myGrid");
    agGrid.createGrid(gridDiv, gridOptions); // This initializes the grid with the data

  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
  
  function onBtnExport() {
    if (window.gridAPI) {
      window.gridAPI.exportDataAsCsv();
    } else {
      console.error("Grid API is not initialized.");
    }

  }


  
  