class StatusIconRenderer {
  eGui;

  init(params) {
      // Create the img element to display the status icon
      const statusIcon = document.createElement("img");
      
      // Get the value passed to the cellRenderer (this will be a status-trend combination)
      const statusTrend = params.value;
      
      // Use statusTrendImageMap from main.js to map the status-trend combination to an image path
      const statusImage = statusTrendImageMap[statusTrend] || "images/DefaultIcon.png";  // Fallback to default icon if not found
      
      // Set the image source
      statusIcon.src = statusImage;

      // Optionally, add a CSS class for styling the image
      statusIcon.setAttribute("class", "status-icon");

      // Create a wrapper element to hold the image
      this.eGui = document.createElement("span");
      this.eGui.setAttribute("class", "imgSpanLogo");
      this.eGui.appendChild(statusIcon);
  }

  // Return the created DOM element (the image wrapped in a span)
  getGui() {
      return this.eGui;
  }

  // Return false since we don't need to refresh the renderer on data change
  refresh() {
      return false;
  }
}
