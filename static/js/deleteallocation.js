
    $("#delete").click(function () {
      var id = $("#data-id").val();
      var allocation = $("#data-allocation").val();

      $.ajax({
          url: $("#delete").data('url'),
          data: {
              'id': id,
              'allocation': allocation
          },
          datatype: 'json',
          success: function (data) {
              var html = ""
              if (data){
                  console.log(data.task, typeof JSON.parse(data.task))
                  tasks = JSON.parse(data.task)
                  tasks.forEach(function (d,i) {
                      console.log(d)
                      html+='<option value='+d.pk+'>'+d.fields.name+'</option>';
                  })
                  $("#div-task").html($(html))
              }
          }
      });
    });