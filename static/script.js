function sendKey(key) {
    fetch(`/press/${key}`)
        .then(response => response.text());
}

async function updateNowPlaying() {
  try {
    const res = await fetch("/current");
    const data = await res.json();

    const container = document.getElementById("media-details");

    if (data.status === "none") {
      container.textContent = "Nothing playing right now";
      return;
    }

    const details = data.details;

    container.innerHTML = `
      <h3>${details.title || details.name}</h3>
      ${data.media.format === "tv" ? `<p>Season ${data.media.season}, Episode ${data.media.episode}</p>` : ""}
    `;
  } catch (err) {
    console.error("Error updating Now Playing:", err);
  }
}

// run once when page loads
document.addEventListener("DOMContentLoaded", () => {
  updateNowPlaying();
  // keep updating every 10 seconds
  setInterval(updateNowPlaying, 10000);
});
