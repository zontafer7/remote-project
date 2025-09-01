document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const resultsDiv = document.getElementById("results");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();

    resultsDiv.innerHTML = "";

    if (data.error || data.results.length === 0) {
      resultsDiv.textContent = "No results.";
      return;
    }

    data.results.forEach(movie => {
      const div = document.createElement("div");
      div.className = "movie";

      const posterUrl = movie.poster_path
      ? `https://image.tmdb.org/t/p/w200${movie.poster_path}`
      : "https://via.placeholder.com/200x300?text=No+Image";

      div.innerHTML = `
        <img src="${posterUrl}" alt=${movie.title} />
        <h3>${movie.title || movie.name}</h3>
        <button data-id="${movie.id}" data-type=${movie.media_type}>Select</button>
      `;

      resultsDiv.appendChild(div);
    });

    // Add click events to select buttons
    document.querySelectorAll("button[data-id]").forEach(button => {
      button.addEventListener("click", async () => {
        const movieId = button.dataset.id;
        const mediaType = button.dataset.type
        await fetch(`/select/${mediaType}/${movieId}`);
      });
    });
  });
});
