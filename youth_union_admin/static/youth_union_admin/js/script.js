$(document).ready(function () {
    $("#id_start_date").addClass("flatpickr");
    const start_date = document.querySelector(".flatpickr");
    const fp = flatpickr(start_date, {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
    });
});