// get the grid to put the data into
let gridOptions;
let gridAPI;
// Column Definitions
const columnDefs = [
  { headerName: "TRPA Trust Fund Account", field: "trustFundAccount", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2
  },
  { headerName: "Beginning Balance July 1, 2019", field: "beginningBalance", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: currencyFormatter
  },
  { headerName: "Contributions and Interest (July 1, 2019 through June 30, 2023)", field: "contributionsInterest", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: currencyFormatter
  },
  { headerName: "Expenditures (July 1, 2019 through June 30, 2023)", field: "expenditures", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: currencyFormatter
  },
  { headerName: "Ending Balance June 30, 2023", field: "endingBalance", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: currencyFormatter
  },
];

// Row Data
const rowData = [
  { trustFundAccount: "Water Quality Mitigation", beginningBalance: 2796528, contributionsInterest: 2209112, expenditures: 2346285, endingBalance: 2659355 },
  { trustFundAccount: "Stream Zone Restoration Program", beginningBalance: 1008863, contributionsInterest: 784724, expenditures: 683636, endingBalance: 1109951 },
  { trustFundAccount: "Air Quality Mitigation", beginningBalance: 1376612, contributionsInterest: 942631, expenditures: 834119, endingBalance: 1484905 },
  { trustFundAccount: "Mobility Mitigation", beginningBalance: 0, contributionsInterest: 371981, expenditures: 2146, endingBalance: 369835 },
  { trustFundAccount: "Operations & Maintenance", beginningBalance: 1471618, contributionsInterest: 1011128, expenditures: 451491, endingBalance: 2031254 },
  { trustFundAccount: "Excess & Offsite Land Coverage Mitigation", beginningBalance: 4287810, contributionsInterest: 6152034, expenditures: 4014086, endingBalance: 6425759 },
];

// Currency Formatter
function currencyFormatter(params) {
  return "$" + params.value.toLocaleString();
}
// Calculate totals
const totalRow = rowData.reduce((acc, row) => {
  Object.keys(row).forEach((key) => {
    if (key !== "trustFundAccount") {
      acc[key] = (acc[key] || 0) + (row[key] || 0);
    }
  });
  return acc;

}, { trustFundAccount: "Total" });  
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
    if (params.data && params.data.trustFundAccount === "Total") {
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
      fileName: 'Table22_TRPACapitalImprovementExpenditures.csv' 
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
  