           <script>
                document.querySelectorAll('.attendance-btn').forEach(btn => {
                    btn.addEventListener('click', function () {
                        const memberId = this.dataset.member;
                        const csrftoken = '{{ csrf_token }}';

                        fetch("{% url 'members:ajax_mark_attendance' %}", {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": csrftoken,
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                member_id: memberId,
                                service_type: "{{ service_type }}",
                                date: "{{ today }}"
                            })
                        })
                        .then(res => res.json())
                        .then(data => {
                            this.classList.toggle("present", data.present);
                            this.classList.toggle("absent", !data.present);
                            this.textContent = data.present ? "✔" : "✖";
                        });
                    });
                });
           </script>





<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');


        $('.attendance-btn').click(function () {
        const btn = $(this);
        const memberId = btn.data('member');
        const serviceType = '{{ service_type }}';
        const today = '{{ today }}';

        const isPresent = btn.hasClass('present');

        $.ajax({
            url: "{% url 'members:ajax_mark_attendance' %}",
            method: "POST",
            data: {
                member_id: memberId,
                service_type: serviceType,
                date: today,
                present: !isPresent,   // 👈 KEY FIX
                csrfmiddlewaretoken: csrftoken
            },
            success: function (response) {
                if (response.present) {
                    btn.removeClass('absent').addClass('present').text('✔');
                } else {
                    btn.removeClass('present').addClass('absent').text('✖');
                }
            }
            });
        });


            function bulkMark(markPresent){
                $('.attendance-btn').each(function(){
                    const btn = $(this);
                    const isPresent = btn.hasClass('present');
                    if(markPresent && !isPresent){
                        btn.click();
                    }
                    if(!markPresent && isPresent){
                        btn.click();
                    }
                });
            }
            btn.prop("disabled", true);

            success: function (response) {
           btn.prop("disabled", false);
           }
    </script>
        {% endblock %}
{% endblock %}


