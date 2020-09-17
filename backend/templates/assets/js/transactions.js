$(function($) {
  $('#tbl_order_list').DataTable({
    order: [[3, 'desc']],
    responsive: true,
  });

  $('body').on('click', '.link_detail', function() {
    $('#dialogTitle').html('Transaction Detail');
    $('#booking_form button').hide();
    $('#request_order_dialog').modal('show');
    $.ajax({
      type: 'get',
      url: `transaction-detail/${$(this).attr('data-id')}`,
      dataType: 'json',
      success(data) {
        console.log('asdfasdfasdf')
        $('#book_id').val(data.id);
        $('#txt_email')
          .attr('disabled', true)
          .val(data.title);
        $('#txt_username')
          .attr('disabled', true)
          .val(data.price);
        $('#txt_name')
          .attr('disabled', true)
          .val(data.currency);
        $('#txt_address')
          .attr('disabled', true)
          .val(data.description);
        $('#txt_owner')
          .attr('disabled', true)
          .val(data.category);
        $('#txt_overview')
          .attr('disabled', true)
          .val(data.user);
        $('#txt_created_at')
          .attr('disabled', true)
          .val(data.created);
        $('#txt_active')
          .attr('disabled', true)
          .val(data.active == 2 ? '2' : '1');
        $('#txt_updated_at')
          .attr('disabled', true)
          .val(data.updated);
      },
    });
  });

  $('body').on('click', '.link_edit', function() {
    $('#dialogTitle').html('Update Transaction');
    $('#booking_form button spanspan').html('Update Transaction Request');
    $('#booking_form button').show();
    $('#request_order_dialog').modal('show');
    // $('#booking_form .contentbar input').attr('disabled', false).val('');
    $.ajax({
      type: 'get',
      url: `transaction-update/${$(this).attr('data-id')}`,
      dataType: 'json',
      success(data) {
        $('#book_id').val(data.id);
        console.log(data.active);
        $('#txt_email')
          .attr('disabled', true)
          .val(data.title);
        $('#txt_username')
          .attr('disabled', true)
          .val(data.price);
        $('#txt_name')
          .attr('disabled', true)
          .val(data.currency);
        $('#txt_address')
          .attr('disabled', true)
          .val(data.description);
        $('#txt_created_at')
          .attr('disabled', true)
          .val(data.created);
        $('#txt_updated_at')
          .attr('disabled', true)
          .val(data.updated);
        $('#txt_active')
          .attr('disabled', false)
          .val(data.active == 2 ? '2' : '1');
        $('#txt_overview')
          .attr('disabled', true)
          .val(data.user);
        $('#txt_owner')
          .attr('disabled', true)
          .val(data.category);
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
          document.location = `transaction-delete/${dataid}`;
        }
      },
    });
  });

  $('#btn_new_booking').click(function() {
    $('#dialogTitle').html('New Product');
    $('#booking_form button span').html('Create Product Request');
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
