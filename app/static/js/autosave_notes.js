document.addEventListener("DOMContentLoaded", function () {
    const noteTextarea = document.getElementById("note-area");

    if (noteTextarea) {
        noteTextarea.addEventListener("input", function () {
            const content = noteTextarea.value;

            fetch("/save_note", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log("Note saved successfully:", data);
                })
                .catch((error) => {
                    console.error("Error saving note:", error);
                });
        });
    }
});

