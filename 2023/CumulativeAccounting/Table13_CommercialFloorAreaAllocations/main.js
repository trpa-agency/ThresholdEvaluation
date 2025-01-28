// Get the grid to put the data into
let gridAPI;
let gridOptions;

// Column Definitions
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', flex: 2 },
  { field: "2012", headerName: "2012", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2013", headerName: "2013", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2014", headerName: "2014", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2015", headerName: "2015",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2016", headerName: "2016", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2017", headerName: "2017", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2018", headerName: "2018", 
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2019", headerName: "2019",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2020", headerName: "2020",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2021", headerName: "2021",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2022", headerName: "2022",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
  { field: "2023", headerName: "2023",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0' },
];

// Row Data
const rowData = [
  { Jurisdiction: "City of South Lake Tahoe", 2012: 0, 2013: 8847, 2014: 0, 2015: 11429, 2016: 6443, 2017: 0, 2018: 2510, 2019: 2220, 2020: 0, 2021: 2379, 2022: 3941, 2023: 1972 },
  { Jurisdiction: "Douglas County", 2012: 0, 2013: 0, 2014: 2730, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0 },
  { Jurisdiction: "El Dorado County", 2012: 2500, 2013: 255, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0 },
  { Jurisdiction: "Placer County", 2012: 0, 2013: 5104, 2014: 0, 2015: 4375, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 418, 2022: 1044, 2023: 0 },
  { Jurisdiction: "Washoe County", 2012: 0, 2013: 0, 2014: 0, 2015: -8000, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 2974, 2021: 5226, 2022: 0, 2023: 0 },
  { Jurisdiction: "Carson County", 2012: 0, 2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0 },
  { Jurisdiction: "TRPA Incentive Pool", 2012: 0, 2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0 },
  { Jurisdiction: "Total", 2012: 2500, 2013: 14206, 2014: 2730, 2015: 7804, 2016: 6443, 2017: 0, 2018: 2510, 2019: 2220, 2020: 5353, 2021: 9585, 2022: 3016, 2023: 0 },
];

// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  },
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
      fileName: 'Table13_CommercialFloorAreaAllocations.csv' 
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