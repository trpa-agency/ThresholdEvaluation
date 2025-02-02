// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', minWidth: 150, flex: 2 },
  { field: "Total_Existing", headerName: "Existing Tourist Units",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Non_Sensitive", headerName: "Non-Sensitive",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Sensitive", headerName: "Sensitive",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "SEZ", headerName: "Stream Environment Zone",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Remote_Areas", headerName: "Remote Areas",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Within_Quarter_Mile_of_Town_Cen", headerName: "Within 1/4 mile of a Town Center",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Town_Centers", headerName: "Town Centers",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }}
];

// Fetch data from the API
fetch(
"https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/115/query?where=Development_Type%20%3D%20'TOURIST%20ACCOMMODATION%20UNITS'&outFields=*&outSR=4326&f=json"
 )
  .then((response) => response.json())
  .then((data) => {
    // Map the results to the format needed for the grid
    const rowData = data.features.map((feature) => ({
                        Jurisdiction: feature.attributes.Jurisdiction,
                        Total_Existing: feature.attributes.Total_Existing,
                        Non_Sensitive: feature.attributes.Non_Sensitive,
                        Sensitive: feature.attributes.Sensitive,
                        SEZ: feature.attributes.SEZ,
                        Remote_Areas: feature.attributes.Remote_Areas,
                        Within_Quarter_Mile_of_Town_Cen: feature.attributes.Within_Quarter_Mile_of_Town_Cen,
                        Town_Centers: feature.attributes.Town_Centers
    }));
    console.log("Data fetched:", rowData); // Log the data to ensure it is correct
   
  // Grid Options with the fetched data as rowData
  gridOptions = {
      columnDefs: columnDefs,
      rowData: rowData, // Use the fetched data
      theme: "legacy",
      // grandTotalRow: "bottom",
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
      const params = {
        fileName: 'Table15_TouristAccommodationUnitsByLandCapabilityLandUseDistrict.csv' 
      };
      window.gridAPI.exportDataAsCsv(params);
    } else {
      console.error("Grid API is not initialized.");
    }
  }