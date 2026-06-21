async function searchHadith() {
    let q = document.getElementById("query").value;

    if (!q) return;

    document.getElementById("results").innerHTML = "Searching...";

    let res = await fetch(`/search?q=${encodeURIComponent(q)}`);
    let data = await res.json();

    let html = "";

    data.results.forEach(r => {
        html += `
        <div class="result">
            <b>${r.book}</b><br>
            ${r.text}<br>
            <small>Score: ${r.score.toFixed(3)}</small>
        </div>
        `;
    });

    document.getElementById("results").innerHTML = html;
}