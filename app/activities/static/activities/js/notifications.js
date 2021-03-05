$(function () {
  // $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

  $("#notifications").click(function () {
    // if ($(".popover").is(":visible")) {
    //   $("#notifications").popover('hide');
    // }
    // else {
    //   $("#notifications").popover('show');
    //   $.ajax({
    //     url: '/notifications/last/',
    //     beforeSend: function () {
    //       $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
    //       $("#notifications").removeClass("new-notifications");
    //     },
    //     success: function (data) {
    //       $(".popover-content").html(data);
    //     }
    //   });
    // }
    // return false;
    $.ajax({
        url: '/notifications/last/',
        beforeSend: function () {
          $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
          $("#notifications").removeClass("new-notifications");
        },
        success: function (data) {
          $(".popover-content").html(data);
        }
      });
    
  });

  function check_notifications() {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
          $("#notifications").addClass("new-notifications");
          notifications_alert();
        }
        else {
          $("#notifications").removeClass("new-notifications");
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, 30000);
      }
    });
  };

  (function worker() {
    $.ajax({
      url: '/notifications/show/',
      success: function (data) {
        if (!data.message) return;
        check_notifications();
        $.niftyNoty({
          type: "dark",
          container: "floating",
          title: "You have new notification",
          message: data.message,
          closeBtn: false,
          timer: 5000
        });
      }
    });
    setTimeout(worker, 5000);
  })();
});