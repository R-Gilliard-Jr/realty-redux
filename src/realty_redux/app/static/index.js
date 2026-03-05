var map = L.map("map").setView([39.8, -98.5], 4);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "OSM", maxZoom: 19 }).addTo(map);

var allListings = [], markers = [], searchResults = [], assumptions = {}, searchTerms = {};

fetch("/assumptions").then(function (r) { return r.json() }).then(function (a) { assumptions = a; renderSettings() });
renderAdvanced();

function cfColor(cf) { if (cf >= 500) return "rgba(0,200,80,.75)"; if (cf >= 200) return "rgba(80,210,80,.65)"; if (cf >= 0) return "rgba(255,210,50,.6)"; if (cf >= -200) return "rgba(255,130,40,.65)"; return "rgba(220,40,40,.7)" }
function cfBord(cf) { if (cf >= 500) return "#00c850"; if (cf >= 200) return "#40c840"; if (cf >= 0) return "#d4a020"; if (cf >= -200) return "#e06020"; return "#c02020" }

function renderMap() {
    markers.forEach(function (m) { map.removeLayer(m) });
    markers = [];
    var pts = allListings.filter(function (l) { return l.lat && l.lng });
    pts.forEach(function (l, i) {
        var cf = (l.cf && l.cf.mcf) || 0;
        var ic = L.divIcon({ className: "", html: '<div style="width:36px;height:36px;border-radius:50%;background:' + cfColor(cf) + ';border:3px solid ' + cfBord(cf) + ';display:flex;align-items:center;justify-content:center;font-weight:800;font-size:10px;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.7);box-shadow:0 2px 10px rgba(0,0,0,.4);cursor:pointer">' + (cf >= 0 ? "+" : "") + ("$" + Math.round(cf)) + '</div>', iconSize: [36, 36], iconAnchor: [18, 18] });
        var mk = L.marker([l.lat, l.lng], { icon: ic }).addTo(map);
        mk.on("click", function () { showDetail(i) });
        markers.push(mk);
    });
    if (pts.length === 1) map.setView([pts[0].lat, pts[0].lng], 13);
    else if (pts.length > 1) map.fitBounds(L.latLngBounds(pts.map(function (p) { return [p.lat, p.lng] })), { padding: [50, 50] });
    document.getElementById("empty-state").style.display = allListings.length ? "none" : "";
    updateStats(); updateSubtitle();
}

function updateStats() {
    var ls = allListings;
    if (!ls.length) { document.getElementById("stats").innerHTML = ""; return }
    var tcf = 0, tv = 0, ti = 0;
    ls.forEach(function (l) { tcf += (l.cf && l.cf.mcf) || 0; tv += l.price; ti += (l.cf && l.cf.inv) || 0; });
    var coc = ti > 0 ? tcf * 12 / ti * 100 : 0;
    document.getElementById("stats").innerHTML =
        '<div class="stat"><label>Properties</label><div class="v">' + ls.length + '</div></div>' +
        '<div class="stat"><label>Monthly CF</label><div class="v ' + (tcf >= 0 ? "pos" : "neg") + '">$' + tcf.toFixed(0) + '</div></div>' +
        '<div class="stat"><label>Annual CF</label><div class="v ' + (tcf >= 0 ? "pos" : "neg") + '">$' + (tcf * 12).toFixed(0) + '</div></div>' +
        '<div class="stat"><label>Portfolio</label><div class="v">$' + (tv >= 1e6 ? (tv / 1e6).toFixed(2) + "M" : (tv / 1e3).toFixed(0) + "k") + '</div></div>' +
        '<div class="stat"><label>CoC</label><div class="v" style="color:#a78bfa">' + coc.toFixed(1) + '%</div></div>';
}
function updateSubtitle() { document.getElementById("subtitle").textContent = allListings.length + " listings | Rent: " + (assumptions.rent_pct * 100).toFixed(1) + "%/yr" }

function showDetail(i) {
    var l = allListings[i]; var c = l.cf || {}; var p = document.getElementById("detail-panel");
    p.className = "panel show";
    var mcf = (c.mcf || 0);
    p.innerHTML =
        '<div class="panel-hdr"><b style="font-size:13px;line-height:1.3">' + l.address + '</b><button class="close" onclick="hidePanel(\'detail-panel\')">&#x2715;</button></div>' +
        '<div style="padding:6px 12px">' +
        '<div style="font-size:11px;color:#64748b">' + (l.beds || "?") + 'bd / ' + (l.baths || "?") + 'ba' + (l.sqft ? " &middot; " + l.sqft.toLocaleString() + "sf" : "") + '</div>' +
        (l.summary ? '<div style="font-size:11px;color:#94a3b8;margin-top:4px">' + l.summary.slice(0, 150) + '</div>' : "") +
        (l.url ? '<a href="' + l.url + '" target="_blank" class="link">&#x1f517; View Listing</a>' : "") +
        '</div>' +
        '<div class="grid">' +
        '<div class="cell"><label>PRICE</label><div class="v">$' + l.price.toLocaleString() + '</div></div>' +
        '<div class="cell"><label>RENT</label><div class="v">$' + (c.rent || 0).toFixed(0) + '/mo</div></div>' +
        '<div class="cell"><label>MONTHLY CF</label><div class="v ' + (mcf >= 0 ? "pos" : "neg") + '">' + (mcf >= 0 ? "+" : "") + ("$" + mcf.toFixed(0)) + '</div></div>' +
        '<div class="cell"><label>ANNUAL CF</label><div class="v ' + ((c.acf || 0) >= 0 ? "pos" : "neg") + '">$' + (c.acf || 0).toFixed(0) + '</div></div>' +
        '<div class="cell"><label>CoC ROI</label><div class="v" style="color:#a78bfa">' + (c.coc || 0).toFixed(1) + '%</div></div>' +
        '<div class="cell"><label>CAP RATE</label><div class="v" style="color:#38bdf8">' + (c.cap || 0).toFixed(1) + '%</div></div>' +
        '<div class="cell"><label>MORTGAGE</label><div class="v">$' + (c.mort || 0).toFixed(0) + '/mo</div></div>' +
        '<div class="cell"><label>DSCR</label><div class="v ' + (c.dscr >= 1.25 ? "pos" : c.dscr >= 1 ? "" : "neg") + '">' + (c.dscr || 0).toFixed(2) + '</div></div>' +
        '</div>' +
        '<div class="row3">' +
        '<div class="cell"><label>DOWN</label><div class="v">$' + ((c.down || 0) / 1e3).toFixed(0) + 'k</div></div>' +
        '<div class="cell"><label>INVESTED</label><div class="v">$' + ((c.inv || 0) / 1e3).toFixed(0) + 'k</div></div>' +
        '<div class="cell"><label>LOAN</label><div class="v">$' + ((c.loan || 0) / 1e3).toFixed(0) + 'k</div></div>' +
        '</div>' +
        '<div style="padding:0 12px 10px"><button class="btn btn-danger" style="width:100%;justify-content:center" onclick="removeListing(' + i + ')">Remove</button></div>';
}

function removeListing(i) { allListings.splice(i, 1); hidePanel("detail-panel"); renderMap(); renderList() }

function doSearch() {
    var q = document.getElementById("q").value.trim();
    if (!q) return;
    document.getElementById("search-btn").innerHTML = '<span class="spinner"></span>';
    document.getElementById("search-msg").innerHTML = '<div class="msg info">Searching listings...</div>';
    document.getElementById("search-results").innerHTML = "";
    document.getElementById("search-actions").style.display = "none";
    fetch("/search", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: q }) })
        .then(function (r) { return r.json() })
        .then(function (d) {
            if (d.error) {
                document.getElementById("search-msg").innerHTML = '<div class="msg err">' + d.error + '</div>';
            } else if (!d.listings || !d.listings.length) {
                var emsg = d.message || "No listings found. Try different terms.";
                document.getElementById("search-msg").innerHTML = '<div class="msg err">' + emsg + '</div>';
            } else {
                searchResults = d.listings;
                document.getElementById("search-msg").innerHTML = '<div class="msg ok">Found ' + d.count + ' active listings</div>';
                document.getElementById("search-actions").style.display = "block";
                var html = "";
                d.listings.forEach(function (l, i) {
                    var cf = (l.cf && l.cf.mcf) || 0;
                    var onMap = allListings.some(function (x) { return x.address === l.address });
                    html += '<div class="item" onclick="addResult(' + i + ')" style="' + (onMap ? "opacity:.5" : "") + '">' +
                        '<div style="min-width:0"><div class="addr">' + l.address + '</div>' +
                        '<div class="meta">$' + l.price.toLocaleString() + (l.beds ? " &middot; " + l.beds + "bd" : "") + (l.baths ? " / " + l.baths + "ba" : "") + (l.sqft ? " &middot; " + l.sqft.toLocaleString() + "sf" : "") + '</div>' +
                        (l.url ? '<a href="' + l.url + '" target="_blank" class="link" onclick="event.stopPropagation()">View</a>' : "") +
                        (onMap ? '<span style="font-size:9px;color:#3b82f6;font-weight:700"> ON MAP</span>' : "") +
                        '</div><div class="cf ' + (cf >= 0 ? "pos" : "neg") + '">' + (cf >= 0 ? "+" : "") + "$" + cf.toFixed(0) + '<small>/mo</small></div></div>';
                });
                document.getElementById("search-results").innerHTML = html;
            }
            document.getElementById("search-btn").innerHTML = "&#x1f50d;";
        })
        .catch(function (e) {
            document.getElementById("search-msg").innerHTML = '<div class="msg err">Error: ' + e.message + '</div>';
            document.getElementById("search-btn").innerHTML = "&#x1f50d;";
        });
}

function addResult(i) {
    var l = searchResults[i];
    if (!l) return;
    var dup = allListings.some(function (x) { return x.address === l.address });
    if (dup) return;
    allListings.push(l); renderMap(); renderList();
}
function addAllResults() {
    searchResults.forEach(function (l) {
        if (!allListings.some(function (x) { return x.address === l.address })) {
            allListings.push(l);
        }
    });
    renderMap(); renderList();
}

function renderList() {
    document.getElementById("list-title").textContent = "Properties (" + allListings.length + ")";
    var html = "";
    allListings.forEach(function (l, i) {
        var cf = (l.cf && l.cf.mcf) || 0;
        html += '<div class="item" onclick="showDetail(' + i + ')">' +
            '<div style="min-width:0"><div class="addr">' + l.address + '</div>' +
            '<div class="meta">$' + l.price.toLocaleString() + (l.url ? ' <a href="' + l.url + '" target="_blank" class="link" onclick="event.stopPropagation()" style="margin:0;display:inline">View</a>' : "") +
            '</div></div><div class="cf ' + (cf >= 0 ? "pos" : "neg") + '">' + (cf >= 0 ? "+" : "") + "$" + cf.toFixed(0) + '<small>/mo</small></div></div>';
    });
    if (!html) html = '<div style="padding:20px;text-align:center;color:#64748b">No properties yet</div>';
    document.getElementById("list-body").innerHTML = html;
}

function renderSettings() {
    var labels = { "rent_pct": "Rent %/yr", "down_pct": "Down %", "rate": "Interest %", "term": "Term yr", "closing_pct": "Closing %", "vacancy_pct": "Vacancy %", "tax_pct": "Tax %", "ins_pct": "Insurance %", "maint": "Maint $/mo", "capex": "CapEx $/mo", "pm_pct": "PM %", "hoa": "HOA $/mo", "util": "Util $/mo" };
    var pre = { "maint": "$", "capex": "$", "hoa": "$", "util": "$" };
    var suf = { "rent_pct": "%", "down_pct": "%", "rate": "%", "term": "yr", "closing_pct": "%", "vacancy_pct": "%", "tax_pct": "%", "ins_pct": "%", "pm_pct": "%" };
    var html = "";
    for (var k in assumptions) {
        var val = k === "rent_pct" ? (assumptions[k] * 100).toFixed(1) : assumptions[k];
        html += '<div class="sfld"><label>' + (labels[k] || k) + '</label><div class="inp">' + (pre[k] ? '<span>' + pre[k] + '</span>' : "") +
            '<input type="number" value="' + val + '" data-key="' + k + '" step="any"/>' + (suf[k] ? '<span>' + suf[k] + '</span>' : "") + '</div></div>';
    }
    document.getElementById("settings-body").innerHTML = html;
}
function saveSettings() {
    var inputs = document.querySelectorAll("#settings-body input");
    var body = {};
    inputs.forEach(function (inp) { var v = parseFloat(inp.value) || 0; if (inp.dataset.key === "rent_pct") v = v / 100; body[inp.dataset.key] = v; });
    fetch("/assumptions", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then(function (r) { return r.json() })
        .then(function (a) {
            assumptions = a;
            if (allListings.length) {
                return fetch("/recalc", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ listings: allListings }) }).then(function (r) { return r.json() });
            }
        })
        .then(function (d) {
            if (d && d.listings) allListings = d.listings;
            renderMap(); renderList(); updateSubtitle(); hidePanel("settings-panel");
        });
}

function togglePanel(id) { document.getElementById(id).classList.toggle("show") }
function hidePanel(id) { document.getElementById(id).classList.remove("show") }

function exportCSV() {
    var h = ["Address", "Price", "Beds", "Baths", "Sqft", "Rent/mo", "CF/mo", "CF/yr", "CoC%", "Cap%", "DSCR", "Lat", "Lng", "URL"];
    var rows = allListings.map(function (l) { var c = l.cf || {}; return [l.address, l.price, l.beds || "", l.baths || "", l.sqft || "", (c.rent || 0).toFixed(0), (c.mcf || 0).toFixed(0), (c.acf || 0).toFixed(0), (c.coc || 0).toFixed(2), (c.cap || 0).toFixed(2), (c.dscr || 0).toFixed(2), l.lat || "", l.lng || "", l.url || ""].map(function (v) { return '"' + v + '"' }).join(",") });
    var csv = [h.join(",")].concat(rows).join("\n");
    var a = document.createElement("a"); a.href = "data:text/csv," + encodeURIComponent(csv); a.download = "cashflow_export.csv"; a.click();
}

function renderAdvanced() {
    var searchOptions = {
        "limit": ["Limit", "int"],
        "offset": ["Page", "int"],
        "state_code": ["State Code", "string"],
        "city": ["City", "string"],
        "street_name": ["Street Name", "string"],
        "address": ["Address", "string"],
        "postal_code": ["Postal Code", "string"],
        "agent_source_id": ["Agent Source ID", "string"],
        "selling_agent_name": ["Selling Agent Name", "string"],
        "source_listing_id": ["Source Listing ID", "string"],
        "property_id": ["Property ID", "string"],
        "fulfillment_id": ["Fullfillment ID", "string"],
        // "search_location": ["Search Location", "object"],
        // "radius": ["Radius", "int"],
        // "location": ["Location", "string"],
        // "status": ["Status", "array"],
        // "type": ["Type", "array"],
        // "keywords": ["Keywords", "array"],
        "boundary": ["Boundary", "object"],
        "baths": ["Baths", "object"],
        "beds": ["Beds", "object"],
        "open_house": ["Open House", "object"],
        "year_built": ["Year Built", "object"],
        "sold_price": ["Sold Price", "object"],
        "sold_date": ["Sold Date", "object"],
        "list_price": ["List Price", "object"],
        "lot_sqft": ["Lot SQ. FT.", "object"],
        "sqft": ["SQ. FT.", "object"],
        "hoa_fee": ["HOA Fee", "object"],
        "no_hoa_fee": ["No HOA Fee", "boolean"],
        "pending": ["Pending", "boolean"],
        "contingent": ["Contingent", "boolean"],
        "foreclosure": ["Foreclosure", "boolean"],
        "has_tour": ["Has Tour", "boolean"],
        "new_construction": ["New Construction", "boolean"],
        "cats": ["Cats", "boolean"],
        "dogs": ["Dogs", "boolean"],
        "matterport": ["Matterport", "boolean"],
        // "sort": ["Sort", "object"],
        // "direction": ["Direction", "string"],
        // "field": ["Field", "string"]
    };
    var entry = {
        "int": ["input", "number"],
        "string": ["input", "text"],
        "boolean": ["input", "checkbox"],
        "object": ["input", "text", "placeholder='min,max: 0,1'"],
        "array": ["input", "text"]
    }
    var html = "";
    for (var opt in searchOptions) {
        let label = searchOptions[opt][0];
        let type_ = searchOptions[opt][1];
        html += '<div class="sfld"><label>' +
            (label || opt) +
            '</label><div class="inp">' +
            `<${entry[type_][0]} type="${entry[type_][1]}" value="" data-key="${opt}" ${entry[type_][2] ? entry[type_][2].split(",") : ""}/>` +
            '</div>' +
            '</div>';
    }
    document.getElementById("advanced-search-body").innerHTML = html;
}

renderList();

document.togglePanel = togglePanel;
document.hidePanel = hidePanel;
document.doSearch = doSearch;
document.addAllResults = addAllResults;
document.addResult = addResult;
document.removeListing = removeListing;
document.exportCsv = exportCSV;
document.saveSettings = saveSettings;
document.showDetail = showDetail;