// Get the grid to put the data into
let gridAPI;

// Column Definitions
const columnDefs = [
  { field: "PAOTCategory", headerName: "PAOT Categories",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "RegionalPlanAllocations", headerName: "Regional Plan Allocations", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "AssignedAsOf2019Evaluation", headerName: "Assigned as of 2019 Evaluation", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "Assigned2020To2023", headerName: "Assigned 2020 to 2023", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "PAOTsRemaining", headerName: "PAOTs Remaining", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { field: "PercentOfAllPAOTsAssigned", headerName: "Percent of All PAOTs Assigned", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }}
  ];

// Row Data
const rowData = [
  { PAOTCategory: "Summer Day Use", RegionalPlanAllocations: 6761, AssignedAsOf2019Evaluation: 1814, Assigned2020To2023: 521, PAOTsRemaining: 4426, PercentOfAllPAOTsAssigned: "34.5%" },
  { PAOTCategory: "Winter Day Use", RegionalPlanAllocations: 12400, AssignedAsOf2019Evaluation: 5435, Assigned2020To2023: 0, PAOTsRemaining: 6965, PercentOfAllPAOTsAssigned: "43.8%" },
  { PAOTCategory: "Summer Overnight", RegionalPlanAllocations: 6114, AssignedAsOf2019Evaluation: 394, Assigned2020To2023: 0, PAOTsRemaining: 5720, PercentOfAllPAOTsAssigned: "6.4%" },
  { PAOTCategory: "Total", RegionalPlanAllocations: 25275, AssignedAsOf2019Evaluation: 7643, Assigned2020To2023: 521, PAOTsRemaining: 17111, PercentOfAllPAOTsAssigned: "32.3%" },
];

// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  domLayout: 'autoHeight',
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  },
  popupParent: document.body,
  getRowClass: (params) => {
    // Apply a custom class to the row containing the "Total" account
    if (params.data && params.data.PAOTCategory === "Total") {
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
      fileName: 'Table16_CumulativeAccountingOfPAOT.csv' 
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