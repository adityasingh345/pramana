chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.type === "GET_PAGE_DATA") {
    sendResponse({
      url: window.location.href,
      title: document.title,
      text: document.body.innerText.slice(0, 5000)
    });
  }
  return true; // needed
});
