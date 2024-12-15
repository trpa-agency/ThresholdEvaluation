// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { headerName: "Rental Car Mitigation", field: "rentalCarMitigation", flex: 1 },
  { headerName: "FY 2020", field: "fy2020", flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2021", field: "fy2021", flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2022", field: "fy2022", flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2023", field: "fy2023", flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2024", field: "fy2024", flex: 1, valueFormatter: currencyFormatter },
  {
    headerName: "Total", 
    field: "total", 
    flex: 1, 
    valueFormatter: currencyFormatter,
    cellClass: 'total-column' // Add the custom CSS class for the 'Total' column
  }
];

// Row Data
const rowData = [
  { rentalCarMitigation: "Revenue", fy2020: 84183, fy2021: 107300, fy2022: 102289, fy2023: 81051, fy2024: 92465, total: 467287 },
  { rentalCarMitigation: "Expenses", fy2020: 101822, fy2021: 107300, fy2022: 102289, fy2023: 81051, fy2024: 89645, total: 482106 }
];

// Currency Formatter
function currencyFormatter(params) {
  return "$" + params.value.toLocaleString();
}
// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  defaultColDef: {
    flex: 1,
    minWidth: 5,
    resizable: true
  },
  popupParent: document.body,
  getRowClass: (params) => {
    // Apply a custom class to the row containing the "Total" account
    if (params.data && params.data.projectType === "Total") {
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
    window.gridAPI.exportDataAsCsv();
  } else {
    console.error("Grid API is not initialized.");
  }
}

// setup the grid after the page has finished loading
document.addEventListener("DOMContentLoaded", function () {
  var gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);
});
  
  