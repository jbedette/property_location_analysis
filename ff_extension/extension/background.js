// Extract details from the URL when the user clicks the extension icon.
browser.browserAction.onClicked.addListener(async (tab) => {
    const url = new URL(tab.url);
  
    if (url.hostname === "www.redfin.com") {
      const parts = url.pathname.split("/");
      const state = parts[1];
      const city = parts[2];
      const address = parts[3];
  
      if (state && city && address) {
        // Send data to a local Python server for processing
        const response = await fetch("http://localhost:5000/process", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ state, city, address })
        });
  
        const result = await response.json();
        if (result.mapUrl) {
          browser.tabs.create({ url: result.mapUrl });
        } else {
          alert("Failed to generate map.");
        }
      } else {
        alert("Unable to extract location details from the URL.");
      }
    } else {
      alert("This extension only works on Redfin URLs.");
    }
  });
  