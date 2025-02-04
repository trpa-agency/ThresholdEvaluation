// get the grid to put the data into
let gridOptions;
let gridAPI;

// Column Definitions
const columnDefs = [
  { headerName: "Rental Car Mitigation", field: "rentalCarMitigation", flex: 1 },
  { headerName: "FY 2020", field: "fy2020", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2021", field: "fy2021", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2022", field: "fy2022", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2023", field: "fy2023",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter },
  { headerName: "FY 2024", field: "fy2024",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter },
  {
    headerName: "Total", field: "total", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, valueFormatter: currencyFormatter,
    cellClass: 'total-column'
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
  domLayout: 'autoHeight',
  popupParent: document.body,
  onGridReady: (params) => {
    // Save the grid API reference for later use
    window.gridAPI = params.api; // Make API globally available if needed
  },
};

function onBtnExport() {
  if (window.gridAPI) {
    const params = {
      fileName: 'Table24_RentalCarMitigationFeeRevenueExpenses.csv' 
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
  
  