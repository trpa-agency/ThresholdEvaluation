// Get the grid to put the data into
let gridAPIDVTE, gridAPIVMT;

// Column Definitions for DVTE
const columnDefsDVTE = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2
},
  { field: "DVTE_2018", headerName: "2018", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "DVTE_2019", headerName: "2019", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "DVTE_2020", headerName: "2020", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "DVTE_2021", headerName: "2021", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "DVTE_2022", headerName: "2022", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "DVTE_Total", headerName: "Total", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
  ];

// Column Definitions for VMT
const columnDefsVMT = [
  { field: "Jurisdiction", headerName: "Jurisdiction", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 150,
    cellDataType: 'text', flex: 2
},
  { field: "VMT_2018", headerName: "2018", 
    wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
    cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
    valueFormatter: (params) => {return params.value.toLocaleString();
  }},
    { field: "VMT_2019", headerName: "2019", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();
    }},
    { field: "VMT_2020", headerName: "2020", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();
    }},
    { field: "VMT_2021", headerName: "2021", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();
    }},
    { field: "VMT_2022", headerName: "2022", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();
    }},
    { field: "VMT_Total", headerName: "Total", 
      wrapHeaderText: true, autoHeaderHeight: true, minWidth: 100,
      cellDataType: 'numeric', type: 'rightAligned', flex: 1, 
      valueFormatter: (params) => {return params.value.toLocaleString();
    }},
  ];

// Row Data
const rowData = [
  {
    Jurisdiction: "Douglas County",
    DVTE_2018: -2400, DVTE_2019: 3500, DVTE_2020: -4600, DVTE_2021: 6550, DVTE_2022: -8350, DVTE_Total: -5300,
    VMT_2018: 62352, VMT_2019: 38781, VMT_2020: -19682, VMT_2021: 221677, VMT_2022: -17665, VMT_Total: -24802
  },
  {
    Jurisdiction: "Washoe County",
    DVTE_2018: 1300, DVTE_2019: -300, DVTE_2020: -1750, DVTE_2021: 1350, DVTE_2022: 500, DVTE_Total: 1100,
    VMT_2018: -33774, VMT_2019: -3324, VMT_2020: -7488, VMT_2021: 45689, VMT_2022: 1058, VMT_Total: 5148
  },
  {
    Jurisdiction: "El Dorado County",
    DVTE_2018: 4450, DVTE_2019: 0, DVTE_2020: -22000, DVTE_2021: -7150, DVTE_2022: -22400, DVTE_Total: -47100,
    VMT_2018: -115611, VMT_2019: 0, VMT_2020: -94132, VMT_2021: -241983, VMT_2022: -47388, VMT_Total: -220408
  },
  {
    Jurisdiction: "Placer County",
    DVTE_2018: -100, DVTE_2019: 0, DVTE_2020: -5900, DVTE_2021: -1500, DVTE_2022: -3800, DVTE_Total: -11300,
    VMT_2018: 2598, VMT_2019: 0, VMT_2020: -25244, VMT_2021: -50766, VMT_2022: -8039, VMT_Total: -52879
  },
  {
    Jurisdiction: "Regional Total",
    DVTE_2018: 3250, DVTE_2019: 3200, DVTE_2020: -34250, DVTE_2021: -750, DVTE_2022: -34050, DVTE_Total: -62600,
    VMT_2018: -84435, VMT_2019: 35457, VMT_2020: -146546, VMT_2021: -25383, VMT_2022: -72034, VMT_Total: -292941
  }
];

// Grid Options for DVTE
const gridOptionsDVTE = {
  columnDefs: columnDefsDVTE,
  rowData: rowData,
  suppressExcelExport: true,
  domLayout: "autoHeight",
  popupParent: document.body,
  theme: "legacy",
  onGridReady: (params) => {
    gridAPIDVTE = params.api; // Make API globally available if needed
  },
};

// Grid Options for VMT
const gridOptionsVMT = {
  columnDefs: columnDefsVMT,
  rowData: rowData,
  suppressExcelExport: true,
  theme: "legacy",
  domLayout: "autoHeight",
  popupParent: document.body,
  onGridReady: (params) => {
    gridAPIVMT = params.api; // Make API globally available if needed
  },
};

// Initialize the DVTE Grid
const gridDivDVTE = document.querySelector("#myGridDVTE");
agGrid.createGrid(gridDivDVTE, gridOptionsDVTE); // This initializes the grid with DVTE data

// Initialize the VMT Grid
const gridDivVMT = document.querySelector("#myGridVMT");
agGrid.createGrid(gridDivVMT, gridOptionsVMT); // This initializes the grid with VMT data

// Export Data as CSV
function onBtnExport() {
  if (gridAPIDVTE) {
    gridAPIDVTE.exportDataAsCsv({fileName: 'DVTE_Data.csv'});
  }
  if (gridAPIVMT) {
    gridAPIVMT.exportDataAsCsv({fileName: 'VMT_Data.csv'});
  }
}
