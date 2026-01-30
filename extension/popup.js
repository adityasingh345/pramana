document.getElementById("analyze").onclick = async () => {
  const tabs = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  const tab = tabs[0];

  chrome.tabs.sendMessage(tab.id, { type: "GET_PAGE_DATA" }, async (data) => {

    if (!data) {
      document.getElementById("result").innerText =
        "Cannot read page";
      return;
    }

    console.log("Page data:", data);

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    console.log("API result:", result);

    document.getElementById("result").innerText =
      "Result: " + result.status;
  });
};
