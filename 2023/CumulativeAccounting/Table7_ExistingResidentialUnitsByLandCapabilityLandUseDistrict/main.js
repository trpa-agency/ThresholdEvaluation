// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Total_Existing", headerName: "Existing Residential Units",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Non_Sensitive", headerName: "Non-Sensitive",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Sensitive", headerName: "Sensitive",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "SEZ", headerName: "Stream Environment Zone",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Remote_Areas", headerName: "Remote Areas",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Within_Quarter_Mile_of_Town_Cen", headerName: "Within 1/4 mile of a Town Center",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "Town_Centers", headerName: "Town Centers",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
];

// Fetch data from the API
fetch(
"https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/115/query?where=Development_Type%20%3D%20'RESIDENTIAL%20UNITS'&outFields=*&outSR=4326&f=json"
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
    // Calculate totals
  const totalRow = rowData.reduce((acc, row) => {
    Object.keys(row).forEach((key) => {
      if (key !== "Jurisdiction") {
        acc[key] = (acc[key] || 0) + (row[key] || 0);
      }
    });
    return acc;
  }, { Jurisdiction: "Total" });  
  // Grid Options with the fetched data as rowData
  gridOptions = {
      columnDefs: columnDefs,
      rowData: rowData,
      pinnedBottomRowData: [totalRow], 
      theme: "legacy",
      domLayout: "autoHeight",
      suppressExcelExport: true,
      popupParent: document.body,
      getRowClass: (params) => {
        // Apply a custom class to the row containing the "Total" account
        if (params.data && params.data.Jurisdiction === "Total") {
          return "total-row-highlight"; // Custom CSS class for highlighting
        }
      },
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
        fileName: 'Table7_ExistingResidentialUnitsByLandCapabilityLandUseDistrict.csv' 
      };
      window.gridAPI.exportDataAsCsv(params);
    } else {
      console.error("Grid API is not initialized.");
    }
  }