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
