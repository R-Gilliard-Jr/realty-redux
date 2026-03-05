function parseCards() {
    const cardSelector = "div[data-testid='rdc-property-card']";
    const propertyCharacteristics = ["property-meta-beds", "property-meta-baths", "property-meta-lot-size", "card-price", "card-address-1", "card-address-2"];
    sessionStorage.setItem("processedCards", JSON.stringify([]));
    sessionStorage.setItem("cardData", JSON.stringify([]));
    const card_list = document.querySelectorAll(cardSelector);
    const card_array = [...card_list];
    console.log(`ARRAY LENGTH: ${card_array.length}`);
    card_array.forEach((card) => {
        const processedCards = JSON.parse(sessionStorage.getItem("processedCards"));
        const cardDataList = JSON.parse(sessionStorage.getItem("cardData"));
        const address = card.querySelector("div[data-testid='card-address']").textContent;
        const url = card.querySelector(".card-image-wrapper").querySelector("a").getAttribute("href");
        if (!(processedCards.includes(address))) {
            const cardContent = card.querySelector("div[data-testid='card-content']");
            const cardData = {};
            for (i = 0; i < propertyCharacteristics.length; i++) {
                const characteristic = propertyCharacteristics[i];
                try {
                    var value = cardContent.querySelector(`div[data-testid=${characteristic}], li[data-testid=${characteristic}] span[class='meta-value'], li[data-testid=${characteristic}] span[data-testid='meta-value']`).textContent;
                }
                catch {
                    var value = null;
                }
                cardData[characteristic] = value;
            }
            cardData["url"] = url;
            console.log(cardData);
            processedCards.push(address);
            cardDataList.push(cardData);
            sessionStorage.setItem("processedCards", JSON.stringify(processedCards));
            sessionStorage.setItem("cardData", JSON.stringify(cardDataList));
        }
    })
    return sessionStorage.getItem("cardData");
}