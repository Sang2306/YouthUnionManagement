$(document).ready(function () {
    try {
        $("#id_start_date").addClass("flatpickr");
        const start_date = document.querySelector(".flatpickr");
        const fp = flatpickr(start_date, {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        });
    } catch (e) {

    }

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
            data: {
                "csrfmiddlewaretoken": document.querySelector("input[name=csrfmiddlewaretoken]").value
            },
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

    $("#id_point").on("keyup", function (e) {
        let point = parseInt($(this).val());
        if (point > 10) {
            alert("Điểm hoạt động không được >= 10");
            $(this).val(10);
        }
    })
});