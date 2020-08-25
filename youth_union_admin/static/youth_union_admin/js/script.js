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
    });

    $(".sp-delete").on("click", function () {
        $.ajax({
            url: Urls["youth_union_admin:delete_activity"](this.getAttribute("data-id")),
            method: "post",
            statusCode: {
                404: function (data) {
                    console.error(data["status"]);
                },
                204: function (data) {
                    window.location.reload();
                }
            }
        })
    });
});