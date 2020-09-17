$(function($) {
  $('#tbl_order_list').DataTable({
    order: [[3, 'desc']],
    responsive: true,
  });

  $('body').on('click', '.link_detail', function() {
    $('#dialogTitle').html('User Detail');
    $('#booking_form button').hide();
    $('#request_order_dialog').modal('show');
    $.ajax({
      type: 'get',
      url: `user-detail/${$(this).attr('data-id')}`,
      dataType: 'json',
      success(data) {
        $('#book_id').val(data.id);
        $('#txt_email')
          .attr('disabled', true)
          .val(data.email);
        $('#txt_username')
          .attr('disabled', true)
          .val(data.username);
        $('#txt_name')
          .attr('disabled', true)
          .val(data.name);
        $('#txt_created_at')
          .attr('disabled', true)
          .val(data.create);
        $('#txt_last_login')
          .attr('disabled', true)
          .val(data.last);
        $('#txt_active')
          .attr('disabled', true)
          .val(data.active ? 'True' : 'False');
        $('#txt_address')
          .attr('disabled', true)
          .val(data.address);
        $('#txt_overview')
          .attr('disabled', true)
          .val(data.over);
        $('#txt_mobile')
          .attr('disabled', true)
          .val(data.mobile);
      },
    });
  });

  $('body').on('click', '.link_edit', function() {
    $('#dialogTitle').html('Update User');
    $('#booking_form button span').html('Update User Request');
    $('#booking_form button').show();
    $('#request_order_dialog').modal('show');
    // $('#booking_form .contentbar input').attr('disabled', false).val('');
    $.ajax({
      type: 'get',
      url: `user-update/${$(this).attr('data-id')}`,
      dataType: 'json',
      success(data) {
        $('#book_id').val(data.id);
        console.log(data.active);
        $('#txt_email')
          .attr('disabled', true)
          .val(data.email);
        $('#txt_username')
          .attr('disabled', true)
          .val(data.username);
        $('#txt_name')
          .attr('disabled', true)
          .val(data.name);
        $('#txt_created_at')
          .attr('disabled', true)
          .val(data.create);
        $('#txt_last_login')
          .attr('disabled', true)
          .val(data.last);
        $('#txt_active')
          .attr('disabled', false)
          .val(data.active ? 'True' : 'False');
        $('#txt_address')
          .attr('disabled', false)
          .val(data.address);
        $('#txt_overview')
          .attr('disabled', false)
          .val(data.over);
        $('#txt_mobile')
          .attr('disabled', false)
          .val(data.mobile);
      },
    });
  });

  $('body').on('click', '.link_delete', function() {
    const dataid = $(this).attr('data-id');
    bootbox.confirm({
      message: 'Are you sure?',
      size: 'large',
      callback(result) {
        if (result == true) {
          document.location = `user-delete/${dataid}`;
        }
      },
    });
  });

  $('#btn_new_booking').click(function() {
    $('#dialogTitle').html('Create a User');
    $('#booking_form button span').html('Create User Request');
    $('#booking_form button').show();
    $('#request_order_dialog').modal('show');
    $('#booking_form .contentbar input')
      .attr('disabled', false)
      .val('');
  });

  $('#time-booking').datepicker({
    language: 'en',
    timeFormat: 'hh:ii aa',
    timepicker: true,
    dateTimeSeparator: ' - ',
    autoClose: true,
  });
});
