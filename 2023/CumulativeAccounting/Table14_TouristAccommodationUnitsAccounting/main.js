// Get the grid to put the data into
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "TotalExistingTAUs", headerName: "Total Existing TAUs", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
    { field: "BankedReceivedTAUs", headerName: "Banked/Received TAUs", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();}
    },
    { field: "RemainingFrom1987PlanAnd2012Allocation", headerName: "Remaining from 1987 Plan and 2012 Allocation", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();}
    },
    { field: "TotalDevelopmentPotential", headerName: "Total Development Potential", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();}
    },
  ];

// Row Data
const rowData = [
  { Jurisdiction: "City of South Lake Tahoe", TotalExistingTAUs: 5909, BankedReceivedTAUs: 602, RemainingFrom1987PlanAnd2012Allocation: 25, TotalDevelopmentPotential: 6536 },
  { Jurisdiction: "Douglas County", TotalExistingTAUs: 2792, BankedReceivedTAUs: 40, RemainingFrom1987PlanAnd2012Allocation: 25, TotalDevelopmentPotential: 2857 },
  { Jurisdiction: "El Dorado County", TotalExistingTAUs: 112, BankedReceivedTAUs: 211, RemainingFrom1987PlanAnd2012Allocation: 10, TotalDevelopmentPotential: 333 },
  { Jurisdiction: "Placer County", TotalExistingTAUs: 1224, BankedReceivedTAUs: 253, RemainingFrom1987PlanAnd2012Allocation: 37, TotalDevelopmentPotential: 1514 },
  { Jurisdiction: "Washoe County", TotalExistingTAUs: 1002, BankedReceivedTAUs: 64, RemainingFrom1987PlanAnd2012Allocation: 33, TotalDevelopmentPotential: 1099 },
  { Jurisdiction: "TRPA Incentive Pool", TotalExistingTAUs: 0, BankedReceivedTAUs: 0, RemainingFrom1987PlanAnd2012Allocation: 212, TotalDevelopmentPotential: 212 },
];

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

function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table14_TouristAccommodationUnitsAccounting.csv' 
    };
    window.gridAPI.exportDataAsCsv(params);
  } else {
    console.error("Grid API is not initialized.");
  }
}

// setup the grid after the page has finished loading
document.addEventListener("DOMContentLoaded", function () {
  var gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);
});