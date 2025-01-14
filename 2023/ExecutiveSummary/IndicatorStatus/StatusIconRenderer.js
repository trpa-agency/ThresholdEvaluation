class StatusIconRenderer {
    eGui;
  
    init(params) {
      const statusIcon = document.createElement("img");
      const threshold_status = params.data.threshold_status;
      
      const iconMap = {
        InsufficientData: "icons/InsufficientData.png",
        Failed: "icons/InsufficientDataBad.png",
        Passed: "icons/Implemented.png",
        Warning: "icons/ModerateImprovement.png",
      };
  
      // Set default icon if status is not recognized
      statusIcon.src = iconMap[threshold_status] || "icons/DefaultIcon.png";
  
      statusIcon.setAttribute("class", "logo");
  
      this.eGui = document.createElement("span");
      this.eGui.setAttribute("class", "imgSpanLogo");
      this.eGui.appendChild(statusIcon);
    }
  
    getGui() {
      return this.eGui;
    }
  
    refresh() {
      return false;
    }
  }
  