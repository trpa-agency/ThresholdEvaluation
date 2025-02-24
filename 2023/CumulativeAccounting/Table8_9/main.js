// Get the grid to put the data into
let myGridResAllocationsProvided, myGridResAllocationsRemaining;


let gridOptions_allocated = {
  columnDefs: [],
  rowData: [],
  theme: 'legacy', // Add theme property here
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  }
};

let gridOptions_remaining = {
  columnDefs: [],
  rowData: [],
  theme: 'legacy', // Add theme property here
  defaultColDef: {
    flex: 1,
    minWidth: 10,
    resizable: true
  }
};

// Column Definitions for Dev Lan  
const columnDefsAllocated = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', flex: 2 },
];

const columnDefsRemaining = [
  { field: "Jurisdiction", headerName: "Jurisdiction", cellDataType: 'text', flex: 2 },
];

// Fetch allocation provided data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/47/query?where=Status%20%3D%20'DISTRIBUTED'&outFields=Jurisdiction,Year,Value&returnGeometry=false&outSR=&f=json"
)
  .then((response) => response.json())
  .then((data) => {
    // Extract the relevant fields
    const rawData_allocated = data.features.map((feature) => ({
      Jurisdiction: feature.attributes.Jurisdiction,
      Year: feature.attributes.Year,
      Value: feature.attributes.Value,
    }));

    console.log("Raw data fetched:", rawData_allocated); // Log to verify

    // Find unique years for dynamic column headers
    const uniqueYears_allocated = [...new Set(rawData_allocated.map(item => item.Year))];

    // Create column definitions for each unique year
    const dynamicColumnDefs_Allocated = uniqueYears_allocated.map(year => ({
      field: year.toString(),
      headerName: year.toString(),
      cellDataType: 'numeric',
      type: 'rightAligned',
      valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0', // Format with commas
    }));

    // Add "Jurisdiction" as the first column
    gridOptions_allocated.columnDefs = [
      ...columnDefsAllocated,
      ...dynamicColumnDefs_Allocated
    ];

    // Pivot the data by 'Jurisdiction' and map Year/Value to columns
    const rowData_allocated = [];
    const jurisdictionMap_allocated = new Map();

    rawData_allocated.forEach(item => {
      if (!jurisdictionMap_allocated.has(item.Jurisdiction)) {
        jurisdictionMap_allocated.set(item.Jurisdiction, {});
      }
      const row = jurisdictionMap_allocated.get(item.Jurisdiction);
      row[item.Year] = item.Value;
    });

    // Convert map to an array of row data
    jurisdictionMap_allocated.forEach((value, key) => {
      rowData_allocated.push({
        Jurisdiction: key,
        ...value, // Add year columns to the row
      });
    });

    console.log("Pivoted data:", rowData_allocated); // Log to verify
    const totalRow_allocated = rowData_allocated.reduce((acc, row) => {
      Object.keys(row).forEach((key) => { 
        if (key !== "Jurisdiction") {
          acc[key] = (acc[key] || 0) + (row[key] || 0);
        }
      }
      );
      return acc;
    }, { Jurisdiction: "Total" });
    // Update grid options with the fetched data as rowData
    gridOptions_allocated.rowData = rowData_allocated;
    gridOptions_allocated.pinnedBottomRowData = [totalRow_allocated];

    // Initialize the grid
    const gridDivAllocated = document.querySelector("#myGridResAllocationsProvided");
    agGrid.createGrid(gridDivAllocated, gridOptions_allocated); // This initializes the grid with the data
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
// Fetch data from the API
fetch(
  "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/47/query?where=Status%20%3D%20'REMAINING'&outFields=*&returnGeometry=false&outSR=&f=json"
)
  .then((response) => response.json())
  .then((data) => {
    // Extract the relevant fields
    const rawData_remaining = data.features.map((feature) => ({
      Jurisdiction: feature.attributes.Jurisdiction,
      Year: feature.attributes.Year,
      Value: feature.attributes.Value,
    }));

    console.log("Raw data fetched:", rawData_remaining); // Log to verify

    // Step 1: Find unique years for dynamic column headers
    const uniqueYears = [...new Set(rawData_remaining.map(item => item.Year))];

    // Step 2: Create column definitions for each unique year
    const dynamicColumnDefs = uniqueYears.map(year => ({
      field: year.toString(),
      headerName: year.toString(),
      cellDataType: 'numeric',
      type: 'rightAligned',
      valueFormatter: (params) => params.value ? params.value.toLocaleString() : '0', // Format with commas
    }));

    // Add "Jurisdiction" as the first column
    gridOptions_remaining.columnDefs = [
      ...columnDefsRemaining,
      ...dynamicColumnDefs
    ];

    // Step 3: Pivot the data by 'Jurisdiction' and map Year/Value to columns
    const rowData = [];
    const jurisdictionMap_remaining = new Map();

    rawData_remaining.forEach(item => {
      if (!jurisdictionMap_remaining.has(item.Jurisdiction)) {
        jurisdictionMap_remaining.set(item.Jurisdiction, {});
      }
      const row = jurisdictionMap_remaining.get(item.Jurisdiction);
      row[item.Year] = item.Value;
    });

    // Convert map to an array of row data
    jurisdictionMap_remaining.forEach((value, key) => {
      rowData.push({
        Jurisdiction: key,
        ...value, // Add year columns to the row
      });
    });

    console.log("Pivoted data:", rowData); // Log to verify
    const totalRow_remaining = rowData.reduce((acc, row) => {
      Object.keys(row).forEach((key) => {
        if (key !== "Jurisdiction") {
          acc[key] = (acc[key] || 0) + (row[key] || 0);
        }
      });
      return acc;
    }, { Jurisdiction: "Total" });
    gridOptions_remaining.pinnedBottomRowData = [totalRow_remaining];
    // Update grid options with the fetched data as rowData
    gridOptions_remaining.rowData = rowData;

    // Initialize the grid
    const gridDivRemaining = document.querySelector("#myGridResAllocationsRemaining");
    agGrid.createGrid(gridDivRemaining, gridOptions_remaining); // This initializes the grid with the data
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });


// Export Data as CSV
function onBtnExport() {
  if (myGridResAllocationsProvided) {
    myGridResAllocationsProvided.exportDataAsCsv({fileName: 'Table8_ResidentialAllocationsProvided.csv'});
  }
  if (myGridResAllocationsProvided) {
    myGridResAllocationsProvided.exportDataAsCsv({fileName: 'Table9_ResidentialAllocationsRemaining.csv'});
  }
}
