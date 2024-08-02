document.addEventListener("DOMContentLoaded", function() {
    var statusElement = document.getElementById("status");

    if (statusElement.textContent.trim() === "open") {
        statusElement.classList.add("green");
    } else if (statusElement.textContent.trim() === "close") {
        statusElement.classList.add("red");
    }
});
