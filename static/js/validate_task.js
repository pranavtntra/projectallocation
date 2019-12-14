
    $("#project").change(function () {
      var project = $(this).val();
      $.ajax({
          url: $(this).data('url'),
          data: {
              'project': project
          },
          datatype: 'json',
          success: function (data) {
              var html = ""
              if (data){
                  console.log(data.employee, typeof JSON.parse(data.employee))
                  console.log(data.task, typeof JSON.parse(data.task))
                  tasks = JSON.parse(data.task)
                  employees = JSON.parse(data.employee)
                  tasks.forEach(function (d,i) {
                      console.log(d)
                      html+='<option value='+d.pk+'>'+d.fields.name+'</option>';
                  })
                  $("#div-task").html($(html))
              }
          }
      });
    });