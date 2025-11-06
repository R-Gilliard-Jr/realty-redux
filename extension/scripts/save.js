function saveSessionStorageToDisk() {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {action: "download"})
    })
}

saveSessionStorageToDisk();
