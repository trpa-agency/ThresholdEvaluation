// Get the grid to put the data into
let gridAPI;
let gridOptions = {
  columnDefs: [],
  rowData: [],
  theme: 'legacy', // Add theme property here
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  }
};

// Column Definitions (Initially empty, to be populated dynamically)
const columnDefs = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', flex: 2 },
];

// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/47/query?where=Status%20%3D%20'REMAINING'&outFields=*&returnGeometry=false&outSR=&f=json"
)
  .then((response) => response.json())
  .then((data) => {
    // Extract the relevant fields
    const rawData = data.features.map((feature) => ({
      Jurisdiction: feature.attributes.Jurisdiction,
      Year: feature.attributes.Year,
      Value: feature.attributes.Value,
    }));

    console.log("Raw data fetched:", rawData); // Log to verify

    // Step 1: Find unique years for dynamic column headers
    const uniqueYears = [...new Set(rawData.map(item => item.Year))];

    // Step 2: Create column definitions for each unique year
    const dynamicColumnDefs = uniqueYears.map(year => ({
      field: year.toString(),
      headerName: year.toString(),
      cellDataType: 'numeric',
      valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0', // Format with commas
    }));

    // Add "Jurisdiction" as the first column
    gridOptions.columnDefs = [
      ...columnDefs,
      ...dynamicColumnDefs
    ];

    // Step 3: Pivot the data by 'Jurisdiction' and map Year/Value to columns
    const rowData = [];
    const jurisdictionMap = new Map();

    rawData.forEach(item => {
      if (!jurisdictionMap.has(item.Jurisdiction)) {
        jurisdictionMap.set(item.Jurisdiction, {});
      }
      const row = jurisdictionMap.get(item.Jurisdiction);
      row[item.Year] = item.Value;
    });

    // Convert map to an array of row data
    jurisdictionMap.forEach((value, key) => {
      rowData.push({
        Jurisdiction: key,
        ...value, // Add year columns to the row
      });
    });

    console.log("Pivoted data:", rowData); // Log to verify

    // Update grid options with the fetched data as rowData
    gridOptions.rowData = rowData;

    // Initialize the grid
    const gridDiv = document.querySelector("#myGrid");
    agGrid.createGrid(gridDiv, gridOptions); // This initializes the grid with the data
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

function onBtnExport() {
  if (window.gridAPI) {
    window.gridAPI.exportDataAsCsv();
  } else {
    console.error("Grid API is not initialized.");
  }
}
