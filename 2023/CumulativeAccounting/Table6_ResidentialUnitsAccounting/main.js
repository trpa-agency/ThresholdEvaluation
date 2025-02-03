// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2 
  },
  { field: "EstimatedExisting", headerName: "Existing Residential Units ",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "BankedExisting", headerName: "Banked Existing Residential Units",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "RemainingAllocations_ReleasedLo", headerName: "Remaining Unused Allocations Released to Local Jurisdictions",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "RemainingAllocations_Unreleased", headerName: "Remaining Unreleased Residential Allocations",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "ResidentialBonusUnits", headerName: "Remaining Bonus Units",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "TotalDevelopmentPotential", headerName: "Total",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    cellClass: 'total-column',
    valueFormatter: (params) => { return params.value.toLocaleString(); 
  }},

];

// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/61/query?where=Reported%20%3D%20'2023%20TVAL'&outFields=*&returnGeometry=false&outSR=&f=json"
  )
  .then((response) => response.json())
  .then((data) => {
    // Map the results to the format needed for the grid
    const rowData = data.features.map((feature) => ({
                        Jurisdiction: feature.attributes.Jurisdiction,
                        EstimatedExisting: feature.attributes.EstimatedExisting,
                        BankedExisting: feature.attributes.BankedExisting,
                        RemainingAllocations_ReleasedLo: feature.attributes.RemainingAllocations_ReleasedLo,
                        RemainingAllocations_Unreleased: feature.attributes.RemainingAllocations_Unreleased,
                        ResidentialBonusUnits: feature.attributes.ResidentialBonusUnits,
                        TotalDevelopmentPotential: feature.attributes.TotalDevelopmentPotential
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
      rowData: rowData, // Use the fetched data
      pinnedBottomRowData: [totalRow],
      theme:"legacy",
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
        fileName: 'Table6_ResidentialUnitsAccounting.csv' 
      };
      window.gridAPI.exportDataAsCsv(params);
    } else {
      console.error("Grid API is not initialized.");
    }
  }

  
  