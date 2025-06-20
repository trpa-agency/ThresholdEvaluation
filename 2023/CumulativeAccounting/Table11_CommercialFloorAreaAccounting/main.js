// Grid API and options
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    cellDataType: 'text', flex: 1, minWidth: 200 },
  { field: "TotalExistingCFA", headerName: "Total Existing CFA", cellDataType: 'numeric', 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "BankedCFA", headerName: "Banked CFA", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "RemainingFrom1987PlanAnd2012Allocation", headerName: "Remaining from 1987 Plan and 2012 Allocation", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  },
  { field: "TotalExistingAndPotentialDevelopment", headerName: "Total Existing and Potential Development", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100, cellClass: 'total-column',
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();}
  }
];

// Row Data
const rowData = [
  { Jurisdiction: "City of South Lake Tahoe", TotalExistingCFA: 2992830, BankedCFA: 110308, RemainingFrom1987PlanAnd2012Allocation: 28889, TotalExistingAndPotentialDevelopment: 3132027 },
  { Jurisdiction: "Douglas County", TotalExistingCFA: 670802, BankedCFA: 85756, RemainingFrom1987PlanAnd2012Allocation: 33520, TotalExistingAndPotentialDevelopment: 790078 },
  { Jurisdiction: "El Dorado County", TotalExistingCFA: 335706, BankedCFA: 8245, RemainingFrom1987PlanAnd2012Allocation: 33395, TotalExistingAndPotentialDevelopment: 377346 },
  { Jurisdiction: "Placer County", TotalExistingCFA: 1276531, BankedCFA: 56776, RemainingFrom1987PlanAnd2012Allocation: 63648, TotalExistingAndPotentialDevelopment: 1396955 },
  { Jurisdiction: "Washoe County", TotalExistingCFA: 1184357, BankedCFA: 83337, RemainingFrom1987PlanAnd2012Allocation: 10000, TotalExistingAndPotentialDevelopment: 1277694 },
  { Jurisdiction: "TRPA Incentive Pool", TotalExistingCFA: 0, BankedCFA: 0, RemainingFrom1987PlanAnd2012Allocation: 360428, TotalExistingAndPotentialDevelopment: 360428 },
  { Jurisdiction: "Total", TotalExistingCFA: 6460226, BankedCFA: 344422, RemainingFrom1987PlanAnd2012Allocation: 553036, TotalExistingAndPotentialDevelopment: 7357684 },
];

// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  domLayout: 'autoHeight',
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
      fileName: 'Table11_CommercialFloorAreaAccounting.csv' 
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