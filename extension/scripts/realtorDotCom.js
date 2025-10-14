const cardSelector = "div[data-testid='rdc-property-card']"
const propertyCharacteristics = ["property-meta-beds", "property-meta-baths", "property-meta-lot-size", "card-price", "card-address"]

function parseCards() {
    const card_list = document.querySelectorAll(cardSelector);
    const card_array = [...card_list];
    console.log(`ARRAY LENGTH: ${card_array.length}`);
    card_array.forEach((card) => {
        const cardContent = card.querySelector("div[data-testid='card-content']");
        const cardData = {};
        for (i = 0; i < propertyCharacteristics.length; i++) {
            const characteristic = propertyCharacteristics[i];
            try {
                var value = cardContent.querySelector(`div[data-testid=${characteristic}],li[data-testid=${characteristic}]`).textContent;
            }
            catch {
                var value = null;
            }
            cardData[characteristic] = value;
        }
        console.log(cardData);
    })
}

// document.addEventListener("DOMContentLoaded", function() {
//     parseCards();
// });

parseCards();

const observer = new MutationObserver((mutations) => {
    // for (const mutation of mutations) {
    //     for (const node of mutation.addedNodes) {
    //         if (node instanceof element && node.matches(cardSelector)) {
    //             parseCards();
    //         }
    //     }
    // }
    parseCards();
});

observer.observe(
    document.querySelector("section[data-testid='property-list']"),
    {
        subtree: true,
        childList: true
    }
)