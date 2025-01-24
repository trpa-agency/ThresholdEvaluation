class StatusIconRenderer {
  eGui;

  init(params) {
    try {
      console.log('StatusIconRenderer init with value:', params.value);
      // Create the img element to display the status icon
      const statusIcon = document.createElement("img");
      
      // Get the value and add error checking
      const statusTrend = params?.value || 'nan';
      
      // Map status/trend combinations to image paths
      const statusTrendImageMap = {
          'Implemented': './images/Implemented.png',
          'nan': './images/nan.png',
          'At or Somewhat Better Than Target-Moderate Decline': './images/at_or_somewhat_better_than_target-moderate_decline.png',
          'At or Somewhat Better Than Target-Insufficient Data to Determine Trend': './images/at_or_somewhat_better_than_target-insufficient_data_to_determine_trend.png',
          'Considerably Worse Than Target-Little or No Change': './images/considerably_worse_than_target-little_or_no_change.png',
          'Insufficient Data to Determine Status or No Target Established-Rapid Improvement': './images/insufficient_data_to_determine_status_or_no_target_established-rapid_improvement.png',
          'Considerably Better Than Target-Insufficient Data to Determine Trend': './images/considerably_better_than_target-insufficient_data_to_determine_trend.png',
          'Insufficient Data to Determine Status or No Target Established-Little or No Change': './images/insufficient_data_to_determine_status_or_no_target_established-little_or_no_change.png',
          'Somewhat Worse Than Target-Rapid Decline': './images/somewhat_worse_than_target-rapid_decline.png',
          'Considerably Worse Than Target-Rapid Decline': './images/considerably_worse_than_target-rapid_decline.png',
          'At or Somewhat Better Than Target-Little or No Change': './images/at_or_somewhat_better_than_target-little_or_no_change.png',
          'Considerably Better Than Target-Moderate Decline': './images/considerably_better_than_target-moderate_decline.png',
          'Insufficient Data to Determine Status or No Target Established-Moderate Improvement': './images/insufficient_data_to_determine_status_or_no_target_established-moderate_improvement.png',
          'Somewhat Worse Than Target-Little or No Change': './images/somewhat_worse_than_target-little_or_no_change.png',
          'Somewhat Worse Than Target-Moderate Improvement': './images/somewhat_worse_than_target-moderate_improvement.png',
          'Considerably Worse Than Target-Moderate Decline': './images/considerably_worse_than_target-moderate_decline.png',
          'Somewhat Worse Than Target-Moderate Decline': './images/somewhat_worse_than_target-moderate_decline.png',
          'At or Somewhat Better Than Target-Moderate Improvement': './images/at_or_somewhat_better_than_target-moderate_improvement.png',
          'Considerably Better Than Target-Little or No Change': './images/considerably_better_than_target-little_or_no_change.png',
          'Considerably Worse Than Target-Insufficient Data to Determine Trend': './images/considerably_worse_than_target-insufficient_data_to_determine_trend.png',
          'Considerably Better Than Target-Moderate Improvement': './images/considerably_better_than_target-moderate_improvement.png',
          'Considerably Better Than Target-Rapid Improvement': './images/considerably_better_than_target-rapid_improvement.png',
          'Somewhat Worse Than Target-Insufficient Data to Determine Trend': './images/somewhat_worse_than_target-insufficient_data_to_determine_trend.png',
          'Considerably Worse Than Target-Moderate Improvement': './images/considerably_worse_than_target-moderate_improvement.png',
          'Insufficient Data to Determine Status or No Target Established-Insufficient Data to Determine Trend': './images/insufficient_data_to_determine_status_or_no_target_established-insufficient_data_to_determine_trend.png',
      };

      // Use statusTrendImageMap and add error logging
      const statusImage = statusTrendImageMap[statusTrend];
      if (!statusImage) {
          console.warn(`No image mapping found for status-trend: ${statusTrend}`);
      }
      
      // Set the image source with fallback
      statusIcon.src = statusImage || './images/nan.png';
      
      // Add error handling for image load failures
      statusIcon.onerror = () => {
          console.error(`Failed to load image: ${statusIcon.src}`);
          // Create a fallback text element instead of trying to load another image
          const fallbackText = document.createElement('span');
          fallbackText.textContent = statusTrend;
          fallbackText.style.fontSize = '12px';
          fallbackText.style.color = '#666';
          this.eGui.innerHTML = '';
          this.eGui.appendChild(fallbackText);
      };

      statusIcon.setAttribute("class", "status-icon");
      
      // Create a wrapper element
      this.eGui = document.createElement("span");
      this.eGui.setAttribute("class", "imgSpanLogo");
      this.eGui.appendChild(statusIcon);
      
    } catch (error) {
      console.error('Error in StatusIconRenderer:', error);
      this.eGui = document.createElement("span");
      this.eGui.textContent = params?.value || "Error";
    }
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

// Make sure the class is globally available
window.StatusIconRenderer = StatusIconRenderer;
