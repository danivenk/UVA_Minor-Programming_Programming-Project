// Dani van Enk, 11823526

// init() executes after DOMContent has been loaded
function init() {
    // find form and validation items in the page
    const forms = document.querySelectorAll("form");
    const dropdown_menu = document.querySelector("#drop_menu");
    const dropdown_link = document.querySelector("#drop_link");
    const navbar = document.querySelector("#nav_menu");

    // loop over each form
    forms.forEach(function(form) {
        // check if required fields are empty upon submitting and stop it if that's the case
        form.addEventListener("submit", function(event) {
            // find the items to validate in the form
            const validation_items = event.target.closest(".needs-validation").querySelectorAll(".form-control");
            
            // for each to be validated item validate
            for (const item of validation_items) {
                if (item.value === "") {
                    event.preventDefault();
                    event.stopPropagation();
                }
            };

            // give was-validated class to form if validation was completed
            form.classList.remove("needs-validation");
            form.classList.add("was-validated");

            // keep the login dropdown showing after validation
            if (form.parentElement.id == "drop_menu") {
                dropdown_menu.classList.add("show");
                navbar.classList.add("show");
                dropdown_link.getAttribute("aria-expanded") = true;
            };
        }, false);
    });

    // define model-list table on admin side
    const tables = document.querySelectorAll("table.model-list");

    // add table-responsive only on mobile sized screens
    window.addEventListener("resize", function() {
        
        // add table-responsive to model-list tables
        tables.forEach(function(table) {
            if (document.body.clientWidth < 768) {
                table.classList.add("table-responsive");
            }
        });
    });
    
}
// make sure DOMContent is loaded before the code runs
document.addEventListener("DOMContentLoaded", init, false);