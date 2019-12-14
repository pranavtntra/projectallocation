
    $("#sort").change(function () {
      var type = $(this).val();
      var list = $("#list").val();
      $.ajax({
          url: $(this).data('url'),
          data: {
              'type': type,
              'list': list
          },
          datatype: 'json',
          success: function (data) {
              console.log(data)
              // var html = ""
              // if (project_list){
              //     console.log(project_list)
              //     tasks.forEach(function (d,i) {
              //         console.log(d)
              //         html+='<option value='+d.pk+'>'+d.fields.name+'</option>';
              //     })
              //     $("#div-task").html($(html))
              // }
          }
      });
    });