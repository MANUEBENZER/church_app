$(document).ready(function () {
    console.log("Attendance checkbox JS loaded");

    $('.attendance-checkbox').on('change', function () {
        const checkbox = $(this);

        $.ajax({
            url: "/ajax/mark-attendance/",
            method: "POST",
            data: {
                member_id: checkbox.data('member'),
                service_type: checkbox.data('service'),
                date: checkbox.data('date'),
                present: checkbox.is(':checked'),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log("Saved:", response.present);
            },
            error: function () {
                alert("Failed to save attendance");
                checkbox.prop('checked', !checkbox.is(':checked')); // revert
            }
        });
    });
});
function updateRowStyle(checkbox) {
    const row = checkbox.closest("tr");
    row.classList.toggle("present-row", checkbox.checked);
    row.classList.toggle("absent-row", !checkbox.checked);
}
$("#mark-all").on("click", function () {
    $(".attendance-checkbox").each(function () {
        if (!this.checked) {
            this.checked = true;
            updateRowStyle(this);
            sendAttendance(this);
        }
    });
});
function updateCounters() {
    const total = $(".attendance-checkbox").length;
    const present = $(".attendance-checkbox:checked").length;
    $("#present-count").text(present);
    $("#absent-count").text(total - present);
    $("#total-count").text(total);
}
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function sendAttendance(checkbox) {
    $.ajax({
        url: "/ajax/mark-attendance/",
        type: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        data: {
            member_id: checkbox.dataset.member,
            service_type: checkbox.dataset.service,
            date: checkbox.dataset.date,
            present: checkbox.checked
        },
        success: function () {
            updateCounters();
        }
    });
}

$(".attendance-checkbox").on("change", function () {
    updateRowStyle(this);
    sendAttendance(this);
});
