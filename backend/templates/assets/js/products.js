$(function($) {
  $('#tbl_order_list').DataTable({
    order: [[3, 'desc']],
    responsive: true,
  });

  $('body').on('click', '.link_detail', function() {
    $('#dialogTitle').html('Product Detail');
    $('#booking_form button').hide();
    $('#request_order_dialog').modal('show');
    $.ajax({
      type: 'get',
      url: `product-detail/${$(this).attr('data-id')}`,
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
          .attr('disabled', true)
          .val(data.active ? 'True' : 'False');
        $('#txt_overview')
          .attr('disabled', true)
          .val(data.user);
      },
    });
  });

  $('body').on('click', '.link_edit', function() {
    $('#dialogTitle').html('Update Product');
    $('#booking_form button span').html('Update Product Request');
    $('#booking_form button').show();
    $('#request_order_dialog').modal('show');
    // $('#booking_form .contentbar input').attr('disabled', false).val('');
    $.ajax({
      type: 'get',
      url: `product-update/${$(this).attr('data-id')}`,
      dataType: 'json',
      success(data) {
        $('#book_id').val(data.id);
        console.log(data.active);
        $('#txt_email')
          .attr('disabled', false)
          .val(data.title);
        $('#txt_username')
          .attr('disabled', false)
          .val(data.price);
        $('#txt_name')
          .attr('disabled', false)
          .val(data.currency);
        $('#txt_address')
          .attr('disabled', false)
          .val(data.description);
        $('#txt_created_at')
          .attr('disabled', false)
          .val(data.created);
        $('#txt_updated_at')
          .attr('disabled', false)
          .val(data.updated);
        $('#txt_active')
          .attr('disabled', false)
          .val(data.active ? 'True' : 'False');
        $('#txt_overview')
          .attr('disabled', false)
          .val(data.user);
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
          document.location = `product-delete/${dataid}`;
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
