var myChart = null;
$("#user").change(function () {
      var user = $(this).val();
    $.ajax({
        url: $(this).data('url'),
        data: {
              'user': user
          },
          datatype: 'json',
        success: function (data) {
            $('#div').removeAttr('hidden');
            var canvas = document.getElementById('employeechart')
            var ctx = canvas.getContext('2d');
            ctx.clearRect(0,0,canvas.width,canvas.height)
            if(myChart){
                myChart.destroy()
            }
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.projects,
                    datasets: [{
                        label: 'Percentage vs Projects',
                        data: data.allocation,
                    }]
                },
            });
        }
    });
});