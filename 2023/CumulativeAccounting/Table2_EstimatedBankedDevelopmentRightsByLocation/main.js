// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Development_Right", headerName: "Development Right", cellDataType: 'text', flex: 2 },
  { field: "Total_Banked", headerName: "Total Banked",cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
  }},
  { field: "Stream_Environment_Zones", headerName: "Stream Environment Zones",cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
  }},
  { field: "Remote_Areas", headerName: "Remote Area",cellDataType: 'numeric', flex: 1, 
      valueFormatter: (params) => {
      return params.value.toLocaleString(); // Format with commas
  }}
];

// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/49/query?where=Reported%20%3D%20'2023%20TVAL'&outFields=Development_Right,Total_Banked,Stream_Environment_Zones,Remote_Areas&outSR=4326&f=json"
  )
  .then((response) => response.json())
  .then((data) => {
    // Map the results to the format needed for the grid
    const rowData = data.features.map((feature) => ({
                        Development_Right: feature.attributes.Development_Right,
                        Total_Banked: feature.attributes.Total_Banked,
                        Stream_Environment_Zones: feature.attributes.Stream_Environment_Zones,
                        Remote_Areas: feature.attributes.Remote_Areas
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


  
  