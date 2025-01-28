// get the grid to put the data into
let gridOptions;
let gridAPI;
// Function to format numbers with commas and round them
function formatNumber(value, decimals = 0) {
  if (value === null || value === undefined) return '';
  return value.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

// Column Definitions
const columnDefs = [
  { headerName: "Land Capability", field: "landCapability" },
  { 
    headerName: "Total Acres", field: "totalAcres",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => formatNumber(params.value) 
  },
  { 
    headerName: "(%) Covered", field: "percentCovered", 
    type: 'rightAligned', flex: 1,
    valueGetter: (params) => {
      if (params.data && params.data.landCapability === "Total") {
        return "-";
      }
      return params.data.totalAcres && params.data.acresCoverage2023 ? 
        Math.round((params.data.acresCoverage2023 / params.data.totalAcres) * 100) : 0;
    },
    valueFormatter: (params) => params.value + "%" 
  },
  { 
    headerName: "Acres Covered", field: "acresCoverage2023",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => formatNumber(params.value)
  },
  { 
    headerName: "Acres of New Coverage", field: "acresNewCoverage",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => formatNumber(params.value, 1) 
  },
  { 
    headerName: "Threshold (%) Allowed", field: "thresholdValue",
    type: 'rightAligned', flex: 1,
    valueGetter: (params) => {
      if (params.data && params.data.landCapability === "Total") {
        return "-";
      }
      return params.data.thresholdValue;
    },
    valueFormatter: (params) => params.value + "%" 
  },
  { 
    headerName: "Threshold Acres Allowed", field: "thresholdAcres",
    cellDataType: 'numeric', type: 'rightAligned', flex: 1,
    valueFormatter: (params) => formatNumber(params.value)
  }
];

// Row Data
const rowData = [
  { landCapability: "1A", totalAcres: 23966.92736043, acresCoverage2023: 210.61516123291554, acresNewCoverage: -0.06299357208448117, thresholdValue: "1", thresholdAcres: 239.6692736043 },
  { landCapability: "1B", totalAcres: 11404.76030555, acresCoverage2023: 797.3222534666254, acresNewCoverage: -1.6011019283746557, thresholdValue: "1", thresholdAcres: 114.0476030555 },
  { landCapability: "1C", totalAcres: 53725.60651663, acresCoverage2023: 494.53718135500003, acresNewCoverage: 0.0, thresholdValue: "1", thresholdAcres: 537.2560651663 },
  { landCapability: "2", totalAcres: 23249.509538539998, acresCoverage2023: 304.873298355, acresNewCoverage: 0.0, thresholdValue: "1", thresholdAcres: 232.4950953854 },
  { landCapability: "3", totalAcres: 17694.8280334, acresCoverage2023: 381.71607078, acresNewCoverage: 0.0, thresholdValue: "5", thresholdAcres: 884.7414016700001 },
  { landCapability: "4", totalAcres: 31447.46201914, acresCoverage2023: 1322.9379841256098, acresNewCoverage: 1.2461158506095042, thresholdValue: "20", thresholdAcres: 6289.4924038280005 },
  { landCapability: "5", totalAcres: 12187.42759342, acresCoverage2023: 1134.149290796911, acresNewCoverage: -0.5694198830890725, thresholdValue: "25", thresholdAcres: 3046.856898355 },
  { landCapability: "6", totalAcres: 23199.99067221, acresCoverage2023: 2286.823749769103, acresNewCoverage: 7.071220514103077, thresholdValue: "30", thresholdAcres: 6959.997201662999 },
  { landCapability: "7", totalAcres: 5015.10433546, acresCoverage2023: 1351.020834621235, acresNewCoverage: 21.026344456235076, thresholdValue: "30", thresholdAcres: 1504.531300638 },
];

// Calculate totals for the Total row
const totalRow = {
  landCapability: "Total",
  totalAcres: rowData.reduce((sum, row) => sum + (row.totalAcres || 0), 0),
  acresCoverage2023: rowData.reduce((sum, row) => sum + (row.acresCoverage2023 || 0), 0),
  acresNewCoverage: rowData.reduce((sum, row) => sum + (row.acresNewCoverage || 0), 0),
  thresholdValue: "-",  // Set "-" for the Total row in Threshold Value
  thresholdAcres: rowData.reduce((sum, row) => sum + (row.thresholdAcres || 0), 0),
  percentCovered: "-"  // Set "-" for the Total row in Percent Covered
};
// Grid Options with the fetched data as rowData
gridOptions = {
  columnDefs: columnDefs,
  rowData: rowData, // Use the fetched data
  theme:"legacy",
  suppressExcelExport: true,
  pinnedBottomRowData: [totalRow],
  defaultColDef: {
    flex: 1,
    minWidth: 5,
    resizable: true
  },
  popupParent: document.body,
  getRowClass: (params) => {
    // Apply a custom class to the row containing the "Total" account
    if (params.data && params.data.landCapability === "Total") {
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
      fileName: 'Table19_EstimatedImperviousCoverByLandCapability.csv' 
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
  
  