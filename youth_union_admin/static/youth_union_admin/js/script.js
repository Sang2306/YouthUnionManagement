$(document).ready(function () {
    $("#id_start_date").addClass("flatpickr");
    const start_date = document.querySelector(".flatpickr");
    const fp = flatpickr(start_date, {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
    });

    $(".sp-info").on("click", function () {
        $.get(
            Urls["youth_union_admin:activity_detail_view"](this.getAttribute("data-id")),
            {},
            function (data) {
                $(".info-modal").html(data["rendered"])
            }
        )
    })
});