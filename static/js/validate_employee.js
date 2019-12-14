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
                  employees.forEach(function (e) {
                      console.log("d.id")
                      console.log(e.user)
                      html+='<option value='+e.user+'>'+e.user__username + " Allocated: " + e.user__percentage+"%"+'</option>';
                  })
                  $("#div-employee").html($(html))
              }
          }
      });
    });