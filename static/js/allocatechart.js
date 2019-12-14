$("#container").click(function () {
    console.log($("#container").attr("data-url"))
    $.ajax({
        url: $(this).data('url'),
        success: function (data) {
            console.log(data.projects)
            $('#hide').removeAttr('hidden');
            var ctx = document.getElementById('chart').getContext('2d');
            console.log((ctx))
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.projects,
                    datasets: [{
                        label: 'Project vs Employee Allocation',
                        data: data.allocation,
                    }]
                },
            });
        }
    });
});