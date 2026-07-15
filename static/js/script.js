const modal = document.getElementById("movieModal");

const closeBtn = document.querySelector(".close");

document.querySelectorAll(".details-btn").forEach(button => {

    button.addEventListener("click", () => {

        document.getElementById("modalTitle").innerText =
            button.dataset.title;

        document.getElementById("modalMeta").innerHTML =
            `⭐ ${button.dataset.rating}
            | 📅 ${button.dataset.year}
            | 🎭 ${button.dataset.genre}
            | ⏱️ ${button.dataset.runtime} min
            | 👍 ${button.dataset.votes}`;

        document.getElementById("modalOverview").innerText =
            button.dataset.overview;

        modal.style.display = "flex";

    });

});

closeBtn.onclick = () => {

    modal.style.display = "none";

};

window.onclick = (event) => {

    if(event.target === modal){

        modal.style.display = "none";

    }

};