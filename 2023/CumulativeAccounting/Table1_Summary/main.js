// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Type", headerName: "Type", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'text', flex: 1, minWidth: 120,
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Existing", headerName: "Existing",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Banked", headerName: "Banked",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Remaining", headerName: "Remaining Allocations",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Total", headerName: "Total", 
    cellDataType: 'numeric', headerClass: "ag-right-aligned-header", flex: 1,
    valueGetter: (params) => {
      return params.data.Existing + params.data.Banked + params.data.Remaining;
    },
    cellClass: 'total-column',
    valueFormatter: (params) => {
      return params.value.toLocaleString();
  }}
];

// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/66/query?where=Reported%20%3D%20%272023%20TVAL%27&outFields=*&outSR=4326&f=json"
  )
  .then((response) => response.json())
  .then((data) => {
    // Map the results to the format needed for the grid
    const rowData = data.features.map((feature) => ({
                        Type: feature.attributes.Type,
                        Existing: feature.attributes.Existing,
                        Banked: feature.attributes.Banked,
                        Remaining: feature.attributes.Remaining,
                        Total: feature.attributes.Total
    }));
    console.log("Data fetched:", rowData); // Log the data to ensure it is correct
    
  // Grid Options with the fetched data as rowData
  gridOptions = {
      columnDefs: columnDefs,
      rowData: rowData, // Use the fetched data
      theme: 'legacy',
      domLayout: 'autoHeight',
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
        fileName: 'Table1_Summary.csv' // Replace 'GridTitle' with the actual title of your grid
      };
      window.gridAPI.exportDataAsCsv(params);
    } else {
      console.error("Grid API is not initialized.");
    }
  }


  
  