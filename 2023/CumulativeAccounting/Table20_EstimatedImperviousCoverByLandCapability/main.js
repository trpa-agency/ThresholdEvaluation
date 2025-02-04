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
  { headerName: "Land Capability", field: "landCapability",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'text', flex: 1
   },
  { 
    headerName: "Total Acres", field: "totalAcres",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { 
    headerName: "(%) Covered", field: "percentCovered", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
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
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { 
    headerName: "Acres of New Coverage", field: "acresNewCoverage",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  { 
    headerName: "Threshold (%) Allowed", field: "thresholdValue",
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
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
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 120,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
];

// Row Data
const rowData = [
  { landCapability: "1A", totalAcres: Math.round(23966.92736043), acresCoverage2023: Math.round(210.61516123291554), acresNewCoverage: Math.round(-0.06299357208448117), thresholdValue: "1", thresholdAcres: Math.round(239.6692736043) },
  { landCapability: "1B", totalAcres: Math.round(11404.76030555), acresCoverage2023: Math.round(797.3222534666254), acresNewCoverage: Math.round(-1.6011019283746557), thresholdValue: "1", thresholdAcres: Math.round(114.0476030555) },
  { landCapability: "1C", totalAcres: Math.round(53725.60651663), acresCoverage2023: Math.round(494.53718135500003), acresNewCoverage: Math.round(0.0), thresholdValue: "1", thresholdAcres: Math.round(537.2560651663) },
  { landCapability: "2", totalAcres: Math.round(23249.509538539998), acresCoverage2023: Math.round(304.873298355), acresNewCoverage: Math.round(0.0), thresholdValue: "1", thresholdAcres: Math.round(232.4950953854) },
  { landCapability: "3", totalAcres: Math.round(17694.8280334), acresCoverage2023: Math.round(381.71607078), acresNewCoverage: Math.round(0.0), thresholdValue: "5", thresholdAcres: Math.round(884.7414016700001) },
  { landCapability: "4", totalAcres: Math.round(31447.46201914), acresCoverage2023: Math.round(1322.9379841256098), acresNewCoverage: Math.round(1.2461158506095042), thresholdValue: "20", thresholdAcres: Math.round(6289.4924038280005) },
  { landCapability: "5", totalAcres: Math.round(12187.42759342), acresCoverage2023: Math.round(1134.149290796911), acresNewCoverage: Math.round(-0.5694198830890725), thresholdValue: "25", thresholdAcres: Math.round(3046.856898355) },
  { landCapability: "6", totalAcres: Math.round(23199.99067221), acresCoverage2023: Math.round(2286.823749769103), acresNewCoverage: Math.round(7.071220514103077), thresholdValue: "30", thresholdAcres: Math.round(6959.997201662999) },
  { landCapability: "7", totalAcres: Math.round(5015.10433546), acresCoverage2023: Math.round(1351.020834621235), acresNewCoverage: Math.round(21.026344456235076), thresholdValue: "30", thresholdAcres: Math.round(1504.531300638) },
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
  domLayout: "autoHeight",
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
      fileName: 'Table20_EstimatedImperviousCoverByLandCapability.csv' 
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
  
  