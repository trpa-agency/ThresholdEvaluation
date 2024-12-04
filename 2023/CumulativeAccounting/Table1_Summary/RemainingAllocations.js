// adapt sample from https://stackblitz.com/edit/js-ag-grid-52eyso?file=data.js\
// create master level data example https://www.ag-grid.com/javascript-data-grid/master-detail/

// create master level data for Remaining Allocations
var rowData = [
    {
      allocation_type: "Residential Unit of Use",
      id: 0,
      data: [
        { type: "Unused Residential Allocations Released to Local Jurisdictions", total: 960},
        { type: "Residential Bonus Units)", total: 1445},
        { type: "Unreleased Residential Allocations", total: 1042}
        ]
    },
    {
      allocation_type: "Commercial Floor Area",
      id: 1,
      data: [
        { type: "Local Pools Remaining from 1987 Plan", total: 169452},
        { type: "Remaining in TRPA Pool from 1987 Plan", total: 160428},
        { type: "Allocated by 2012 Regional Plan", total: 200000}
        ]
    },
    {
      allocation_type: "Tourist Accommodation Unit",
      id: 2,
      data: [
        { type: "Area/Community Plans", total: 130},
        { type: "Reserved for Homewood/Boulder Bay/Tahoe City Lodge Projects", total: 138},
        { type: "TRPA Bonus Unit Pool", total: 74}
        ]
    }
];
export default rowData;


