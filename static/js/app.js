const form = document.getElementById("generate-form");

if (form) {
    const projectName = document.getElementById("project_name");
    const rawNotes = document.getElementById("raw_notes");

    const button = document.getElementById("generate-btn");
    const text = document.getElementById("generate-text");
    const spinner = document.getElementById("generate-spinner");

    function validate() {
        const valid =
            projectName.value.trim() !== "" &&
            rawNotes.value.trim() !== "";

        if (valid) {
            button.disabled = false;

            button.classList.remove("bg-[#B8C4E8]");
            button.classList.add(
                "bg-[#4F6BFF]",
                "hover:bg-[#4258E8]"
            );
        } else {
            button.disabled = true;

            button.classList.remove(
                "bg-[#4F6BFF]",
                "hover:bg-[#4258E8]"
            );

            button.classList.add("bg-[#B8C4E8]");
        }
    }

    projectName.addEventListener("input", validate);
    rawNotes.addEventListener("input", validate);

    validate();

    form.addEventListener("submit", () => {

        button.disabled = true;

        button.classList.remove(
            "bg-[#4F6BFF]",
            "hover:bg-[#4258E8]"
        );

        button.classList.add("bg-[#B8C4E8]");

        spinner.classList.remove("hidden");

        text.textContent = "Generating case fields...";
    });
}